##
# This file contains various build steps used to make sure the data the Hedy application
# uses is up-to-date.
#
# Functions that start with the name `task_` create a "task", which runs one or more
# "actions" (shell commands or Python functions). Tasks can have file dependencies and
# file outputs, as well as other task dependencies. If none of the files that a task
# depends on have changed since the last time it ran, the task will be skipped. That's
# good for speed!
#
# Keep the following in mind:
# - You can specify commands as a string `'mkdir dir'` or as an array `['mkdir', 'dir']`.
#   The second case doesn't allow shell features, but is safer in case of variables.
# - `file_dep` requires a list of source files, but you can use `glob('*.yaml')`
#   to have Python list them. That way you don't have to keep the list of files up-to-date
#   by hand.
# - It's important to be complete in the list of inputs that go into a build step. You
#   have to list all input files, or the step will not accurately re-run when you change
#   one of the forgotten dependencies.
# - For eexample: include the script itself in the list of `file_dep`s as well;
#   otherwise, even if you change the script the task won't re-run.

import os
from os import path
from glob import glob
import sys


# The current Python interpreter, use to run other Python scripts as well
python3 = sys.executable

# When run without arguments, run deploy
DOIT_CONFIG = {'default_tasks': ['deploy']}


def task_tailwind():
    """Build Tailwind.

    We will automatically switch between DEV and PROD mode depending
    on where we run.
    """
    prod = os.getenv('DYNO') is not None

    if prod:
        script = 'build-tools/heroku/tailwind/generate-prod-css'
        target = 'static/css/generated.css'
    else:
        script = 'build-tools/heroku/tailwind/generate-development-css'
        target = 'static/css/generated.full.css'

    return dict(
        file_dep=[
            *glob('templates/**/*.html'),
            *glob('main/**/*.md'),
            *glob('content/**/*.md'),
            *glob('static/js/*.ts'),
            script,
        ],
        title=lambda _: 'Generate Tailwind CSS',
        actions=[
            [script],
        ],
        targets=[target],

        verbosity=0,  # stderr is too noisy by default
    )


def task_generate_highlighting():
    """Generate JSON files that will be used for syntax highlighting."""
    script = 'highlighting/generate-rules-highlighting.py'

    return dict(
        title=lambda _: 'Generate highlighting rules',
        file_dep=[
            *glob('highlighting/*.py'),
            script,
        ],
        actions=[
            [python3, script],
        ],
        targets=['highlighting/highlighting.json', 'highlighting/highlighting-trad.json'],
    )


def task_compile_babel():
    """Compile .po files for use with Babel."""
    return dict(
        title=lambda _: 'Compile Babel files',
        file_dep=pofiles,
        actions=[
            'pybabel compile -f -d translations',
        ],
        # Every .po file leads to a .mo file
        targets=mofiles,

        verbosity=0,  # stderr is too noisy by default
    )


def task_generate_static_babel_content():
    """Extract information from Babel at build time.

    We do this so we don't have to keep Babel's locale database in memory at
    runtime.
    """
    script = 'build-tools/heroku/generate-static-babel-content'
    return dict(
        title=lambda _: 'Generate static Babel content',
        file_dep=[script],
        actions=[
            [python3, script],
        ],
        targets=['static_babel_content.json'],
        uptodate=[babel_version_unchanged],
    )


def task_client_messages():
    """Use Python to extract messages to a .ts file that will be used in the frontend."""
    script = 'build-tools/heroku/generate-client-messages.py'

    return dict(
        title=lambda _: 'Generate client messages',

        # Depends on a specific YAML file and the .mo files
        file_dep=[
            *glob('content/client-messages/*.yaml'),
            *mofiles,
            script,
        ],
        actions=[
            [python3, script],
        ],
        targets=[
            'static/js/message-translations.ts',
        ],
    )


