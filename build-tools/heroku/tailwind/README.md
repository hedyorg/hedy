Tailwind for Hedy
=================

This directory contains two scripts:

* `generate-prod-css`: gets run on deploy to generate minimal CSS which gets
  served on the real site.
* `generate-development-css`: can be run by developers to regenerate the
  full development CSS file. You should almost never need to do this, just
  when you want to use Tailwind condition classes (like `hover:`, `group-hover:`, etc).