# Biobb Model changelog

## What's new in version [5.1.0](https://github.com/bioexcel/biobb_model/releases/tag/v5.1.0)?

### Changes

* [UPDATE]: Update to biobb_common 5.1.0
* [UPDATE]: Update to biobb_structure_checking 3.15.6

## What's new in version [5.0.0](https://github.com/bioexcel/biobb_model/releases/tag/v5.0.0)?

### Changes

* [CI/CD](linting_and_testing.yml): Update set-up micromamba.
* [CI/CD](linting_and_testing.yaml): Update GA test workflow to Python >3.9
* [DOCS](.readthedocs.yaml): Updating to Python 3.9
* [CI/CD](GITIGNORE): Update .gitignore to include the new file extensions to ignore
* [CI/CD](tests) Updating the fixbackbone test reference PDB
* [CI/CD](tests) Updating the test_checking_log
* [CI/CD](conf.yml): Change test conf.yml to adapt to new settings configuration
* [FIX] Adding execution permissions to fix_pdb
* [FEATURE] New sandbox_path property

## What's new in version [4.2.3](https://github.com/bioexcel/biobb_model/releases/tag/v5.0.0)?

### Changes

* [FIX] Minor fix in FixPdb

## What's new in version [4.2.2](https://github.com/bioexcel/biobb_model/releases/tag/v4.2.2)?

### Changes

* [FIX] Minor fix in FixPdb

## What's new in version [4.2.1](https://github.com/bioexcel/biobb_model/releases/tag/v4.2.1)?

### Changes

* [FIX] Minor fix in FixPdb

## What's new in version [5.0.0](https://github.com/bioexcel/biobb_model/releases/tag/v5.0.0)?

### Changes

* [FIX] Fix type hints
* [CI/CD] Adding workflow to synchronize with CASTIEL gitlab
* [FIX] Ignoring Biopython deprecation warnings
* [UPDATE] Updated CITATION.cff
* [UPDATE] Updating json schemas
* [DOCS] Adding description to fix_altlocs and fix_ssbonds modules
* [DOCS] Add description to fix_pdb module
* [FIX] Ignore biopython deprecation warnings
* [DOCS] Add description to fix_altlocs module
* [FIX] Adding module imports to package __init__ files
* [DOCS] Adding fair software badge and GA

## What's new in version [4.0.1](https://github.com/bioexcel/biobb_model/releases/tag/v4.0.1)?
In version 4.1.0 new biobb_structure_checking 3.13.5 and minimum Python version 3.8.0

## What's new in version [4.0.1](https://github.com/bioexcel/biobb_model/releases/tag/v4.0.1)?
In version 4.0.1 new biobb_structure_checking 3.13.0

## What's new in version [4.0.0](https://github.com/bioexcel/biobb_model/releases/tag/v4.0.0)?
In version 4.0.0 new biobb_common 4.0.0

### New features

* All fix_... will execute dry runs producing an unmodified output file if no problem is detected

## What's new in version [3.9.0](https://github.com/bioexcel/biobb_model/releases/tag/v3.9.0)?
In version 3.9.0 new biobb_common 3.9.0


## What's new in version [3.8.1](https://github.com/bioexcel/biobb_model/releases/tag/v3.8.1)?
In version 3.8.1 new fix_pdb block.

### New features

* Adding new fix_pdb block (general)

## What's new in version [3.8.0](https://github.com/bioexcel/biobb_model/releases/tag/v3.8.0)?
In version 3.8.0 the dependency biobb_common has been updated to 3.8.1 version.

### New features

* Update to biobb_common 3.8.1 (general)
* Update to biobb_structure_checking 3.10.1 (general)

## What's new in version [3.7.0](https://github.com/bioexcel/biobb_model/releases/tag/v3.7.0)?
In version 3.7.0 the dependency biobb_common has been updated to 3.7.0 version.

### New features

* Update to biobb_common 3.7.0 (general)
* Update to biobb_structure_checking 3.8.5 (general)

## What's new in version [3.0.1](https://github.com/bioexcel/biobb_model/releases/tag/v3.0.1)?
In version 3.0.0 Python has been updated to version 3.7 and Biopython to version 1.76.
Big changes in the documentation style and content. Finally a new conda installation recipe has been introduced.

### New features

* Update to Python 3.7 (general)
* Update to Biopython 1.76 (general)
* New conda installer (installation)
* Adding type hinting for easier usage (API)
* Deprecating os.path in favour of pathlib.path (modules)
* New command line documentation (documentation)

### Bug fixes

* Replace container Quay.io badge (documentation)
* Remove unused system and step arguments from command line causing execution errors (cli) [#9](https://github.com/bioexcel/biobb_model/issues/9)
* Remove system argument from commandline (cli)

### Other changes

* New documentation styles (documentation) [#8](https://github.com/bioexcel/biobb_model/issues/8)
