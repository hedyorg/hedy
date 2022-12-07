Helping build Hedy
------------

We would be grateful if you help make Hedy better! First you will want to follow the instructions below to run the code locally and configuring your machine as explained below. After that, you want to look at these things:

**Open issues**

First have a look at the open issues, there are three categories of issues you can work on:
* [Good first issues](https://github.com/Felienne/hedy/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) are issues that we think are doable for people new to the project.
* [Bugs](https://github.com/hedyorg/hedy/issues?q=is%3Aopen+is%3Aissue+label%3Abug) are problems that people have reported, which we want to see fixed.
* [Approved](https://github.com/hedyorg/hedy/issues?q=is%3Aopen+is%3Aissue+label%3Aapproved) are issues we have decided we want to move forward.

All other issues should not be picked up without contacting us on Discord (see below) since these issues require more deliberation. 

**Project boards**

The core team (currently consisting of [Felienne](https://github.com/Felienne), [boryanagoncharenko](https://github.com/boryanagoncharenko), [Jesus Pelay](https://github.com/jpelay) and [tibiba](https://github.com/tibiba)) keeps track of the issues they will work on in the future on the [Core Team Project Board](https://github.com/Felienne/hedy/projects/5). If there are issues on the Code team Board that you want to help out with, that is always welcome, the core team is kind of busy with many things :)! But do [reach out](mailto:hello@hedy.org) to prevent us from working on the same thing.

Other project boards are student projects that keep track of their own issues, these are typically not open for contributors to work on since we want the students to do their own projects :)

**Discord**

We also run a Discord channel to enable users and contributors to get in touch with us, ask any questions and show off awesome Hedy related content. It is a great way for you as a contributor to stay connected and up-to-date with the Hedy project. Feel free to join the channel to get in touch with us! You can join the channel through [this](https://discord.gg/8yY7dEme9r) Discord link.

**Discussions**

The [Discussion board](https://github.com/Felienne/hedy/discussions) has ideas that are not yet detailed enough to be put into issue, like big new features or overhauls of the language or architecture. If you are interested in picking up such a large feature do [let us know](mailto:hello@hedy.org) and read the corresponding discussion to see what has already been considered.

**For newcomers: No PR without an issue and no "issue + PR"**

While we really love people to help out, we work and prioritize our work as a team and we have a lot of work still on our backlog. 'Random' pull requests can be overwhelming and not always helpful. If you want to help, please pick an open issue to work on. We have a few labeled "good first issue" to get started, or [reach out](mailto:hello@hedy.org). We are always happy to jump on a call to chat about how you can help!!

Run Hedy code on your machine
------------

If you are going to contribute to the code of Hedy, you will probably want to run the code on your own computer. For this you need to:
- install Python 3.7 or higher;
- install Microsoft Visual C++ 14.0 or higher, which you can [download here](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
Then, here's how to get started once you have downloaded or cloned the code:

```bash
$ python3 -m venv .env
$ source .env/bin/activate
(.env)$ pip install -r requirements.txt
```

Or if you're on windows in a powershell window with py launcher installed:
```bash
> py -m venv .env
> ./.env/Scripts/activate.ps1
(.env)> pip install -r requirements.txt
```

If you want to run the website version locally, run:
```bash
(.env)$ python app.py
```
Your local Hedy version should be available on address `http://0.0.0.0:8080/`. It appears that on some Windows machines this address does not work, make sure the server is still running and try visiting the website on `http://localhost:8080/`. 

Additionally, some pages are known to give a type error about string concatenation. This can be fixed by creating an environment variable for the "BASE_URL" and setting it to `http://localhost:8080/`.

To run the unit tests:

```bash
(.env)$ python -m pytest
```

To run the front-end tests, you probably first need to install Cypress.

To install Cypress, the front-end test framework, execute the following commands:
```bash
$ cd tests
$ npm install cypress --save-dev
```

To run the tests go to `/tests/` first.
You can then the tests on the command line with the following: `npx cypress run --spec "[path to test(s)]"`
An example of running cypress: `npx cypress run --spec "cypress/e2e/login_page/*"`

Do note a few things:
* Run the `feed_dev_database.sh` script before running the tests as they something belong on certain users or classes being present in the database
* Run pybabel before running the tests as they can also rely on exact labels
* For the same reason, set your app to English

If you want to connect Cypress to the online dashboard, use:

`npx cypress run --record --key <key here>`

You can also open the Cypress panel, using this in `/tests`:
```
$ npx cypress open
```

You will see the Cypress Launchpad in which you should choose to open the End2End testing panel. Afterwards you are able to run all the tests configured in the test suite, as well as adding your own according to [the documentation of Cypress](https://docs.cypress.io/guides/end-to-end-testing/writing-your-first-end-to-end-test).

### Feeding the local database

Hedy uses a local database in developing environments. This database is called `dev_database.py` and it's not tracked by Git. To feed this local database you can use the one that's been filled with data already, `data-for-testing.json`, it contains:

1. Five users, from user1 to user5.
2. One teacher called teacher1.
3. Five students, from student1 to student5.
4. A class called CLASS1.
5. Several saved programs, quiz attempt and some users have achievements.

The password to all of the accounts is 123456

To feed the dev database with the data in this one, you can run:

```
bash feed_dev_database.sh
```

## Python code styling
As this project is growing and multiple people are working on it, we want to move to a more uniformly styled code base. We choose to stick to PEP8 guidelines, with the exception of a max line length of 120 characters instead of 79. To ensure your code adheres to these guidelines, you can install the pre-commit configuration to automatically check modified code when you make a commit. Installing this pre-commit hook has to be done manually (for security reasons) and can be done using the following commands. The pre-commit hook is available for installation once you run `requirements.txt`:

```
pre-commit install
```

After this, every modification you commit will be linted by flake8 according to the configuration in setup.cfg. If there are any issues with your code, you can fix these manually using the output, or alternatively use autopep8 to solve these issues automatically (although autopep8 can't fix some issues). If you want to do this, install autopep8 using `pip install autopep8` and run `autopep8 --in-place --max-line-length=100 [your-file]`. 

If you want, you can bypass the pre-commit check by adding a no-verify flag:
```git commit -m "your message" --no-verify```

When you push code to the repository or make a pull request, a Github Actions workflow will also automatically check your code. At the moment failing this check does not prevent from merging, as there is still some work to do to make the entire codebase compliant. However, it is appreciated if your modifications of new code follow PEP8 styling guidelines. Keep the Boy Scout Rule in mind: always leave the code better than you found it! 

## Working on the web front-end in TypeScript/JavaScript
Part of the code base of Hedy is written in Python, which runs on the server.
The parts that run in the browser are written in TypeScript, and are compiled to
JavaScript.

So that most people won't have to install special tools, the generated
JavaScript code is checked in. However, if you are working on the browser code,
you need to edit the TypeScript source files and regenerate the JavaScript
bundle by running:

```
# You only need to run 'npm ci' once to install the tools
$ npm ci

# Afterwards run this:
$ build-tools/heroku/generate-typescript --watch
```

The ```--watch``` command will keep looking for changes and automatically update the files. 
To just keep it running while you are working on the front-end code. 
If you just want to run the code once, simply remove this parameter.
Make sure to re-load your browser (and work in incognito mode) to see the changes. 
These files are also automatically generated on deploy, so don't worry if you forget to generate them.

## Working on the web front-end in Tailwind
All the styling in our front-end HTML templates is done using the Tailwind library. 
This library has generated classes for styling which we can call on HTML elements.
To make sure you have access to all possible styling classes, generate the development css file:
```
$ ./build-tools/heroku/tailwind/generate-development-css
```
When merging we want to keep the CSS file as small as possible for performance reasons. 
Tailwind has a built-in ```purge``` option to only generate CSS for classes that are actually being used.
Please run the following command so Tailwind only generated actual used classes:
```
$ ./build-tools/heroku/tailwind/generate-css
```
For all possible styling classes and more, take a look at their [website](https://tailwindcss.com).
If you want to combine different Tailwind classes into one class or one element, we can do this in the ```/build-tool/heroku/tailwind/styles.css``` file.
By using the ```@apply``` attribute we can assign classes to other styling. For example, we styled the ```<h1>``` element with multiple Tailwind classes like this:
```
h1 {
  @apply font-extralight text-4xl;
}
```
If you want to use styling that is not available in the Tailwind library this can be added to the ```static/css/additional.css``` file.
But please, try to use the Tailwind classes as much as possible as these are optimized and keep our code base consistent and readable.
Also, please refrain from using inline CSS styling, as this makes the templates hard to read, maintain and alter.

## Working with translations

For our multilingual web structure we use a combination of YAML files and Babel to deliver language-dependent content.
The content you see in the tabs, mail-templates, achievements, puzzles and quizzes are all stored using YAML files.
All our front-end UI strings, error messages and other "small" translations are stored using Babel.
To help translating any of these, please follow the explanation in [TRANSLATING.md](./TRANSLATING.md).

If you see placeholders with underscores one the website instead of proper texts, like this:

![image](https://user-images.githubusercontent.com/1003685/187742388-27fe3f28-5692-4f42-be0e-93bb9c1131be.png)

That means you will have to run pybabel once:

`pybabel compile -f -d translations`

## Adding new translation keys

When adding new content or implementing a feature that requires new translations you need to manually add these translation keys.

When adding YAML translations please add these to the corresponding YAML file in the ```/content``` folder.
Make sure that you comform to the already existing YAML structure.  As English is the fallback language, the translation should always be available in the English YAML file. Feel free to manually add the translation to as many languages as you know, but don't worry: otherwise these will be translated by other contributors through Weblate.

When adding new Babel translations the implementation is a bit more complex, but don't worry! It should al work fine with the following steps:
1. First we add the translation "placeholder" to either the front-end or back-end
    * When on the front-end (in a .html template) we do this like this: ```{{ _('test') }}```
    * Notice that the ```{{ }}``` characters are Jinja2 template placeholders for variables
    * When on the back-end we do this like this: ```gettext('test')```
2. Next we run the following command to let Babel search for keys. We do not want line numbers since those will lead to lots of Weblate merge conflicts:
    * ```pybabel extract -F babel.cfg -o messages.pot . --no-location```
3. We now have to add the found keys to all translation files, with the following command:
    * ```pybabel update -i messages.pot -d translations -N  --no-wrap```
4. All keys will be automatically stored in the /translations folder
5. Search for the .po files for the languages you know and find the empty msgstr for your added key(s)
6. Add your translations there, the other translation will hopefully be quickly picked up by other translators
7. If you want to test it locally, run:
    * ```pybabel compile -f -d translations```
8. This action will also always be run on deployment to make sure the translations are up-to-date

## Solving common merge conflicts
When working on an issue in a branch it might happen that the main branch is updated before your contribution is finished.
If you create a Pull Request it is possible that GitHub returns _merge conflicts_: 
you've worked on the same code as the updated part of main and GitHub in uncertain on which code to keep when merging.
Always make sure that there are no merge conflicts when setting your PR to _Ready for Review_. 
In this section we describe the most common merge conflicts and how to solve them:

- Conflict with `generated.css`
- Conflict with some (or all of the) `.po files`
- Conflicts with 'appbundle.js' and `appbundle.js.map`

#### Conflict with `generated.css`
When having a merge conflict with the `generated.css` file this is probably the result of you working on CSS code and updating files with the Tailwind script.
While working on this the file is updated on the `main` branch as well. In this case you can simply accept your own branch when a conflict occurs.
If your PR still needs a review, make sure to run the Tailwind script again after the conflicts are solved.
Don't worry if you make a mistake here, the files are always generated again on deploy. Making sure they are always up-to-date.

#### Conflict with some (or all of the) `.po files`
When having a merge conflict with (some of) the .po files this is probably the result of you working with the Babel translations.
When adding a new translatable string all .po files are updated and the _Last revision_ header of each file is updated as well.
As Weblate automatically updates these files as well it might happen that another branch already merge into main triggered Weblate, resulting in merge conflicts in your branch.
These headers don't have influence on the functionality, but it is good practice to keep the main branch header when solving these conflicts.
The po files are **not** generated on deploy, so we should be careful to correctly merge these.

#### Conflict with `appbundle.js` and `appbundle.js.map`
When having a merge conflict with the `appbundle` files this is probably the result of you working on TypeScript code and updating the files.
While working on this the file is updated on the `main` branch as well. In this case you can simply accept your own branch when a conflict occurs.
If your PR still needs a review, make sure to run the TypeScript script again after the conflicts are solved.
Don't worry if you make a mistake here, the files are always generated again on deploy. Making sure they are always up-to-date.

## Using Docker

If you want to run the website locally, but would prefer to use Docker instead
of installing python, you can build a container image and run it like so:

```bash
docker build -t hedy .
```

and then:

```bash
docker run -it --rm -p 8080:8080 --mount type=bind,source="$(pwd)",target=/app hedy
```

## Testing Teacher facing features locally

For some things like making classes you need a teacher's account and you might want to test that locally. To do so, you have to first make an account, this works offline without issues. Then you have to run Hedy with the environment variable ADMIN_USER set to your username, f.e. ADMIN_USER=Pete. It works a bit differently in each IDE, this is what it looks like for PyCharm:

![image](https://user-images.githubusercontent.com/1003685/152981667-0ab1f273-c668-429d-8ac4-9dd554f9bab3.png)

Once you have made yourself an admin, you can access the admin interface on http://localhost:8080/admin. Go to the Users Overview, and on the users page, select the tick-mark under Teacher to make your account a teacher:

![image](https://user-images.githubusercontent.com/1003685/152981987-64010e8b-a850-4178-aa51-42b0f6cd3aeb.png)



Pre-release environment
-----------------------

When you have your PR accepted into `main`, that version will be deployed on [hedy-alpha.herokuapp.com](https://hedy-alpha.herokuapp.com).

We do periodic deploys of `main` to the [production version](https://hedy.org) of Hedy.

Accessing logs 
-----------------------

We store programs for logging purposes on s3. If you want to access the logs, you can use this command (if you have AWS access, mainly this is a note to self for Felienne!):

`aws s3 sync s3://hedy-parse-logs/hedy-beta/ .`

Likely you will have to first set your AWS credentials using:

`aws configure`

You can fetch these credentials here: https://console.aws.amazon.com/iam/home?#security_credential