def task_typescript():
    """Compile typescript."""
    return dict(
        file_dep=[
            *glob('static/js/**/*.ts', recursive=True),
            # Some non-.ts files that we also own
            'static/js/buttons.js',
            'static/js/skulpt_debugger.js',
        ],
        task_dep=['generate_highlighting', 'client_messages'],
        title=lambda _: 'Compile TypeScript',
        actions=[
            # Use tsc to generate .js (this downlevels to old JavaScript versions for old browsers)
            ['npx', 'tsc', '--outDir', '__tmp__'],

            # Then bundle JavaScript into a single bundle
            ['npx', 'esbuild', '__tmp__/static/js/index.js',
             '--bundle', '--sourcemap', '--minify', '--target=es2017',
             '--global-name=hedyApp', '--platform=browser',
             '--outfile=static/js/appbundle.js'],

            # Delete tempdir
            ['rm', '-rf', '__tmp__'],
        ],
        targets=['static/js/appbundle.js'],
        verbosity=0,  # stderr is too noisy by default
    )


def task_lark():
    """Generate Lark grammar files based on keyword information in YAMLs."""
    script = 'content/yaml_to_lark_utils.py'
    keyword_yamls = glob('content/keywords/*.yaml')
    grammars = ['grammars/keywords-' + replace_ext(path.basename(y), '.lark') for y in keyword_yamls]

    return dict(
        title=lambda _: 'Creating Lark grammar files',
        file_dep=[
            script,
            'grammars/keywords-template.lark',
            *keyword_yamls,
        ],
        actions=[
            [python3, script],
        ],
        targets=grammars,
    )


def task_prefixes():
    """Generate Python prefixes for TypeScript"""
    script = 'build-tools/heroku/generate-prefixes-ts'

    return dict(
        title=lambda _: 'Generate Python prefixes for TypeScript',
        file_dep=[
            script,
            *glob('prefixes/*.py'),
        ],
        actions=[
            [script],
        ],
        targets=[
            'static/js/pythonPrefixes.ts'
        ],
    )


def task_lezer_parsers():
    """Generate Lezer parsers."""
    script = 'build-tools/heroku/generate-lezer-parsers'
    grammars = glob('highlighting/lezer-grammars/level*.grammar')
    lezer_files = []
    for grammar in grammars:
        base = replace_ext(path.basename(grammar), '')
        lezer_files.append(f'static/js/lezer-parsers/{base}-parser.ts')
        lezer_files.append(f'static/js/lezer-parsers/{base}-parser.terms.ts')

    return dict(
        title=lambda _: 'Generate Lezer parsers',
        file_dep=[
            *grammars,
            script,
        ],
        actions=[
            [script],
        ],
        targets=lezer_files,
    )


def task_deploy():
    """Commands to run at deploy time on Heroku.

    This groups other commands.
    """
    return dict(
        actions=None,
        task_dep=[
            'tailwind',
            'typescript',
            'compile_babel',
        ]
    )


def task_resetdb():
    """Reset the testing database."""
    return dict(
        title=lambda _: 'Reset testing database (restart app.py to take effect)',
        actions=[
            'cp data-for-testing.json dev_database.json',
        ],
        file_dep=['data-for-testing.json'],
        targets=['dev_database.json'],
    )


def task_extract():
    """Extract new translateable keys from the code."""
    return dict(
        title=lambda _: 'Extract new keys from the code',
        actions=[
            'pybabel extract -F babel.cfg -o messages.pot . --no-location --sort-output',
            'pybabel update -i messages.pot -d translations -N --no-wrap',
        ],
    )


######################################################################################
# Below this line are helpers for the task definitions
#


def replace_ext(filename, ext):
    """Replace the extension of a filename."""
    return path.splitext(filename)[0] + ext


def babel_version_unchanged(task, values):
    """Return True if the Babel version is the same as the last time we ran."""
    babel_version = 0
    try:
        import babel
        babel_version = babel.__version__
    except:
        # This might fail, that's annoying but shouldn't stop the presses.
        print('oops')
        pass

    def save_on_success():
        """This function gets called at the end of a successful build."""
        return {'babel-version': babel_version}
    task.value_savers.append(save_on_success)

    return values.get('babel-version') == babel_version


# These are used in more than one task. Find all .po files, and calculate the
# .mo files that would be generated from them.
pofiles = glob('translations/*/*/*.po')
mofiles = [replace_ext(f, '.mo') for f in pofiles]
