import sys
from os import path
import glob
import collections
from ruamel import yaml
from io import StringIO


yaml_writer = yaml.YAML(typ="rt")


def main():
    dirs = sys.argv[1:]
    reference_files = [f'content/{dir}/en.yaml' for dir in dirs] if dirs else glob.glob('content/*/en.yaml')

    any_failure = False
    for reference_file in reference_files:
        en = load_yaml(reference_file)
        structure_dir = path.basename(path.dirname(reference_file))

        mismatches = {comparison_file: find_mismatched_types(en, load_yaml(comparison_file))
                      for comparison_file in glob.glob(f'content/{structure_dir}/*.yaml')
                      if comparison_file != reference_file}
        mismatches = {file: mis for file, mis in mismatches.items() if mis}

        if mismatches:
            any_failure = True

            print(f'==================== {path.dirname(reference_file)} =======================')
            print('The script ensures that the structure of the language yamls is a subset of the English yaml.')
            print('It checks that the following are true:')
            print('    - properties are of the same type (e.g. list, dict)')
            print('    - a list in the language yaml does not have more elements than the English yaml')
            print('    - a dict in the language yaml does not have a key that is not present in the English yaml')
            print()

            # If there are many mismatches, the most natural way to present this information
            # is { path -> file -> mismatch }, but we have { file -> path -> mismatch }, so
            # we have to transpose.
            unique_paths = list(sorted(set(p for paths in mismatches.values() for p in paths)))
            for p in unique_paths:
                mis_by_file = {lang_file: mis_by_path[p]
                               for lang_file, mis_by_path in mismatches.items() if mis_by_path.get(p)}
                first_mis = mis_by_file[next(iter(mis_by_file.keys()))]

                print(f'---------------[ Path in YAML: {p}, Error: {first_mis.err} ]---------------------')
                print(f'{first_mis.msg}')
                print('')
                print(f'Reference file: {reference_file}')
                print('')
                print(indent(4, yaml_to_string(shortened(first_mis.left))))

                for file, mis in mis_by_file.items():
                    print(f'Language file: {file}')
                    print('')
                    print(indent(4, yaml_to_string(shortened(mis.right))))

                print('')
    return 1 if any_failure else 0


Mismatch = collections.namedtuple('Mismatch', ('left', 'right', 'err', 'msg'))


def find_mismatched_types(reference, other):
    """Recurse through the given structure and find mismatched arrays.

    Disregard mismatched structure, if types aren't correct or not all
    object keys are present, we don't care about that (Weblate will fix it
    later, but Weblate can't fix array mismatches).
    """
    ret = {}

    def recurse(ref, oth, p):
        """Returns True if any mismatches were found, in which case we stop iterating lists."""

        path_str = ''.join(p)

        if isinstance(ref, str) and isinstance(oth, dict):
            ret[path_str] = Mismatch(
                ref, oth, 'Type mismatch', (f'The path {path_str} is a string in the reference file but a '
                                            'dict in the lang file.'))
            return True

        if isinstance(ref, dict) and oth:
            if not isinstance(oth, dict):
                ret[path_str] = Mismatch(ref, oth, 'Type mismatch', (f'The path {path_str} is of type dict in the '
                                                                     'reference file but not in the lang file.'))
                return True

            exk = set(oth.keys()) - set(ref.keys())
            if exk:
                ret[path_str] = Mismatch(ref, oth, 'Extra keys in dict', (f'The path {path_str} is a dict that '
                                                                          'contains more keys than the reference '
                                                                          f'file: {exk}'))
                return True

            any_mismatch = False
            for key in set(ref.keys()) & set(oth.keys()):
                any_mismatch |= recurse(ref[key], oth[key], p + [f'.{key}'])
            return any_mismatch

        if isinstance(ref, list) and oth:
            if not isinstance(oth, list):
                ret[path_str] = Mismatch(ref, oth, 'Type mismatch', (f'The path {path_str} is of type list in '
                                                                     'the reference file but not in the lang file.'))
                return True

            if len(ref) < len(oth):
                ret[path_str] = Mismatch(ref, oth, 'Array length mismatch', (f'The path {path_str} is a list with more '
                                                                             f'elements than in the reference file.'))
                return True

            for i in range(min(len(ref), len(oth))):
                # Early break on iterating lists, the issue is probably with first list element and reporting on
                # following failures is just noisy and confusing
                if recurse(ref[i], oth[i], p + [f'[{i}]']):
                    return True

        return False

    recurse(reference, other, [])
    return ret


def diff_type(ref, oth, cl):
    return (isinstance(ref, cl) and not isinstance(oth, cl)) or (not isinstance(ref, cl) and isinstance(oth, cl))


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
