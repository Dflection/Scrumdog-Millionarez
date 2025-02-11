import random
from queue import Queue
from Student_Class import OneDayStudent, TwoDayStudent, ThreeDayStudent, FourDayStudent, FiveDayStudent
import Database3


class CircularLinkedList:
    """A circular linked list to manage and rotate signs in the simulation."""
    
    def __init__(self, random_sign_order=False):
        self.items = []
        self.current_index = 0
        self.random_sign_order = random_sign_order

    def append(self, index, time):
        """Adds a new sign to the list."""
        self.items.append(Sign(index, time))

    def finalize_signs(self):
        """Randomizes sign order if enabled."""
        if self.random_sign_order:
            random.shuffle(self.items)

    def get_current_item(self):
        """Retrieves the current sign being displayed."""
        if self.items:
            return self.items[self.current_index]
        return None

    def rotate(self):
        """Moves to the next sign in the list."""
        if self.items:
            self.current_index = (self.current_index + 1) % len(self.items)


class Sign:
    """Represents a sign with an index and display time."""
    
    def __init__(self, index, time):
        self.index = index
        self.time = time


class SignProcessingSystem:
    """Manages student interactions with signs and tracks viewership data."""
    
    def __init__(self, students, signs, random_sign_order=False):
        self.students = students
        self.signs = signs
        self.total_signs = len(signs.items)
        if random_sign_order:
            self.signs.finalize_signs()
        self.initialize_viewership_stats()

    def initialize_viewership_stats(self):
        """Initializes each student's viewership statistics for up to 20 signs."""
        for student in self.students:
            student.viewership_stats = {i: 0 for i in range(1, 21)}
            student.unique_signs_seen = set()  # Track unique signs seen

    def process_queue_and_signs(self, student_queue):
        """Processes students as they view signs and records interactions."""
        results = []

        while not student_queue.empty():
            student = student_queue.get()
            student_time_remaining = student.time  # Total time student has to view signs

            while student_time_remaining > 0:
                current_sign = self.signs.get_current_item()
                if not current_sign:
                    break

                if current_sign.time > student_time_remaining:
                    # Partial sign view
                    view_time = student_time_remaining
                    current_sign.time -= student_time_remaining
                    student_time_remaining = 0
                else:
                    # Full sign view
                    view_time = current_sign.time
                    student_time_remaining -= current_sign.time
                    self.signs.rotate()  # Move to next sign **only after sufficient view time**

                # ✅ Only record the sign if it was viewed for at least 0.25 seconds
                if view_time >= 0.25 and current_sign.index not in student.unique_signs_seen:
                    student.viewership_stats[current_sign.index] += round(view_time, 2)
                    student.unique_signs_seen.add(current_sign.index)  # Mark sign as seen

            # Store student viewership data
            student_data = {
                "student_id": student.identifier,
                "speed": student.speed,
                "view_time": student.time,
                "num_days_attended": len(student.attendance_days),
                "days_attended": student.attendance_days,
            }

            # Store viewing time per sign
            for i in range(1, self.total_signs + 1):
                student_data[f"sign{i}"] = round(student.viewership_stats.get(i, 0), 2)

            results.append(student_data)

        return results

    def process_students_for_week(self):
        """Processes students for the entire week and compiles viewership data."""
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        weekly_results = []
        final_results = []

        for day in days_of_week:
            daily_queue = Queue()

            # Add students who attended that day to the queue
            for student in self.students:
                if day in student.attendance_days:
                    daily_queue.put(student)

            daily_results = self.process_queue_and_signs(daily_queue)
            weekly_results.extend(daily_results)

            for item in weekly_results:
                # Check if student already exists in final results
                existing_item = next(
                    (entry for entry in final_results if int(entry['student_id']) == int(item['student_id'])), None
                )

                if existing_item:
                    # Accumulate sign viewing times across multiple days
                    for key in item:
                        if key.startswith("sign") and key in existing_item:
                            existing_item[key] += item[key]
                else:
                    final_results.append(item)

        final_results.sort(key=lambda x: int(x['student_id']))
        return final_results
