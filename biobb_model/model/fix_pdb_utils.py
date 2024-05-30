import os
import urllib.request
import json
import math
from bisect import bisect
from Bio import pairwise2  # type: ignore
from Bio.pairwise2 import format_alignment  # type: ignore
from Bio.Blast import NCBIWWW  # type: ignore
import xmltodict  # type: ignore
from typing import List, Tuple, Optional, Union
Coords = Tuple[float, float, float]

try:
    from Bio.SubsMat import MatrixInfo  # type: ignore
    blosum62 = MatrixInfo.blosum62
except ImportError:
    from Bio.Align import substitution_matrices  # type: ignore
    blosum62 = substitution_matrices.load("BLOSUM62")


# An atom
class Atom:
    def __init__(self, name: Optional[str] = None, element: Optional[str] = None, coords: Optional[Coords] = None):
        self.name = name
        self.element = element
        self.coords = coords
        # Set variables to store references to other related instances
        # These variables will be set further by the structure
        self._structure: Optional[Structure] = None
        self._index: Optional[int] = None
        self._residue_index: Optional[int] = None

    def __repr__(self):
        return '<Atom ' + str(self.name) + '>'

    def __eq__(self, other):
        return self._residue_index == other._residue_index and self.name == other.name

    # The parent structure (read only)
    # This value is set by the structure itself
    def get_structure(self):
        return self._structure
    structure = property(get_structure, None, None, "The parent structure (read only)")

    # The residue index according to parent structure residues (read only)
    # This value is set by the structure itself
    def get_index(self):
        return self._index
    index = property(get_index, None, None, "The residue index according to parent structure residues (read only)")

    # The atom residue index according to parent structure residues
    # If residue index is set then make changes in all the structure to make this change coherent
    def get_residue_index(self) -> Optional[int]:
        return self._residue_index

    def set_residue_index(self, new_residue_index: int):
        # If there is not strucutre yet it means the residue is beeing set before the structure
        # We just save the residue index and wait for the structure to be set
        if not self.structure:
            self._residue_index = new_residue_index
            return
        # Relational indices are updated through a top-down hierarchy
        # Affected residues are the ones to update this atom internal residue index
        current_residue = self.residue
        current_residue.remove_atom(self)
        new_residue = self.structure.residues[new_residue_index]
        new_residue.add_atom(self)
    residue_index = property(get_residue_index, set_residue_index, None, "The atom residue index according to parent structure residues")

    # The atom residue
    # If residue is set then make changes in all the structure to make this change coherent
    def get_residue(self) -> Optional['Residue']:
        # If there is not strucutre yet it means the atom is beeing set before the structure
        # In this case it is not possible to get related residues in the structure
        if not self.structure:
            return None
        # Get the residue in the structure according to the residue index
        return self.structure.residues[self.residue_index]

    def set_residue(self, new_residue: 'Residue'):
        # Find the new residue index and set it as the atom residue index
        # Note that the residue must be set in the structure already
        new_residue_index = new_residue.index
        if new_residue_index is None:
            raise ValueError('Residue ' + str(new_residue) + ' is not set in the structure')
        self.set_residue_index(new_residue_index)
    residue = property(get_residue, set_residue, None, "The atom residue")

    # The atom chain index according to parent structure chains (read only)
    # In order to change the chain index it must be changed in the atom residue
    def get_chain_index(self) -> int:
        return self.residue.chain_index
    chain_index = property(get_chain_index, None, None, "The atom chain index according to parent structure chains (read only)")

    # The atom chain(read only)
    # In order to change the chain it must be changed in the atom residue
    def get_chain(self) -> 'Chain':
        # Get the chain in the structure according to the chain index
        return self.structure.chains[self.chain_index]
    chain = property(get_chain, None, None, "The atom chain (read only)")


