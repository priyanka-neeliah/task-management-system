
# Assignment : Sensor Aggregation System

import threading
import time
import random


# QUESTION 1.1 A - Basic simulation with threads

print("\n" + "="*60)
print("QUESTION 1.1 A - Basic simulation")
print("="*60)

# Make some fake sensor data
sensor_data = []
for i in range(10):  # 10 sensors for testing
    # Each sensor has ID and random processing time between 0.1-1.0 seconds
    sensor_data.append({'sensor_id': i, 'proc_time': random.uniform(0.1, 1.0)})

print(f"Created {len(sensor_data)} sensor readings")

# Simple aggregator class
class BasicAggregator:
    def __init__(self, agg_id):
        self.id = agg_id
        print(f"Basic Aggregator {self.id} ready")
    
    def process_data(self, reading):
        """Process one sensor reading - just sleep for its processing time"""
        print(f"Agg{self.id} started reading {reading['sensor_id']} (will take {reading['proc_time']:.2f}s)")
        time.sleep(reading['proc_time'])  # Simulate work
        print(f"Agg{self.id} finished reading {reading['sensor_id']}")

# Create 3 aggregators
aggregators_list = [BasicAggregator(i) for i in range(3)]

# Distribute work and process with threads
threads_list = []
start_time = time.time()

# Simple round-robin assignment
for i, reading in enumerate(sensor_data):
    # Choose aggregator: 0,1,2,0,1,2,etc...
    agg = aggregators_list[i % len(aggregators_list)]
    
    # Create thread for this reading
    t = threading.Thread(target=agg.process_data, args=(reading,))
    threads_list.append(t)
    t.start()

# Wait for all threads to finish
for t in threads_list:
    t.join()

end_time = time.time()
print(f"\nAll basic processing done in {end_time - start_time:.2f} seconds")

# QUESTIONS 1.2 B & 1.3 C - Thread safety and capacity limits

print("\n" + "="*60)
print("QUESTIONS 1.2 B & 1.3 C - Advanced version")
print("="*60)

# New settings for advanced version
NUM_READINGS = 50
NUM_AGGS = 5
MAX_CAPACITY = 2  # Each aggregator can only handle 2 readings at once

# Create more sensor data
readings_list = []
for i in range(NUM_READINGS):
    readings_list.append({'sensor_id': i, 'proc_time': random.uniform(0.1, 0.5)})

print(f"Created {len(readings_list)} sensor readings for advanced test")

class SmartAggregator:
    def __init__(self, agg_id, max_cap):
        self.id = agg_id
        self.capacity = max_cap
        self.current_work = 0  # How many readings being processed now
        self.lock = threading.Lock()  # For thread safety - QUESTION 1.2 B
        print(f"Smart Aggregator {self.id} ready (capacity: {self.capacity})")
    
    def can_take_more(self):
        """Check if this aggregator has space - uses lock for thread safety"""
        with self.lock:
            # QUESTION 1.3 C - Check capacity limit
            return self.current_work < self.capacity
    
    def assign_reading(self, reading):
        """Try to assign reading to this aggregator. Returns True if successful."""
        with self.lock:
            if self.current_work >= self.capacity:
                return False  # No space available right now
            
            # If we have space, take the reading
            self.current_work += 1
            print(f"Reading {reading['sensor_id']} -> Agg{self.id} (load: {self.current_work}/{self.capacity})")
        
        # Process the reading (outside the lock so we don't block others)
        self.do_processing(reading)
        
        # Mark as finished
        with self.lock:
            self.current_work -= 1
            print(f"Reading {reading['sensor_id']} <- Agg{self.id} (load: {self.current_work}/{self.capacity})")
        
        return True
    
    def do_processing(self, reading):
        """Actually process the reading"""
        print(f"Agg{self.id} working on reading {reading['sensor_id']}")
        time.sleep(reading['proc_time'])
        print(f"Agg{self.id} done with reading {reading['sensor_id']}")

# Create smart aggregators with capacity limits
smart_aggs = [SmartAggregator(i, MAX_CAPACITY) for i in range(NUM_AGGS)]

