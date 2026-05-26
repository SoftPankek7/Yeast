# The Yeast Programming Language Changes

#### For: Version 1.0.4

----

## Added Features

- Removed match/case to allow running on python 3.6+, not just 3.10+ (F-strings are going next)
- Allows ``forcedeletedir`` to work on windows!

----

## Fixed Bugs / Enhancements

- Removed some return notations to compact space. This cleaned up on 1 module.
- Refactored code to make it slightly more readable
- Allows using --help without an input file.
- Makes sure you are using yeast when doing arbituary C.
- Standalized ``"`` over ``'`` in the source code, making it a bit more clean.
- Fixed a function to not use an arg (it wasnt accessed)
- Ensured ``_help()`` exited after printing help.
- Fixed a bug if you have a file in dir named "--help", it wouldnt trigger help.
- Added macros ``endfunc`` and ``endfunction`` for yeast (I dont know why they werent there)
