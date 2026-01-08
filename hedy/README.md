hedy
============

This package contains all the language and translation specific
parts of `hedy`.

This package should be isolated: it should not depend on any source or data
files outside the `hedy` directory.

The other way around is okay: source files outside this package can depend on
source files inside the package -- though they can't assume any specific path of
data files and need to go through publicly exposed APIs to read files.

Why this package?
-----------------

This package is being staged here during a refactoring operation, ready to be
moved out to a separate GitHub repository once the refactoring is complete.

The tests for it are in the `hedy_tests` directory.