def find_home_for_reading(reading, aggregators):
    """Keep trying to find an aggregator that can take this reading"""
    assigned = False
    attempts = 0
    
    while not assigned:
        for agg in aggregators:
            if agg.can_take_more():
                assigned = agg.assign_reading(reading)
                if assigned:
                    break  # Found one!
        
        # If still not assigned, all aggregators are full
        if not assigned:
            attempts += 1
            if attempts % 10 == 0:  # Print message every 10 attempts
                print(f"Reading {reading['sensor_id']} waiting for free aggregator...")
            time.sleep(0.01)  # Don't spam the CPU

# Start the advanced simulation
start_time_adv = time.time()
threads_adv = []

print(f"\nStarting to process {NUM_READINGS} readings with {NUM_AGGS} aggregators...")

# Create a thread for each reading
for reading in readings_list:
    t = threading.Thread(target=find_home_for_reading, args=(reading, smart_aggs))
    threads_adv.append(t)
    t.start()

# Wait for all to finish
for t in threads_adv:
    t.join()

end_time_adv = time.time()
print(f"\nAll advanced processing done in {end_time_adv - start_time_adv:.2f} seconds")



# QUESTION 1.5 B - Simulation and Discussion
# Simulation of 50 sensor readings with 5 aggregators (capacity: 2 each)

import threading
import time
import random

# Settings for the simulation
num_sensors = 50
num_aggregators = 5
max_capacity = 2  # Each aggregator can handle 2 at once

class Aggregator:
    def __init__(self, agg_id):
        self.id = agg_id
        self.current = 0  # Current number of readings being processed
        self.lock = threading.Lock()  # For thread safety - QUESTION 1.2 B
        print(f"Aggregator {self.id} ready (max: {max_capacity})")
    
    def has_space(self):
        # Check if this aggregator can take more work
        with self.lock:
            return self.current < max_capacity
    
    def process(self, reading_id, proc_time):
        # Start processing a reading - QUESTION 1.3 C (capacity limits)
        with self.lock:
            self.current += 1
            print(f"Reading {reading_id} -> Aggregator {self.id} ({self.current}/{max_capacity})")
        
        # Simulate the actual work
        time.sleep(proc_time)
        
        # Finish processing
        with self.lock:
            self.current -= 1
            print(f"Reading {reading_id} <- Aggregator {self.id} ({self.current}/{max_capacity})")

def handle_sensor_reading(reading_id):
    # Time this reading takes to process
    processing_time = random.uniform(0.1, 0.3)
    got_spot = False
    
    # Keep trying until we find an aggregator with space
    while not got_spot:
        for agg in all_aggregators:
            if agg.has_space():
                agg.process(reading_id, processing_time)
                got_spot = True
                break
        
        # If all aggregators are full, wait a bit
        if not got_spot:
            print(f"Reading {reading_id} waiting...")
            time.sleep(0.01)


# MAIN SIMULATION CODE - QUESTION 1.5 B

print("=== QUESTION 1.5 B - Sensor Aggregation Simulation ===")
print(f"Sensors: {num_sensors}, Aggregators: {num_aggregators}, Capacity: {max_capacity}")
print()

# Create all aggregators
all_aggregators = []
for i in range(num_aggregators):
    all_aggregators.append(Aggregator(i))

print("\nStarting to process readings...")
start = time.time()

# Create threads for each sensor reading
thread_list = []
for sensor_id in range(num_sensors):
    thread = threading.Thread(target=handle_sensor_reading, args=(sensor_id,))
    thread_list.append(thread)
    thread.start()

# Wait for all threads to finish
for t in thread_list:
    t.join()

end = time.time()
print(f"\nDone! All {num_sensors} readings processed in {end-start:.1f} seconds")
print("\n=== Simulation Complete ===")










# QUESTION 2.1
import abc
from typing import List


# OBSERVER PATTERN - For notifying users about task changes

    class User:
    """Observer class - users who want to get notified about their tasks"""
    def __init__(self, name: str):
        self.name = name
    
    def update(self, task, old_status: str, new_status: str):
        """Called when a task's status changes"""
        print(f"[{self.name}] Notification: Task '{task.title}' changed from '{old_status}' to '{new_status}'")


# FACTORY METHOD PATTERN - For creating different types of tasks

