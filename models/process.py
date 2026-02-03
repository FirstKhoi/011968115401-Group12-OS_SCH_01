class Process:
    
    def __init__(self, pid: str, arrival_time: int, burst_time: int):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = 0          
        self.completion_time = 0       
        self.turnaround_time = 0      
        self.waiting_time = 0          
    
    def __repr__(self):
        return f"Process({self.pid}, AT={self.arrival_time}, BT={self.burst_time})"
    
    def to_dict(self) -> dict:
        return {
            'PID': self.pid,
            'ArrivalTime': self.arrival_time,
            'BurstTime': self.burst_time,
            'StartTime': self.start_time,
            'CompletionTime': self.completion_time,
            'TurnaroundTime': self.turnaround_time,
            'WaitingTime': self.waiting_time
        }