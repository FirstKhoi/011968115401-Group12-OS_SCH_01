import time
import random
import copy
from models.process import Process
from algorithms.fcfs import fcfs_scheduling
from algorithms.sjf import sjf_non_preemptive
from utils.calculator import calculate_metrics
import csv
import os
from datetime import datetime


def generate_random_processes(num_processes: int) -> list:
    processes = []
    for i in range(num_processes):
        p = Process(
            pid=f"P{i+1}",
            arrival_time=random. randint(0, num_processes // 2),
            burst_time=random.randint(1, 20)
        )
        processes.append(p)
    return processes


def run_stress_test(num_processes: int) -> dict:
    print(f"\n{'='*55}")
    print(f"  STRESS TEST - {num_processes} PROCESSES")
    print("=" * 55)
    
    processes = generate_random_processes(num_processes)
    
    # Test FCFS
    fcfs_copy = copy.deepcopy(processes)
    start_time = time.time()
    fcfs_result = fcfs_scheduling(fcfs_copy)
    fcfs_exec_time = time.time() - start_time
    fcfs_metrics = calculate_metrics(fcfs_result)
    
    # Test SJF
    sjf_copy = copy.deepcopy(processes)
    start_time = time.time()
    sjf_result = sjf_non_preemptive(sjf_copy)
    sjf_exec_time = time.time() - start_time
    sjf_metrics = calculate_metrics(sjf_result)
    
    # Display
    print(f"\n{'Algorithm':<12}{'Exec Time':<15}{'Avg WT':<12}{'Avg TAT':<12}")
    print("-" * 50)
    print(f"{'FCFS':<12}{fcfs_exec_time:<15.4f}{fcfs_metrics['avg_waiting_time']:<12.2f}"
          f"{fcfs_metrics['avg_turnaround_time']:<12.2f}")
    print(f"{'SJF':<12}{sjf_exec_time:<15.4f}{sjf_metrics['avg_waiting_time']:<12.2f}"
          f"{sjf_metrics['avg_turnaround_time']:<12.2f}")
    
    return {
        'num_processes': num_processes,
        'fcfs_exec_time': fcfs_exec_time,
        'sjf_exec_time': sjf_exec_time,
        'fcfs_avg_wt': fcfs_metrics['avg_waiting_time'],
        'sjf_avg_wt': sjf_metrics['avg_waiting_time']
    }


def run_multiple_stress_tests(output_folder: str = "output"):
    test_sizes = [100, 500, 1000, 2000]
    results = []
    
    print("\n" + "=" * 55)
    print("  RUNNING STRESS TESTS")
    print("=" * 55)
    
    for size in test_sizes: 
        result = run_stress_test(size)
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("  STRESS TEST SUMMARY")
    print("=" * 60)
    print(f"{'Processes':<12}{'FCFS Time':<15}{'SJF Time':<15}{'Faster':<10}")
    print("-" * 52)
    
    for r in results:
        faster = "FCFS" if r['fcfs_exec_time'] < r['sjf_exec_time'] else "SJF"
        print(f"{r['num_processes']:<12}{r['fcfs_exec_time']:<15.4f}"
              f"{r['sjf_exec_time']:<15.4f}{faster:<10}")
    
    
    # Export to CSV
    os.makedirs(output_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(output_folder, f"StressTest_Results_{timestamp}.csv")
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            f.write("=== STRESS TEST RESULTS ===\n")
            f.write(f"Timestamp,{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            fieldnames = ['NumProcesses', 'FCFS_Time', 'SJF_Time', 'Faster_Algo', 
                          'FCFS_Avg_WT', 'SJF_Avg_WT']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for r in results:
                faster = "FCFS" if r['fcfs_exec_time'] < r['sjf_exec_time'] else "SJF"
                writer.writerow({
                    'NumProcesses': r['num_processes'],
                    'FCFS_Time': f"{r['fcfs_exec_time']:.6f}",
                    'SJF_Time': f"{r['sjf_exec_time']:.6f}",
                    'Faster_Algo': faster,
                    'FCFS_Avg_WT': f"{r['fcfs_avg_wt']:.2f}",
                    'SJF_Avg_WT': f"{r['sjf_avg_wt']:.2f}"
                })
        print(f"\n[✓] Stress test results exported to: {filepath}")
    except Exception as e:
        print(f"\n[✗] Failed to export stress test results: {e}")
    
    return results