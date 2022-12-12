const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: 'a1fbb9',
  watchForFileChanges: false,
  video: false,
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
    hedy_level2_page: '/hedy/2',
    admin_page: '/admin',
    admin_users_page: '/admin/users',
    teachers_page: '/for-teachers',
    customize_class_page: '/for-teachers/customize-class/', // You should concatenate this with the class id e.g. /for-teachers/customize_class/<class id>
    stats_page: '/stats/class/', // You should concatenate this with the class id e.g. /stats/class/<class id>
    logs_page: '/logs/class/', // You should concatenate this with the class id e.g. /logs/class/<class id>
    register_student_page: '/signup?teacher=false',
    register_teacher_page: '/signup?teacher=true',
    admin_page: '/admin',
    admin_stats_page: '/admin/stats',
    admin_adventures_page: '/admin/adventures',
    admin_achievements_page: '/admin/achievements'
  }
});
