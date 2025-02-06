import random
from queue import Queue
from Student_Class import OneDayStudent, TwoDayStudent, ThreeDayStudent, FourDayStudent, FiveDayStudent
import Database3


class CircularLinkedList:
    """
    A circular linked list to manage and rotate signs in the simulation.

    Attributes:
        items (list): List of Sign objects representing signs displayed to students.
        current_index (int): Tracks the current sign being displayed in the rotation.
        random_sign_order (bool): Determines whether the order of signs should be randomized.
    """
    def __init__(self, random_sign_order=False):
        self.items = []  # List to hold the Sign objects
        self.current_index = 0  # Index to track the current sign being displayed
        self.random_sign_order = random_sign_order  # Flag to shuffle signs if set to True

    def append(self, index, time):
        """
        Adds a new sign to the circular linked list.

        Args:
            index (int): Unique identifier for the sign.
            time (float): Duration the sign remains visible before rotation.
        """
        self.items.append(Sign(index, time))  # Append a new Sign object to the list

    def finalize_signs(self):
        """
        Finalizes the list of signs, shuffling their order if random_sign_order is enabled.
        This ensures that students see signs in a different order each simulation run if set to True.
        """
        if self.random_sign_order:
            random.shuffle(self.items)  # Shuffle the signs if random order is enabled

    def get_current_item(self):
        """
        Retrieves the current sign being displayed.

        Returns:
            Sign: The current sign object or None if there are no signs.
        """
        if self.items:
            return self.items[self.current_index]  # Return the current sign being displayed
        return None

    def rotate(self):
        """
        Rotates to the next sign in the circular linked list.
        This allows students to see a new sign after a certain duration.
        """
        if self.items:
            self.current_index = (self.current_index + 1) % len(self.items)  # Rotate to the next sign


class Sign:
    """
    Represents a sign with an index and display time.

    Attributes:
        index (int): Identifier for the sign.
        time (float): The amount of time the sign is visible before switching to the next.
    """
    def __init__(self, index, time):
        self.index = index  # Set the sign's index
        self.time = time  # Set the time for which the sign is displayed


