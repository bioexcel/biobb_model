# Biobb Model changelog

## What's new in version [4.0.1](https://github.com/bioexcel/biobb_model/releases/tag/v4.0.1)?
In version 4.1.0 new biobb_structure_checking 3.13.4 and minimum Python version 3.8.0

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
