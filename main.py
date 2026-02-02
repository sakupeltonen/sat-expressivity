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

    info['time'] = end - start

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
    parser.add_argument('--file_size_limit_mb', type=float, default=1, help='Max file size in megabytes (default: 1 MB)')
    parser.add_argument('--max_iter', type=int, default=8, help='Maximum number of iterations for WL')
    parser.add_argument('--n_jobs', type=int, default=cpu_count(), help='Number of parallel processes to use (default: all available CPUs)')
    parser.add_argument('--output_file', type=str, default='results.csv', help='Output filename for the results CSV')

    opts = parser.parse_args()

    print(f"Processing files in {opts.folder}")
    print(f"Options: file_size_limit_mb={opts.file_size_limit_mb}, max_iter={opts.max_iter}, n_jobs={opts.n_jobs}")

    # Ensure the output directory exists
    os.makedirs(opts.output_dir, exist_ok=True)

    # Save DataFrame to CSV
    output_filepath = os.path.join(opts.output_dir, opts.output_file)
    print(f"Saving results to {output_filepath}")

    if os.path.exists(output_filepath):
        previous_results = pd.read_csv(output_filepath)
        # print(f"Found {len(previous_results)} already processed files")
    else:
        previous_results = pd.DataFrame(columns=['file_name'])

    # Find a list of files
    file_paths = []
    for root, _, files in os.walk(opts.folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size = os.path.getsize(file_path)
            file_ext = os.path.splitext(file_name)[1]

            instance_name = file_name.split('.')[0]

            if instance_name in previous_results['file_name'].values:
                print(f"Skipping {file_name} (already processed)")
                continue

            if file_ext == '.cnf' and file_size <= opts.file_size_limit_mb * 1024 * 1024:
                file_paths.append(file_path)
    
    print(f"Found {len(file_paths)} files to process")


    if opts.n_jobs > 1:
        # Process files in parallel
        with Pool(processes=opts.n_jobs) as pool:
            pool.starmap(process_file, 
                            [(file_path, opts.max_iter, output_filepath) for i, file_path in enumerate(file_paths)])
    else:
        for i, file_path in enumerate(file_paths):
            process_file(file_path, opts.max_iter, output_filepath)


if __name__ == "__main__":
    main()