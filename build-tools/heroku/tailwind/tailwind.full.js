const baseConfig = require('./tailwind.config');

module.exports = {
  ...baseConfig,

  // This makes it so we don't strip anything, but keep all classes
  // in the full CSS file
  safelist: [
    { pattern: /./ },
  ],
};