class Task(abc.ABC):
    """Abstract base class for all tasks"""
    def __init__(self, title: str, assignee: User = None):
        self.title = title
        self.assignee = assignee
        self.status = "Not Started"
        self.observers: List[User] = []
        
        if assignee:
            self.add_observer(assignee)
    
    def add_observer(self, user: User):
        """Add a user to be notified of changes"""
        if user not in self.observers:
            self.observers.append(user)
    
    def remove_observer(self, user: User):
        """Remove a user from notifications"""
        if user in self.observers:
            self.observers.remove(user)
    
    def set_status(self, new_status: str):
        """Update task status and notify observers"""
        old_status = self.status
        self.status = new_status
        self._notify_observers(old_status, new_status)
    
    def _notify_observers(self, old_status: str, new_status: str):
        """Notify all observers about the status change"""
        for user in self.observers:
            user.update(self, old_status, new_status)
    
    @abc.abstractmethod
    def get_type(self) -> str:
        """Return the type of task"""
        pass

class DesignTask(Task):
    """Concrete product - Design Task"""
    def get_type(self) -> str:
        return "Design"

class ReviewTask(Task):
    """Concrete product - Review Task"""
    def get_type(self) -> str:
        return "Review"

class DeploymentTask(Task):
    """Concrete product - Deployment Task"""
    def get_type(self) -> str:
        return "Deployment"

class TaskFactory:
    """Factory class for creating tasks"""
    @staticmethod
    def create_task(task_type: str, title: str, assignee: User = None) -> Task:
        if task_type.lower() == "design":
            return DesignTask(title, assignee)
        elif task_type.lower() == "review":
            return ReviewTask(title, assignee)
        elif task_type.lower() == "deployment":
            return DeploymentTask(title, assignee)
        else:
            raise ValueError(f"Unknown task type: {task_type}")


# SINGLETON PATTERN - Only one TaskManager instance

class TaskManager:
    """Singleton class to manage all tasks in the system"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskManager, cls).__new__(cls)
            cls._instance.tasks = []
        return cls._instance
    
    def create_task(self, task_type: str, title: str, assignee: User = None) -> Task:
        """Create a new task using the factory"""
        task = TaskFactory.create_task(task_type, title, assignee)
        self.tasks.append(task)
        print(f"Created {task.get_type()} task: '{title}' assigned to {assignee.name if assignee else 'Nobody'}")
        return task
    
    def change_task_status(self, task_title: str, new_status: str):
        """Change the status of a task"""
        for task in self.tasks:
            if task.title == task_title:
                task.set_status(new_status)
                return True
        print(f"Task '{task_title}' not found")
        return False
    
    def list_tasks(self):
        """Display all tasks in the system"""
        print("\n=== ALL TASKS ===")
        for task in self.tasks:
            assignee_name = task.assignee.name if task.assignee else "Unassigned"
            print(f"• {task.get_type()}: '{task.title}' - {assignee_name} - Status: {task.status}")
        print()


# MAIN DEMONSTRATION CODE - QUESTION 2.1

def main():
    print("=== TASK MANAGEMENT SYSTEM DEMONSTRATION ===")
    print()
    
    # Create users
    jordan = User("Jordan")
    taylor = User("Taylor")
    alex = User("Alex")
    
    print("Created users: Jordan, Taylor, Alex")
    print()
    
    # Get the singleton TaskManager instance
    task_manager = TaskManager()
    
    # Create tasks using Factory Method Pattern
    print("--- Creating Tasks ---")
    task1 = task_manager.create_task("design", "Design new logo", jordan)
    task2 = task_manager.create_task("review", "Review website layout", taylor)
    task3 = task_manager.create_task("deployment", "Deploy to production", alex)
    task4 = task_manager.create_task("design", "Design business cards", jordan)  # Another task for Jordan
    
    print()
    
    # Show all tasks
    task_manager.list_tasks()
    
    # Change task statuses to demonstrate Observer Pattern
    print("--- Updating Task Statuses ---")
    task_manager.change_task_status("Design new logo", "In Progress")
    print()
    task_manager.change_task_status("Review website layout", "Completed")
    print()
    task_manager.change_task_status("Deploy to production", "In Progress")
    print()
    task_manager.change_task_status("Design new logo", "Completed")
    print()
    task_manager.change_task_status("Design business cards", "In Progress")
    
    print()
    
    # Show final state of all tasks
    task_manager.list_tasks()
    print("=== DEMONSTRATION COMPLETE ===")

if __name__ == "__main__":
    main()
    





    # QUESTIONS 3.3 
    import logging
import os

class StudentMicroservice:
    def __init__(self):
        self.students = {}  # Dictionary to store students
        self._setup_logging()
        logging.info("Microservice started - ready to accept commands")
    
    def _setup_logging(self):
        """Setup logging that won't crash with permission errors"""
        try:
            # Try to create log file in current directory
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler("student_service.log"),
                    logging.StreamHandler()
                ]
            )
        except PermissionError:
            # If we can't write to file, just use console logging
            print("Note: Cannot create log file (permission denied). Using console logging only.")
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[logging.StreamHandler()]
            )
        except Exception as e:
            # Any other error, just use basic console logging
            print(f"Note: Logging setup failed: {e}. Using console logging only.")
            logging.basicConfig(
                level=logging.INFO,
                format='%(levelname)s - %(message)s'
            )
    
    def add_student(self, student_id, name, course):
        """Add a new student to the system"""
        if student_id in self.students:
            logging.warning(f"Failed to add {student_id}: ID already exists")
            print("Error: Student ID already exists!")
            return False
        
        self.students[student_id] = {
            'name': name,
            'course': course
        }
        logging.info(f"Added student: {student_id} - {name} ({course})")
        print(f"Success: Added {name} to {course}")
        return True
    
    def get_student(self, student_id):
        """Get student details by ID"""
        if student_id in self.students:
            student = self.students[student_id]
            logging.info(f"Retrieved student: {student_id}")
            return student
        else:
            logging.warning(f"Student not found: {student_id}")
            return None
    
    def list_students(self):
        """List all registered students"""
        logging.info("Listing all students")
        return self.students
    
    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("STUDENT MANAGEMENT MICROSERVICE")
        print("="*50)
        print("1. Add a new student")
        print("2. Find a student by ID")
        print("3. List all students")
        print("4. Exit")
        print("="*50)

