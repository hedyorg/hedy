const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: 'a1fbb9',
  watchForFileChanges: false,
  video: false,
  redirectionLimit: 100,
  // numTestsKeptInMemory: 0,
  experimentalMemoryManagement: true,
  e2e: {
    baseUrl: 'http://localhost:8080',
    setupNodeEvents(on, config) {
      require('@cypress/code-coverage/task')(on, config)
      // include any other plugin code...

      // It's IMPORTANT to return the config object
      // with any changed environment variables
      return config
    },
  },
  env: {
    admin_achievements_page: '/admin/achievements',
    admin_adventures_page: '/admin/adventures',
    admin_classes_page: '/admin/classes',
    admin_page: '/admin',
    admin_stats_page: '/admin/stats',
    admin_users_page: '/admin/users',
    adventure_page: '/hedy/1#print_command',
    class_page: '/for-teachers/class/',
    customize_class_page: '/for-teachers/customize-class/', // You should concatenate this with the class id e.g. /for-teachers/customize_class/<class id>
    grid_overview_page: '/grid_overview/class', 
    hedy_english_keywords: '/hedy?keyword_language=en',
    hedy_level2_page: '/hedy/2',
    hedy_level5_page: '/hedy/5',
    hedy_page: '/hedy',
    learn_more_page: '/learn-more',
    login_page: '/login',
    logs_page: '/logs/class/', // You should concatenate this with the class id e.g. /logs/class/<class id>
    manual_page: '/for-teachers/manual',
    privacy_page: '/privacy',
    profile_page: '/my-profile',
    programs_page: '/programs',
    public_adventures: '/public-adventures',
    recover_page: '/recover',
    signup_page: '/signup',
    stats_page: '/stats/class/', // You should concatenate this with the class id e.g. /stats/class/<class id>
    subscribe_page: '/subscribe',
    teachers_page: '/for-teachers',
  }
});
