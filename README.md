# GNN Expressivity for SAT

This repository provides code for running the Weisfeiler-Leman (WL) algorithm on SAT instances. It identifies the smallest iteration where satisfiable formulas remain satisfiable when WL-equivalent variables are constrained to the same value.

## Setup

We recommend using the following lines to get started: 
````
conda create -n sat-experiments python=3.9
conda activate sat-experiments
pip install -r requirements.txt
````

## Files

- `main.py` – Entry point for running experiments.
- `WL_test.py` – Contains the main logic for running the Weisfeiler-Lehman (WL) algorithm and finding the critical iteration.
- `g4satbench/utils/utils.py` - Utility functions, credits to the [G4SATBench repository](https://github.com/zhaoyu-li/G4SATBench/blob/main/g4satbench/utils/utils.py). 


## Basic Examples

To run a simple test with a few 3-SAT instances:

```
python main.py examples/3-sat --n_jobs 1
```

## Competition Instances 

Visit the [Benchmark database](https://benchmark-database.de/) for more information on the instances. 

### Fetching the 2024 Benchmark Instances
1. To fetch the satisfiable 2024 benchmark instances download this [`.uri` file](https://benchmark-database.de/getinstances?query=track%3Dmain_2024+and+result%3Dsat&context=cnf)
2. Run the following command to download all instances
```
wget --content-disposition -i track_main_2024_and_result_sat.uri
```
3. Unzip the downloaded files (note that some files are very large)

## Random Instances

The dataset is generated using G4SATBench. Please follow the instructions in the [G4SATBench repository](https://github.com/zhaoyu-li/G4SATBench) to create random instances. 