# A residue
class Residue:
    def __init__(self, name: Optional[str] = None, number: Optional[int] = None, icode: Optional[str] = None):
        self.name = name
        self.number = number
        self.icode = icode
        # Set variables to store references to other related instaces
        # These variables will be set further by the structure
        self._structure: Optional[Structure] = None
        self._index: Optional[int] = None
        self._atom_indices: List[int] = []
        self._chain_index: Optional[int] = None

    def __repr__(self):
        return '<Residue ' + str(self.name) + str(self.number) + (self.icode if self.icode else '') + '>'

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return False
        return (self._chain_index == other._chain_index and self.number == other.number and self.icode == other.icode)

    def __hash__(self):
        # WARNING: This is susceptible to duplicated residues
        return hash((self._chain_index, self.number, self.icode))
        # WARNING: This is not susceptible to duplicated residues
        # return hash(tuple(self._atom_indices))

    def same_inputs_as(self, other) -> bool:
        return (
            self.name == other.name and
            self.number == other.number and
            self.icode == other.icode
        )

    # The parent structure (read only)
    # This value is set by the structure itself
    def get_structure(self):
        return self._structure
    structure = property(get_structure, None, None, "The parent structure (read only)")

    # The residue index according to parent structure residues (read only)
    # This value is set by the structure itself
    def get_index(self):
        return self._index
    index = property(get_index, None, None, "The residue index according to parent structure residues(read only)")

    # The atom indices according to parent structure atoms for atoms in this residue
    # If atom indices are set then make changes in all the structure to make this change coherent
    def get_atom_indices(self) -> List[int]:
        return self._atom_indices

    def set_atom_indices(self, new_atom_indices: List[int]):
        # If there is not strucutre yet it means the residue is beeing set before the structure
        # We just save atom indices and wait for the structure to be set
        if not self.structure:
            self._atom_indices = new_atom_indices
            return
        # Update the current atoms
        for atom in self.atoms:
            atom._residue_index = None
        # Update the new atoms
        for index in new_atom_indices:
            atom = self.structure.atoms[index]
            atom._residue_index = self.index
        # Now new indices are coherent and thus we can save them
        self._atom_indices = new_atom_indices
    atom_indices = property(get_atom_indices, set_atom_indices, None, "The atom indices according to parent structure atoms for atoms in this residue")

    # The atoms in this residue
    # If atoms are set then make changes in all the structure to make this change coherent
    def get_atoms(self) -> List['Atom']:
        # If there is not strucutre yet it means the chain is beeing set before the structure
        # In this case it is not possible to get related atoms in the structure
        if not self.structure:
            return []
        # Get atoms in the structure according to atom indices
        atoms = self.structure.atoms
        return [atoms[atom_index] for atom_index in self.atom_indices]

    def set_atoms(self, new_atoms: List['Atom']):
        # Find indices for new atoms and set their indices as the new atom indices
        # Note that atoms must be set in the structure already
        new_atom_indices = []
        for new_atom in new_atoms:
            new_atom_index = new_atom.index
            if new_atom_index is None:
                raise ValueError('Atom ' + str(new_atom) + ' is not set in the structure')
            new_atom_indices.append(new_atom_index)
        self.set_atom_indices(new_atom_indices)
    atoms = property(get_atoms, set_atoms, None, "The atoms in this residue")

    # Add an atom to the residue
    def add_atom(self, new_atom: 'Atom'):
        # Insert the new atom index in the list of atom indices keeping the order
        new_atom_index = new_atom.index
        sorted_atom_index = bisect(self.atom_indices, new_atom_index)
        self.atom_indices.insert(sorted_atom_index, new_atom_index)
        # Update the atom internal index
        new_atom._residue_index = self.index

    # Remove an atom from the residue
    def remove_atom(self, current_atom: 'Atom'):
        # Remove the current atom index from the atom indices list
        self.atom_indices.remove(current_atom.index)  # This index MUST be in the list
        # Update the atom internal index
        current_atom._residue_index = None

    # The residue chain index according to parent structure chains
    # If chain index is set then make changes in all the structure to make this change coherent
    def get_chain_index(self) -> Optional[int]:
        return self._chain_index

    def set_chain_index(self, new_chain_index: int):
        # If there is not strucutre yet it means the chain is beeing set before the structure
        # We just save the chain index and wait for the structure to be set
        if not self.structure:
            self._chain_index = new_chain_index
            return
        # Relational indices are updated through a top-down hierarchy
        # Affected chains are the ones to update this residue internal chain index
        # WARNING: It is critical to find both current and new chains before removing/adding residues
        # WARNING: It may happend that we remove the last residue in the current chain and the current chain is purged
        # WARNING: Thus the 'new_chain_index' would be obsolete since the structure.chains list would have changed
        current_chain = self.chain
        new_chain = self.structure.chains[new_chain_index]
        current_chain.remove_residue(self)
        new_chain.add_residue(self)
    chain_index = property(get_chain_index, set_chain_index, None, "The residue chain index according to parent structure chains")

    # The residue chain
    # If chain is set then make changes in all the structure to make this change coherent
    def get_chain(self) -> Union['Chain', List]:
        # If there is not strucutre yet it means the residue is beeing set before the structure
        # In this case it is not possible to get related chain in the structure
        if not self.structure:
            return []
        # Get the chain in the structure according to the chain index
        return self.structure.chains[self.chain_index]

    def set_chain(self, new_chain: Union['Chain', str]):
        # In case the chain is just a string we must find/create the corresponding chain
        if isinstance(new_chain, str):
            letter = new_chain
            # Get the residue structure
            structure = self.structure
            if not structure:
                raise ValueError('Cannot find the corresponding ' + new_chain + ' chain without the structure')
            # Find if the letter belongs to an already existing chain
            new_chain = structure.get_chain_by_name(letter)
            # If the chain does not exist yet then create it
            if not new_chain:
                new_chain = Chain(name=letter)
                structure.set_new_chain(new_chain)
        # Find the new chain index and set it as the residue chain index
        # Note that the chain must be set in the structure already
        new_chain_index = new_chain.index
        if new_chain_index is None:
            raise ValueError('Chain ' + str(new_chain) + ' is not set in the structure')
        if isinstance(new_chain_index, int):
            self.set_chain_index(new_chain_index)
    chain = property(get_chain, set_chain, None, "The residue chain")


