import tkinter as tk
import random
import scrumdog_queue
import Student_Class
import Database3


class Scrum_Gui:
    def __init__(self, window):
        self.window = window
        self.window.title("Scrumdog Gui")
        self.window.geometry("520x250")
        self.window.resizable(False, False)

        # Frame for the entry boxes
        entry_frame = tk.Frame(window)
        entry_frame.pack(pady=10)

        # Number of students entry box
        tk.Label(entry_frame, text="Number of Students:").grid(row=0, column=0, padx=5)
        self.keyword1_entry = tk.Entry(entry_frame, width=15)
        self.keyword1_entry.grid(row=0, column=1, padx=5)

        # Speed of cars entry box
        tk.Label(entry_frame, text="Speed of Cars:").grid(row=0, column=2, padx=5)
        self.keyword2_entry = tk.Entry(entry_frame, width=15)
        self.keyword2_entry.grid(row=0, column=3, padx=5)

        # Time of sign display entry box
        tk.Label(entry_frame, text="Time of Sign Display:").grid(row=1, column=0, padx=5)
        self.keyword3_entry = tk.Entry(entry_frame, width=15)
        self.keyword3_entry.grid(row=1, column=1, padx=5)

        # Number of signs to display entry box
        tk.Label(entry_frame, text="# of Signs to Display:").grid(row=1, column=2, padx=5)
        self.keyword4_entry = tk.Entry(entry_frame, width=15)
        self.keyword4_entry.grid(row=1, column=3, padx=5)

        # Display Results
        self.results = tk.Text(window, height=7, width=60)
        self.results.pack(padx=5, pady=5)

        # Submit button
        self.submit_button = tk.Button(window, text="Submit", width=20, command=self.submit)
        self.submit_button.pack(pady=10)

    def submit(self):
        try:
            # Collect data from the entry fields
            num_students = int(self.keyword1_entry.get())
            # speed_of_cars = float(self.keyword2_entry.get())
            sign_display_time = float(self.keyword3_entry.get())
            num_signs = int(self.keyword4_entry.get())

            # Create a list of students using random selection from the student types
            student_classes = [Student_Class.OneDayStudent, Student_Class.TwoDayStudent, Student_Class.ThreeDayStudent,
                               Student_Class.FourDayStudent, Student_Class.FiveDayStudent]
            students = [random.choice(student_classes)(i) for i in range(1, num_students + 1)]

            # Create the Circular Linked List for signs
            signs = scrumdog_queue.CircularLinkedList(random_sign_order=True)
            for i in range(1, num_signs + 1):
                signs.append(i, sign_display_time)  # Adding signs with display times
            signs.finalize_signs()  # Shuffle the signs if required

            # Process the students and their interaction with the signs
            sign_system = scrumdog_queue.SignProcessingSystem(students, signs, random_sign_order=True)
            results = sign_system.process_students_for_week()

            # Save the results to a CSV file using Database3.py
            db = Database3.Database('test.csv')
            db.excel(results)

            # Get the averages of time each sign was seen
            averages = db.averages(1)  # You can change the number here if you want averages for a number of days

            # Prepare the averages output
            averages_output = "Average Time Each Sign Was Seen (in seconds):\n"
            for avg in averages:
                averages_output += f"Sign {avg['Sign']}: {avg['Average_Seconds_Seen']} sec\n"

            # Display the averages in the text area
            self.results.delete(1.0, tk.END)  # Clear the previous results
            self.results.insert(tk.END, averages_output)

        except Exception as e:
            # Print error message in the results box in case of any issues
            self.results.delete(1.0, tk.END)  # Clear the previous results
            self.results.insert(tk.END, f"An error occurred: {e}\n")


if __name__ == "__main__":
    try:
        # Initialize and run the GUI
        window = tk.Tk()
        gui = Scrum_Gui(window)
        window.mainloop()
    except Exception as e:
        print(f"An error occurred while initializing the GUI: {e}")