def main():
    # Create the microservice instance
    service = StudentMicroservice()
    
    # Add the sample data required by the assignment
    print("Loading sample data...")
    service.add_student("ST100", "Michael Smith", "Data Science")
    service.add_student("ST101", "Emma Johnson", "Cyber security")
    print("Sample data loaded successfully!")
    
    while True:
        # Show the menu
        service.show_menu()
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                print("\n--- ADD NEW STUDENT ---")
                student_id = input("Enter student ID: ").strip()
                name = input("Enter student name: ").strip()
                course = input("Enter course: ").strip()
                
                if student_id and name and course:
                    service.add_student(student_id, name, course)
                else:
                    print("Error: All fields are required!")
                    logging.warning("Attempted to add student with missing fields")
            
            elif choice == "2":
                print("\n--- FIND STUDENT ---")
                student_id = input("Enter student ID: ").strip()
                
                student = service.get_student(student_id)
                if student:
                    print(f"\nStudent Found:")
                    print(f"ID: {student_id}")
                    print(f"Name: {student['name']}")
                    print(f"Course: {student['course']}")
                else:
                    print("Error: Student not found!")
            
            elif choice == "3":
                print("\n--- ALL STUDENTS ---")
                all_students = service.list_students()
                
                if all_students:
                    print(f"Total students: {len(all_students)}")
                    print("-" * 40)
                    for sid, info in all_students.items():
                        print(f"ID: {sid}")
                        print(f"Name: {info['name']}")
                        print(f"Course: {info['course']}")
                        print("-" * 40)
                else:
                    print("No students registered yet.")
            
            elif choice == "4":
                print("Shutting down microservice...")
                logging.info("Microservice stopped by user")
                break
            
            else:
                print("Invalid choice! Please enter 1-4.")
                logging.warning(f"Invalid menu choice: {choice}")
        
        except KeyboardInterrupt:
            print("\n\nMicroservice interrupted by user")
            logging.warning("Microservice interrupted unexpectedly")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"Error in microservice: {e}")

if __name__ == "__main__":
    print("Starting Student Management Microservice...")
    main()




