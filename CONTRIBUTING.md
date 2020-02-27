Contributing to Hedy
======================

Installation
------------

Prerequisites:

* Python 3

Here's how to get started:

```
$ python3 -m venv .env
$ source .env/bin/activate
(.env)$ pip install -r requirements.txt

$ python app.py
```

Pre-release environment
-----------------------

The contents of branch `master` are always available on
[hedy-beta.herokuapp.com](https://hedy-beta.herokuapp.com).

The contents of branch `development` are available on
[hedy-alpha.herokuapp.com](https://hedy-alpha.herokuapp.com). This
branch should be treated as read-only, and is forcibly overwritten
to test feature branches locally on the alpha environment.

To push the current commit to the Alpha environment on Heroku:

```
$ git push -f origin HEAD:development
```
