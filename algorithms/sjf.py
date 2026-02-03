def sjf_non_preemptive(processes:  list) -> list:
    processes.sort(key=lambda p: (p.arrival_time, p.pid))

    n = len(processes)
    completed = [False] * n
    current_time = 0
    result = []
    
    for _ in range(n):
        min_burst = float('inf')
        shortest_idx = -1
        
        for i, process in enumerate(processes):
            if (not completed[i] and 
                process.arrival_time <= current_time and 
                process.burst_time < min_burst):
                min_burst = process.burst_time
                shortest_idx = i
        if shortest_idx == -1:
            current_time = min(p.arrival_time for i, p in enumerate(processes) 
                              if not completed[i])
            continue
        
        process = processes[shortest_idx]
        process.start_time = current_time
        process.completion_time = current_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        
        current_time = process.completion_time
        completed[shortest_idx] = True
        result.append(process)
    
    return result