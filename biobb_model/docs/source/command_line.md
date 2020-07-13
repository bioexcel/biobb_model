# BioBB MODEL Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Mutate
Class to mutate one amino acid by another in a 3d structure.
### Get help
Command:
```python
mutate -h
```
    usage: mutate [-h] [-c CONFIG] -i INPUT_PDB_PATH -o OUTPUT_PDB_PATH
    
    Model the missing atoms in aminoacid side chains of a PDB.
    
    optional arguments:
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
* **input_pdb_path** (*string*): Input PDB file path. File type: None. [Sample file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/model/2ki5.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output PDB file path. File type: None. [Sample file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/reference/model/output_mutated_pdb_path.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **mutation_list** (*string*): (A:Val2Ala) separated by commas. If no chain is provided as chain code all the chains in the pdb file will be mutated. ie: "A:ALA15CYS".
* **remove_tmp** (*boolean*): (True) [WF property] Remove temporal files..
* **restart** (*boolean*): (False) [WF property] Do not execute if output files exist..
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

## Fix_side_chain
Class to model the missing atoms in amino acid side chains of a PDB.
### Get help
Command:
```python
fix_side_chain -h
```
    usage: fix_side_chain [-h] [-c CONFIG] -i INPUT_PDB_PATH -o OUTPUT_PDB_PATH
    
    Model the missing atoms in amino acid side chains of a PDB.
    
    optional arguments:
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
* **input_pdb_path** (*string*): Input PDB file path. File type: None. [Sample file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/data/model/2ki5.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output PDB file path. File type: None. [Sample file](https://github.com/bioexcel/biobb_model/blob/master/biobb_model/test/reference/model/output_pdb_path.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **remove_tmp** (*boolean*): (True) [WF property] Remove temporal files..
* **restart** (*boolean*): (False) [WF property] Do not execute if output files exist..
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
