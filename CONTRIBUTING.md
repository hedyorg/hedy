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

## Working on the browser JavaScript

Part of the code base of Hedy is written in Python, which runs on the server.
The parts that run in the browser are written in TypeScript, and are compiled to
JavaScript.

So that most people won't have to install special tools, the generated
JavaScript code is checked in. However, if you are working on the browser code,
you need to edit the TypeScript source files and regenerate the JavaScript
bundle by running:

```
$ build-tools/heroku/generate-typescript
```

Before reloading your browser.

## Using Docker

If you want to run the website locally, but would prefer to use Docker instead
of installing python, you can build a container image and run it like so:

```bash
docker build -t hedy .
```

and then:

```bash
docker run -it --rm -p 5000:5000 hedy
```

## Running Hedy files from the command line

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
