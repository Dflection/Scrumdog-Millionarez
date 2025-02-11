# Written by Joshua Fernandez
# Database for Scrumdogs
# Created 1/27/2025


import csv

# The class for our database.
class Database:
    def __init__(self, file=None) -> None:
        # self.file is the only required attribute for this class.
        self.file = file

    # This method allows us to input any list of dictionaries into our Scrumabase.
    def excel(self, studentlist) -> None:
        """
        This method will take a list of dictionary items and
        write each dictionary item into a row in a CSV File.

        Takes 1 argument. Requires a list of dictionary items.
        """

        file = self.file
        # df = pd.read_csv(file, quotechar='"')

        # This bit of code opens the file math in the mode we need as well as the character style encoding.
        with open(file, mode='w', newline='', encoding='utf-8') as file:
            # writer is a variable for the csv.DictWriter function that creates a csv file and takes an argument for the
            # file and the fieldnames.
            writer = csv.DictWriter(file, fieldnames=studentlist[0].keys())
            # This is a method from the csv library DictWriter Class.
            writer.writeheader()
            # Method to write multiple rows of dictionary items.
            writer.writerows(studentlist)

    # This bit of code allows to to extract the information from the csv into a list of dictionaries.
    def csv_to_dict(self) -> None:
        """
        This function takes each row in a CSV file and makes dictionaries.

        Does not need to take in any arguments.
        """
        file = self.file

        with open(file, mode='r', encoding='utf-8') as file:
            # The "DictReader" class automatically uses the Headers of the CSV files as keys.
            csv_reader = csv.DictReader(file)
            data = [dict(row) for row in csv_reader]  # Convert each row into a dictionary

        return data

    def averages(self, days, numsigns) -> None:
        """
        This method will read the csv file and return and avg number.
        """

        # This is a list of numbers for each signs seconds seen by students that attended x days.
        numbies = []
        # This is the list of students that attended x days
        student_group = []
        # This is the total number of signs counted.
        # This is the result of the averages
        final_numbies = []
        # This calls the method csv_to_dict to get dictionary items of the e
        data = self.csv_to_dict()

        # For dictionary's in data if the days variable is in the ['days attended'] value for a student adds students to
        for dictionary in data:

            # if str(days) in str(dictionary['days_attended']) and dictionary not in student_group:
            # student_group.append(dictionary)

            if int(days) == int(dictionary['num_days_attended']) and dictionary not in student_group:
                student_group.append(dictionary)

        # For items in student group make a dictionary of each sign and its second value
        for student in student_group:
            # 20 is the maximum number of signs we decided on.
            for i in range(1, numsigns+1):
                sign_number = str(i)
                # If the number of seconds the sign was seen is greater than 0.
                if float(student[f'sign{sign_number}']) > 0 and student.get(f'sign{sign_number}') not in numbies:
                    Sign_dict = {
                        'sign': str(i),
                        'seconds': student.get(f'sign{sign_number}')
                    }
                    numbies.append(Sign_dict)
                    if float(student[f'sign{sign_number}']) > 1:

                        Sign_num = Sign_dict['sign']

        # For loop for the items in numbies. ie the signs and seconds seen by each student.
        for item in numbies:
            # This variable is = to the existing "entry"(item) in final_numbies is the sign value is already in
            # final_numbies
            existing_item = next((entry for entry in final_numbies if entry['signtest'] == str(item['sign'])), None)

            # If the existing sign is not none then it will add the numbies items seconds to the existing items seconds.
            if existing_item:
                existing_item['seconds'] = str(float(existing_item['seconds']) + float(item['seconds']))
            # if existing item is none then it will create a new dictionary item for final numbies
            else:
                new_dict = {
                    'signtest': str(item['sign']),
                    'seconds': str(item['seconds'])
                }
                final_numbies.append(new_dict)
        # This takes the items in final numbies and averages out the seconds from the total each sign was seen by
        # dividing the total seconds by the number of students
        for total in final_numbies:
            total['seconds'] = str(float(total['seconds'])/float(len(student_group)))
            total['Sign'] = total['signtest']
            total['Average_Seconds_Seen'] = str(round(float(total['seconds']), 2))
            del total['signtest']
            del total['seconds']

        return final_numbies

    def percentages(self, days, numsigns) -> None:
        """
        This method will read the CSV file and return
        the percentage of signs seen by students attending 'days' days.
        """
        numbies = []  # List of signs seen by students
        student_group = []  # List of students attending the given number of days
        total_signs_seen = 0  # Count of actual signs seen
        data = self.csv_to_dict()  # Fetch CSV data
        
        # Get all students who attended 'days' days
        for dictionary in data:
            if int(days) == int(dictionary['num_days_attended']):
                student_group.append(dictionary)
        
        # If no students found, return 0% (prevents division errors)
        if not student_group:
            return 0.0

        # For each student, check which signs they have seen
        for student in student_group:
            for i in range(1, numsigns + 1):  # Loop over all sign columns
                sign_number = str(i)
                seen_time = float(student.get(f'sign{sign_number}', 0))  # Default 0 if missing
                
                if seen_time > 0:  # Count all signs seen, not just those > 2
                    total_signs_seen += 1

        # Correct denominator: total possible signs seen
        Sign_total = numsigns * len(student_group)

        # Avoid division by zero
        if Sign_total == 0:
            return 0.0

        # Calculate percentage correctly
        percentage = round((total_signs_seen / Sign_total) * 100, 2)

        return percentage