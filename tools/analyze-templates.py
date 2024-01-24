import collections
import ast
from glob import glob
from os import path
import re
import json

from jinja2 import Environment, meta


SourceLocation = collections.namedtuple('SourceLocation', ('filename', 'lineno'))
TemplateInfo = collections.namedtuple('TemplateInfo', ('references', 'variables'))

TEMPLATES_DIR = 'templates'


def main():
    template_names = [path.relpath(p, TEMPLATES_DIR) for p in glob(f'{TEMPLATES_DIR}/**/*.html', recursive=True)]
    python_files = glob('**/*.py', recursive=True)

    parsed_python_files = {x: parse_python(x) for x in python_files}
    parsed_templates = {x: parse_template(x) for x in template_names}

    # Find the locations in Python files where template files are referenced
    template_references = find_string_literals(template_names, parsed_python_files)
    template_infos = extract_template_info(parsed_templates)

    # Make { files -> [ (template, location) ] }
    app_template_mappings = collections.defaultdict(list)
    for template_name, references in template_references.items():
        for reference in references:
            key = (reference.filename, template_name)
            app_template_mappings[key].append(reference.lineno)

    # Print a dot graph
    print('digraph G {')

    for template_name, template_info in template_infos.items():
        label = template_name
        if template_info.variables:
            label += '<br/><font color="blue">' + '<br/>'.join(sorted(template_info.variables)) + '</font>'
        print(f'"{template_name}" [shape=rectangle, label=<{label}>];')
        for ref in template_info.references:
            print(f'"{template_name}" -> "{ref}";')

    for (python_file, template_name), linenos in app_template_mappings.items():
        print(f'"{python_file}" [shape=rectangle, style=filled, fillcolor=palegreen2];')
        lines = '\n'.join(f'L{line}' for line in sorted(linenos))
        print(f'"{python_file}" -> "{template_name}" [label={json.dumps(lines)}];')

    print('}')

    # Parse template files using Jinja


def parse_python(fname):
    with open(fname) as f:
        return ast.parse(f.read(), fname)


def parse_template(fname):
    env = Environment()
    env.filters['commonmark'] = True
    env.filters['slugify'] = True
    env.filters['markdown_retain_newlines'] = True
    with open(path.join(TEMPLATES_DIR, fname)) as f:
        return env.parse(f.read(), fname, fname)


def find_string_literals(strings, asts):
    """Find all occurrences of the given string literals in the ASTs."""
    ret = collections.defaultdict(list)
    strings = set(strings)

    for filename, file_ast in asts.items():
        for node in ast.walk(file_ast):
            if isinstance(node, ast.Constant):
                if node.value in strings:
                    ret[node.value].append(SourceLocation(filename=filename, lineno=node.lineno))

    return ret


def extract_template_info(parsed_templates):
    ret = {}
    for name, abstract_syntax_tree in parsed_templates.items():
        variables = meta.find_undeclared_variables(abstract_syntax_tree) - set(['_'])
        references = set(meta.find_referenced_templates(abstract_syntax_tree))
        if None in references:
            references = references - set([None]) | set(['«dynamic»'])
        ret[name] = TemplateInfo(references=references, variables=variables)
    return ret


def slugify(x):
    return re.sub('[^a-zA-Z0-9.]+', '_', x)


if __name__ == '__main__':
    main()
