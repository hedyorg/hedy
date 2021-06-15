const fs = require ('fs');
const yaml = require ('yaml');

const ajv = new (require ('ajv'));

const path = require ('path').join (process.argv [2], '../coursedata/texts') + '/';

const file = fs.readFileSync(path + 'en.yaml', 'utf8');

const texts = yaml.parse (file);

const properties = {};
Object.keys (texts).map (function (topKey) {
  const props = {};
  Object.keys (texts [topKey]).map (function (subKey) {
    props [subKey] = {type: 'string'};
  });
  properties [topKey] = {type: 'object', additionalProperties: false, properties: props, required: Object.keys (props)};
});

const schema = {type: 'object', additionalProperties: false, properties: properties, required: Object.keys (properties)};

const files = fs.readdirSync(path);

files.map (function (file) {
  if (! file.match (/.yaml$/)) return;

  let parsed;

  try {
    parsed = yaml.parse (fs.readFileSync (path + file, 'utf8'));
  }
  catch (error) {
    console.log ('Invalid yaml ' + file);
    process.exit (1);
  }
  if (! ajv.validate (schema, parsed)) {
    console.log ('Invalid file ' + file, JSON.stringify (ajv.errors));
    process.exit (1);
  }
  console.log (path + file, 'OK');
});
