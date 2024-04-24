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
import platform

from doit.tools import LongRunning

if os.getenv('GITHUB_ACTION') and platform.system() == 'Windows':
    # Add MSYS2 to the path, so we can use commands like 'bash' and 'cp' and 'mv'.
    # https://github.com/actions/runner-images/blob/win22/20240204.1/images/windows/Windows2022-Readme.md
    print('Detected a Windows GitHub runner. Adding MSYS2 to the PATH.')
    msys_dir = 'C:\\msys64\\usr\\bin'
    os.environ['PATH'] = msys_dir + ';' + os.environ['PATH']

    # We need to explicitly invoke bash from this directory, otherwise
    # it will pick up a bash that requires WSL to run, which is not installed.
    # And npx must be invoked like this as well.
    npx = 'npx.cmd'
    bash = f'{msys_dir}\\bash.exe'
else:
    npx = 'npx'
    bash = 'bash'

# The current Python interpreter, use to run other Python scripts as well
python3 = sys.executable

# When run without arguments, run deploy
DOIT_CONFIG = {'default_tasks': ['deploy']}


def task_npm():
    """Install NPM dependencies.

    If the `package-lock.json` file changes, we will automatically re-install
    NPM dependencies.

    This makes sure everyone's NPM dependencies are at the same version when
    scripts are being run, so build results are consistent and (for example)
    generated Tailwind CSS files are the exact same and don't introduce random
    floating diffs.

    NPM works like this:

    ```
        package.json          # contains version RANGES that you would like to use
            ---> npm install  # install the most recent POINT VERSIONs that match the requested ranges
        package-lock.json     # contains the point versions selected by the last `npm install`
            ---> npm ci       # install exactly the point versions found in the lock file
    ```
    """
    # This task gives problems whhen deploying to Heroku, so not execute it if we are there
    if is_running_on_heroku():
        return dict(title=lambda _: 'Do not install NPM on Heroku', actions=[])

    return dict(
        # `package-lock.json` contains the actual dependency versions that `npm ci` will install
        file_dep=['package-lock.json'],
        title=lambda _: 'Install NPM dependencies',
        actions=[
            'npm ci',
        ],
    )


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
            # exclude files generated for translations
            *[file for file in glob('static/js/*.ts') if file not in \
                ['static/js/message-translations.ts', 'static/js/client-messages.ts']
              ],
            'build-tools/heroku/tailwind/styles.css',
            script,
        ],
        task_dep=['npm'],
        title=lambda _: 'Generate Tailwind CSS',
        actions=[
            [bash, script],
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
        task_dep=['generate_highlighting', 'client_messages', 'npm'],
        title=lambda _: 'Compile TypeScript',
        actions=[
            # Use tsc to do type checking of the .ts files, but don't actually emit.
            # We will bundle using `esbuild`, which will properly handle including the `tw-elements`
            # library (which is ESM-only) from otherwise CommonJS packages.
            [npx, 'tsc', '--noEmit'],

            # Then bundle JavaScript into a single bundle
            [npx, 'esbuild', 'static/js/index.ts',
             '--bundle', '--sourcemap', '--target=es2017',
             '--global-name=hedyApp', '--platform=browser',
             '--outfile=static/js/appbundle.js'],
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
        title=lambda _: 'Create Lark grammar files',
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
            [bash, script],
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
        task_dep=['npm'],
        actions=[
            [bash, script],
        ],
        targets=lezer_files,
    )


def task_extract():
    """Extract new translateable keys from the code.

    To avoid merge conflicts with Weblate as much as possible, we will avoid
    updating the PO file header (which usually contains metadata like
    timestamps etc) -- this is likely to lead to conflicts when both Weblate
    and this script have updated the PO files at the same time.
    """
    restore_po_header = 'build-tools/github/restore-po-header.py'
    return dict(
        title=lambda _: 'Extract new keys from the code',
        actions=[
            # Save current files
            'cp messages.pot messages.pot.tmp',
            *[f'cp {pofile} {pofile}.tmp' for pofile in pofiles],

            # Extract
            'pybabel extract -F babel.cfg -o messages.pot . --no-location --sort-output',
            'pybabel update -i messages.pot -d translations -N --no-wrap',

            # Restore headers, remove tempfiles
            [python3, restore_po_header, 'messages.pot.tmp', 'messages.pot'],
            'rm messages.pot.tmp',
            *[[python3, restore_po_header, f'{pofile}.tmp', pofile] for pofile in pofiles],
            *[f'rm {pofile}.tmp' for pofile in pofiles],
        ],
        # These commands print a bunch of progress to stderr that looks intimidating
        verbosity=0,
    )


def task_devserver():
    """Run a copy of the development server.

    This server is configured to be useful for running cypress tests against.

    No file dependencies, so this task is never skipped.

    Be careful to only depend on `backend` tasks, not `frontend` tasks, so that
    the people running this command still don't need to have Node installed
    if they don't want to work on the frontend.
    """
    return dict(
        title=lambda _: 'Run development server',
        task_dep=['backend'],
        actions=[
            LongRunning([python3, 'app.py'], shell=False, env=dict(
                os.environ,
                # These are required to make some local features work.
                BASE_URL="http://localhost:8080/",
                ADMIN_USER="admin",))
        ],
        verbosity=2,  # show everything live
    )


def task_normalize_yaml():
    """Normalize the YAML files by running a script.

    Makes indentation and key ordering uniform, even if the files get rewritten by
    Weblate.
    """
    yamls = glob('content/**/*.yaml', recursive=True)

    return dict(
        title=lambda _: 'Normalize YAML',
        file_dep=[
            'tools/rewrite-content-yaml.py',
            *yamls,
        ],
        actions=[
            [python3, 'tools/rewrite-content-yaml.py', *yamls]
        ]
    )


######################################################################################
# Some useful task groups
#

def task_backend():
    """Run all tasks necessary to prepare the backend."""
    return dict(
        actions=None,
        task_dep=[
            'compile_babel',
            'generate_static_babel_content',
            'lark',
        ],
    )


def task_frontend():
    """Run all tasks necessary to prepare the frontend."""
    return dict(
        actions=None,
        task_dep=[
            'lezer_parsers',
            'tailwind',
            'typescript',
        ]
    )


def task_deploy():
    """Commands to run at deploy time on Heroku.

    This groups other commands.
    """
    return dict(
        actions=None,
        task_dep=['frontend', 'backend']
    )


def task_devdb():
    """Reset the testing database."""
    return dict(
        title=lambda _: 'Reset testing database (restart app.py to take effect)',
        actions=[
            'cp data-for-testing.json dev_database.json',
        ],
        # No dependencies, so that this script will always run when you invoke it
        targets=['dev_database.json'],
    )


def task__offline():
    """Build the offline Hedy distribution."""

    return dict(
        title=lambda _: 'Build offline Hedy',
        task_dep=['backend', 'frontend'],
        actions=[
            'pyinstaller -y app.spec',
            # We copy this here instead of in the 'spec' file so that we can rename
            # the file (spec file copies cannot do that).
            'cp data-for-testing.json dist/offlinehedy/database.json',
            'cp OFFLINE_README.txt dist/offlinehedy/README.txt',
            # There are some research papers in the distribution that take up a lot
            # of space.
            'rm -rf dist/offlinehedy/_internal/content/research/*',
        ],
    )


def task__autopr():
    """Run code generation tasks that should commit to PRs.

    This runs some tasks, mostly around translation, that contributors should
    run on their machines but tend to forget. That's what machines are for!

    We used to run heavy normalization over the translation files here. However,
    if we do that Weblate will nearly always be in a state of conflicts, which
    leads to scary warnings. Instead, we let Weblate decide what these files
    should look like.
    """

    return dict(
        title=lambda _: 'Run automatic commit updates',
        task_dep=[
            'extract',
            'backend',
            'frontend',
            # No normalization for now!
            # 'normalize_yaml',
        ],
        actions=[
            # No normalization for now!
            # Run a script to strip things that lead to conflicts from po files
            # [python3, 'build-tools/github/normalize-pofiles.py'],
        ])


def task__autopr_weblate():
    """Run code generation tasks that should commit to PRs, only for Weblate PRs.

    This runs YAML snippet tests, in a way that will revert snippets to Enligsh
    if they fail.

    These are separate from normal autofixes because unit tests may take a long time
    to run, and we don't want to hold up normal PRs.

    This script can produce a `.tmp.md` file reporting reverted snippets. When run from
    GitHub Actions, the result will be posted to the PR as a comment.
    """
    os.environ['FIX_FOR_WEBLATE'] = '1'
    return dict(
        title=lambda _: 'Automatic tasks for Weblate only',
        actions=[
            [python3, '-m', 'pytest', '-n', '4', 'tests/test_snippets/'],
        ])

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
    except Exception:
        # This might fail, that's annoying but shouldn't stop the presses.
        print('oops')
        pass

    def save_on_success():
        """This function gets called at the end of a successful build."""
        return {'babel-version': babel_version}
    task.value_savers.append(save_on_success)

    return values.get('babel-version') == babel_version


def is_running_on_heroku():
    """Return True if we are running on Heroku.

    Check an environment variable that Heroku sets by default.
    """
    return 'DYNO' in os.environ


# These are used in more than one task. Find all .po files, and calculate the
# .mo files that would be generated from them.
pofiles = glob('translations/*/*/*.po')
mofiles = [replace_ext(f, '.mo') for f in pofiles]
