Helping build Hedy
------------

We would be grateful if you help make Hedy better! First you will want to follow the instructions below to run the code locally and configuring your manchine as explained below. After that, you want to look at these things:

**Open issues**

First have a look at the open issues. [Good first issues](https://github.com/Felienne/hedy/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) are issues that we think are doable for people new to the project. But of course, you may pick up other issues too! Issues that are currently unassigned, are not planning to be picked up by us in the near future. For issues that look interesting but are already assigned, just reply on the issue to see if your help can be used.

**Project boards**

The core team (currently consisting of [Felienne](https://github.com/Felienne), [boryanagoncharenko](https://github.com/boryanagoncharenko), [Jesus Pelay](https://github.com/jpelay) and [tibiba](https://github.com/tibiba)) keeps track of the issues they will work on in the future on the [Core Team Project Board](https://github.com/Felienne/hedy/projects/5). If there are issues on the Code team Board that you want to help out with, that is always welcome, the core team is kind of busy with many things :)! But do [reach out](mailto:hedy@felienne.com) to prevent us from working on the same thing.

Other project boards are student projects that keep track of their own issues, these are typically not open for contributors to work on since we want the students to do their own projects :)

**Discord**

We also run a Discord channel to enable users and contributors to get in touch with us, ask any questions and show off awesome Hedy related content. It is a great way for you as a contributor to stay connected and up-to-date with the Hedy project. Feel free to join the channel to get in touch with us! You can join the channel through [this](https://discord.gg/8yY7dEme9r) Discord link.

**Discussions**

The [Discussion board](https://github.com/Felienne/hedy/discussions) has ideas that are not yet detailed enough to be put into issue, like big new features or overhuals of the language or architecture. If you are interested in picking up such a large feature do [let us know](mailto:hedy@felienne.com) and read the corresponding discussion to see what has alrady been considered.

**For newcomers: No PR without an issue and no "issue + PR"**

While we really love people to help out, we work and prioritize our work as a team and we have a lot of work still on our backlog. 'Random' pull requests can be overwhelming and not always helpful. If you want to help, please pick an open issue to work on. We have a few labeled "good first issue" to get started, or [reach out](mailto:hedy@felienne.com). We are always happy to jump on a call to chat about how you can help!!

Run Hedy code on your machine
------------

If you are going to contribute to the code of Hedy, you will probably want to run the code on your own computer. For this you need to:
- install Python 3.7 or higher;
- install Microsoft Visual C++ 14.0 or higher, which you can [download here](https://code.visualstudio.com/Download)
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

To run the unit tests:

```bash
(.env)$ python -m pytest
```

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
The adventures, level-defaults, mail-templates, achievements and quizzes are all stored using YAML files.
All our front-end UI strings, error messages and other "small" translations are stored using Babel.
To help translating any of these, please follow the explanation in TRANSLATING.md.

However, when adding new content or implementing a feature that requires new translations you need to manually add these translation keys.
When adding YAML related translations please add these to the corresponding YAML file in the ```/coursedata``` folder.
Make sure that you comform to the already existing YAML structure.  As English is the fallback language, the translation should always be available in the english YAML file.
Feel free to manually add the translation to as many languages as you know, but don't worry: otherwise these will be translated by other contributors through Weblate.

When adding new Babel related translation the implementation is a bit more complex, but don't worry! It should al work fine with the following steps:
1. First we add the translation "placeholder" to either the front-end or back-end
    * When on the front-end (in a .html template) we do this like this: ```{{ _('test') }}```
    * Notice that the ```{{ }}``` characters are Jinja2 template placeholders for variables
    * When on the back-end we do this like this: ```gettext('test')```
2. Next we run the following command to let Babel search for keys:
    * ```pybabel extract -F babel.cfg -o messages.pot .```
3. We now have to add the found keys to all translation files, with the following command:
    * ```pybabel update -i messages.pot -d translations```
4. All keys will be automatically stored in the /translations folder
5. Search for the .po files for the languages you know and find the empty msgstr for your added key(s)
6. Add your translations there, the other translation will hopefully be quickly picked up by other translators
7. If you want to test it locally, run:
    * ```pybabel compile -d translations```
8. This action will also always be run on deployment to make sure the translations are up-to-date

## Using Docker

If you want to run the website locally, but would prefer to use Docker instead
of installing python, you can build a container image and run it like so:

```bash
docker build -t hedy .
```

and then:

```bash
docker run -it --rm -p 8080:8080 hedy
```

## Testing Teacher facing features locally

For some things like making classes you need a teacher's account and you ight want to test that locally. To do so, you have to first make an account, this works offline without issues. Then you have to run Hedy with the environment variable ADMIN_USER set to your username, f.e. ADMIN_USER=Pete. It works a bit differently in each IDE, this is whta it looks like for PyCharm:

![image](https://user-images.githubusercontent.com/1003685/152981667-0ab1f273-c668-429d-8ac4-9dd554f9bab3.png)

Once you have made yourself an admin, you can acess the admin interface on http://localhost:8080/admin. Go to the Users Overview, and on the users page, select the tickmark under Teacher to make your account a teacher:

![image](https://user-images.githubusercontent.com/1003685/152981987-64010e8b-a850-4178-aa51-42b0f6cd3aeb.png)



Pre-release environment
-----------------------

When you have your PR accepted into `main`, that version will be deployed on [hedy-alpha.herokuapp.com](https://hedy-alpha.herokuapp.com).

We do periodic deploys of `main` to the [production version](https://hedycode.com) of Hedy.

Editing YAML files with validation
----------------------------------

If you need to edit the YAML files that make up the Hedy adventure mode,
you can have them validated as-you-type against our JSON schemas.

This does require some manual configuration in your IDE, which we can
unfortunately not do automatically for you. What you need to do depends
on which IDE you are using. Here are the IDEs we know about:

### Visual Studio Code

* Install the Vistual Studio Code [YAML plugin](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)
* After installing the plugin, press **F1**, and type **Preferences: Open Worspace Settings (JSON)**.
* Add the following `yaml.schemas` key to the JSON file that shows up:

```json
{
  // ...
  "yaml.schemas": {
    "content/adventures/adventures.schema.json": "adventures/*.yaml"
  }
}
```

### IntelliJ (PyCharm/WebStorm/...)

* Open **Preferences**
* Navigate to **Languages & Frameworks → Schemas and DTDs → JSON Schema Mappings**.
* Click the **+** to add a new schema.
  * Behind **Schema file or URL**, click the browse button and navigate to the `<your Hedy checkout>/content/adventures/adventures.schema.json` file.
  * Click the **+** at the bottom, select **Directory**. In the new line that appears, paste `content/adventures`.
* Click **OK** to close the window.