class SignProcessingSystem:
    """
    Manages student interactions with signs and tracks viewership data.

    Attributes:
        students (list): List of student objects who will view the signs.
        signs (CircularLinkedList): Circular linked list containing Sign objects.
        total_signs (int): Total number of signs in the system.
    """
    def __init__(self, students, signs, random_sign_order=False):
        self.students = students  # List of students viewing the signs
        self.signs = signs  # Circular linked list of signs
        self.total_signs = len(signs.items)  # Total number of signs available
        if random_sign_order:
            self.signs.finalize_signs()  # Finalize and shuffle signs if random order is set
        self.initialize_viewership_stats()  # Initialize the stats for student interactions with signs

    def initialize_viewership_stats(self):
        """
        Initializes each student's viewership statistics for up to 20 signs.
        Each student's stats start at zero for all signs.
        """
        for student in self.students:
            student.viewership_stats = {i: 0 for i in range(1, 21)}  # Initialize viewership for each sign

    def process_queue_and_signs(self, student_queue):
        """
        Processes students as they view signs and records their interactions.

        Args:
            student_queue (Queue): Queue of students waiting to view signs.

        Returns:
            list: A list of dictionaries containing student details and viewership data.
        """
        results = []  # List to store results of each student's interaction with signs

        while not student_queue.empty():
            student = student_queue.get()  # Get the student from the queue
            student_time_remaining = student.time  # The time the student will interact with the signs

            while student_time_remaining > 0:
                current_sign = self.signs.get_current_item()  # Get the current sign being displayed
                if not current_sign:
                    break  # Break if no sign is available

                if current_sign.time > student_time_remaining:
                    # Student can view part of the sign before time runs out
                    current_sign.time -= student_time_remaining  # Reduce the sign's remaining time
                    student.viewership_stats[current_sign.index] += student_time_remaining  # Update student stats
                    student_time_remaining = 0  # The student is done viewing
                else:
                    # Student can fully view the sign and move on to the next
                    student_time_remaining -= current_sign.time  # Deduct the time spent on the current sign
                    student.viewership_stats[current_sign.index] += current_sign.time  # Update stats
                    self.signs.rotate()  # Move to the next sign

            # Store student viewership data
            student_data = {
                "student_id": student.identifier,  # Student identifier
                "speed": student.speed,  # Student's speed (how fast they view signs)
                "view_time": student.time,  # Total time the student interacts with signs
                "num_days_attended": len(student.attendance_days),  # Number of days the student attended
                "days_attended": student.attendance_days,  # Days the student attended class
            }

            # Record viewing time for up to 20 signs
            for i in range(1, 21):
                # Round the view time to 2 decimals
                student_data[f"sign{i}"] = round(student.viewership_stats.get(i, 0), 2)

            # Check if student data already exists in results (based on student_id)
            existing_student = next((data for data in results if data['student_id'] == student.identifier), None)
            if existing_student:
                # Update the existing student data with the latest data
                existing_student.update(student_data)
            else:
                # If not found, add the new student data
                results.append(student_data)

        return results  # Return the processed results

    def process_students_for_week(self):
        """
        Processes students for each day of the week and compiles the viewership results.

        Returns:
            list: Aggregated list of dictionaries containing viewership data for the week.
        """
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]  # Days of the week
        weekly_results = []  # List to store weekly results

        for day in days_of_week:
            daily_queue = Queue()  # Queue to hold students for the current day
            for student in self.students:
                if day in student.attendance_days:  # Check if the student attended on this day
                    daily_queue.put(student)  # Add the student to the daily queue

            daily_results = self.process_queue_and_signs(daily_queue)  # Process the daily queue
            weekly_results.extend(daily_results)  # Add daily results to the weekly results

        return weekly_results  # Return the aggregated results for the week

    def print_results(self, results):
        """
        Prints the processed results in a structured format.

        Args:
            results (list): List of student viewership data dictionaries.
        """
        print("Raw Data Output:")
        print(results)  # Print raw dictionary output first for diagnostics
        print("\nFormatted Output:")

        for student_data in results:
            print("=" * 40)
            print(f"Student ID: {student_data['student_id']}")
            print(f"Speed: {student_data['speed']:.2f}")  # Display student speed
            print(f"View Time: {student_data['view_time']:.2f}")  # Display student view time
            print(f"Number of Days Attended: {student_data['num_days_attended']}")  # Display number of days attended
            print(f"Days Attended: {', '.join(student_data['days_attended'])}")  # List of days attended
            print("Sign Viewership:")
            for i in range(1, 21):
                if student_data[f"sign{i}"] > 0:
                    print(f"  Sign {i}: {student_data[f'sign{i}']:.2f} sec")  # Display time spent on each sign
            print("=" * 40, "\n")


if __name__ == "__main__":
    # Create circular linked list of signs
    signs = CircularLinkedList(random_sign_order=True)
    for i in range(1, 7):
        signs.append(i, 5)  # Add 6 signs, each with a display time of 5 seconds
    signs.finalize_signs()  # Finalize the sign list (shuffle if random order is enabled)

    # Generate a list of students with randomized types and viewing times
    student_classes = [OneDayStudent, TwoDayStudent, ThreeDayStudent, FourDayStudent, FiveDayStudent]
    students = [
        random.choice(student_classes)(i, time=random.uniform(0.75, 1.25))  # Create students with random attributes
        for i in range(1, 20)
    ]

    # Initialize and process the sign system
    sign_system = SignProcessingSystem(students, signs, random_sign_order=True)
    results = sign_system.process_students_for_week()  # Process students and signs for the week
    sign_system.print_results(results)  # Print the results of the simulation

    test_csv_maker = Database3.Database('test.csv')
    test_csv_maker.excel(results)
    test_csv_maker.averages(1)
