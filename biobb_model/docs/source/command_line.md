# BioBB MODEL Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Checking_log
Class to check the errors of a PDB structure.
### Get help
Command:
```python
checking_log -h
```
    usage: checking_log [-h] [-c CONFIG] -i INPUT_PDB_PATH -o OUTPUT_LOG_PATH
    
    Check the errors of a PDB structure and create a report log file.
    
    options:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_PDB_PATH, --input_pdb_path INPUT_PDB_PATH
                            Input PDB file name
      -o OUTPUT_LOG_PATH, --output_log_path OUTPUT_LOG_PATH
                            Output log file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.pdb). Accepted formats: PDB
* **output_log_path** (*string*): Output report log file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/checking.log). Accepted formats: LOG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **modeller_key** (*string*): (None) Modeller license key..
* **binary_path** (*string*): (check_structure) Path to the check_structure executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_checking_log.yml)
```python
properties:
  restart: false

```
#### Command line
```python
checking_log --config config_checking_log.yml --input_pdb_path 2ki5.pdb --output_log_path checking.log
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_checking_log.json)
```python
{
  "properties": {
    "restart": false
  }
}
```
#### Command line
```python
checking_log --config config_checking_log.json --input_pdb_path 2ki5.pdb --output_log_path checking.log
```

## Fix_altlocs
Fix alternate locations from residues.
### Get help
Command:
```python
fix_altlocs -h
```
    usage: fix_altlocs [-h] [-c CONFIG] -i INPUT_PDB_PATH -o OUTPUT_PDB_PATH
    
    Fix alternate locations from residues
    
    options:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_PDB_PATH, --input_pdb_path INPUT_PDB_PATH
                            Input PDB file name
      -o OUTPUT_PDB_PATH, --output_pdb_path OUTPUT_PDB_PATH
                            Output PDB file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/3ebp.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output PDB file path. File type: output. [Sample file](https://raw.githubusercontent.com/bioexcel/biobb_model/master/biobb_model/test/reference/model/output_altloc.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **altlocs** (*array*): (None) List of alternate locations to fix. Format: ["A339:A", "A171:B", "A768:A"]; where for each residue the format is as follows: "<chain><residue id>:<chosen alternate location>". If empty, no action will be executed..
* **modeller_key** (*string*): (None) Modeller license key..
* **binary_path** (*string*): (check_structure) Path to the check_structure executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_altlocs.yml)
```python
properties:
  altlocs:
  - A339:A
  - A171:B
  - A768:A

```
#### Command line
```python
fix_altlocs --config config_fix_altlocs.yml --input_pdb_path 3ebp.pdb --output_pdb_path output_altloc.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_altlocs.json)
```python
{
  "properties": {
    "altlocs": [
      "A339:A",
      "A171:B",
      "A768:A"
    ]
  }
}
```
#### Command line
```python
fix_altlocs --config config_fix_altlocs.json --input_pdb_path 3ebp.pdb --output_pdb_path output_altloc.pdb
```

## Fix_amides
Fix amide groups from residues.
### Get help
Command:
```python
fix_amides -h
```
    usage: fix_amides [-h] [-c CONFIG] -i INPUT_PDB_PATH -o OUTPUT_PDB_PATH
    
    Flip the clashing amide groups to avoid clashes.
    
    options:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_PDB_PATH, --input_pdb_path INPUT_PDB_PATH
                            Input PDB file name
      -o OUTPUT_PDB_PATH, --output_pdb_path OUTPUT_PDB_PATH
                            Output PDB file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/5s2z.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output PDB file path. File type: output. [Sample file](https://raw.githubusercontent.com/bioexcel/biobb_model/master/biobb_model/test/reference/model/output_amide_pdb_path.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **modeller_key** (*string*): (None) Modeller license key..
* **binary_path** (*string*): (check_structure) Path to the check_structure executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_amides.yml)
```python
properties:
  restart: false

```
#### Command line
```python
fix_amides --config config_fix_amides.yml --input_pdb_path 5s2z.pdb --output_pdb_path output_amide_pdb_path.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_amides.json)
```python
{
  "properties": {
    "restart": false
  }
}
```
#### Command line
```python
fix_amides --config config_fix_amides.json --input_pdb_path 5s2z.pdb --output_pdb_path output_amide_pdb_path.pdb
```

## Fix_backbone
Class to model the missing atoms in the backbone of a PDB structure.
### Get help
Command:
```python
fix_backbone -h
```
    usage: fix_backbone [-h] [-c CONFIG] -i INPUT_PDB_PATH -f INPUT_FASTA_CANONICAL_SEQUENCE_PATH -o OUTPUT_PDB_PATH
    
    Model the missing atoms in the backbone of a PDB structure.
    
    options:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_PDB_PATH, --input_pdb_path INPUT_PDB_PATH
                            Input PDB file name
      -f INPUT_FASTA_CANONICAL_SEQUENCE_PATH, --input_fasta_canonical_sequence_path INPUT_FASTA_CANONICAL_SEQUENCE_PATH
                            Input FASTA file name
      -o OUTPUT_PDB_PATH, --output_pdb_path OUTPUT_PDB_PATH
                            Output PDB file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.pdb). Accepted formats: PDB
* **input_fasta_canonical_sequence_path** (*string*): Input FASTA file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.fasta). Accepted formats: FASTA
* **output_pdb_path** (*string*): Output PDB file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/output_pdb_path.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **add_caps** (*boolean*): (False) Add caps to terminal residues..
* **modeller_key** (*string*): (None) Modeller license key..
* **binary_path** (*string*): (check_structure) Path to the check_structure executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_backbone.yml)
```python
properties:
  add_caps: false
  modeller_key: MODELIRANJE
  restart: false

