def fcfs_scheduling(processes:  list) -> list:
    sorted_processes = sorted(processes, key=lambda p: (p.arrival_time, p.pid))
    
    current_time = 0
    
    for process in sorted_processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        
        process.start_time = current_time
        process.completion_time = current_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        
        current_time = process.completion_time
    
    return sorted_processes