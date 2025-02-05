import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import random
import scrumdog_queue
import Student_Class
import Database3

class ScrumGui:
    # Creates Gui
    def __init__(self, window, on_submit=None):
        self.window = window
        self.window.title("Columbia College Sign Statistics Calculator")
        self.window.geometry("1000x1000")
        self.window.resizable(False, False)
        # External callback for processing data, help from AI with this
        self.on_submit = on_submit

        # Create and resize background photo
        directory_path = os.path.dirname(__file__)
        original_img = Image.open(os.path.join(directory_path, "mkweenie.png"))
        resized_image = original_img.resize((520, 250))
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

        # Display Results of 1 day students
        self.results1 = tk.Text(window, height=6, width=60)
        self.results1.pack(padx=5, pady=5)

        # Display Results of 2 day students
        self.results2 = tk.Text(window, height=6, width=60)
        self.results2.pack(padx=5, pady=5)

        # Display Results of 3 day students
        self.results3 = tk.Text(window, height=6, width=60)
        self.results3.pack(padx=5, pady=5)

        # Display Results of 4 day students
        self.results4 = tk.Text(window, height=6, width=60)
        self.results4.pack(padx=5, pady=5)

        # Display Results of 5 day students
        self.results5 = tk.Text(window, height=6, width=60)
        self.results5.pack(padx=5, pady=5)

        # Submit button
        self.submit_button = tk.Button(window, text="Submit", width=20, command=self.submit)
        self.submit_button.pack(pady=10)

    # Function for submit button to collect data into a dictionary, also has user validation


    def submit(self):
        try:
            # Collect data from the entry fields
            num_students = int(self.student_entry.get())
            # speed_of_cars = float(self.keyword2_entry.get())
            sign_display_time = float(self.sign_entry.get())
            num_signs = int(self.sign_time_entry.get())

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
            averages1 = db.averages(1)  # You can change the number here if you want averages for a number of days

             # Get the averages of time each sign was seen
            averages2 = db.averages(2)  # You can change the number here if you want averages for a number of days

             # Get the averages of time each sign was seen
            averages3 = db.averages(3)  # You can change the number here if you want averages for a number of days

             # Get the averages of time each sign was seen
            averages4 = db.averages(4)  # You can change the number here if you want averages for a number of days

             # Get the averages of time each sign was seen
            averages5 = db.averages(5)  # You can change the number here if you want averages for a number of days

            # Prepare the averages output
            averages_output1 = "Average Time Each Sign Was Seen for 1 day students (seconds):\n"
            for avg in averages1:
                averages_output1 += f"Sign {avg['Sign']}: {avg['Average_Seconds_Seen']} sec\n"
            
            averages_output2 = "Average Time Each Sign Was Seen for 2 day students (seconds):\n"
            for avg in averages2:
                averages_output2 += f"Sign {avg['Sign']}: {avg['Average_Seconds_Seen']} sec\n"

                     
            averages_output3 = "Average Time Each Sign Was Seen for 3 day students (seconds):\n"
            for avg in averages3:
                averages_output3 += f"Sign {avg['Sign']}: {avg['Average_Seconds_Seen']} sec\n"

                     
            averages_output4 = "Average Time Each Sign Was Seen for 4 day students (seconds):\n"
            for avg in averages4:
                averages_output4 += f"Sign {avg['Sign']}: {avg['Average_Seconds_Seen']} sec\n"

                     
            averages_output5 = "Average Time Each Sign Was Seen for 5 day students (seconds):\n"
            for avg in averages5:
                averages_output5 += f"Sign {avg['Sign']}: {avg['Average_Seconds_Seen']} sec\n"


            # Display the averages in the text area
            self.results1.delete(1.0, tk.END)  # Clear the previous results
            self.results1.insert(tk.END, averages_output1)

               # Display the averages in the text area
            self.results2.delete(1.0, tk.END)  # Clear the previous results
            self.results2.insert(tk.END, averages_output2)

               # Display the averages in the text area
            self.results3.delete(1.0, tk.END)  # Clear the previous results
            self.results3.insert(tk.END, averages_output3)

               # Display the averages in the text area
            self.results4.delete(1.0, tk.END)  # Clear the previous results
            self.results4.insert(tk.END, averages_output4)

               # Display the averages in the text area
            self.results5.delete(1.0, tk.END)  # Clear the previous results
            self.results5.insert(tk.END, averages_output5)

        except Exception as e:
            # Print error message in the results box in case of any issues
            self.results1.delete(1.0, tk.END)  # Clear the previous results
            self.results1.insert(tk.END, f"An error occurred: {e}\n")






#     def submit(self):
#         # Clear the results text box
#         self.results.delete(1.0, tk.END)

#         # Get values from the entry boxes
#         student_value = self.student_entry.get()
#         car_speed_value = self.car_speed_entry.get()
#         sign_time_value = self.sign_entry.get()
#         sign_count_value = self.sign_time_entry.get()

#         # Gather values for validation
#         values = [student_value, car_speed_value, sign_time_value, sign_count_value]

#         # Make sure that all boxes are filled and values are only positive integers.
#         if (self.validator.validate_not_empty(values) and 
#             self.validator.validate_integer(student_value) and 
#             self.validator.validate_integer(car_speed_value) and 
#             self.validator.validate_integer(sign_time_value) and 
#             self.validator.validate_integer(sign_count_value)):

#             # Throw values into a dictionary.
#             data = {
#                 "Number of Students": student_value,
#                 "Car Speed": car_speed_value,
#                 "Time of Sign Display": sign_time_value,
#                 "# of Signs to Display": sign_count_value,
#             }
            
#             # Call the external on_submit callback with the data and a reference to this GUI instance. Got help from AI on this
#             if self.on_submit:
#                 self.on_submit(data, self)
#             else:
#                 self.display_message("Running Calculations...")

#     def display_message(self, message):
#         """
#         Clears the results text widget and displays the provided message.

#         Parameters:
#             message (str): The message to display in the results text widget.
#         """
#         self.results.delete(1.0, tk.END)
#         self.results.insert(tk.END, message)

# class UserValidation:
#     def validate_not_empty(self, values):
#         # Check if all of the entry boxes are filled
#         for value in values:
#             if not value.strip():
#                 messagebox.showerror("Invalid Input", "All Entry Boxes must be filled.")
#                 return False
#         return True

#     def validate_integer(self, value):
#         # Check to make sure entries are only positive integers
#         if value.isdigit() and int(value) > 0:
#             return True
#         else:
#             messagebox.showerror("Invalid Input", "Please only enter positive whole numbers.")
#             return False

# If this module is run as a script, launch the GUI.
if __name__ == "__main__":
    def external_processing(data, gui):
        # Process the data, has temporary text, will be replaced
        message = (
            f"Data received:\n"
            f"  Number of Students: {data['Number of Students']}\n"
            f"  Car Speed: {data['Car Speed']} mph\n"
            f"  Time of Sign Display: {data['Time of Sign Display']}s\n"
            f"  # of Signs to Display: {data['# of Signs to Display']}\n"
            "Calculations complete."
        )
        # Display the message in the results text widget.
        gui.display_message(message)

    root = tk.Tk()
    app = ScrumGui(root, on_submit=external_processing)
    root.mainloop()
