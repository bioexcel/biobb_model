# Biobb Model changelog

## [Unreleased]

## What's new in version [5.4.0](https://github.com/bioexcel/biobb_model/releases/tag/v5.4.0)?

### Changes

* [UPDATE] Update to biobb_common 5.4.0.
* [FEATURE] Add the `fix_known` boolean property to `FixBackbone` to optimize only the missing residues with Modeller, keeping the coordinates of the ones in the structure.
* [FEATURE] Add the `extra_gap` integer property to `FixBackbone` to recover additional residues from the model on either side of a break and help fix loop connections.
* [FIX] `Mutate` and `FixSideChain` with `use_modeller` in a container: the side chains are rebuilt with the Modeller of the container. Before, the blocks looked for Modeller in the environment that launches the container and left the rebuild out when it was not installed there.
* [FIX] `FixBackbone` in a container: the canonical sequence reaches check_structure with its `--sequence` option. Before, the block wrote the path of the FASTA file on the host to the standard input of check_structure, a path the container does not have.
* [UPDATE] `FixPdb` writes its messages (reference summary, alignments, BLAST search and its failure) to the log of the block instead of printing them to the standard output.
* [FIX] `FixPdb`: a UniProt request that fails with an HTTP error other than 400 raises that error (it raised an `UnboundLocalError`).
* [FIX] `Mutate`: a `mutation_list` set to None is taken as not given (it raised an `AttributeError`).
* [DOCS] `fix_pdb` and `mutate`: the command line help describes the block (both had the description of another block).
* [UPDATE] Python 3.11 to 3.13.

## What's new in version [5.3.0](https://github.com/bioexcel/biobb_amber/releases/tag/v5.3.0)?

### Changes

* [UPDATE] Update to biobb_common 5.3.1

## What's new in version [5.2.1](https://github.com/bioexcel/biobb_amber/releases/tag/v5.2.1)?

### Changes

* [UPDATE] Update to biobb_common 5.2.2

## What's new in version [5.2.0](https://github.com/bioexcel/biobb_amber/releases/tag/v5.2.0)?

### Changes

* [UPDATE] Update to biobb_common 5.2.0

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
