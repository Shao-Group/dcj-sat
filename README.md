dcj-sat is a software package implemented to compute the edit distance under
the DCJ model for two genomes with duplicate genes using a SAT formulation. It returns
the maximum number of cycles possible in the final decomposition of the adjacency graph of two genomes.


# dcj-sat

## Prerequisites

- [BOOST](http://www.boost.org)
- Python >= 3.7
- [PySAT](https://pysathq.github.io/)

### Setting up BOOST 
Download [BOOST](http://www.boost.org) and uncompress it somewhere (compilation and installation is not necessary). Set environment variable `BOOST_HOME` to indicate the directory of BOOSt. For example, for UNIX platforms, add the following statement to the file ~/.bash_profile:

```sh
export BOOST_HOME='/directory/to/your/boost/boost_1_85_0'
```

### Cloning Repository

```sh
# Clone the repository to your local machine
git clone https://github.com/Shao-Group/dcj-sat.git
cd dcj-sat/
```

### Setting up the environment

```sh
# Create a Python virtual environment using venv (example)
python3 -m venv venv
source venv/bin/activate

# Install the pySAT library
pip install 'python-sat[aiger,approxmc,cryptosat,pblib]'
```

### Building the files
```sh
# You might have to install automake(if not already installed) to build dependencies. For example (using homebrew on mac)
brew install automake
```

```sh
# Make the build script executable and run it
chmod +x build.sh
./build.sh
```

## Input Files
Each input file represents a genome and each line in the file represents a gene. Each line must be in the following format
```sh
<GENE_ID> <GENE_FAMILY> <CHROMOSOME_NAME> <CHROMOSOME_TYPE>
```

GENE_ID: A unique identifier for each gene.
GENE_FAMILY: The gene family as an integer.
CHROMOSOME_NAME: Name of the chromosome as an integer.
CHROMOSOME_TYPE: Type of chromosome (1 for linear, 2 for circular).

## Testing

### Running the test
```sh
# Make the testing script executable and run it
chmod +x run_sat.sh
./run_sat.sh <path_to_g1_file> <path_to_g2_file>
```

## Test Files

### Real Data
You can find the test files for real data in the 'test_files/real_data'. Inside it are three directories corresponding to including all genes and including genes with less than 2 and less than 3 gene families. In each each of these folders is a folder corresponding to each pair. For eg, to compare gorilla and human containing genes with less than 3 gene families:

```sh
<path_to_g1_file>
test_files/real_data/less_than_three/gorilla_human/gorilla.dcj

<path_to_g2_file>
test_files/real_data/less_than_three/gorilla_human/human.dcj
```

### Simulated Data
Test files for simulated data can be found in 'test\_files/simulations'. Inside are two folders 'variable\_dcj\_ops' and 'variable\_gene\_families'. Each of these folders contain a folder corresponding to an instance. This folder contains three files, the original genome, and the two pairs of genomes to compare. For eg, to run the package on the genome with 500 genes, 340 gene families and 150 DCJ operations:

```sh
<path_to_g1_file>
test_files/simulations/variable_gene_families/sim_500_340_150/sim_500_340_150_1.dcj

<path_to_g2_file>
test_files/simulations/variable_gene_families/sim_500_340_150/sim_500_340_150_2.dcj
```
