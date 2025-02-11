The Sign Out Front 1.1
By The Scrumdog Millionaires
(Chase Varvayanis, Joshua Fernandez, Joshua Poe, Dylan Henley, Andrew Lampkin)
2-11-2024

----------------------------------------------------------------------------------\

HOW TO RUN APPLICATION:

  Run by launching the SM-SOF-MAIN file

  Requires the following dependencies not included in Python by default:
    Tkinter
    PIL
    OS

----------------------------------------------------------------------------------

KNOWN ISSUES:

  - The method to randomize the order of the signs instead of a consistent queue is implemented  and to the best of our knowledge functional in the sign list class but not implied in the GUI
  - The Simulation is cheesed, we had an issue where calculating for a number of students over ~50 would not process. We could not resolve the issue, and implemented a feature to calculate for a random number of students under 50 students if the user entered a value above 50