# A chain
class Chain:
    def __init__(self, name: Optional[str] = None):
        self.name = name
        # Set variables to store references to other related instaces
        # These variables will be set further by the structure
        self._structure: Optional[Structure] = None
        self._index: Optional[int] = None
        self.residue_indices = []

    def __repr__(self):
        return '<Chain ' + str(self.name) + '>'

    def __eq__(self, other):
        return self.name == other.name

    # The parent structure(read only)
    # This value is set by the structure itself
    def get_structure(self):
        return self._structure
    structure = property(get_structure, None, None, "The parent structure(read only)")

    # The residue index according to parent structure residues(read only)
    # This value is set by the structure itself
    def get_index(self):
        return self._index

    # When the index is set all residues are updated with the nex chain index
    def set_index(self, index: int):
        for residue in self.residues:
            residue._chain_index = index
        self._index = index
    index = property(get_index, set_index, None, "The residue index according to parent structure residues(read only)")

    # The residue indices according to parent structure residues for residues in this chain
    # If residue indices are set then make changes in all the structure to make this change coherent
    def get_residue_indices(self) -> List[int]:
        return self._residue_indices

    def set_residue_indices(self, new_residue_indices: List[int]):
        # If there is not strucutre yet it means the chain is beeing set before the structure
        # We just save residue indices and wait for the structure to be set
        if not self.structure:
            self._residue_indices = new_residue_indices
            return
        # Update the current residues
        for residue in self.residues:
            residue._chain_index = None
        # Update the new residues
        for index in new_residue_indices:
            residue = self.structure.residues[index]
            residue._chain_index = self.index
        # In case the new residue indices list is empty this chain must be removed from its structure
        if len(new_residue_indices) == 0:
            self.structure.purge_chain(self)
        # Now new indices are coherent and thus we can save them
        self._residue_indices = new_residue_indices
    residue_indices = property(get_residue_indices, set_residue_indices, None, "The residue indices according to parent structure residues for residues in this residue")

    # The residues in this chain
    # If residues are set then make changes in all the structure to make this change coherent
    def get_residues(self) -> List['Residue']:
        # If there is not strucutre yet it means the chain is beeing set before the structure
        # In this case it is not possible to get related residues in the structure
        if not self.structure:
            return []
        # Get residues in the structure according to residue indices
        residues = self.structure.residues
        return [residues[residue_index] for residue_index in self.residue_indices]

    def set_residues(self, new_residues: List['Residue']):
        # Find indices for new residues and set their indices as the new residue indices
        # Note that residues must be set in the structure already
        new_residue_indices = []
        for new_residue in new_residues:
            new_residue_index = new_residue.index
            if new_residue_index is None:
                raise ValueError('Residue ' + str(new_residue) + ' is not set in the structure')
            new_residue_indices.append(new_residue_index)
        self.set_residue_indices(new_residue_indices)
    residues = property(get_residues, set_residues, None, "The residues in this chain")

    # Add a residue to the chain
    def add_residue(self, residue: 'Residue'):
        # Insert the new residue index in the list of residue indices keeping the order
        sorted_residue_index = bisect(self.residue_indices, residue.index)
        self.residue_indices.insert(sorted_residue_index, residue.index)
        # Update the residue internal chain index
        residue._chain_index = self.index

    # Remove a residue from the chain
    # WARNING: Note that this function does not trigger the set_residue_indices
    def remove_residue(self, residue: 'Residue'):
        self.residue_indices.remove(residue.index)  # This index MUST be in the list
        # If we removed the last index then this chain must be removed from its structure
        if len(self.residue_indices) == 0 and self.structure:
            self.structure.purge_chain(self)
        # Update the residue internal chain index
        residue._chain_index = None

    # Atom indices for all atoms in the chain(read only)
    # In order to change atom indices they must be changed in their corresponding residues
    def get_atom_indices(self) -> List[int]:
        return sum([residue.atom_indices for residue in self.residues], [])
    atom_indices = property(get_atom_indices, None, None, "Atom indices for all atoms in the chain(read only)")

    # Atoms in the chain(read only)
    # In order to change atoms they must be changed in their corresponding residues
    def get_atoms(self) -> List[int]:
        return sum([residue.atoms for residue in self.residues], [])
    atoms = property(get_atoms, None, None, "Atoms in the chain(read only)")

    # Get the residues sequence in one-letter code
    def get_sequence(self) -> str:
        return ''.join([residue_name_2_letter(residue.name) for residue in self.residues])


