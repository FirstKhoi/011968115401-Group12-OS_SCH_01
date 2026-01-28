def calculate_metrics(processes: list) -> dict:
    n = len(processes)
    
    if n == 0:
        return {}
    
    # Calculate tổng
    total_waiting = sum(p.waiting_time for p in processes)
    total_turnaround = sum(p. turnaround_time for p in processes)
    total_burst = sum(p.burst_time for p in processes)
    
    # Time to excute
    completion_time = max(p.completion_time for p in processes)
    first_start = min(p.start_time for p in processes)
    total_time = completion_time - first_start

    cpu_utilization = (total_burst / total_time * 100) if total_time > 0 else 0
    
    throughput = n / total_time if total_time > 0 else 0
    
    return {
        'avg_waiting_time': total_waiting / n,
        'avg_turnaround_time':  total_turnaround / n,
        'cpu_utilization': cpu_utilization,
        'throughput': throughput,
        'total_execution_time': completion_time
    }