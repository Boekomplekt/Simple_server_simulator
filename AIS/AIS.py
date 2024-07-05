import random
import math


class Event:
    def __init__(self, time, ev, J1, J2, St, S, n, Q):
        self.time = time
        self.ev = ev
        self.J1 = J1
        self.J2 = J2
        self.St = St
        self.S = S
        self.n = n
        self.Q = Q

class Simulator:
    def __init__(self, end_time):
        self.end_time = end_time
        self.system_time = 0
        self.event_list = []
        self.queue = []
        self.server_busy = False
        self.server_proc_time = 0
        self.J1 = 0  # Initialize next J1 arrival to positive infinity
        self.J2 = 0  # Initialize next J2 arrival to positive infinity
        self.St = 0 # Completion time for current job (initially 0)
        self.S = 0  # Server status (0: free, 1: busy)
        self.n = 0  # Number of jobs in queue
        self.Q = []  # List of jobs in the queue (names)
        self.total_jobs = 0
        self.total_queue_time = 0
        self.server_idle_time = 0

    def schedule_event(self, time, ev, J1, J2, St, S, n, Q):
        event = Event(time, ev, J1, J2, St, S, n, Q)
        self.event_list.append(event)
        self.event_list.sort(key=lambda x: x.time)

    def initiate_simulation(self):
        # Start event
        self.schedule_event(0, "start", 0, 0, 0, 0, 0, "-")
        
        # Print table header
        print("Time\tEvent\tJ1\tJ2\tSt\tS\tn\tQ")

        # Main simulation loop
        while self.event_list and self.system_time < self.end_time:
            event = self.event_list.pop(0)
            self.system_time = event.time
            self._handle_event(event)
            # Print current event
            print(f"{event.time}\t{event.ev}\t{self.J1}\t{self.J2}\t{self.St}\t{event.S}\t{event.n}\t{','.join(event.Q)}")

    def _handle_event(self, event):
        if event.ev == "start":
            self.J1 = custom_rand(job_type="J1")  # Generate next J1 arrival time
            self.J2 = custom_rand(job_type="J2")  # Generate next J2 arrival time
            self.St = 2.3
            self.schedule_event(self.J1, "J1 job arrival", self.J1, self.J2, self.St, self.S, self.n, self.Q)
            self.schedule_event(self.J2, "J2 job arrival", self.J1, self.J2, self.St, self.S, self.n, self.Q)
            self.schedule_event(self.St, "Server Free", self.J1, self.J2, self.St, self.S, self.n, self.Q)
            

        elif event.ev == "J1 job arrival":
            self.J1 = self.system_time + custom_rand(job_type="J1")  
            self.schedule_event(self.J1, "J1 job arrival", self.J1, self.J2, self.St, self.S, self.n, self.Q)  

            self.Q.append("J1")
            self.n += 1

            if not self.server_busy:
                self.server_busy = True
                self.server_proc_time = custom_rand(job_type="Job")  # Processing time for any job
                self.schedule_event(self.St, "Server Free", self.J1, self.J2, self.St, 1, self.n, self.Q)

        elif event.ev == "J2 job arrival":
            self.J2 = self.system_time + custom_rand(job_type="J2")  
            self.schedule_event(self.J2, "J2 job arrival", self.J1, self.J2, self.St, self.S, self.n, self.Q)  

            self.Q.append("J2")
            self.n += 1

            if not self.server_busy:
                self.server_busy = True
                self.server_proc_time = custom_rand(job_type="Job")  # Processing time for any job
                self.schedule_event(self.St, "Server Free", self.J1, self.J2, self.St, 1, self.n, self.Q)

        elif event.ev == "Server Free":
            if not self.Q:
                self.server_busy = False
                self.server_idle_time += self.system_time - self.St
            else:
                job_name = self.Q.pop(0)
                self.n -= 1
                self.total_queue_time += self.system_time - (self.St - self.server_proc_time)  # Account for processing time
                self.total_jobs += 1
                self.St = self.system_time + custom_rand(job_type="Job")
                self.schedule_event(self.St, "Server Free", event.J1, event.J2, self.St, 1, self.n, self.Q)


def custom_rand(job_type=None):
    u = random.random()
    return round(-math.log(1 - u) / 1.4, 2)

simulator = Simulator(3)  # Set your desired end time
simulator.initiate_simulation()