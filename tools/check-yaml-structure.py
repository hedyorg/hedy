import sys
from os import path
import glob
import collections
from ruamel import yaml
from io import StringIO


yaml_writer = yaml.YAML(typ="rt")


def main():
    any_failure = False
    for reference_file in glob.glob('content/*/en.yaml'):
        en = load_yaml(reference_file)
        structure_dir = path.basename(path.dirname(reference_file))

        mismatches = {comparison_file: find_mismatched_arrays(en, load_yaml(comparison_file))
                      for comparison_file in glob.glob(f'content/{structure_dir}/*.yaml')
                      if comparison_file != reference_file}
        mismatches = {file: mis for file, mis in mismatches.items() if mis}

        if mismatches:
            any_failure = True

            print(f'==================== {path.dirname(reference_file)} =======================')
            print('    Different array lengths between English and other languages.')
            print('    Please make the arrays the same by copying the new English content')
            print('    to the right places in the other files.')
            print()

            # If there are many mismatches, the most natural way to present this information
            # is { path -> file -> mismatch }, but we have { file -> path -> mismatch }, so
            # we have to transpose.
            unique_paths = list(sorted(set(p for paths in mismatches.values() for p in paths)))
            for p in unique_paths:
                mis_by_file = {lang_file: mis_by_path[p]
                               for lang_file, mis_by_path in mismatches.items() if mis_by_path.get(p)}
                first_mis = mis_by_file[next(iter(mis_by_file.keys()))]

                print(f'---------------[ Path in YAML: {p} ]---------------------')
                print(f'File: {reference_file} ({len(first_mis.left)} elements)')
                print('')
                print(indent(4, yaml_to_string(shortened(first_mis.left))))

                for file, mis in mis_by_file.items():
                    print(f'File: {file} ({len(mis.right)} elements)')
                    print('')
                    print(indent(4, yaml_to_string(shortened(mis.right))))

                print('')
    return 1 if any_failure else 0


Mismatch = collections.namedtuple('Mismatch', ('left', 'right'))


def find_mismatched_arrays(reference, other):
    """Recurse through the given structure and find mismatched arrays.

    Disregard mismatched structure, if types aren't correct or not all
    object keys are present, we don't care about that (Weblate will fix it
    later, but Weblate can't fix array mismatches).
    """
    ret = {}

    def recurse(ref, oth, p):
        if isinstance(ref, dict) and isinstance(oth, dict):
            for key in set(ref.keys()) & set(oth.keys()):
                recurse(ref[key], oth[key], p + [f'.{key}'])
            return

        if isinstance(ref, list) and isinstance(oth, list):
            if len(ref) != len(oth):
                ret[''.join(p)] = Mismatch(ref, oth)
            else:
                for i in range(min(len(ref), len(oth))):
                    recurse(ref[i], oth[i], p + [f'[{i}]'])
            return

    recurse(reference, other, [])
    return ret


def shortened(obj, depth=2):
    """Recurse through the given structure and make strings shorter for printing,
    as well as stopping recursion after a certain limit.
    """
    if isinstance(obj, str):
        return obj if len(obj) < 60 else obj[:60] + '{...}'
    if isinstance(obj, dict):
        if depth == 0:
            return '{ ' + ', '.join(sorted(obj.keys())) + ' }'
        return {k: shortened(v, depth-1) for k, v in obj.items()}
    if isinstance(obj, list):
        if depth == 0:
            return f'[ ...{len(obj)} elements... ]'
        return [shortened(x, depth-1) for x in obj]
    return obj


def load_yaml(filename):
    with open(filename, 'r') as f:
        return yaml_writer.load(f)


def yaml_to_string(x):
    strm = StringIO()
    yaml_writer.dump(x, strm)
    return strm.getvalue()


def indent(n, x):
    prefix = ' ' * n
    return '\n'.join(prefix + ln for ln in x.split('\n'))


if __name__ == '__main__':
    sys.exit(main())
