import csv
import os
from datetime import datetime
from models.process import Process


def read_processes_from_csv(filepath: str) -> list:
    processes = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    process = Process(
                        pid=row['PID'].strip(),
                        arrival_time=int(row['ArrivalTime']),
                        burst_time=int(row['BurstTime'])
                    )
                    processes.append(process)
                except ValueError as ve:
                    print(f"[!] Skipping invalid row: {row} - Error: {ve}")
        
        print(f"[✓] Read {len(processes)} processes from: {filepath}")
        return processes
        
    except FileNotFoundError:
        print(f"[✗] File not found: {filepath}")
        return None
    except KeyError as e:
        print(f"[✗] CSV missing column: {e}")
        return None
    except Exception as e: 
        print(f"[✗] Error reading file: {e}")
        return None


def export_results_to_csv(processes: list, metrics: dict, 
                          algorithm_name: str, output_folder: str) -> str:
    os.makedirs(output_folder, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{algorithm_name. replace(' ', '_')}_{timestamp}.csv"
    filepath = os.path.join(output_folder, filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        file.write(f"Algorithm,{algorithm_name}\n")
        file.write(f"Generated,{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Total Processes,{len(processes)}\n")
        file.write("\n")
        
        file.write("=== SCHEDULING RESULTS ===\n")
        fieldnames = ['PID', 'ArrivalTime', 'BurstTime', 'StartTime', 
                      'CompletionTime', 'TurnaroundTime', 'WaitingTime']
        
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for p in sorted(processes, key=lambda x:  x.pid):
            writer. writerow(p. to_dict())
        
        file.write("\n=== PERFORMANCE METRICS ===\n")
        file.write(f"Average Waiting Time,{metrics['avg_waiting_time']:.2f}\n")
        file.write(f"Average Turnaround Time,{metrics['avg_turnaround_time']:.2f}\n")
        file.write(f"CPU Utilization (%),{metrics['cpu_utilization']:.2f}\n")
        file.write(f"Throughput (processes/unit),{metrics['throughput']:.4f}\n")
        file.write(f"Total Execution Time,{metrics['total_execution_time']}\n")
    
    print(f"[✓] Exported:  {filepath}")
    return filepath


def export_comparison_to_csv(fcfs_metrics: dict, sjf_metrics: dict, 
                              output_folder: str) -> str:
    os.makedirs(output_folder, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(output_folder, f"Comparison_{timestamp}.csv")
    
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        file.write("=== ALGORITHM COMPARISON:  FCFS vs SJF ===\n")
        file.write(f"Generated,{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        file.write("Metric,FCFS,SJF,Better Algorithm\n")
        
        comparisons = [
            ('Average Waiting Time', 'avg_waiting_time', 'lower'),
            ('Average Turnaround Time', 'avg_turnaround_time', 'lower'),
            ('CPU Utilization (%)', 'cpu_utilization', 'higher'),
            ('Throughput', 'throughput', 'higher'),
        ]
        
        for name, key, better in comparisons:
            fcfs_val = fcfs_metrics[key]
            sjf_val = sjf_metrics[key]
            
            if better == 'lower':
                winner = 'FCFS' if fcfs_val < sjf_val else 'SJF' if sjf_val < fcfs_val else 'Equal'
            else:
                winner = 'FCFS' if fcfs_val > sjf_val else 'SJF' if sjf_val > fcfs_val else 'Equal'
            
            file.write(f"{name},{fcfs_val:.4f},{sjf_val:.4f},{winner}\n")
    
    print(f"[✓] Comparison exported: {filepath}")
    return filepath


def create_sample_csv(filepath: str):
    os.makedirs(os.path. dirname(filepath), exist_ok=True)
    
    sample_data = [
        ['PID', 'ArrivalTime', 'BurstTime'],
        ['P1', '0', '6'],
        ['P2', '1', '8'],
        ['P3', '2', '7'],
        ['P4', '3', '3'],
        ['P5', '5', '4'],
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)
    
    print(f"[✓] Created sample CSV: {filepath}")