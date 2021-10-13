Helping build Hedy
------------

We would be grateful if you help make Hedy better! First you will want to follow the instructions below to run the code locally and configuring your manchine as explained below. After that, you want to look at these things:

**Open issues**

First have a look at the open issues. [Good first issues](https://github.com/Felienne/hedy/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) are issues that we think are doable for people new to the project. But of course, you may pick up other issues too! Issues that are currently unassigned, are not planning to be picked up by us in the near future. For issues that look interesting but are already assigned, just reply on the issue to see if your help can be used.

**Project boards**

The core team (currently consisting of [Felienne](https://github.com/Felienne), [fpereiro](https://github.com/fpereiro) & [boryanagoncharenko](https://github.com/boryanagoncharenko)) keeps track of the issues they will work on in the future on the [Core Team Project Board](https://github.com/Felienne/hedy/projects/5). If there are issues on the Code team Board that you want to help out with, that is always welcome, the core team is kind of busy with many things :)! But do [reach out](mailto:hedy@felienne.com) to prevent us from working on the same thing.

Other project boards are student projects that keep track of their own issues, these are typically not open for contributors to work on since we want the students to do their own projects :) 

**Discussions**

The [Discussion board](https://github.com/Felienne/hedy/discussions) has ideas that are not yet detailed enough to be put into issue, like big new features or overhuals of the langauge or architecture. If you are interested in picking up such a large feature do [let us know](mailto:hedy@felienne.com) and read the corresponding discussion to see what has alrady been thought about.


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

If you prefer to avoid development mode (which might make the app reloads slower when opening Hedy in the browser), pass the `NO_DEBUG_MODE` environment variable.

```bash
(.env)$ env NO_DEBUG_MODE=1 python app.py
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