# A structure is a group of atoms organized in chains and residues
class Structure:
    def __init__(self, atoms: List['Atom'] = [], residues: List['Residue'] = [], chains: List['Chain'] = []):
        self.atoms: List[Atom] = []
        self.residues: List[Residue] = []
        self.chains: List[Chain] = []
        # Set references between instances
        for atom in atoms:
            self.set_new_atom(atom)
        for residue in residues:
            self.set_new_residue(residue)
        for chain in chains:
            self.set_new_chain(chain)

    def __repr__(self):
        return '<Structure(' + str(len(self.atoms)) + ' atoms)>'

    # Set a new atom in the structure
    def set_new_atom(self, atom: 'Atom'):
        atom._structure = self
        new_atom_index = len(self.atoms)
        self.atoms.append(atom)
        atom._index = new_atom_index

    # Set a new residue in the structure
    # WARNING: Atoms must be set already before setting residues
    def set_new_residue(self, residue: 'Residue'):
        residue._structure = self
        new_residue_index = len(self.residues)
        self.residues.append(residue)
        residue._index = new_residue_index
        # In case the residue has atom indices, set relational indices on each atom
        for atom_index in residue.atom_indices:
            atom = self.atoms[atom_index]
            atom._residue_index = new_residue_index

    # Set a new chain in the structure
    # WARNING: Residues and atoms must be set already before setting chains
    def set_new_chain(self, chain: 'Chain'):
        chain._structure = self
        new_chain_index = len(self.chains)
        self.chains.append(chain)
        chain._index = new_chain_index
        # In case the chain has residue indices, set relational indices on each residue
        for residue_index in chain.residue_indices:
            residue = self.residues[residue_index]
            residue._chain_index = new_chain_index

    # Purge chain from the structure
    # This can be done only when the chain has no residues left in the structure
    # Renumerate all chain indices which have been offsetted as a result of the purge
    def purge_chain(self, chain: 'Chain'):
        # Check the chain can be purged
        if chain not in self.chains:
            raise ValueError('Chain ' + str(chain.name) + ' is not in the structure already')
        if len(chain.residue_indices) > 0:
            raise ValueError('Chain ' + str(chain.name) + ' is still having residues and thus it cannot be purged')
        # Get the current index of the chain to be purged
        purged_index = chain.index
        # Chains and their residues below this index are not to be modified
        # Chains and their residues over this index must be renumerated
        for affected_chain in self.chains[purged_index+1:]:
            # Chaging the index automatically changes all chain residues '_chain_index' values.
            affected_chain.index -= 1
        # Finally, remove the current chain from the list of chains in the structure
        self.chains.remove(chain)

    # Set the structure from a pdb file
    @classmethod
    def from_pdb_file(cls, pdb_filename: str):
        if not os.path.exists(pdb_filename):
            raise SystemExit('File "' + pdb_filename + '" not found')
        # Read the pdb file line by line and set the parsed atoms, residues and chains
        parsed_atoms = []
        parsed_residues: List[Residue] = []
        parsed_chains: List[Chain] = []
        atom_index = -1
        residue_index = -1
        with open(pdb_filename, 'r') as file:
            for line in file:
                # Parse atoms only
                start = line[0:6]
                is_atom = start == 'ATOM  ' or start == 'HETATM'
                if not is_atom:
                    continue
                # Mine all atom data
                atom_name = line[11:16].strip()
                residue_name = line[17:21].strip()
                chain = line[21:22]
                residue_number = int(line[22:26])
                icode = line[26:27]
                if icode == ' ':
                    icode = ''
                x_coord = float(line[30:38])
                y_coord = float(line[38:46])
                z_coord = float(line[46:54])
                element = line[77:79].strip()
                # Set the parsed atom, residue and chain
                parsed_atom = Atom(name=atom_name, element=element, coords=(x_coord, y_coord, z_coord))
                parsed_residue = Residue(name=residue_name, number=residue_number, icode=icode)
                parsed_chain = Chain(name=chain)
                # Add the parsed atom to the list and update the current atom index
                parsed_atoms.append(parsed_atom)
                atom_index += 1
                # Check if we are in the same chain/residue than before
                same_chain = parsed_chains and parsed_chains[-1] == parsed_chain
                same_residue = same_chain and parsed_residues and parsed_residue.same_inputs_as(parsed_residues[-1])
                # Update the residue atom indices
                # If the residue equals the last parsed residue then use the previous instead
                if same_residue:
                    parsed_residue = parsed_residues[-1]
                    parsed_residue.atom_indices.append(atom_index)
                    # If it is the same residue then it will be the same chain as well so we can proceed
                    continue
                # Otherwise, include the new residue in the list and update the current residue index
                parsed_residues.append(parsed_residue)
                residue_index += 1
                parsed_residue.atom_indices.append(atom_index)
                # If the chain equals the last parsed chain then use the previous instead
                if same_chain:
                    parsed_chain = parsed_chains[-1]
                    parsed_chain.residue_indices.append(residue_index)
                    continue
                # Otherwise, include the new chain in the list
                parsed_chains.append(parsed_chain)
                parsed_chain.residue_indices.append(residue_index)
        return cls(atoms=parsed_atoms, residues=parsed_residues, chains=parsed_chains)

    # Fix atom elements by gueesing them when missing
    # Set all elements with the first letter upper and the second(if any) lower
    # def fix_atom_elements(self):
    #     for atom in self.atoms:
    #         # Make sure elements have the first letter cap and the second letter not cap
    #         if atom.element:
    #             atom.element = first_cap_only(atom.element)
    #         # If elements are missing then guess them from atom names
    #         else:
    #             atom.element = guess_name_element(atom.name)

    # Generate a pdb file with current structure
    def generate_pdb_file(self, pdb_filename: str):
        with open(pdb_filename, "w") as file:
            file.write('REMARK mdtoolbelt generated pdb file\n')
            for a, atom in enumerate(self.atoms):
                residue = atom.residue
                index = str((a+1) % 100000).rjust(5)
                name = ' ' + str(atom.name).ljust(3) if len(str(atom.name)) < 4 else atom.name
                residue_name = residue.name.ljust(4)
                chain = atom.chain.name.rjust(1)
                residue_number = str(residue.number).rjust(4)
                icode = residue.icode.rjust(1)
                coords: Optional[Coords] = atom.coords
                if not coords:
                    raise ValueError('Atom ' + str(atom) + ' has no coordinates')
                else:
                    x_coord, y_coord, z_coord = ["{:.3f}".format(coord).rjust(8) for coord in coords]
                occupancy = '1.00'  # Just a placeholder
                temp_factor = '0.00'  # Just a placeholder
                element = atom.element
                atom_line = ('ATOM  ' + str(index) + ' ' + str(name) + ' ' + residue_name + chain + residue_number + icode + '   ' + x_coord + y_coord + z_coord + '  ' + occupancy + '  ' + temp_factor + '           ' + element).ljust(80) + '\n'
                file.write(atom_line)

    # Get a chain by its name
    def get_chain_by_name(self, name: str) -> Optional[Chain]:
        return next((c for c in self.chains if c.name == name), None)

    # Get a summary of the structure
    def display_summary(self):
        print('Atoms: ' + str(len(self.atoms)))
        print('Residues: ' + str(len(self.residues)))
        print('Chains: ' + str(len(self.chains)))
        for chain in self.chains:
            print('Chain ' + str(chain.name) + ' (' + str(len(chain.residue_indices)) + ' residues)')
            print(' -> ' + chain.get_sequence())

    # This is an alternative system to find protein chains(anything else is chained as 'X')
    # This system does not depend on VMD
    # It totally overrides previous chains since it is expected to be used only when chains are missing
    def raw_protein_chainer(self):
        current_chain = self.get_next_available_chain_name()
        previous_alpha_carbon = None
        for residue in self.residues:
            alpha_carbon = next((atom for atom in residue.atoms if atom.name == 'CA'), None)
            if not alpha_carbon:
                residue.set_chain('X')
                continue
            # Connected aminoacids have their alpha carbons at a distance of around 3.8 Ångstroms
            residues_are_connected = previous_alpha_carbon and calculate_distance(previous_alpha_carbon, alpha_carbon) < 4
            if not residues_are_connected:
                current_chain = self.get_next_available_chain_name()
            if current_chain:
                residue.set_chain(current_chain)
            previous_alpha_carbon = alpha_carbon

    # Get the next available chain name
    # Find alphabetically the first letter which is not yet used as a chain name
    # If all letters in the alphabet are used already then return None
    def get_next_available_chain_name(self) -> Optional[str]:
        current_chain_names = [chain.name for chain in self.chains]
        return next((name for name in available_caps if name not in current_chain_names), None)


