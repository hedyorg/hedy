const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: "6y9x8a",
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
  env: {
    base_url: "localhost:8080",
  },
});
