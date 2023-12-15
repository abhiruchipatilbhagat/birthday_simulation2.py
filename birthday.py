import tkinter as tk
from tkinter import ttk
import random
import datetime
from math import prod

class BirthdaySimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Birthday Problem Simulation")

        self.configure(bg="#F0F0F0")  # Set background color

        self.people_count = 0
        self.birthday_list = []
        self.birthday_counts = {}
        self.duplicate_birthdays = []

        self.label = ttk.Label(self, text="Number of people in the room:", background="#F0F0F0", font=("Arial", 12))
        self.label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.add_button = ttk.Button(self, text="Add", command=self.add_person, style="TButton")
        self.add_button.grid(row=0, column=1, pady=10, padx=10, sticky="e")

        self.text_widget = tk.Text(self, height=10, width=40, wrap="word", font=("Arial", 10))
        self.text_widget.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        self.duplicates_label = ttk.Label(self, text="Duplicate Birthdays:", background="#F0F0F0", font=("Arial", 12))
        self.duplicates_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        self.duplicates_listbox = tk.Listbox(self, height=5, width=40, font=("Arial", 10), selectbackground="#BFBFBF")
        self.duplicates_listbox.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

        self.people_added_label = ttk.Label(self, text="Number of People Added: 0", background="#F0F0F0", font=("Arial", 12))
        self.people_added_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")

        self.probability_label = ttk.Label(self, text="Probability of at least one match: 0.0000", background="#F0F0F0", font=("Arial", 12))
        self.probability_label.grid(row=5, column=0, pady=10, padx=10, sticky="w")

        # Configure style for the Add button
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), background="#4CAF50", foreground="white", padding=5)

        # Set the theme to clam for a modern look
        self.style.theme_use("clam")

    def calculate_birthday_probability(self):
        # Calculate the probability of no matches (all birthdays are unique) at the current room count.
        unique_birthday_prob = prod((365 - i) / 365 for i in range(self.people_count))

        # Subtract the probability of no matches from 1 to get the probability of at least one match.
        at_least_one_match_prob = 1 - unique_birthday_prob

        return at_least_one_match_prob

    def add_person(self):
        def get_date_from_day_of_year(day_of_year, year):
            # Create a datetime object for January 1 of the specified year
            base_date = datetime.datetime(year, 1, 1)

            # Calculate the date by adding the day_of_year - 1 (since it starts from 1)
            target_date = base_date + datetime.timedelta(days=day_of_year - 1)

            return target_date

        # Increment the people count
        self.people_count += 1

        # Generate a random birthday (1 to 365, assuming a non-leap year)
        birthday = random.randint(1, 365)
        birthday_date = get_date_from_day_of_year(birthday, 2023)

        # Add the birthday to the list and update counts
        self.birthday_list.append(birthday_date)
        self.birthday_counts[birthday_date] = self.birthday_counts.get(birthday_date, 0) + 1

        # Display information in the text widget
        info = f"Person {self.people_count}: {birthday_date.strftime('%d %B')}, Count: {self.birthday_counts[birthday_date]}\n"
        self.text_widget.insert(tk.END, info)
        self.text_widget.see(tk.END)  # Scroll to the end

        # Check for duplicates
        duplicates = [b for b, count in self.birthday_counts.items() if count > 1]

        # Update duplicates listbox
        self.update_duplicates_listbox(duplicates)

        # Update the number of people added label
        self.people_added_label.config(text=f"Number of People Added: {self.people_count}")

        # Calculate and update the probability label
        probability = self.calculate_birthday_probability()
        self.probability_label.config(text=f"Probability of at least one match: {probability:.4f}")

    def update_duplicates_listbox(self, duplicates):
        # Clear existing items in the listbox
        self.duplicates_listbox.delete(0, tk.END)

        # Add duplicates to the listbox
        for birthday in duplicates:
            self.duplicates_listbox.insert(tk.END, f"Birthday {birthday.strftime('%d %B')} has occurred {self.birthday_counts[birthday]} times")

# Example usage:
if __name__ == "__main__":
    app = BirthdaySimulator()
    app.mainloop()