# Calculate the distance between two atoms
def calculate_distance(atom_1: Atom, atom_2: Atom) -> float:
    squared_distances_sum = 0.0
    if atom_1.coords is not None and atom_2.coords is not None:
        for i in {'x': 0, 'y': 1, 'z': 2}.values():
            squared_distances_sum += (atom_1.coords[i] - atom_2.coords[i])**2
    return math.sqrt(squared_distances_sum)


# Set all available chains according to pdb standards
available_caps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                  'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Protein residues
aminoacids = {
    "ALA": "A",
    "ALAN": "A",
    "ALAC": "A",
    "ARG": "R",
    "ARGN": "R",
    "ARGC": "R",
    "ASN": "N",
    "ASNN": "N",
    "ASNC": "N",
    "ASP": "D",
    "ASPN": "D",
    "ASPC": "D",
    "CYS": "C",
    "CYSN": "C",
    "CYSC": "C",
    "CYH": "C",
    "CSH": "C",
    "CSS": "C",
    "CYX": "C",
    "CYP": "C",
    "GLN": "Q",
    "GLNN": "Q",
    "GLNC": "Q",
    "GLU": "E",
    "GLUN": "E",
    "GLUC": "E",
    "GLY": "G",
    "GLYN": "G",
    "GLYC": "G",
    "HIS": "H",
    "HISN": "H",
    "HISC": "H",
    "HID": "H",
    "HIE": "H",
    "HIP": "H",
    "HSD": "H",
    "HSE": "H",
    "ILE": "I",
    "ILEN": "I",
    "ILEC": "I",
    "ILU": "I",
    "LEU": "L",
    "LEUN": "L",
    "LEUC": "L",
    "LYS": "K",
    "LYSN": "K",
    "LYSC": "K",
    "MET": "M",
    "METN": "M",
    "METC": "M",
    "PHE": "F",
    "PHEN": "F",
    "PHEC": "F",
    "PRO": "P",
    "PRON": "P",
    "PROC": "P",
    "PRØ": "P",
    "PR0": "P",
    "PRZ": "P",
    "SER": "S",
    "SERN": "S",
    "SERC": "S",
    "THR": "T",
    "THRN": "T",
    "THRC": "R",
    "TRP": "W",
    "TRPN": "W",
    "TRPC": "W",
    "TRY": "W",
    "TYR": "Y",
    "TYRN": "Y",
    "TYRC": "Y",
    "VAL": "V",
    "VALN": "V",
    "VALC": "V"
}

