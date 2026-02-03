import copy
import os
import argparse
import sys

# Import modules
from models.process import Process
from algorithms.fcfs import fcfs_scheduling
from algorithms.sjf import sjf_non_preemptive
from utils.calculator import calculate_metrics
from utils.csv_handler import (
    read_processes_from_csv, 
    export_results_to_csv, 
    export_comparison_to_csv,
    create_sample_csv
)
from utils.stress_test import run_multiple_stress_tests
from ui.display import (
    display_input_table,
    display_results, 
    display_metrics,
    draw_gantt_chart,
    display_comparison
)


DEFAULT_INPUT_FILE = "input/processes.csv"
DEFAULT_OUTPUT_FOLDER = "output"


def parse_arguments():
    parser = argparse.ArgumentParser(description='CPU Scheduling Algorithm Simulator')
    parser.add_argument('--input', type=str, default=DEFAULT_INPUT_FILE,
                        help=f'Path to the input CSV file containing processes (default: {DEFAULT_INPUT_FILE})')
    parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT_FOLDER,
                        help=f'Path to the output directory (default: {DEFAULT_OUTPUT_FOLDER})')
    parser.add_argument('--stress-test', action='store_true',
                        help='Run stress tests immediately after simulation without prompting')
    return parser.parse_args()


def print_header():
    print("\n" + "=" * 65)
    print("  ╔═══════════════════════════════════════════════════════════╗")
    print("  ║       CPU SCHEDULING ALGORITHM SIMULATOR                  ║")
    print("  ║       Algorithms: FCFS & SJF (Non-Preemptive)             ║")
    print("  ║       Operating System Course Project                     ║")
    print("  ╚═══════════════════════════════════════════════════════════╝")
    print("=" * 65)


def print_footer(input_file, output_folder):
    print("\n" + "=" * 65)
    print("  ✅ PROGRAM COMPLETED SUCCESSFULLY!")
    print(f"  📁 Input file  : {input_file}")
    print(f"  📁 Output folder: {output_folder}/")
    print("=" * 65)


def run_algorithm(algorithm_func, algorithm_name: str, processes: list, output_folder: str) -> tuple:
    print("\n" + "█" * 65)
    print(f"  ALGORITHM: {algorithm_name}")
    print("█" * 65)

    algo_processes = copy.deepcopy(processes)

    result = algorithm_func(algo_processes)
    metrics = calculate_metrics(result)
    
    # Display results
    display_results(result, algorithm_name)
    display_metrics(metrics)
    draw_gantt_chart(result, algorithm_name)

    # Export results
    export_results_to_csv(result, metrics, algorithm_name.split()[0], output_folder) # Use first word for filename usually (e.g. FCFS, SJF)
    
    return result, metrics


def main():
    try:
        args = parse_arguments()

        print_header()
        
        try:
            os.makedirs(args.output, exist_ok=True)
        except OSError as e:
            print(f"\n[ERROR] Failed to create output directory '{args.output}': {e}")
            sys.exit(1)
        
        processes = read_processes_from_csv(args.input)

        if processes is None:
            if args.input == DEFAULT_INPUT_FILE:
                print("\n[INFO] Creating sample CSV file...")
                try:
                    create_sample_csv(args.input)
                    processes = read_processes_from_csv(args.input)
                except Exception as e:
                    print(f"[ERROR] Could not create sample file: {e}")
                    sys.exit(1)
            else:
                print(f"\n[ERROR] Could not read input file: {args.input}")
                sys.exit(1)

        if not processes:
            print("\n[ERROR] No processes found in input file.")
            sys.exit(1)

        display_input_table(processes)
        
        # Run FCFS
        fcfs_result, fcfs_metrics = run_algorithm(
            fcfs_scheduling, 
            "FCFS (First-Come, First-Served)", 
            processes, 
            args.output
        )
        
        # Run SJF
        sjf_result, sjf_metrics = run_algorithm(
            sjf_non_preemptive, 
            "SJF Non-Preemptive (Shortest Job First)", 
            processes, 
            args.output
        )
        
        # Compare
        display_comparison(fcfs_metrics, sjf_metrics)
        export_comparison_to_csv(fcfs_metrics, sjf_metrics, args.output)
        
        # Stress Test
        print("\n" + "=" * 65)
        if args.stress_test:
             run_multiple_stress_tests(args.output)
        else:
            run_stress = input(" Would you like to run the STRESS TEST(y/n): ").strip().lower()
            if run_stress == 'y':
                run_multiple_stress_tests(args.output)
        
        print_footer(args.input, args.output)

    except KeyboardInterrupt:
        print("\n\n[INFO] Program interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()