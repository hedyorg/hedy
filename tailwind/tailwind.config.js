// Control the Tailwind file size by disabling stuff we don't need.
module.exports = {
  theme: {
    extend: {},
    screens: {
      // We only need a few breakpoints
      sm: '640px',
      // md: '768px',
    },
  },
  variants: {},
  corePlugins: {
    opacity: false,
    // No animations
    transitionDuration: false,
    transitionProperty: false,
    transitionTimingFunction: false,

    // No fancy CSS graphics
    scale: false,
    rotate: false,
    translate: false,
    skew: false,
    transformOrigin: false,
  },
  plugins: [],
}
