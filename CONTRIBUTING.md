Contributing to Hedy
======================


Help Hedy with translations
------------

Hedy is now available in Dutch, French, English, Brazilian Portugese and Spanish, but we'd love to support more languages!

If you would like to add a new translation, there are four places where files that need to be translated:

1) The folder [level-defaults](https://github.com/Felienne/hedy/blob/master/coursedata/level-defaults/) has a file for each language. That file controls what the landing page for each levels looks like. It is probably easiest to copy the [English file](https://github.com/Felienne/hedy/blob/master/coursedata/level-defaults/en.yaml), rename it and translate that. Tip: example variables can be translated too, that is probably helpful for learners!

2) In the folder [texts](https://github.com/Felienne/hedy/tree/master/coursedata/texts) there is a file for each language too. That file translate UI-elements like menu headers, and, important, the error messages Hedy programmers will see. As above, copying the [English file](https://github.com/Felienne/hedy/blob/master/coursedata/texts/en.yaml) and translate that.

3) The folder [main](https://github.com/Felienne/hedy/tree/master/main) controls the web pages around Hedy. [start](https://github.com/Felienne/hedy/blob/master/main/start-en.md) holds the content of the start page, and there is a page with press, and with contact info too. If you want to, you can skip those pages (people will then see the English version)

4) There is also a [folder](https://github.com/Felienne/hedy/tree/master/coursedata/course/hedy/docs-en) with extra instructions for each of the levels. While not mandatory, the docs in this section are of help for kids to better explore each level.

Translated all of that?

Two more small things to do!

1) Add your language to the [menu](https://github.com/Felienne/hedy/blob/master/main/menu.json).

2) Now go to [app.py](https://github.com/Felienne/hedy/blob/master/app.py) and add your language to this list:

```
ALL_LANGUAGES = {
    'en': 'English',
    'nl': 'Nederlands',
    'es': 'Español',
    'fr': 'Français',
    'pt_br': 'Português',
    'de': 'Deutsch',
    'it': 'Italiano'
}
```

In some places, we are missing translations to the existing language. You can find those locations as [issues](https://github.com/Felienne/hedy/issues?q=is%3Aissue+is%3Aopen+label%3A%22translation+needed%22)


Run Hedy code on your machine
------------

If you are going to contribute to the code of Hedy, you will probably want to run the code on your own computer. For this you need to install Python 3.6 or higher. Then, here's how to get started once you have downloaded or cloned the code:

```bash
$ python3 -m venv .env
$ source .env/bin/activate
(.env)$ pip install -r requirements.txt
```

If you want to run the website version locally, run:
```bash
(.env)$ python app.py
```

If you don't want to use a website, you can run the code locally without the need of a website. To create a file use:
```bash
$ touch FILENAME.hedy
```
If you use a higher level than 1, specify the level at the top of the file by typing ```#LEVEL 1-8```. This will let the interpreter know which level you want to run the code on. Now to acctually run the code, type the following command in the terminal:
```bash
(.env)$ python runhedy.py FILENAME.hedy
```
If all did correctly, you will see the output of your code right into the terminal.

If you don't want to specify the level itself in the file, you can use the ```--level``` argument after the filename. You can do it like this:
```bash
(.env)$ python runhedy.py FILENAME.hedy --level 1-8
```
When you execute this, the interpreter will use the specified level.

Pre-release environment
-----------------------

When you have your PR accepted into `master`, that version will be deployed on [hedy-alpha.herokuapp.com](https://hedy-alpha.herokuapp.com).

We do periodic deploys of `master` to the [production version](https://hedycode.com) of Hedy.

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
    "coursedata/adventures/adventures.schema.json": "adventures/*.yaml"
  }
}
```

### IntelliJ (PyCharm/WebStorm/...)

(Instructions still to figure out)