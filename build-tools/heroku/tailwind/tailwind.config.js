// Control the Tailwind file size by disabling stuff we don't need.
module.exports = {
  purge: {
    enabled: true,
    content: [
      // PurgeCSS will look for all things that look like css classes in these
      // files and drop all styles not referenced in any of them.
      // Put any file here that could contain HTML or CSS classes.
      '../templates/**/*.html',
      '../main/**/*.md',
      '../coursedata/**/*.md',
      '../static/js/**/*.js',
    ],
  },
  theme: {
    extend: {},
    screens: {
      // We only need a few breakpoints
      sm: '640px',
      lg: '1024px',
      xl: '1280px',
    },
  },
  variants: {},
  corePlugins: {
    opacity: false,
    // No animations
    transitionDuration: false,
    transitionProperty: false,
    transitionTimingFunction: false,

    // No fancy CSS transforms
    scale: false,
    rotate: false,
    translate: false,
    skew: false,
    transformOrigin: false,

    // No need for placeholder colors
    placeholderColor: false,

  },
  plugins: [],
}
