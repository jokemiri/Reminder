from tkinter import *
import tkinter.messagebox as messagebox
from datetime import datetime, timedelta

class Reminder:
    def __init__(self, date, message):
        self.date = date
        self.message = message
    
    def __repr__(self):
        return f"{self.date}: {self.message}"

class ReminderApp:
    def __init__(self, master):
        self.master = master
        master.title("Reminder App")

        self.reminders = []

        # create GUI elements
        self.date_label = Label(master, text="Date (YYYY-MM-DD HH:MM):")
        self.date_label.pack()

        self.date_entry = Entry(master)
        self.date_entry.pack()

        self.message_label = Label(master, text="Reminder Message:")
        self.message_label.pack()

        self.message_entry = Entry(master)
        self.message_entry.pack()

        self.add_button = Button(master, text="Add Reminder", command=self.add_reminder)
        self.add_button.pack()

        self.reminders_label = Label(master, text="Reminders:")
        self.reminders_label.pack()

        self.reminders_listbox = Listbox(master, width=50)
        self.reminders_listbox.pack()

        self.delete_button = Button(master, text="Delete Selected Reminder", command=self.delete_reminder)
        self.delete_button.pack()

        self.load_reminders()

    def add_reminder(self):
        date_str = self.date_entry.get()
        message = self.message_entry.get()

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD HH:MM")
            return

        reminder = Reminder(date, message)
        self.reminders.append(reminder)

        self.save_reminders()

        self.date_entry.delete(0, END)
        self.message_entry.delete(0, END)

        self.update_reminders_listbox()

        now = datetime.now()
        if date > now:
            delta = (date - now).total_seconds()
            self.master.after(int(delta * 1000), lambda: self.show_reminder(message))

    def show_reminder(self, message):
        messagebox.showinfo("Reminder", message)

    def delete_reminder(self):
        selection = self.reminders_listbox.curselection()
        if len(selection) == 0:
            messagebox.showwarning("No Selection", "Please select a reminder to delete")
            return

        index = selection[0]
        reminder = self.reminders[index]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the reminder:\n{reminder}")
        if confirm:
            self.reminders.pop(index)
            self.save_reminders()
            self.update_reminders_listbox()

    def update_reminders_listbox(self):
        self.reminders_listbox.delete(0, END)
        for reminder in self.reminders:
            self.reminders_listbox.insert(END, reminder)

    def load_reminders(self):
        try:
            with open("reminders.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    date_str, message = line.strip().split(": ")
                    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                    reminder = Reminder(date, message)
                    self.reminders.append(reminder)

                self.update_reminders_listbox()

        except FileNotFoundError:
            pass

    def save_reminders(self):
        with open("reminders.txt", "w") as f:
            for reminder in self.reminders:
                date_str = reminder.date.strftime("%Y-%m-%d %H:%M")
                message = reminder.message
                f.write(f"{date_str}: {message}\n")

root = Tk()
app = ReminderApp(root)
root.mainloop()