```
#### Command line
```python
fix_backbone --config config_fix_backbone.yml --input_pdb_path 2ki5.pdb --input_fasta_canonical_sequence_path 2ki5.fasta --output_pdb_path output_pdb_path.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_backbone.json)
```python
{
  "properties": {
    "restart": false,
    "add_caps": false,
    "modeller_key": "MODELIRANJE"
  }
}
```
#### Command line
```python
fix_backbone --config config_fix_backbone.json --input_pdb_path 2ki5.pdb --input_fasta_canonical_sequence_path 2ki5.fasta --output_pdb_path output_pdb_path.pdb
```

## Fix_chirality
Fix chirality errors of residues.
### Get help
Command:
```python
fix_chirality -h
```
    usage: fix_chirality [-h] [-c CONFIG] -i INPUT_PDB_PATH -o OUTPUT_PDB_PATH
    
    Fix stereochemical errors in residues changing It's chirality.
    
    options:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_PDB_PATH, --input_pdb_path INPUT_PDB_PATH
                            Input PDB file name
      -o OUTPUT_PDB_PATH, --output_pdb_path OUTPUT_PDB_PATH
                            Output PDB file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/5s2z.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output PDB file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/output_amide_pdb_path.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **modeller_key** (*string*): (None) Modeller license key..
* **binary_path** (*string*): (check_structure) Path to the check_structure executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_chirality.yml)
```python
properties:
  restart: false

```
#### Command line
```python
fix_chirality --config config_fix_chirality.yml --input_pdb_path 5s2z.pdb --output_pdb_path output_amide_pdb_path.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_chirality.json)
```python
{
  "properties": {
    "restart": false
  }
}
```
#### Command line
```python
fix_chirality --config config_fix_chirality.json --input_pdb_path 5s2z.pdb --output_pdb_path output_amide_pdb_path.pdb
```

## Fix_pdb
Class to renumerate residues in a PDB structure according to a reference sequence from UniProt.
### Get help
Command:
```python
fix_pdb -h
```
    usage: fix_pdb [-h] [-c CONFIG] -i INPUT_PDB_PATH -o OUTPUT_PDB_PATH
    
    Model the missing atoms in the backbone of a PDB structure.
    
    options:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_PDB_PATH, --input_pdb_path INPUT_PDB_PATH
                            Input PDB file name
      -o OUTPUT_PDB_PATH, --output_pdb_path OUTPUT_PDB_PATH
                            Output PDB file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output PDB file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/output_pdb_path.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **forced_uniprot_references** (*string*): (None) Set the UniProt accessions for sequences to be used as reference..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_pdb.yml)
```python
properties:
  forced_uniprot_references:
  - P0DTC2
  - Q9BYF1
  restart: false

```
#### Command line
```python
fix_pdb --config config_fix_pdb.yml --input_pdb_path 2ki5.pdb --output_pdb_path output_pdb_path.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_pdb.json)
```python
{
  "properties": {
    "restart": false,
    "forced_uniprot_references": [
      "P0DTC2",
      "Q9BYF1"
    ]
  }
}
```
#### Command line
```python
fix_pdb --config config_fix_pdb.json --input_pdb_path 2ki5.pdb --output_pdb_path output_pdb_path.pdb
```

