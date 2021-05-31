Contributing to Hedy
======================

Hedy is now available in Dutch, French, English, Brazilian Portugese, Greek Mandarin, Hungarian and Spanish, but we'd love to support more languages!

Help Hedy with translations (easy, no programming needed!)
------------

The easiest way to translate Hedy is by using or translation UI website!

Simply go to https://www.hedycode.com/translate/en/new and translate our texts that are shown on the left in the boxes on the right. When you are done, you can use the three download button at the end of the page, and [send us the files](mailto:hedy@felienne.com).

![image](https://user-images.githubusercontent.com/1003685/116811756-3ed55f80-ab4b-11eb-881a-85677a30ef5e.png)

You can also use this interface to extend or repair existing translations, then you have to use the iso code of the langage that you want to work with in the url instead of new, f.e. https://www.hedycode.com/translate/en/es for Spanish. That will show the existing translated texts for you to update. After you have made changes again download the files and send them to us per email.


Help Hedy with translations (in the code base, some coding experience needed)
------------

If you would like to add a new translation, there are four places where files are located that need to be translated:

1) The folder [level-defaults](https://github.com/Felienne/hedy/blob/main/coursedata/level-defaults/) has a file for each language. That file controls what the landing page for each levels looks like. It is probably easiest to copy the [English file](https://github.com/Felienne/hedy/blob/main/coursedata/level-defaults/en.yaml), rename it and translate that. Tip: example variables can be translated too, that is probably helpful for learners!

2) In the folder [texts](https://github.com/Felienne/hedy/tree/main/coursedata/texts) there is a file for each language too. That file translate UI-elements like menu headers, and, important, the error messages Hedy programmers will see. As above, copying the [English file](https://github.com/Felienne/hedy/blob/main/coursedata/texts/en.yaml) and translate that.

3) The [folder](https://github.com/Felienne/hedy/tree/main/coursedata/adventures) that control the assignments kids see in the user interface for each of the levels. While not mandatory, the assignments in this section are of help for kids to better explore each level. If you do not translate them, the English version will be shown.

4) *optional* The folder [main](https://github.com/Felienne/hedy/tree/main/main) controls the web pages around Hedy. [start](https://github.com/Felienne/hedy/blob/main/main/start-en.md) holds the content of the start page, and there are page with press, contact info too. These do not necessariyl have to be translated, if you don't people will then see the English version, but kids can still program in their own native language.


Translated all of that?

Two more small things to do!

1) Add your language to the [menu](https://github.com/Felienne/hedy/blob/main/main/menu.json).

2) Now go to [app.py](https://github.com/Felienne/hedy/blob/main/app.py) and add your language to this list:

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

To run the unit tests:

```bash
(.env)$ python -m unittest discover -s tests
```

To make debugging a lot more convenient, enable **development mode**. If you do this, any HTML templates and Python
source files you change and save will automatically be reloaded.

(Be aware that your program may stop with a `SyntaxError` if you save a Python file
while the code is not complete. If this happens too often because you reflexively hit Ctrl-S 😉
you can wrap the command in a loop to restart the server quickly).


```bash
(.env)$ env FLASK_ENV=development python app.py
# or in a loop if it stops too often
(.env)$ while true; do env FLASK_ENV=development python app.py; sleep 1; done
```

If you want to run the website locally, but would prefer to use Docker instead of installing python, you can build a container image and run it like so:

```bash
docker build -t hedy .
```
and then
```bash
docker run -it --rm -p 5000:5000 hedy
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
    "coursedata/adventures/adventures.schema.json": "adventures/*.yaml"
  }
}
```

### IntelliJ (PyCharm/WebStorm/...)

* Open **Preferences**
* Navigate to **Languages & Frameworks → Schemas and DTDs → JSON Schema Mappings**.
* Click the **+** to add a new schema.
  * Behind **Schema file or URL**, click the browse button and navigate to the `<your Hedy checkout>/coursedata/adventures/adventures.schema.json` file.
  * Click the **+** at the bottom, select **Directory**. In the new line that appears, paste `coursedata/adventures`.
* Click **OK** to close the window.
