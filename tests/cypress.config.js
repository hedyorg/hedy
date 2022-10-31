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
    landing_page: '/landing-page',
    login_page: '/login',
    recover_page: '/recover',
    hedy_page: '/hedy',
    stats_class_page: '/stats/class',
    teachers_page: '/for-teachers',
    register_student_page: '/signup?teacher=false',
    register_teacher_page: '/signup?teacher=true'
  }
});
