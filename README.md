# On the Expressive Power of GNNs for SAT

This repository provides code for running the Weisfeiler-Leman (WL) algorithm on SAT instances. It identifies the smallest iteration where satisfiable formulas remain satisfiable when WL-equivalent literals are constrained to the same value.

## Setup

We recommend setting up the environment as follows:

````
conda create -n sat-experiments python=3.9
conda activate sat-experiments
pip install -r requirements.txt
````

## Files

- `main.py` – Entry point for running experiments.
- `WL_test.py` – Contains the main logic for running the Weisfeiler-Lehman (WL) algorithm and finding the critical iteration.
- `g4satbench/utils/utils.py` - Utility functions, credits to the [G4SATBench repository](https://github.com/zhaoyu-li/G4SATBench/blob/main/g4satbench/utils/utils.py). 


## Use

The examples folder contains sample instances. To run a simple test with a few 3-SAT instances:

```
python main.py examples/3-sat/easy --n_jobs 1
```

### Command-Line Arguments

- `folder` (str, required): Folder containing files to process.
- `--output_dir` (str, default: `results`): Directory to save output files.
- `--file_size_limit_mb` (float, default: `1`): Max file size in megabytes.
- `--max_iter` (int, default: `8`): Maximum number of WL iterations.
- `--n_jobs` (int, default: number of CPUs): Number of parallel processes to use.
- `--output_file` (str, default: `results.csv`): Filename for the output CSV. **Note:** The simplified setup requires the output file to be changed when rerunning the script on files from a different input folder. 



## Data

### Competition Instances

A few example instances are included in `examples/comp`. For these, change `--max_iter` to a larger value (e.g. 40). Processing can take several minutes.

Visit the [Benchmark database](https://benchmark-database.de/) for more information on the instances. 

#### Fetching the 2024 Benchmark Instances
1. To fetch the satisfiable 2024 benchmark instances download this [`.uri` file](https://benchmark-database.de/getinstances?query=track%3Dmain_2024+and+result%3Dsat&context=cnf)
2. Run the following command to download all instances
```
wget --content-disposition -i track_main_2024_and_result_sat.uri
```
3. Unzip the downloaded files (note that some files are very large)

## Random Instances

The dataset is generated using G4SATBench. Please follow the instructions in the [G4SATBench repository](https://github.com/zhaoyu-li/G4SATBench) to create random instances. 

## Citation

When using this code, please cite our paper:

```
@inproceedings{peltonen2026satgnn,
  title     = {On the Expressive Power of GNNs for Boolean Satisfiability},
  author    = {Peltonen, Saku and Wattenhofer, Roger},
  booktitle = {International Conference on Learning Representations},
  year      = {2026}
}
```