const fs = require ('fs');
const yaml = require ('yaml');

const ajv = new (require ('ajv'));

const path = require ('path').join (process.argv [2], '../../content/texts') + '/';

// The English translation is our reference
const texts = yaml.parse (fs.readFileSync(path + 'en.yaml', 'utf8'));

// This assumes that texts are grouped in objects that have two levels of depth, and that the outermost objects have no text fields
const properties = {};
Object.keys (texts).map (function (topKey) {
  const props = {};
  Object.keys (texts [topKey]).map (function (subKey) {
    properties [topKey + '::' + subKey] = texts [topKey] [subKey];
  });
});

const files = fs.readdirSync(path);

// We warn (but not throw an error) for 1) fields missing in a non-English translation; 2) fields in a non-English translation that are the same as those of the English translation (hence not translated yet); 3) fields not present in the English translation
files.map (function (file) {
  if (! file.match (/.yaml$/) || file.match (/en\.yaml$/)) return;

  try {
    const currentLanguage = yaml.parse (fs.readFileSync (path + file, 'utf8'));

    Object.keys (currentLanguage).map (function (topKey) {
      Object.keys (currentLanguage [topKey]).map (function (subKey) {
        const enText = properties [topKey + '::' + subKey], currentText = currentLanguage [topKey] [subKey];
        if (enText      === undefined) console.log ('Extraneous field',   topKey + '.' + subKey, 'in file', path + file);
        if (currentText === enText)    console.log ('Untranslated field', topKey + '.' + subKey, 'in file', path + file);
      });
    });
    Object.keys (properties).map (function (key) {
      key = key.split ('::');
      if (currentLanguage [key [0]] [key [1]] === undefined) console.log ('Missing field', key [0] + '::' + key [1], 'in file', path + file);
    });
  }
  catch (error) {
    console.log (error);
    // We do throw an error if the non-English yaml file is outright invalid
    console.log ('Invalid yaml ' + file);
    process.exit (1);
  }
});
