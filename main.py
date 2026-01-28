import copy
import os

# Import từ các module
from models.process import Process
from algorithms. fcfs import fcfs_scheduling
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


INPUT_FILE = "input/processes.csv"
OUTPUT_FOLDER = "output"


def print_header():
    print("\n" + "=" * 65)
    print("  ╔═══════════════════════════════════════════════════════════╗")
    print("  ║       CPU SCHEDULING ALGORITHM SIMULATOR                  ║")
    print("  ║       Algorithms: FCFS & SJF (Non-Preemptive)             ║")
    print("  ║       Operating System Course Project                     ║")
    print("  ╚═══════════════════════════════════════════════════════════╝")
    print("=" * 65)


def print_footer():
    print("\n" + "=" * 65)
    print("  ✅ PROGRAM COMPLETED SUCCESSFULLY!")
    print(f"  📁 Input file  : {INPUT_FILE}")
    print(f"  📁 Output folder: {OUTPUT_FOLDER}/")
    print("=" * 65)


def run_fcfs(processes: list) -> tuple:
    print("\n" + "█" * 65)
    print("  ALGORITHM 1: FCFS (First-Come, First-Served)")
    print("█" * 65)

    fcfs_processes = copy.deepcopy(processes)

    result = fcfs_scheduling(fcfs_processes)
    metrics = calculate_metrics(result)
    
    display_results(result, "FCFS")
    display_metrics(metrics)
    draw_gantt_chart(result, "FCFS")

    export_results_to_csv(result, metrics, "FCFS", OUTPUT_FOLDER)
    
    return result, metrics


def run_sjf(processes: list) -> tuple:
    print("\n" + "█" * 65)
    print("  ALGORITHM 2: SJF Non-Preemptive (Shortest Job First)")
    print("█" * 65)

    sjf_processes = copy. deepcopy(processes)

    result = sjf_non_preemptive(sjf_processes)
    metrics = calculate_metrics(result)
    

    display_results(result, "SJF Non-Preemptive")
    display_metrics(metrics)
    draw_gantt_chart(result, "SJF Non-Preemptive")

    
    export_results_to_csv(result, metrics, "SJF", OUTPUT_FOLDER)
    
    return result, metrics


def main():
    # In header
    print_header()
    
    # Tạo thư mục output
    os. makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    processes = read_processes_from_csv(INPUT_FILE)

    if processes is None:
        print("\n[INFO] Tạo file CSV mẫu...")
        create_sample_csv(INPUT_FILE)
        processes = read_processes_from_csv(INPUT_FILE)

    display_input_table(processes)
    
    fcfs_result, fcfs_metrics = run_fcfs(processes)
    
    sjf_result, sjf_metrics = run_sjf(processes)
    
    display_comparison(fcfs_metrics, sjf_metrics)
    export_comparison_to_csv(fcfs_metrics, sjf_metrics, OUTPUT_FOLDER)
    
    print("\n" + "=" * 65)
    run_stress = input(" Would you like to run the STRESS TEST(y/n): ").strip().lower()
    
    if run_stress == 'y':
        run_multiple_stress_tests()
    
    # In footer
    print_footer()


# Entry point
if __name__ == "__main__":
    main()