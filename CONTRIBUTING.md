Contributing to Hedy
======================


Help Hedy with translations
------------

Hedy is now available in Dutch, French, English and Spanish, but we'd love to support more languages! 

If you would like to add a translation, there a three places where files that need to be translated:

1) The folder [level-defaults](https://github.com/Felienne/hedy/blob/master/coursedata/level-defaults/) has a file for each language. That file controls what the landing page for each levels looks like. It is probably easiest to copy the [English file](https://github.com/Felienne/hedy/blob/master/coursedata/level-defaults/en.yaml), rename it and translate that. Tip: example variables can be translated too, that is probably helpful for learners!

2) In the folder [texts](https://github.com/Felienne/hedy/tree/master/coursedata/texts) there is a file for each language too. That file translate UI-elements like menu headers, and, important, the error messages Hedy programmers will see. As above, copying the English file [English file](https://github.com/Felienne/hedy/blob/master/coursedata/texts/en.yaml) and translate that.

3) The folder [main](https://github.com/Felienne/hedy/tree/master/main) controls the web pages around Hedy. [start](https://github.com/Felienne/hedy/blob/master/main/start-en.md) holds the content of the start page, and there is a page with press, and with contact info too. If you want to, you can skip those pages (people will then see the English version)

Translated all of that? 

Two more small things to do!

1) Add your language to the [menu](https://github.com/Felienne/hedy/blob/master/main/menu.json).

2) Now go to [app.py](https://github.com/Felienne/hedy/blob/master/app.py) and add your language to this list:

ALL_LANGUAGES = {
    'en': '🇺🇸',
    'nl': '🇳🇱',
    'es': '🇪🇸',
    'fr': '🇫🇷',
}

You can check the status of the several translation efforts [here](/STATUS.md) and see what you can best work on. Would be lovely if you update your own translations there too :)


Run Hedy code on your machine
------------

If you are going to contribute to the code of Hedy, you will probably want to run the code on your own computer. For this you need to install Python 3. Then, here's how to get started once you have downloaded or cloned the code:

```bash
$ python3 -m venv .env
$ source .env/bin/activate
(.env)$ pip install -r requirements.txt

$ python app.py
```

Pre-release environment
-----------------------

When you push to `master` or have your PR accepted, that version will be deployed on
[hedy-beta.herokuapp.com](https://hedy-beta.herokuapp.com).

If you want to try experimental versions live, you can use the `development` branch, which will be deployed to [hedy-alpha.herokuapp.com](https://hedy-alpha.herokuapp.com). 
This branch should be treated as read-only, and is forcibly overwritten to test feature branches locally on the alpha environment.

To push the current commit to the Alpha environment on Heroku:

```bash
$ git push -f origin HEAD:development
```
