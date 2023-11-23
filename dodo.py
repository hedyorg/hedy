import os
from os import path
import glob


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
        file_dep=(
            glob.glob('templates/**/*.html') +
            glob.glob('main/**/*.md') +
            glob.glob('content/**/*.md') +
            glob.glob('static/js/*.ts')
        ),
        title=lambda _: 'Generate Tailwind CSS',
        actions=[
            [script],
        ],
        targets=[target],

        verbosity=0,  # stderr is too noisy by default
    )


def task_compile_babel():
    """Compile .po files for use with Babel."""
    pofiles = glob.glob('translations/*/*/*.po')

    return dict(
        title=lambda _: 'Compile Babel files',
        file_dep=pofiles,
        actions=[
            ['pybabel', 'compile', '-f', '-d', 'translations'],
        ],
        # Every .po file leads to a .mo file
        targets=[replace_ext(f, '.mo') for f in pofiles],

        verbosity=0,  # stderr is too noisy by default
    )


def task_generate_static_babel_content():
    """Extract information from Babel at build time.

    We do this so we don't have to keep Babel's locale database in memory at
    runtime.
    """
    return dict(
        title=lambda _: 'Generate static Babel content',
        actions=[
            ['build-tools/heroku/generate-static-babel-content'],
        ],
        targets=['static_babel_content.json'],
        uptodate=[babel_version_unchanged],
    )


def task_typescript():
    """Compile typescript."""
    return dict(
        file_dep=glob.glob('static/js/*.ts'),
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
