# Minify [![License][LicenseIMGURL]][LicenseURL] [![Dependency Status][DependencyStatusIMGURL]][DependencyStatusURL] [![Build Status][BuildStatusIMGURL]][BuildStatusURL] [![NPM version][NPMIMGURL]][NPMURL]

[NPMIMGURL]: https://img.shields.io/npm/v/minify.svg?style=flat
[BuildStatusURL]: https://github.com/coderaiser/minify/actions/runs/525234132
[BuildStatusIMGURL]: https://github.com/coderaiser/minify/workflows/CI/badge.svg
[DependencyStatusIMGURL]: https://img.shields.io/david/coderaiser/minify.svg?style=flat
[LicenseIMGURL]: https://img.shields.io/badge/license-MIT-317BF9.svg?style=flat
[NPM_INFO_IMG]: https://nodei.co/npm/minify.png?stars
[NPMURL]: http://npmjs.org/package/minify
[LicenseURL]: https://tldrlegal.com/license/mit-license "MIT License"
[DependencyStatusURL]: https://david-dm.org/coderaiser/minify "Dependency Status"

[Minify](http://coderaiser.github.io/minify "Minify") - a minifier of js, css, html and img files.
To use `minify` as middleware try [Mollify](https://github.com/coderaiser/node-mollify "Mollify").

## Install

```
npm i minify -g
```

## How to use?

### CLI

The bash command below creates a code snippet saved as "hello.js".

Simply copy + paste the code starting with cat, including the EOT on the last line, and press <enter>.

```sh
$ cat << EOT > hello.js
const hello = 'world';

for (let i = 0; i < hello.length; i++) {
    console.log(hello[i]);
}
EOT
```

Use the command `minify` followed by the path to and name of the js file intended to be minified. This will minify the code and output it to the screen.

```sh
$ minify hello.js
const hello="world";for(let l=0;l<hello.length;l++)console.log(hello[l]);
```

You can capture the output with the following:

```sh
$ minify hello.js > hello.min.js
```

### Code Example

`minify` can be used as a `promise`:

```js
const minify = require('minify');
const options = {
    html: {
        removeAttributeQuotes: false,
        removeOptionalTags: false,
    },
};

minify('./client.js', options)
    .then(console.log)
    .catch(console.error);

```

Or with `async-await` and [try-to-catch](https://github.com/coderaiser/try-to-catch):

```js
import minify from 'minify';
import tryToCatch from 'try-to-catch';
const options = {
    html: {
        removeAttributeQuotes: false,
        removeOptionalTags: false,
    },
};

const [error, data] = await tryToCatch(minify, './client.js', options);

if (error)
    return console.error(error.message);
```

## Options

The options object accepts configuration for `html`, `css`, `js`, and `img` like so:

```js
const options = {
    html: {
        removeAttributeQuotes: false,
    },
    css: {
        compatibility: '*',
    },
    js: {
        ecma: 5,
    },
    img: {
        maxSize: 4096,
    },
};
```

Full documentation for options that each file type accepts can be found on the pages of the libraries used by minify to process the files:

- HTML: https://github.com/kangax/html-minifier
- CSS: https://github.com/jakubpawlowicz/clean-css
- JS: https://github.com/terser/terser
- IMG: https://github.com/Filirom1/css-base64-images

Minify sets a few defaults for HTML that may differ from the base `html-minifier` settings:

- removeComments:                 true
- removeCommentsFromCDATA:        true
- removeCDATASectionsFromCDATA:   true
- collapseWhitespace:             true
- collapseBooleanAttributes:      true
- removeAttributeQuotes:          true
- removeRedundantAttributes:      true
- useShortDoctype:                true
- removeEmptyAttributes:          true
- removeEmptyElements:            false
- removeOptionalTags:             true
- removeScriptTypeAttributes:     true
- removeStyleLinkTypeAttributes:  true
- minifyJS:                       true
- minifyCSS:                      true

## License

MIT
