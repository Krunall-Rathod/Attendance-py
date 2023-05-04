import tkinter as tk
import sqlite3
import pandas as pd

conn = sqlite3.connect('attendance.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS attendance
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              status TEXT NOT NULL,
              date DATE NOT NULL)''')
conn.commit()

def mark_attendance():
    name = name_entry.get()
    status = status_var.get()
    date = date_entry.get()

    c.execute("INSERT INTO attendance (name, status, date) VALUES (?, ?, ?)",
              (name, status, date))
    conn.commit()

    name_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

def export_data():
    c.execute("SELECT * FROM attendance")
    data = c.fetchall()

    df = pd.DataFrame(data, columns=['ID', 'Name', 'Status', 'Date'])

    df.to_excel('attendance.db', index=False)

root = tk.Tk()
root.title('Attendance System')

tk.Label(root, text='Name: ').grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text='Status: ').grid(row=1, column=0, padx=5, pady=5)
status_var = tk.StringVar(value='Present')
status_entry = tk.OptionMenu(root, status_var, 'Present', 'Absent')
status_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text='Date: ').grid(row=2, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=2, column=1, padx=5, pady=5)

submit_button = tk.Button(root, text='Submit', command=mark_attendance)
submit_button.grid(row=3, column=0, padx=5, pady=5)

export_button = tk.Button(root, text='Export', command=export_data)
export_button.grid(row=3, column=1, padx=5, pady=5)

root.mainloop()

conn.close()
