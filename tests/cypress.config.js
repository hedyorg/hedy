const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: '6y9x8a',
  watchForFileChanges: false,
  e2e: {
    baseUrl: 'http://localhost:8080',
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
  env: {
    login_page: '/login',
    hedy_page: '/hedy',
    stats_class_page: '/stats/class'
  }
});
