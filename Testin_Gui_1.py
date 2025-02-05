import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

import scrumdog_queue
import Student_Class
import Database3

# main file import
'''import Main'''

# directory_path = os.path.dirname(__file__)

class Scrum_Gui:
    # Creates a Gui window
    def __init__(self, window):
        self.window = window
        self.window.title("Scrumdog Gui")
        self.window.geometry("520x250")
        self.window.resizable(False, False)

        # Create and resize background photo
        # original_img = Image.open(os.path.join(directory_path, "Photo.png"))
        # resized_image = original_img.resize((520, 180))
        # self.new_image = ImageTk.PhotoImage(resized_image)
        # self.background_label = tk.Label(window, image=self.new_image)
        # self.background_label.place(relwidth=1, relheight=1)

        # Frame for the entry boxes
        entry_frame = tk.Frame(window)
        entry_frame.pack(pady=10)

        # Number of students entry box
        tk.Label(entry_frame, text="Number of Students:").grid(row=0, column=0, padx=5)
        self.keyword1_entry = tk.Entry(entry_frame, width=15)
        self.keyword1_entry.grid(row=0, column=1, padx=5)

        # Number of signs to display entry box
        tk.Label(entry_frame, text="Speed of Cars:").grid(row=0, column=2, padx=5)
        self.keyword2_entry = tk.Entry(entry_frame, width=15)
        self.keyword2_entry.grid(row=0, column=3, padx=5)

        # Sign display time entry box
        tk.Label(entry_frame, text="Time of Sign Display:").grid(row=1, column=0, padx=5)
        self.keyword3_entry = tk.Entry(entry_frame, width=15)
        self.keyword3_entry.grid(row=1, column=1, padx=5)

        # Number of Signs to Display Entry box
        tk.Label(entry_frame, text="# of Signs to Display:").grid(row=1, column=2, padx=5)
        self.keyword4_entry = tk.Entry(entry_frame, width=15)
        self.keyword4_entry.grid(row=1, column=3, padx=5)

        # Display Results
        self.results = tk.Text(window, height=7, width=60)
        self.results.pack(padx=5, pady=5)

        # Submit button
        self.submit_button = tk.Button(window, text="Submit", width=20)
        self.submit_button.pack(pady=10)

        # # load data from 'Main' File
        # self.load_data()

    # Function for submit button to collect data into a dictionary
    def submit(self):
        data = {
            "Number of Students": self.keyword1_entry.get(),
            "Speed of Cars": self.keyword2_entry.get(),
            "Time of Sign Display": self.keyword3_entry.get(),
            "# of Signs to Display": self.keyword4_entry.get(),
        }

        '''
        # THIS IS WHERE WE WILL CALL THE MAIN FILE
        Main.send_data(data)
        '''

    '''
    # Function to load data from main file and display it in the text box
    def load_data(self):
        imported_data = Main.get_information()
        # Clear the current content of the text box
        self.results.delete(1.0, tk.END)
        # Put the data imported from Main into the Results text box
        self.results.insert(tk.END, imported_data)
    '''


if __name__ == "__main__":
    window = tk.Tk()
    gui = Scrum_Gui(window)
    window.mainloop()
