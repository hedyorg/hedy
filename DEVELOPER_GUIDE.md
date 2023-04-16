# Hedy Developer Guide

This document describes conventions used in Hedy development. Read this document
if you are looking to learn more about how to implement new features, or how to
organize your code.

You may see existing code in the current code base that contradicts these
recommendations. Code may be in the wrong place, named incorrectly, or
implemented using non-recommended strategies. If the code has a good reason to
deviate from the advice given here, there will be a code comment explaining why.
Otherwise, the code is from before we wrote down this guidance, and it will be
refactored to match the guide in due time.

## Technologies

The technologies used in building Hedy are the following:

### Backend: Python, Flask, Jinja2, DynamoDB

The backend is a web server, implemented in Python using the Flask framework.
Data is stored in AWS DynamoDB.

The backend accesses the database and renders HTML pages in response to HTTP
requests. HTML pages are rendered using the templating framework Jinja2.

Resources:

* [Flask tutorial](https://flask.palletsprojects.com/en/2.2.x/tutorial/)
* [Jinja2 Template Designer Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)


### Front-end: HTML, Tailwind, HTMX, HyperScript, TypeScript

The front-end is preferably plain HTML and CSS, with a minimal amount of
client-side code (written in TypeScript).

In-page interactivity is added by using either HTMX or HyperScript: HTMX does a
server request and an inline page update, and should be used if the server needs
to be involved in the interaction. HyperScript is like JavaScript but more
expressive, and can be used to add light interactivity to the page. For example:

- If clicking a button needs to read or write something to the database, use
  HTMX.
- If clicking a button needs to show or hide some page element, or change the
  style of some other element, use Hyperscript.

For more advanced use cases that cannot be solved using any of these existing
mechanism, new TypeScript can be added instead. However, this should rarely be
necessary.

For CSS, we use Tailwind. Tailwind is a utility-based class framework, which
means there are a lot of classes to set individual CSS properties. Usually, you
put those classes directly into the HTML. In case it's desirable or necessary,
a combination of styles can be made into a new class using a build step.

* [Tailwind class reference](https://tailwindcss.com/docs/border-radius)
* [HTMX Website](https://htmx.org), pay special attention to the [examples](https://htmx.org/examples/)
* [Hyperscript introduction](https://hyperscript.org/docs/)
* [TypeScript Documentation](https://www.typescriptlang.org/docs/), check the
  **Get Started** column.

## Jinja2 Templates

The main source of how we control what ends up on the page is by using Jinja2
templates. Most Flask routes end in a `render_template('example.html',
my_variable=my_variable)` call, which would take the file
`templates/example.html`, substitute any variables in it (for example, using the
value `{{ my_variable }}`, and send it to the user's browser.

### Reducing code duplication in templates

Jinja2 has the following capabilities to reduce on the amount of copy/pasted
code:

- `{% for %}` loops. Use this if you need to display the same (or similar) HTML
  elements a number of times, for each element in a collection. Even if the
  collection is a fixed size, or the elements are slightly different each time
  (for example, each has a different color), you can still use for loops. Have
  the Python code that provides the variables for the template precalculate the
  attributes that are different, or use the `cycle` function. For example, the
  quiz and the front page both use loops, even though the elements are different
  every time.
- `{% extends %}` and `{% block %}`s. Use this if multiple pages have the same
  basic page structure, but have placeholders where different types of content
  are injected. For example, all pages ultimately extend `layout.html`, which
  includes the menu bar, the CSS and all scripts.
- `{% include %}`. Use this either to reuse small snippets of HTML across
  multiple pages, or to separate out a bit of HTML to a different file for
  better code organization and readability. Files that are designed to be
  included (rather than used in a call to `render_template`). For example, the
  quiz has `incl-question-progress.html`, which is used on multiple pages
  to render the UI that indicates the current question number. Alternatively,
  `menubar.html` is only included from one place, but by splitting it off into a
  separate file the code for it is easy to find.
- `{% macro xyz(...) %}`. Macros are like function calls: they are a way to
  define a paramaterized template fragment that can be instantiated multiple
  times with different values. This is useful if you want to reduce duplication
  but the reused code isn't significant enough to warrant its own file. Macros
  can be defined in includable files to make libraries of reusable snippets
  (if you are planning to go this route, try to explore simpler options first).
  For example, `adventure-tabs.html` has a macro to render a tab, which gets
  called multiple times with multiple arguments. `macros/stats-shared.html`
  is a template designed to be included that defines a bunch of macros that are
  used in the statistics pages.

#### Conventions in template organization

We use the following organization and naming conventions in the templates:

- There are a lot of files in this directory. To keep it organized, prefer
  using a directory by feature or site area if possible.
- Template files that are intended to be included from other templates either
  start with `incl-` or are in the `incl/` directory.
- Template files that are intended to be rendered from Python using
  `render_template()`, but in response to an HTMX request so they don't render
  a full HTML page, start with `hx-`.

## Where to put code

### Deciding between server and client

### How to organize code

## How to make common changes

### How to add hover effects

### How to add click effects, selection effects

### Adding new tables

### GET vs POST


## The database

### Adding new tables

### Querying

## Tailwind

## How to reduce Flask duplication

- `g`
- Scope of variables
- `session`
- preprocessor
