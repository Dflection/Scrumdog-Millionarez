import random
from queue import Queue
from Student_Class import OneDayStudent, TwoDayStudent, ThreeDayStudent, FourDayStudent, FiveDayStudent


class CircularLinkedList:
    """
    A circular linked list to manage and rotate signs in the simulation.

    Attributes:
        items (list): List of Sign objects representing signs displayed to students.
        current_index (int): Tracks the current sign being displayed in the rotation.
        random_sign_order (bool): Determines whether the order of signs should be randomized.
    """
    def __init__(self, random_sign_order=False):
        self.items = []
        self.current_index = 0
        self.random_sign_order = random_sign_order

    def append(self, index, time):
        """
        Adds a new sign to the circular linked list.

        Args:
            index (int): Unique identifier for the sign.
            time (float): Duration the sign remains visible before rotation.
        """
        self.items.append(Sign(index, time))

    def finalize_signs(self):
        """
        Finalizes the list of signs, shuffling their order if random_sign_order is enabled.
        This ensures that students see signs in a different order each simulation run if set to True.
        """
        if self.random_sign_order:
            random.shuffle(self.items)

    def get_current_item(self):
        """
        Retrieves the current sign being displayed.

        Returns:
            Sign: The current sign object or None if there are no signs.
        """
        if self.items:
            return self.items[self.current_index]
        return None

    def rotate(self):
        """
        Rotates to the next sign in the circular linked list.
        This allows students to see a new sign after a certain duration.
        """
        if self.items:
            self.current_index = (self.current_index + 1) % len(self.items)


class Sign:
    """
    Represents a sign with an index and display time.

    Attributes:
        index (int): Identifier for the sign.
        time (float): The amount of time the sign is visible before switching to the next.
    """
    def __init__(self, index, time):
        self.index = index
        self.time = time


class SignProcessingSystem:
    """
    Manages student interactions with signs and tracks viewership data.

    Attributes:
        students (list): List of student objects who will view the signs.
        signs (CircularLinkedList): Circular linked list containing Sign objects.
        total_signs (int): Total number of signs in the system.
    """
    def __init__(self, students, signs, random_sign_order=False):
        self.students = students
        self.signs = signs
        self.total_signs = len(signs.items)
        if random_sign_order:
            self.signs.finalize_signs()
        self.initialize_viewership_stats()

    def initialize_viewership_stats(self):
        """
        Initializes each student's viewership statistics for up to 20 signs.
        Each student's stats start at zero for all signs.
        """
        for student in self.students:
            student.viewership_stats = {i: 0 for i in range(1, 21)}

    def process_queue_and_signs(self, student_queue):
        """
        Processes students as they view signs and records their interactions.
        //TODO fix duplication issue probably here

        Args:
            student_queue (Queue): Queue of students waiting to view signs.

        Returns:
            list: A list of dictionaries containing student details and viewership data.
        """
        results = []

        while not student_queue.empty():
            student = student_queue.get()
            student_time_remaining = student.time

            while student_time_remaining > 0:
                current_sign = self.signs.get_current_item()
                if not current_sign:
                    break

                if current_sign.time > student_time_remaining:
                    # Partial view of the sign
                    current_sign.time -= student_time_remaining
                    student.viewership_stats[current_sign.index] += student_time_remaining
                    student_time_remaining = 0
                else:
                    # Full view of the sign before moving to next
                    student_time_remaining -= current_sign.time
                    student.viewership_stats[current_sign.index] += current_sign.time
                    self.signs.rotate()

            # Store student viewership data
            student_data = {
                "student_id": student.identifier,
                "speed": student.speed,
                "view_time": student.time,
                "days_attended": student.attendance_days,
            }

            # Record viewing time for up to 20 signs
            for i in range(1, 21):
                student_data[f"sign{i}"] = round(student.viewership_stats.get(i, 0), 2)

            results.append(student_data)

        return results

    def process_students_for_week(self):
        """
        Processes students for each day of the week and compiles the viewership results.

        Returns:
            list: Aggregated list of dictionaries containing viewership data for the week.
        """
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        weekly_results = []

        for day in days_of_week:
            daily_queue = Queue()
            for student in self.students:
                if day in student.attendance_days:
                    daily_queue.put(student)

            daily_results = self.process_queue_and_signs(daily_queue)
            weekly_results.extend(daily_results)

        return weekly_results

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
            print(f"Speed: {student_data['speed']:.2f}")
            print(f"View Time: {student_data['view_time']:.2f}")
            print(f"Days Attended: {', '.join(student_data['days_attended'])}")
            print("Sign Viewership:")
            for i in range(1, 21):
                if student_data[f"sign{i}"] > 0:
                    print(f"  Sign {i}: {student_data[f'sign{i}']:.2f} sec")
            print("=" * 40, "\n")


if __name__ == "__main__":
    # Create circular linked list of signs
    signs = CircularLinkedList(random_sign_order=True)
    for i in range(1, 7):
        signs.append(i, 5)
    signs.finalize_signs()

    # Generate a list of students with randomized types and viewing times
    student_classes = [OneDayStudent, TwoDayStudent, ThreeDayStudent, FourDayStudent, FiveDayStudent]
    students = [
        random.choice(student_classes)(i, time=random.uniform(0.75, 1.25))
        for i in range(1, 20)
    ]

    # Initialize and process the sign system
    sign_system = SignProcessingSystem(students, signs, random_sign_order=True)
    results = sign_system.process_students_for_week()
    sign_system.print_results(results)
