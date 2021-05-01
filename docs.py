from ruamel import yaml
import glob
import re
import unicodedata

def slugify(s):
  if s is None:
    return None
  return re.sub('[^a-zA-Z0-9]', '-', strip_accents(s)).lower()


def strip_accents(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s)
                 if unicodedata.category(c) != 'Mn')

class DocCollection:
  def __init__(self, keys=[], synth={}):
    self.docs = []
    self.index = {}
    self.keys = keys
    self.synth = synth

  def get(self, *keys):
    v = self.index
    for key in keys:
      v = v.get(key)
      if not v:
        return {} if len(keys) < len(self.keys) else None
    return v

  def load_dir(self, rootdir):
    files = glob.glob(f'{rootdir}/**/*.md', recursive=True)
    for file in sorted(files):
      doc = MarkdownDoc.from_file(file)

      for k, v in self.synth.items():
        doc.front_matter[k] = v(doc)

      self.docs.append(doc)
      self.add_to_index(doc)

  def add_to_index(self, doc):
    if not self.keys:
      return

    d = self.index
    for key in self.keys[:-1]:
      value = doc.front_matter.get(key, None)
      if not value:
        return
      d = d.setdefault(value, {})

    key = self.keys[-1]
    value = doc.front_matter.get(key, None)
    if value:
      d[value] = doc

class MarkdownDoc:
  @staticmethod
  def from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
      contents = f.read()
    parts = re.split('^---+$', contents, maxsplit=1, flags=re.M)
    if len(parts) == 1:
      return MarkdownDoc({}, parts[0])
    return MarkdownDoc(yaml.safe_load(parts[0]), parts[1])

  def __init__(self, front_matter, doc):
    self.front_matter = front_matter
    self.markdown = doc
