# The Yeast Programming Language Changes

#### For: Version 1.0.1

----

- Edited docs/COMMANDS.md to correctly specify using C (compilers) instead of C++ (compilers)
- Allowed comments (``;; comment``) to be inline
- Clarified help menu with compiler
- Changed default entrypoint from ``int main(){`` to ``int main(int argc, char *argv[]) {``, allowing command line arguments
- Made a lot of the ``error()``s now use ``___to_c_err()`` - making code a bit smaller, and the ``___to_c_err()`` statement more meaningful.
- Made MIT notice in C source & H file more specific
- Removed @ shorthand for print, making way for custom headers in a future update.
- Changed ``def to_c(string) -> str | None:`` to ``def to_c(string) -> Optional[str]:`` as per version compatibility