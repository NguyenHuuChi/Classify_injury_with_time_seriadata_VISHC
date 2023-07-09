import tkinter as tk
from tkinter import filedialog

def open_file(mass):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    print("Selected file:", file_path)
    process_file(file_path, mass)

def process_file(file_path, mass):
    # Perform your processing logic here
    print("Processing file:", file_path)
    print("Mass of person:", mass)

def submit_mass():
    mass = mass_entry.get()
    print("Mass of person:", mass)
    open_file(mass)

# Create the main window
window = tk.Tk()
window.geometry("400x400")

# Create a label and entry for user input
mass_label = tk.Label(window, text="Enter mass (kg):")
mass_label.pack()
mass_entry = tk.Entry(window)
mass_entry.pack()

# Create a submit button for mass input
submit_button = tk.Button(window, text="Select CSV File", command=submit_mass)
submit_button.pack(pady=20)

# Start the main event loop
window.mainloop()
