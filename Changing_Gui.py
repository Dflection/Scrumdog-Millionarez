import tkinter as tk
import os
from PIL import Image, ImageTk
import random
import scrumdog_queue
import Student_Class
import Database3
from random import randint

class ScrumGui:
    # Creates Gui
    def __init__(self, window):
        self.window = window
        self.window.title("Columbia College Sign Statistics Calculator")
        self.window.geometry("700x700")
        self.window.resizable(False, False)
        # External callback for processing data, help from AI with this
        

        # Create and resize background photo
        directory_path = os.path.dirname(__file__)
        original_img = Image.open(os.path.join(directory_path, "red2.png"))
        resized_image = original_img.resize((700, 700))
        self.new_image = ImageTk.PhotoImage(resized_image)
        self.background_label = tk.Label(window, image=self.new_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Frame for the entry boxes
        entry_frame = tk.Frame(window)
        entry_frame.pack(pady=10)

        # Create an instance of the UserValidation class
        # self.validator = UserValidation()

        # Number of Students entry box
        tk.Label(entry_frame, text="Number of Students:").grid(row=0, column=0, padx=5)
        self.student_entry = tk.Entry(entry_frame, width=15)
        self.student_entry.grid(row=0, column=1, padx=5)

        # Speed of Cars entry box
        tk.Label(entry_frame, text="Car Speed:").grid(row=0, column=2, padx=5)
        self.car_speed_entry = tk.Entry(entry_frame, width=15)
        self.car_speed_entry.grid(row=0, column=3, padx=5)

        # Time of Sign Display entry box
        tk.Label(entry_frame, text="Time of Sign Display:").grid(row=1, column=0, padx=5)
        self.sign_entry = tk.Entry(entry_frame, width=15)
        self.sign_entry.grid(row=1, column=1, padx=5)

        # Number of Signs to Display entry box
        tk.Label(entry_frame, text="# of Signs to Display:").grid(row=1, column=2, padx=5)
        self.sign_time_entry = tk.Entry(entry_frame, width=15)
        self.sign_time_entry.grid(row=1, column=3, padx=5)

        # Single results display box
        self.results = tk.Text(window, height=20, width=80)  # Increased height to fit all data
        self.results.pack(padx=5, pady=5)

        # Submit button
        self.submit_button = tk.Button(window, text="Submit", width=20, command=self.submit)
        self.submit_button.pack(pady=10)


    # Function for submit button to collect data into a dictionary, also has user validation
    def submit(self):
        try:
            # Collect and validate input
            num_students = int(self.student_entry.get())
            num_students = num_students if num_students < 51 else randint(20, 49)
            sign_display_time = float(self.sign_entry.get())
            num_signs = int(self.sign_time_entry.get())

            # Create student instances
            student_classes = [
                Student_Class.OneDayStudent, Student_Class.TwoDayStudent,
                Student_Class.ThreeDayStudent, Student_Class.FourDayStudent,
                Student_Class.FiveDayStudent
            ]
            students = [random.choice(student_classes)(i) for i in range(1, num_students + 1)]

            # Create Circular Linked List for signs
            signs = scrumdog_queue.CircularLinkedList(random_sign_order=True)
            for i in range(1, num_signs + 2):
                signs.append(i, sign_display_time)
            signs.finalize_signs()

            # Process students with signs
            sign_system = scrumdog_queue.SignProcessingSystem(students, signs, random_sign_order=True)
            results = sign_system.process_students_for_week()

            # Save results to CSV
            db = Database3.Database('test.csv')
            db.excel(results)

            # Compute averages and percentages for each student type
            final_output = ""

            for days in range(1, 6):
                avg_times = db.averages(days, num_signs)
                percentage = db.percentages(days, num_signs)

                final_output += f"\n{percentage}% of the signs were seen by {days}-day students.\n"
                final_output += "\n" + "-" * 50  # Separator for readability

            # Display all results in one text widget
            self.results.delete(1.0, tk.END)
            self.results.insert(tk.END, final_output)

        except Exception as e:
            # Handle errors gracefully in the same single results box
            self.results.delete(1.0, tk.END)
            self.results.insert(tk.END, f"An error occurred: {e}\n")


# If this module is run as a script, launch the GUI.
if __name__ == "__main__":
    root = tk.Tk()
    app = ScrumGui(root)
    root.mainloop()
