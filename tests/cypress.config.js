const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: '6y9x8a',
  watchForFileChanges: false,
  e2e: {
    
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
  env: {
    base_url: 'http://localhost:8080',
    login_page: '/login',
    hedy_page: '/hedy'
  }
});
