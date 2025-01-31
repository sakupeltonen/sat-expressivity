import os
import argparse
import pandas as pd
import time
from multiprocessing import Pool, cpu_count
from datetime import datetime

from WL_test import find_critical_iter


def process_file(file_path, max_iter, output_filepath):
    """
    Processes a single file using find_critical_iter and returns the result.
    """
    file_name = os.path.basename(file_path)
    print(f"Started processing {file_name} at {datetime.now().strftime('%H:%M')}\n")

    start = time.time()
    info = find_critical_iter(file_path, max_iter)
    end = time.time()
    
    print_str = f"Processed {file_name} (took {end - start:.0f}s):\n"
    if info['sat']:
        print_str += f"crit {info['iter_critical']}, "
    else:
        print_str += "unsat, "
    if info['converged']:
        print_str += f"converged {info['iter_converged']}, "
    else:
        print_str += "not converged, "
    print_str += f"nvars {info['n_vars']}, nclauses {info['n_clauses']}\n"
    print(print_str)

    df = pd.DataFrame([info])  # Convert the result to a DataFrame row
    with open(output_filepath, 'a') as f:  # parallel-safe (appending is atomic)
        df.to_csv(f, index=False, header=f.tell() == 0)  # Write header only if file is empty

    return info


def main():
    """
    Processes files in a folder, filters them based on size, runs find_critical_iter, 
    and saves the results to a csv.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=str, help='Folder containing files to process')
    parser.add_argument('--output_dir', type=str, default='results', help='Output CSV file to save results')
    parser.add_argument('--file_size_limit_mb', type=float, default=10, help='Max file size in megabytes (default: 50 MB)')
    parser.add_argument('--max_iter', type=int, default=10, help='Maximum number of iterations for WL')
    parser.add_argument('--n_jobs', type=int, default=cpu_count(), help='Number of parallel processes to use (default: all available CPUs)')

    opts = parser.parse_args()

    print(f"Processing files in {opts.folder}")
    print(f"Options: file_size_limit_mb={opts.file_size_limit_mb}, max_iter={opts.max_iter}, n_jobs={opts.n_jobs}")

    # Create a valid filename from the path
    sanitized_name = opts.folder.replace("/", "_").replace("\\", "_").replace(":", "_")
    output_filename = sanitized_name + f"{str(opts.file_size_limit_mb)}MB_{opts.max_iter}iter.csv"
    
    # Ensure the output directory exists
    os.makedirs(opts.output_dir, exist_ok=True)

    # Save DataFrame to CSV
    output_filepath = os.path.join(opts.output_dir, output_filename)
    print(f"Saving results to {output_filepath}")

    # Find a list of files
    file_paths = []
    for root, _, files in os.walk(opts.folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size = os.path.getsize(file_path)
            file_ext = os.path.splitext(file_name)[1]

            if file_ext == '.cnf' and file_size <= opts.file_size_limit_mb * 1024 * 1024:
                file_paths.append(file_path)
    
    print(f"Found {len(file_paths)} files to process")


    # Process files in parallel
    with Pool(processes=opts.n_jobs) as pool:
        pool.starmap(process_file, 
                     [(file_path, opts.max_iter, output_filepath) for file_path in file_paths])


if __name__ == "__main__":
    main()