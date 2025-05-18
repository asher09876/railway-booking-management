import mysql.connector
import tkinter as tk
from tkinter import messagebox

# --------- Database Setup ---------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",  # Replace with your MySQL password
    database="railway_db"
)
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255)
)''')

c.execute('''CREATE TABLE IF NOT EXISTS trains (
    id INT AUTO_INCREMENT PRIMARY KEY,
    train_name VARCHAR(255),
    source VARCHAR(255),
    destination VARCHAR(255),
    seats_available INT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    train_id INT,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(train_id) REFERENCES trains(id)
)''')

# Seed some trains
c.execute("SELECT COUNT(*) FROM trains")
if c.fetchone()[0] == 0:
    c.execute("SELECT COUNT(*) FROM trains")
if c.fetchone()[0] == 0:
    train_data = [
        ('Express 101', 'Bangalore', 'Chennai', 5),
        ('Fast 202', 'Mumbai', 'Delhi', 3),
        ('Super 303', 'Hyderabad', 'Kolkata', 4)
    ]
    c.executemany("INSERT INTO trains (train_name, source, destination, seats_available) VALUES (%s, %s, %s, %s)", train_data)
    

    conn.commit()

# --------- App Functions ---------
current_user = None

def register():
    uname = entry_username.get()
    pwd = entry_password.get()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (uname, pwd))
        conn.commit()
        messagebox.showinfo("Success", "Registered successfully!")
    except mysql.connector.errors.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

def login():
    global current_user
    uname = entry_username.get()
    pwd = entry_password.get()
    c.execute("SELECT * FROM users WHERE username = %s AND password = %s", (uname, pwd))
    user = c.fetchone()
    if user:
        current_user = user
        open_booking_window()
    else:
        messagebox.showerror("Error", "Invalid credentials.")

def book_ticket(train_id):
    if not current_user:
        messagebox.showerror("Error", "User not logged in.")
        return
    c.execute("SELECT seats_available FROM trains WHERE id = %s", (train_id,))
    seats = c.fetchone()[0]
    if seats > 0:
        c.execute("INSERT INTO bookings (user_id, train_id) VALUES (%s, %s)", (current_user[0], train_id))
        c.execute("UPDATE trains SET seats_available = seats_available - 1 WHERE id = %s", (train_id,))
        conn.commit()
        messagebox.showinfo("Success", "Ticket booked!")
        booking_window.destroy()
    else:
        messagebox.showerror("Error", "No seats available.")

def open_booking_window():
    global booking_window
    booking_window = tk.Toplevel(root)
    booking_window.title("Book Ticket")
    
    tk.Label(booking_window, text="Available Trains:", font=('Arial', 14)).pack()

    c.execute("SELECT * FROM trains")
    for row in c.fetchall():
        train_info = f"{row[1]} - {row[2]} to {row[3]} | Seats: {row[4]}"
        btn = tk.Button(booking_window, text=train_info, command=lambda id=row[0]: book_ticket(id))
        btn.pack(pady=5)

# --------- UI Setup ---------
root = tk.Tk()
root.title("Railway Ticket Booking System")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="Username:").grid(row=0, column=0)
entry_username = tk.Entry(frame)
entry_username.grid(row=0, column=1)

tk.Label(frame, text="Password:").grid(row=1, column=0)
entry_password = tk.Entry(frame, show='*')
entry_password.grid(row=1, column=1)

tk.Button(frame, text="Register", command=register).grid(row=2, column=0, pady=10)
tk.Button(frame, text="Login", command=login).grid(row=2, column=1)

root.mainloop()

conn.close()