# Nucleic acid residues
nucleotides = {
    "A": "A",
    "A3": "A",
    "A5": "A",
    "C": "C",
    "C3": "C",
    "C5": "C",
    "T": "T",
    "T3": "T",
    "T5": "T",
    "G": "G",
    "G3": "G",
    "G5": "G",
    "U": "U",
    "U3": "U",
    "U5": "U",
    "DA": "A",
    "DT": "T",
    "DC": "C",
    "DG": "G",
}

# All supported residues
supported_residues = {**aminoacids, **nucleotides}


# Transform a residue name to its equivalent single letter code
# If the residue name is not recognized then return "X"
# e.g. "ARG" -> "R", "WTF" -> "X"
# You can choose which residue types are targeted(e.g. aminoacids only)
# Options are: 'all', 'aminoacids' or 'nucleotides'
# All residue types are targeted by default
def residue_name_2_letter(residue_name: str, residue_types: str = "all") -> str:
    # Set the target residues
    if residue_types == "all":
        target_residues = supported_residues
    elif residue_types == "aminoacids":
        target_residues = aminoacids
    elif residue_types == "nucleotides":
        target_residues = nucleotides
    else:
        raise ValueError('Unrecognized residue types ' + str(residue_types))
    # Now find the corresponding letter among the target residues
    ref = target_residues.get(residue_name, 'X')
    return ref


# Map the structure aminoacids sequences against the standard reference sequences
# References are uniprot accession ids and they are optional
# For each reference, align the reference sequence with the topology sequence
# Chains which do not match any reference sequence will be blasted
# Note that an internet connection is required both to retireve the uniprot reference sequence and to do the blast
# NEVER FORGET: This system relies on the fact that topology chains are not repeated
def generate_map_online(structure: 'Structure', forced_references: List[str] = []) -> Optional[dict]:
    # Store all the references which are got through this process
    # Note that not all references may be used at the end
    references = {}
    # Get the structure chain sequences
    structure_sequences = get_chain_sequences(structure)
    # Find out which chains are protein
    protein_sequences = []
    for structure_sequence in structure_sequences:
        sequence = structure_sequence['sequence']
        if next((letter for letter in sequence if letter != 'X'), None):
            structure_sequence['match'] = {'ref': None, 'map': None, 'score': 0}
            protein_sequences.append(structure_sequence)
    # For each input forced reference, get the reference sequence
    reference_sequences = {}
    if forced_references:
        # Check forced_references is not a string
        if isinstance(forced_references, str):
            raise TypeError('Forced references should be a list and not a string a this point')
        for uniprot_id in forced_references:
            reference = get_uniprot_reference(uniprot_id)
            reference_sequences[reference['uniprot']] = reference['sequence']
            # Save the current whole reference object for later
            references[reference['uniprot']] = reference

    # Try to match all protein sequences with the available reference sequences
    # In case of match, objects in the 'protein_sequences' list are modified by adding the result
    # Finally, return True if all protein sequences were matched with the available reference sequences or False if not
    def match_sequences() -> bool:
        # Track each chain-reference alignment match and keep the score of successful alignments
        # Now for each structure sequence, align all reference sequences and keep the best alignment(if it meets the minimum)
        for structure_sequence in protein_sequences:
            for uniprot_id, reference_sequence in reference_sequences.items():
                # Align the structure sequence with the reference sequence
                align_results = align(reference_sequence, structure_sequence['sequence'])
                if not align_results:
                    continue
                # In case we have a valid alignment, check the alignment score is better than the current reference score(if any)
                sequence_map, align_score = align_results
                current_reference = structure_sequence['match']
                if current_reference['score'] > align_score:
                    continue
                reference = references[uniprot_id]
                # If the alignment is better then we impose the new reference
                structure_sequence['match'] = {'ref': reference, 'map': sequence_map, 'score': align_score}
        # Sum up the current matching
        print('Reference summary:')
        for structure_sequence in structure_sequences:
            name = structure_sequence['name']
            match = structure_sequence.get('match', None)
            if not match:
                print('   ' + name + ' -> Not protein')
                continue
            reference = structure_sequence['match'].get('ref', None)
            if not reference:
                print('   ' + name + ' -> ¿?')
                continue
            uniprot_id = reference['uniprot']
            print('   ' + name + ' -> ' + uniprot_id)
        # Finally, return True if all protein sequences were matched with the available reference sequences or False if not
        return all([structure_sequence['match']['ref'] for structure_sequence in protein_sequences])
    # If we have every protein chain matched with a reference already then we stop here
    if match_sequences():
        return format_topology_data(structure, protein_sequences)
    # If there are still any chain which is not matched with a reference then we need more references
    # To get them, we run a blast with each orphan chain sequence
    for structure_sequence in protein_sequences:
        # Skip already references chains
        if structure_sequence['match']['ref']:
            continue
        # Run the blast
        sequence = structure_sequence['sequence']
        uniprot_id = blast(sequence)[0]
        # Build a new reference from the resulting uniprot
        reference = get_uniprot_reference(uniprot_id)
        reference_sequences[reference['uniprot']] = reference['sequence']
        # Save the current whole reference object for later
        references[reference['uniprot']] = reference
        # If we have every protein chain matched with a reference already then we stop here
        if match_sequences():
            return format_topology_data(structure, protein_sequences)
    print('The BLAST failed to find a matching reference sequence for at least one protein sequence')
    return None


