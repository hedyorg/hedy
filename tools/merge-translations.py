from collections.abc import Mapping
import shutil
from glob import glob
from os import path
from ruamel import yaml


yaml_loader = yaml.YAML(pure=True)


def main():
    merge_yaml_files('content-raw', 'content')
    merge_po_files('translations-raw', 'translations')


def merge_yaml_files(source_dir, target_dir):
    yaml_loader.preserve_quotes = True
    yaml_loader.default_flow_style = False

    translated_files = glob(f'{source_dir}/*/*.yaml')
    for current_filename in translated_files:
        dir_name = path.basename(path.dirname(current_filename))
        fallback_filename = path.join(source_dir, dir_name, f'{get_fallback_language()}.yaml')
        output_filename = path.join(target_dir, dir_name, path.basename(current_filename))

        if fallback_filename == current_filename:
            shutil.copyfile(current_filename, output_filename)
        else:
            current_file = load_yaml_file(current_filename)
            fallback_file = load_yaml_file(fallback_filename)
            result = merge_dicts(current_file, fallback_file)

            with open(output_filename, 'w') as yaml_output:
                yaml_output.write(f"# Generated file. Do not edit. Add your changes to {source_dir}/\n")
                yaml_loader.dump(result, yaml_output)


def merge_dicts(source, fallback):
    """ Merges 2 dictionaries containing nested dictionaries """
    for key, value in source.items():
        if value and isinstance(value, Mapping):
            returned = merge_dicts(value, fallback.get(key, {}))
            fallback[key] = returned
        else:
            fallback[key] = source[key]
    return fallback


def merge_po_files(source_dir, target_dir):
    raw_files = glob(f'{source_dir}/**/*.po')
    # for now English is the fallback for all
    fallback = get_po_fallback_dict(source_dir)
    cur_msg_id = None
    for rf in raw_files:
        lines = []
        with open(rf, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith('msgid'):
                    cur_msg_id = line

                line_wf = fallback[cur_msg_id] if line.startswith('msgstr ""') else line
                lines.append(line_wf)

        with open(rf.replace(source_dir, target_dir), 'w') as output:
            output.write("".join(lines))


def get_po_fallback_dict(source_dir):
    result = dict()
    fallback_lang = get_fallback_language()
    cur_msg_id = None
    with open(f"{source_dir}/{fallback_lang}/LC_MESSAGES/messages.po", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith('msgid'):
                cur_msg_id = line
            elif line.startswith('msgstr'):
                result[cur_msg_id] = line
    return result


def get_fallback_language():
    # TODO: for now return English, but add a mapping in the future
    return 'en'


def load_yaml_file(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        return yaml_loader.load(f)


if __name__ == "__main__":
    main()
