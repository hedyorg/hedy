// Control the Tailwind file size by disabling stuff we don't need.
module.exports = {
  theme: {
    extend: {},
    screens: {
      // We only need a few breakpoints
      sm: '640px',
      lg: '1024px',
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