# Try to match all protein sequences with the available reference sequences
# In case of match, objects in the 'protein_sequences' list are modified by adding the result
# Finally, return True if all protein sequences were matched with the available reference sequences or False if not
# def match_sequences(protein_sequences: list, reference_sequences: dict) -> bool:
#     # Track each chain-reference alignment match and keep the score of successful alignments
#     # Now for each structure sequence, align all reference sequences and keep the best alignment(if it meets the minimum)
#     for structure_sequence in protein_sequences:
#         for uniprot_id, reference_sequence in reference_sequences.items():
#             # Align the structure sequence with the reference sequence
#             align_results = align(reference_sequence, structure_sequence['sequence'])
#             if not align_results:
#                 continue
#             # In case we have a valid alignment, check the alignment score is better than the current reference score(if any)
#             sequence_map, align_score = align_results
#             current_reference = structure_sequence['match']
#             if current_reference['score'] > align_score:
#                 continue
#             reference = references[uniprot_id]  # type: ignore

#             # If the alignment is better then we impose the new reference
#             structure_sequence['match'] = {'ref': reference, 'map': sequence_map, 'score': align_score}
#     # Finally, return True if all protein sequences were matched with the available reference sequences or False if not
#     return all([structure_sequence['match']['ref'] for structure_sequence in protein_sequences])


# Reformat mapping data to the topology system(introduced later)
def format_topology_data(structure: 'Structure', mapping_data: list) -> dict:
    # Get the count of residues from the structure
    residues_count = len(structure.residues)
    # Now format data
    reference_ids = []
    residue_reference_indices: List = [None] * residues_count
    residue_reference_numbers = [None] * residues_count
    for data in mapping_data:
        match = data['match']
        # Get the reference index
        # Note that several matches may belong to the same reference and thus have the same index
        reference = match['ref']
        uniprot_id = reference['uniprot']
        if uniprot_id not in reference_ids:
            reference_ids.append(reference['uniprot'])
        reference_index = reference_ids.index(uniprot_id)
        residue_indices = data['residue_indices']
        for r, residue_number in enumerate(match['map']):
            if residue_number is None:
                continue
            residue_index = residue_indices[r]
            residue_reference_indices[residue_index] = reference_index
            residue_reference_numbers[residue_index] = residue_number
    # If there are not references at the end then set all fields as None, in order to save space
    if len(reference_ids) == 0:
        reference_ids = []
        residue_reference_indices = []
        residue_reference_numbers = []
    # Return the 3 topology fields as they are in the database
    residues_map = {'references': reference_ids, 'residue_reference_indices': residue_reference_indices, 'residue_reference_numbers': residue_reference_numbers}
    return residues_map


# Align a reference aminoacid sequence with each chain sequence in a topology
# NEVER FORGET: This system relies on the fact that topology chains are not repeated
def map_sequence(ref_sequence: str, structure: 'Structure') -> list:
    sequences = get_chain_sequences(structure)
    mapping: List = []
    for s in sequences:
        sequence = sequences[s]
        sequence_map = align(ref_sequence, sequence)
        if sequence_map:
            mapping += sequence_map
    return mapping