## Fix_side_chain
Class to model the missing atoms in amino acid side chains of a PDB.
### Get help
Command:
```python
fix_side_chain -h
```
    usage: fix_side_chain [-h] [-c CONFIG] -i INPUT_PDB_PATH -o OUTPUT_PDB_PATH
    
    Model the missing atoms in amino acid side chains of a PDB.
    
    options:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_PDB_PATH, --input_pdb_path INPUT_PDB_PATH
                            Input PDB file name
      -o OUTPUT_PDB_PATH, --output_pdb_path OUTPUT_PDB_PATH
                            Output PDB file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output PDB file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/output_pdb_path.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **use_modeller** (*boolean*): (False) Use Modeller suite to rebuild the missing side chain atoms..
* **modeller_key** (*string*): (None) Modeller license key..
* **binary_path** (*string*): (check_structure) Path to the check_structure executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_side_chain.yml)
```python
properties:
  restart: false

```
#### Command line
```python
fix_side_chain --config config_fix_side_chain.yml --input_pdb_path 2ki5.pdb --output_pdb_path output_pdb_path.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_side_chain.json)
```python
{
  "properties": {
    "restart": false
  }
}
```
#### Command line
```python
fix_side_chain --config config_fix_side_chain.json --input_pdb_path 2ki5.pdb --output_pdb_path output_pdb_path.pdb
```

## Fix_ssbonds
Fix SS bonds from residues.
### Get help
Command:
```python
fix_ssbonds -h
```
    usage: fix_ssbonds [-h] [-c CONFIG] -i INPUT_PDB_PATH -o OUTPUT_PDB_PATH
    
    Fix SS bonds from residues
    
    options:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_PDB_PATH, --input_pdb_path INPUT_PDB_PATH
                            Input PDB file name
      -o OUTPUT_PDB_PATH, --output_pdb_path OUTPUT_PDB_PATH
                            Output PDB file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/1aki.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output PDB file path. File type: output. [Sample file](https://raw.githubusercontent.com/bioexcel/biobb_model/master/biobb_model/test/reference/model/output_ssbonds.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **modeller_key** (*string*): (None) Modeller license key..
* **binary_path** (*string*): (check_structure) Path to the check_structure executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_ssbonds.yml)
```python
properties:
  restart: false

```
#### Command line
```python
fix_ssbonds --config config_fix_ssbonds.yml --input_pdb_path 1aki.pdb --output_pdb_path output_ssbonds.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_fix_ssbonds.json)
```python
{
  "properties": {
    "restart": false
  }
}
```
#### Command line
```python
fix_ssbonds --config config_fix_ssbonds.json --input_pdb_path 1aki.pdb --output_pdb_path output_ssbonds.pdb
```

## Mutate
Class to mutate one amino acid by another in a 3d structure.
### Get help
Command:
```python
mutate -h
```
    usage: mutate [-h] [-c CONFIG] -i INPUT_PDB_PATH -o OUTPUT_PDB_PATH
    
    Model the missing atoms in aminoacid side chains of a PDB.
    
    options:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_PDB_PATH, --input_pdb_path INPUT_PDB_PATH
                            Input PDB file name
      -o OUTPUT_PDB_PATH, --output_pdb_path OUTPUT_PDB_PATH
                            Output PDB file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output PDB file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/output_mutated_pdb_path.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **mutation_list** (*string*): (None) Mutation list in the format "Chain:WT_AA_ThreeLeterCode Resnum MUT_AA_ThreeLeterCode" (no spaces between the elements) separated by commas. If no chain is provided as chain code all the chains in the pdb file will be mutated. ie: "A:ALA15CYS".
* **use_modeller** (*boolean*): (False) Use Modeller suite to optimize the side chains..
* **modeller_key** (*string*): (None) Modeller license key..
* **binary_path** (*string*): (check_structure) Path to the check_structure executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_mutate.yml)
```python
properties:
  mutation_list: Leu49Ile, B:arg51Lys

```
#### Command line
```python
mutate --config config_mutate.yml --input_pdb_path 2ki5.pdb --output_pdb_path output_mutated_pdb_path.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/config/config_mutate.json)
```python
{
  "properties": {
    "mutation_list": "Leu49Ile, B:arg51Lys"
  }
}
```
#### Command line
```python
mutate --config config_mutate.json --input_pdb_path 2ki5.pdb --output_pdb_path output_mutated_pdb_path.pdb
```
