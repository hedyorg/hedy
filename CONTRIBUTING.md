Contributing to Hedy
======================


Help Hedy with translations
------------

Hedy is now available in Dutch and English and Spanish, but we'd love to support more languages! To contribute, add translations for all elements in the JSON files [levels](https://github.com/Felienne/hedy/blob/master/static/levels.json) and [texts](https://github.com/Felienne/hedy/blob/master/static/texts.json). The easiest way is to make a copy of the English versions and then change the field `language`. 

You can check the status of the several translation efforts [here](/STATUS.md) and see what you can best work on! 


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
