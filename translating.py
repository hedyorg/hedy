"""
Helper routines for the translation page.
"""
from ruamel import yaml


class TranslatableFile:
  def __init__(self, caption, file, strings):
    self.caption = caption
    self.file = file
    self.strings = strings

  def add_string(self, string):
    self.strings.append(string)


class TranslatableString:
  def __init__(self, path, original, translated):
    self.is_header = False
    self.path = path
    self.original = original
    self.translated = translated
    self.key = path[-1] if path else ''

  @property
  def encoded_path(self):
    return '.'.join(self.path)

  @staticmethod
  def decode_path(path):
    return [try_int(x) for x in path.split('.')]


class TranslatableSection:
  def __init__(self, caption):
    self.is_header = True
    self.caption = caption


def try_int(x):
  try:
    return int(x)
  except ValueError:
    return x



def struct_to_sections(struct1, struct2):
  assert(isinstance(struct1, dict))

  def recurse(x, y, path):
    if isinstance(x, str):
      strings.append(TranslatableString(path, str(x), str(y or '')))
      return

    if isinstance(x, list):
      y = y if isinstance(y, list) else []

      for i, el in enumerate(x):
        if not isinstance(el, str):
          strings.append(TranslatableSection(str(i + 1)))
        recurse(el, y[i] if i < len(y) else None, path + ['a:' + str(i)])
      return

    if isinstance(x, dict):
      y = y if isinstance(y, dict) else {}

      for key, el in x.items():
        if not isinstance(el, str):
          strings.append(TranslatableSection(str(key)))
        recurse(el, y.get(key, None), path + [str(key)])

  strings = []
  recurse(struct1, struct2, [])
  return strings


def apply_form_change(data, encoded_path, value):
  """Apply a change submitted via the web form to the given data.

  We need to make minimal mutations to the YAML in order
  for the Ruamel Yaml parser to maintain the original
  source locations, comments, etc.
  """
  path = TranslatableString.decode_path(encoded_path)
  return apply_change(data, path, value)


def apply_change(data, path, value):
  if not path:
    raise RuntimeError('Path cannot be empty')

  key = path[-1]
  container = value_at(data, path[:-1])

  if str(key).startswith('a:'):
    # Expecting index into a list
    if not isinstance(container, list):
      container = apply_change(data, path[:-1], [])

    index = int(key[2:])
    while len(container) < index + 1:
      container.append({})
    container[index] = value
    return container[index]
  else:
    # Expecting to index into a dict
    if not isinstance(container, dict):
      container = apply_change(data, path[:-1], {})
    container[key] = value
    return container[key]


def value_at(data, path):
  for p in path:
    if str(p).startswith('a:'):
      # Expecting to index into a list
      index = int(p[2:])
      if not isinstance(data, list): return None
      if len(data) <= index: return None
      data = data[index]
    else:
      # Expecting to index into a dict (but the index could still be a number)
      if not isinstance(data, dict): return None
      data = data.get(p, None)
  return data


def render_caption(path):
  return ' » '.join(path)


def str_presenter(dumper, data):
  """For use with yaml.dump to get mostly human-sensible results."""
  try:
      dlen = len(data.splitlines())
      if (dlen > 1):
          return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
  except TypeError as ex:
      return dumper.represent_scalar('tag:yaml.org,2002:str', data)
  return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def normalize_yaml_blocks(data):
  """Replace all string containing newlines with a special string that the Yaml parser will serialize as a | block.

  This will make your YAML pretty and easy to work with.
  """
  if isinstance(data, list):
    for i, el in enumerate(data):
      if isinstance(el, str):
        pass
        data[i] = maybe_translate_to_block(el)
      else:
        normalize_yaml_blocks(el)
    return data

  if isinstance(data, dict):
    for key, value in list(data.items()):
      if isinstance(value, str):
        pass
        data[key] = maybe_translate_to_block(value)
      else:
        normalize_yaml_blocks(value)
    return data

  return data


def maybe_translate_to_block(x):
  newlines = '\n' in x
  if newlines and not isinstance(x, yaml.scalarstring.LiteralScalarString):
    return yaml.scalarstring.LiteralScalarString(str(x))
  return x


def normalize_newlines(x):
  """Turn Windows/web newlines into Linux newlines."""
  return x.replace('\r\n', '\n')