# Get each chain name and aminoacids sequence in a topology
# Output format example: [{'sequence': 'VNLTT', 'indices': [1, 2, 3, 4, 5]}, ...]
def get_chain_sequences(structure: 'Structure') -> list:
    sequences = []
    chains = structure.chains
    for chain in chains:
        name = chain.name
        sequence = ''
        residue_indices = []
        for residue in chain.residues:
            letter = residue_name_2_letter(residue.name, 'aminoacids')
            sequence += letter
            residue_indices.append(residue.index)
        # Save sequences by chain name (i.e. chain id or chain letter)
        sequence_object = {'name': name, 'sequence': sequence, 'residue_indices': residue_indices}
        sequences.append(sequence_object)
    return sequences


# Align two aminoacid sequences
# Return a list with the reference residue indexes (values)
# which match each new sequence residues indexes (indexes)
# Return also the score of the alignment
# Return None when there is not valid alignment at all
def align(ref_sequence: str, new_sequence: str) -> Optional[Tuple[list, float]]:

    # print('- REFERENCE\n' + ref_sequence + '\n- NEW\n' + new_sequence)

    # If the new sequence is all 'X' stop here, since this would make the alignment infinite
    # Then an array filled with None is returned
    if all([letter == 'X' for letter in new_sequence]):
        return None

    # Return the new sequence as best aligned as possible with the reference sequence
    alignments = pairwise2.align.localds(ref_sequence, new_sequence, blosum62, -10, -0.5)  # type: ignore
    # DANI: Habría que hacerlo de esta otra forma según el deprecation warning (arriba hay más código)
    # DANI: El problema es que el output lo tiene todo menos la sequencia en formato alienada
    # DANI: i.e. formato '----VNLTT', que es justo el que necesito
    # alignments = aligner.align(ref_sequence, new_sequence)

    # In case there are no alignments it means the current chain has nothing to do with this reference
    # Then an array filled with None is returned
    if len(alignments) == 0:
        return None

    # Several alignments may be returned, specially when it is a difficult or impossible alignment
    # Output format example: '----VNLTT'
    best_alignment = alignments[0]
    aligned_sequence = best_alignment[1]
    print(format_alignment(*alignments[0]))
    score = alignments[0][2]
    # WARNING: Do not use 'aligned_sequence' length here since it has the total sequence length
    normalized_score = score / len(new_sequence)
    print('Normalized score: ' + str(normalized_score))

    # If the normalized score does not reaches the minimum we consider the alignment is not valid
    # It may happen when the reference goes for a specific chain but we must map all chains
    # This 1 has been found experimentally
    # Non maching sequence may return a 0.1-0.3 normalized score
    # Matching sequence may return >4 normalized score
    if normalized_score < 1:
        print('Not valid alignment')
        return None

    # Match each residue
    aligned_mapping: List = []
    aligned_index = 0
    for l_index, letter in enumerate(aligned_sequence):
        # Guions are skipped
        if letter == '-':
            continue
        # Get the current residue of the new sequence
        equivalent_letter = new_sequence[aligned_index]
        if not letter == equivalent_letter:
            raise SystemExit('Something was wrong:S')
        # 'X' residues cannot be mapped since reference sequences should never have any 'X'
        if letter == 'X':
            aligned_mapping.append(None)
            aligned_index += 1
            continue
        # Otherwise add the equivalent aligned index to the mapping
        # WARNING: Add +1 since uniprot residue counts start at 1, not 0
        aligned_mapping.append(l_index + 1)
        aligned_index += 1

    return aligned_mapping, normalized_score


# Given an aminoacids sequence, return a list of uniprot ids
# Note that we are blasting against UniProtKB / Swiss-Prot so results will always be valid UniProt accessions
# WARNING: This always means results will correspond to curated entries only
#   If your sequence is from an exotic organism the result may be not from it but from other more studied organism
def blast(sequence: str) -> List[str]:
    print('Throwing blast... (this may take a few minutes)')
    result = NCBIWWW.qblast(program="blastp", database="swissprot", sequence=sequence)
    parsed_result = xmltodict.parse(result.read())
    hits = parsed_result['BlastOutput']['BlastOutput_iterations']['Iteration']['Iteration_hits']['Hit']
    # Get the first result only
    result = hits[0]
    # Return the accession
    # DANI: Si algun día tienes problemas porque te falta el '.1' al final del accession puedes sacarlo de Hit_id
    accession = result['Hit_accession']
    print('Result: ' + accession)
    print(result['Hit_def'])
    return accession


# Given a uniprot accession, use the uniprot API to request its data and then mine what is needed for the database
def get_uniprot_reference(uniprot_accession: str) -> dict:
    # Request Uniprot
    request_url = 'https://www.ebi.ac.uk/proteins/api/proteins/' + uniprot_accession
    try:
        with urllib.request.urlopen(request_url) as response:
            parsed_response = json.loads(response.read().decode("utf-8"))
    # If the accession is not found in UniProt then the id is not valid
    except urllib.error.HTTPError as error:  # type: ignore
        if error.code == 400:
            raise ValueError('Something went wrong with the Uniprot request: ' + request_url)
    # Get the aminoacids sequence
    sequence = parsed_response['sequence']['sequence']
    return {'uniprot': uniprot_accession, 'sequence': sequence}
