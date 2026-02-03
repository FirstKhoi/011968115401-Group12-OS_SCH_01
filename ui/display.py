def display_input_table(processes: list):
    print("\n" + "=" * 50)
    print("  INPUT PROCESSES (from CSV file)")
    print("=" * 50)
    print(f"{'PID': <10}{'Arrival Time': <15}{'Burst Time':<15}")
    print("-" * 40)
    for p in processes:
        print(f"{p.pid:<10}{p.arrival_time:<15}{p.burst_time:<15}")
    print("-" * 40)
    print(f"Total: {len(processes)} processes\n")


def display_results(processes: list, algorithm_name: str):
    print("\n" + "=" * 65)
    print(f"  {algorithm_name} SCHEDULING RESULTS")
    print("=" * 65)
    
    # Header
    print(f"{'PID':<8}{'AT':<8}{'BT':<8}{'ST':<8}{'CT':<8}{'TAT':<8}{'WT': <8}")
    print("-" * 56)
    
    # Data rows - sắp xếp theo PID
    for p in sorted(processes, key=lambda x: x.pid):
        print(f"{p.pid:<8}{p.arrival_time:<8}{p.burst_time:<8}"
              f"{p.start_time:<8}{p.completion_time:<8}"
              f"{p.turnaround_time:<8}{p. waiting_time:<8}")
    
    print("-" * 56)
    print("Legend:  AT=Arrival Time, BT=Burst Time, ST=Start Time")
    print("        CT=Completion Time, TAT=Turnaround Time, WT=Waiting Time")


def display_metrics(metrics: dict):
    #Hiển thị các chỉ số đánh giá
    print("\n" + "-" * 45)
    print("  PERFORMANCE METRICS")
    print("-" * 45)
    print(f"  Average Waiting Time    : {metrics['avg_waiting_time']:.2f}")
    print(f"  Average Turnaround Time : {metrics['avg_turnaround_time']:.2f}")
    print(f"  CPU Utilization         : {metrics['cpu_utilization']:.2f}%")
    print(f"  Throughput              :  {metrics['throughput']:.4f} processes/unit")
    print("-" * 45)


def draw_gantt_chart(processes: list, algorithm_name: str):
    print(f"\n{'='*55}")
    print(f"  GANTT CHART - {algorithm_name}")
    print("=" * 55)
    
    if not processes:
        print("  No processes to display.")
        return

    # Sort by execution order (start_time)
    sorted_p = sorted(processes, key=lambda p: p.start_time)
    
    # Calculate total duration for scaling
    total_duration = sorted_p[-1].completion_time - sorted_p[0].start_time
    if total_duration == 0:
        return

    max_chart_width = 80
    scale = max_chart_width / total_duration
    
    segment_widths = []
    for p in sorted_p:
        prop_width = int(p.burst_time * scale)
        actual_width = max(prop_width, len(p.pid) + 2)
        segment_widths.append(actual_width)

    # border tren
    top = "┌"
    for width in segment_widths:
        top += "─" * width + "┬"
    top = top[:-1] + "┐"
    print(top)


    mid = "│"
    for i, p in enumerate(sorted_p):
        width = segment_widths[i]
        mid += f"{p.pid:^{width}}│"
    print(mid)
    
    # Lower border
    bot = "└"
    for width in segment_widths:
        bot += "─" * width + "┴"
    bot = bot[:-1] + "┘"
    print(bot)
    
    # Timeline
    # Start time
    timeline = f"{sorted_p[0].start_time}"
    current_pos_char = len(str(sorted_p[0].start_time))
    
    for i, p in enumerate(sorted_p):
        width = segment_widths[i]

        num_str = str(p.completion_time)
        
        padding = width + 1 - len(num_str)
        padding = max(1, padding) 
        
        timeline += f"{p.completion_time:>{width + 1}}"
        
    print(timeline)
    
    # Execution Order
    execution_order = " -> ".join([p.pid for p in sorted_p])
    print(f"\nExecution Order: {execution_order}")


def display_comparison(fcfs_metrics: dict, sjf_metrics: dict):
    print("\n" + "=" * 65)
    print("  ALGORITHM COMPARISON:  FCFS vs SJF (Non-Preemptive)")
    print("=" * 65)
    
    print(f"{'Metric':<25}{'FCFS':<15}{'SJF':<15}{'Better':<10}")
    print("-" * 65)
    
    comparisons = [
        ('Avg Waiting Time', 'avg_waiting_time', 'lower'),
        ('Avg Turnaround Time', 'avg_turnaround_time', 'lower'),
        ('CPU Utilization (%)', 'cpu_utilization', 'higher'),
        ('Throughput', 'throughput', 'higher'),
    ]
    
    for name, key, better in comparisons:
        fcfs_val = fcfs_metrics[key]
        sjf_val = sjf_metrics[key]
        
        if better == 'lower':
            winner = "FCFS" if fcfs_val < sjf_val else "SJF" if sjf_val < fcfs_val else "Equal"
        else: 
            winner = "FCFS" if fcfs_val > sjf_val else "SJF" if sjf_val > fcfs_val else "Equal"
        
        print(f"{name:<25}{fcfs_val: <15.2f}{sjf_val:<15.2f}{winner:<10}")
    
    print("-" * 65)