import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('database_rumahsakit.db')

c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT NOT NULL,
          password TEXT NOT NULL)
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS dokters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            specialist TEXT NOT NULL,
            alamat TEXT NOT NULL,
            no_telp TEXT NOT NULL)
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS pasiens(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            alamat TEXT NOT NULL,
            no_telp TEXT NOT NULL,
            keluhan TEXT NOT NULL)
""")



def add_admin():
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if c.fetchone() is None:
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
        conn.commit()

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def login():
    clear_window()
    root.minsize(300, 300)
    root.maxsize(300, 300)
    root.resizable(False, False)
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get window width and height
    window_width = 300
    window_height = 300

    # Calculate position x and y coordinates
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    login_frame = tk.Frame(root)
    login_frame.rowconfigure(0, weight=1)
    login_frame.rowconfigure(1, weight=0)
    login_frame.rowconfigure(2, weight=0)
    login_frame.rowconfigure(3, weight=0)
    login_frame.rowconfigure(4, weight=1)
    login_frame.columnconfigure(0, weight=1)
    login_frame.columnconfigure(1, weight=0)
    login_frame.columnconfigure(2, weight=1)
    login_frame.columnconfigure(3, weight=1)


    menu = tk.Menu(root)
    root.config(menu=menu)
    menu.add_command(label="Exit", command=root.quit)
    
    tk.Label(login_frame, text="Username : ").grid(row=1, column=1,sticky="ew")
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=1, column=2, sticky="ew")
    
    tk.Label(login_frame, text="Password : ").grid(row=2, column=1, sticky="ew")
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=2, column=2, sticky="ew")

    def check_login():
        username = username_entry.get()
        password = password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Login Failed", "Username and password cannot be empty")
            return
        
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        users = c.fetchall()
        
        if users:
            USERNAME = users[0][1]
            PASSWORD = users[0][2]
            if username == USERNAME and password == PASSWORD:
                global logged_in
                logged_in = True
                main_menu()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

    tk.Button(login_frame, text="Login", command=check_login).grid(row=3, column=1, columnspan=2, sticky="ewsn", pady=10)
    login_frame.pack(expand=True, fill="both")

def logout():
    menu = tk.Menu(root)
    root.config(menu=menu)
    global logged_in
    logged_in = False
    main_menu()

def change_password():
    clear_window()
    menu = tk.Menu(root)
    root.config(menu=menu)
    root.minsize(300, 300)
    root.maxsize(300, 300)
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get window width and height
    window_width = 300
    window_height = 300

    # Calculate position x and y coordinates
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    change_password_frame = tk.Frame(root)
    change_password_frame.rowconfigure(0, weight=1)
    change_password_frame.rowconfigure(1, weight=0)
    change_password_frame.rowconfigure(2, weight=0)
    change_password_frame.rowconfigure(3, weight=0)
    change_password_frame.rowconfigure(4, weight=1)
    change_password_frame.columnconfigure(0, weight=1)
    change_password_frame.columnconfigure(1, weight=0)
    change_password_frame.columnconfigure(2, weight=1)
    change_password_frame.columnconfigure(3, weight=1)


    tk.Label(change_password_frame, text="Old Password : ").grid(row=1, column=1, sticky="ew")
    old_password_entry = tk.Entry(change_password_frame)
    old_password_entry.grid(row=1, column=2, sticky="ew")

    tk.Label(change_password_frame, text="New Password : ").grid(row=2, column=1, sticky="ew")
    new_password_entry = tk.Entry(change_password_frame, show="*")
    new_password_entry.grid(row=2, column=2, sticky="ew")


    def check_password():
        c.execute("SELECT * FROM users WHERE username = 'admin'")
        users = c.fetchall()
        PASSWORD = users[0][2]
        old_pass = old_password_entry.get()
        new_pass = new_password_entry.get()

        if not old_pass or not new_pass:
            messagebox.showerror("Failed", "Old password and new password cannot be empty")
            return

        if old_pass == PASSWORD:
            c.execute("UPDATE users SET password = ? WHERE username = 'admin'", (new_pass,))
            conn.commit()
            messagebox.showinfo("Success", "Password has been changed")
            main_menu()
        else:
            messagebox.showerror("Failed", "Old password is wrong")
            old_password_entry.delete(0, tk.END)
            new_password_entry.delete(0, tk.END)

    tk.Button(change_password_frame, text="Change Password", command=check_password).grid(row=3, column=2, sticky="ewsn", pady=10, padx=30)
    tk.Button(change_password_frame, text="Back", command=main_menu).grid(row=3, column=1, sticky="ewsn", pady=10)
    change_password_frame.pack(expand=True, fill="both")
    

def add_dokter():
    clear_window()
    menu = tk.Menu(root)
    root.config(menu=menu)
    root.minsize(400, 400)
    root.maxsize(400, 400)
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get window width and height
    window_width = 400
    window_height = 400

    # Calculate position x and y coordinates
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    root.config(menu=menu)
    menu.add_command(label="Back", command=data_dokter)
    menu.add_command(label="logout", command=logout)

    add_dokter_frame = tk.Frame(root)
    add_dokter_frame.rowconfigure(0, weight=1)
    add_dokter_frame.rowconfigure(1, weight=0)
    add_dokter_frame.rowconfigure(2, weight=0)
    add_dokter_frame.rowconfigure(3, weight=0)
    add_dokter_frame.rowconfigure(4, weight=0)
    add_dokter_frame.rowconfigure(5, weight=0)
    add_dokter_frame.rowconfigure(6, weight=1)
    add_dokter_frame.columnconfigure(0, weight=0)
    add_dokter_frame.columnconfigure(1, weight=1)
    add_dokter_frame.columnconfigure(2, weight=1)

    tk.Label(add_dokter_frame, text="Nama Dokter : ").grid(row=1, column=0, sticky="ew")
    nama_entry = tk.Entry(add_dokter_frame)
    nama_entry.grid(row=1, column=1, sticky="ew")
    tk.Label(add_dokter_frame, text="Specialist : ").grid(row=2, column=0, sticky="ew")
    specialist_entry = tk.Entry(add_dokter_frame)
    specialist_entry.grid(row=2, column=1, sticky="ew")
    tk.Label(add_dokter_frame, text="Alamat : ").grid(row=3, column=0, sticky="ew")
    alamat_entry = tk.Entry(add_dokter_frame)
    alamat_entry.grid(row=3, column=1, sticky="ew")
    tk.Label(add_dokter_frame, text="No Telp : ").grid(row=4, column=0, sticky="ew")
    no_telp_entry = tk.Entry(add_dokter_frame)
    no_telp_entry.grid(row=4, column=1, sticky="ew")

    def save_dokter():
        nama = nama_entry.get()
        specialist = specialist_entry.get()
        alamat = alamat_entry.get()
        no_telp = no_telp_entry.get()
        
        if not nama or not specialist or not alamat or not no_telp:
            messagebox.showerror("Failed", "All fields must be filled")
            return
        
        try:
            int(no_telp)
        except ValueError:
            messagebox.showerror("Failed", "No telp must be a number")
            no_telp_entry.delete(0, tk.END)
            return

        if nama and specialist and alamat and no_telp:
            c.execute("INSERT INTO dokters (nama, specialist, alamat, no_telp) VALUES (?, ?, ?, ?)", (nama, specialist, alamat, no_telp))
            conn.commit()
            messagebox.showinfo("Success", "Dokter has been added")
            data_dokter()
        else:
            messagebox.showerror("Failed", "All fields must be filled")
    
    tk.Button(add_dokter_frame, text="Save", command=save_dokter).grid(row=5, column=1, sticky="ewsn", pady=10)
    add_dokter_frame.grid(row=0, column=0, rowspan=2 , sticky="nsew")


def edit_dokter(dokter_id):
    clear_window()
    menu = tk.Menu(root)
    root.config(menu=menu)
    root.minsize(400, 400)
    root.maxsize(400, 400)
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get window width and height
    window_width = 400
    window_height = 400

    # Calculate position x and y coordinates
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")


    root.config(menu=menu)
    menu.add_command(label="Back", command=data_dokter)
    menu.add_command(label="logout", command=logout)

    c.execute("SELECT * FROM dokters WHERE id = ?", (dokter_id,))
    dokter = c.fetchone()

    edit_dokter_frame = tk.Frame(root)
    edit_dokter_frame.rowconfigure(0, weight=1)
    edit_dokter_frame.rowconfigure(1, weight=0)
    edit_dokter_frame.rowconfigure(2, weight=0)
    edit_dokter_frame.rowconfigure(3, weight=0)
    edit_dokter_frame.rowconfigure(4, weight=0)
    edit_dokter_frame.rowconfigure(5, weight=0)
    edit_dokter_frame.rowconfigure(6, weight=1)
    edit_dokter_frame.columnconfigure(0, weight=0)
    edit_dokter_frame.columnconfigure(1, weight=1)
    edit_dokter_frame.columnconfigure(2, weight=1)

    tk.Label(edit_dokter_frame, text="Nama Dokter : ").grid(row=1, column=0, sticky="ew")
    nama_entry = tk.Entry(edit_dokter_frame)
    nama_entry.insert(0, dokter[1])
    nama_entry.grid(row=1, column=1, sticky="ew")
    tk.Label(edit_dokter_frame, text="Specialist : ").grid(row=2, column=0, sticky="ew")
    specialist_entry = tk.Entry(edit_dokter_frame)
    specialist_entry.insert(0, dokter[2])
    specialist_entry.grid(row=2, column=1, sticky="ew")
    tk.Label(edit_dokter_frame, text="Alamat : ").grid(row=3, column=0, sticky="ew")
    alamat_entry = tk.Entry(edit_dokter_frame)
    alamat_entry.insert(0, dokter[3])
    alamat_entry.grid(row=3, column=1, sticky="ew")
    tk.Label(edit_dokter_frame, text="No Telp : ").grid(row=4, column=0, sticky="ew")
    no_telp_entry = tk.Entry(edit_dokter_frame)
    no_telp_entry.insert(0, dokter[4])
    no_telp_entry.grid(row=4, column=1, sticky="ew")

    def update_data():
        nama = nama_entry.get()
        specialist = specialist_entry.get()
        alamat = alamat_entry.get()
        no_telp = no_telp_entry.get()

        if not nama or not specialist or not alamat or not no_telp:
            messagebox.showerror("Failed", "All fields must be filled")
            return
        
        try:
            int(no_telp)
        except ValueError:
            messagebox.showerror("Failed", "No telp must be a number")
            no_telp_entry.delete(0, tk.END)
            return

        if nama and specialist and alamat and no_telp:
            c.execute("UPDATE dokters SET nama = ?, specialist = ?, alamat = ?, no_telp = ? WHERE id = ?", (nama, specialist, alamat, no_telp, dokter_id))
            conn.commit()
            messagebox.showinfo("Success", "Data has been updated")
            data_dokter()
        else:
            messagebox.showerror("Failed", "All fields must be filled")

    tk.Button(edit_dokter_frame, text="Update", command=update_data).grid(row=5, column=1, sticky="ewsn", pady=10)
    edit_dokter_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

def data_dokter():
    clear_window()
    menu = tk.Menu(root)
    root.config(menu=menu)
    root.minsize(1000,770)
    root.maxsize(1000, 770)
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get window width and height
    window_width = 1000
    window_height = 770

    # Calculate position x and y coordinates
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")


    root.config(menu=menu)
    menu.add_command(label="Data Managemant Pasien", command=data_pasien)
    menu.add_command(label="Change Password", command=change_password)
    menu.add_command(label="logout", command=logout)


    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    dokter_frame = tk.Frame(root)
    dokter_frame.grid(row=1, column=0, sticky="nsew")
    dokter_frame.rowconfigure(0, weight=0)
    dokter_frame.columnconfigure(0, weight=1)
    dokter_frame.columnconfigure(1, weight=0)
    dokter_frame.columnconfigure(2, weight=0)
    dokter_frame.columnconfigure(3, weight=0)
    dokter_frame.columnconfigure(4, weight=0)
    dokter_frame.columnconfigure(5, weight=1)

    tk.Label(root, text="Data Dokter", font=("Arial", 24), fg="brown").grid(row=0, column=0, pady=10)

    c.execute("SELECT * FROM dokters")
    dokters = c.fetchall()

    if dokters:

        dokter_scroll = ttk.Scrollbar(dokter_frame, orient="vertical")
        dokter_scroll.grid(row=0, column=4, sticky="ns")

        dokter_table = ttk.Treeview(dokter_frame, columns=("Nama", "Specialist", "Alamat", "No Telp"), yscrollcommand=dokter_scroll.set, height=30)
        dokter_table.heading("#0", text="No")
        dokter_table.column("#0", width=50, anchor="w")
        dokter_table.heading("#1", text="Nama")
        dokter_table.column("#1", width=200, anchor="w")
        dokter_table.heading("#2", text="Specialist")
        dokter_table.column("#2", width=200, anchor="w")
        dokter_table.heading("#3", text="Alamat")
        dokter_table.column("#3", width=200, anchor="w")
        dokter_table.heading("#4", text="No Telp")
        dokter_table.column("#4", width=200, anchor="w")
        
        for i, dokter in enumerate(dokters):
            dokter_table.insert("", "end", text=i+1, values=(dokter[1], dokter[2], dokter[3], dokter[4]), tags=(dokter[0],))

        dokter_table.grid(row=0, column=1, columnspan=3, sticky="nsew")
        dokter_scroll.config(command=dokter_table.yview)

        def on_edit_click():
            selected_items = dokter_table.selection()
            if selected_items:
                selected_item = selected_items[0]
                dokter_id = dokter_table.item(selected_item, "tags")[0]
                edit_dokter(dokter_id)
            else:
                messagebox.showerror("Error", "No data selected")

        def on_delete_click():
            selected_items = dokter_table.selection()
            if selected_items:
                selected_item = selected_items[0]
                dokter_id = dokter_table.item(selected_item, "tags")[0]
                c.execute("DELETE FROM dokters WHERE id = ?", (dokter_id,))
                conn.commit()
                messagebox.showinfo("Success", "Data has been deleted")
                data_dokter()
            else:
                messagebox.showerror("Error", "No data selected")

        add_button = tk.Button(dokter_frame, text="Add", command=add_dokter, width=30, height=2)
        add_button.grid(row=1, column=1, pady=10)

        edit_button = tk.Button(dokter_frame, text="Edit", command=on_edit_click, width=30, height=2)
        edit_button.grid(row=1, column=2, pady=10)

        delete_button = tk.Button(dokter_frame, text="Delete", command=on_delete_click, width=30, height=2)
        delete_button.grid(row=1, column=3, pady=10)

    else:
        tk.Label(dokter_frame, text="No data available").grid(row=0, column=1, columnspan=2, sticky="nsew")

def add_pasien():
    clear_window()
    menu = tk.Menu(root)
    root.config(menu=menu)
    root.minsize(400, 400)
    root.maxsize(400, 400)
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get window width and height
    window_width = 400
    window_height = 400

    # Calculate position x and y coordinates
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")


    root.config(menu=menu)
    menu.add_command(label="Back", command=data_pasien)
    menu.add_command(label="logout", command=logout)

    add_pasien_frame = tk.Frame(root)
    add_pasien_frame.rowconfigure(0, weight=1)
    add_pasien_frame.rowconfigure(1, weight=0)
    add_pasien_frame.rowconfigure(2, weight=0)
    add_pasien_frame.rowconfigure(3, weight=0)
    add_pasien_frame.rowconfigure(4, weight=0)
    add_pasien_frame.rowconfigure(5, weight=0)
    add_pasien_frame.rowconfigure(6, weight=1)
    add_pasien_frame.columnconfigure(0, weight=0)
    add_pasien_frame.columnconfigure(1, weight=1)
    add_pasien_frame.columnconfigure(2, weight=1)

    tk.Label(add_pasien_frame, text="Nama Pasien : ").grid(row=1, column=0, sticky="ew")
    nama_entry = tk.Entry(add_pasien_frame)
    nama_entry.grid(row=1, column=1, sticky="ew")
    tk.Label(add_pasien_frame, text="Alamat : ").grid(row=2, column=0, sticky="ew")
    alamat_entry = tk.Entry(add_pasien_frame)
    alamat_entry.grid(row=2, column=1, sticky="ew")
    tk.Label(add_pasien_frame, text="No Telp : ").grid(row=3, column=0, sticky="ew")
    no_telp_entry = tk.Entry(add_pasien_frame)
    no_telp_entry.grid(row=3, column=1, sticky="ew")
    tk.Label(add_pasien_frame, text="Keluhan : ").grid(row=4, column=0, sticky="ew")
    keluhan_entry = tk.Entry(add_pasien_frame)
    keluhan_entry.grid(row=4, column=1, sticky="ew")

    def save_pasien():
        nama = nama_entry.get()
        alamat = alamat_entry.get()
        no_telp = no_telp_entry.get()
        keluhan = keluhan_entry.get()

        if not nama or not alamat or not no_telp or not keluhan:
            messagebox.showerror("Failed", "All fields must be filled")
            return
        
        try:
            int(no_telp)
        except ValueError:
            messagebox.showerror("Failed", "No telp must be a number")
            no_telp_entry.delete(0, tk.END)
            return

        if nama and alamat and no_telp and keluhan:
            c.execute("INSERT INTO pasiens (nama, alamat, no_telp, keluhan) VALUES (?, ?, ?, ?)", (nama, alamat, no_telp, keluhan))
            conn.commit()
            messagebox.showinfo("Success", "Pasien has been added")
            data_pasien()
        else:
            messagebox.showerror("Failed", "All fields must be filled")
    
    tk.Button(add_pasien_frame, text="Save", command=save_pasien).grid(row=5, column=1, sticky="ewsn", pady=10)
    add_pasien_frame.grid(row=0, column=0, rowspan=2 , sticky="nsew")

def edit_pasien(pasien_id):
    clear_window()
    menu = tk.Menu(root)
    root.config(menu=menu)
    root.minsize(400, 400)
    root.maxsize(400, 400)
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get window width and height
    window_width = 400
    window_height = 400

    # Calculate position x and y coordinates
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")


    root.config(menu=menu)
    menu.add_command(label="Back", command=data_pasien)
    menu.add_command(label="logout", command=logout)

    c.execute("SELECT * FROM pasiens WHERE id = ?", (pasien_id,))
    pasien = c.fetchone()

    edit_pasien_frame = tk.Frame(root)
    edit_pasien_frame.rowconfigure(0, weight=1)
    edit_pasien_frame.rowconfigure(1, weight=0)
    edit_pasien_frame.rowconfigure(2, weight=0)
    edit_pasien_frame.rowconfigure(3, weight=0)
    edit_pasien_frame.rowconfigure(4, weight=0)
    edit_pasien_frame.rowconfigure(5, weight=0)
    edit_pasien_frame.rowconfigure(6, weight=1)
    edit_pasien_frame.columnconfigure(0, weight=0)
    edit_pasien_frame.columnconfigure(1, weight=1)
    edit_pasien_frame.columnconfigure(2, weight=1)

    tk.Label(edit_pasien_frame, text="Nama Pasien : ").grid(row=1, column=0, sticky="ew")
    nama_entry = tk.Entry(edit_pasien_frame)
    nama_entry.insert(0, pasien[1])
    nama_entry.grid(row=1, column=1, sticky="ew")
    tk.Label(edit_pasien_frame, text="Alamat : ").grid(row=2, column=0, sticky="ew")
    alamat_entry = tk.Entry(edit_pasien_frame)
    alamat_entry.insert(0, pasien[2])
    alamat_entry.grid(row=2, column=1, sticky="ew")
    tk.Label(edit_pasien_frame, text="No Telp : ").grid(row=3, column=0, sticky="ew")
    no_telp_entry = tk.Entry(edit_pasien_frame)
    no_telp_entry.insert(0, pasien[3])
    no_telp_entry.grid(row=3, column=1, sticky="ew")
    tk.Label(edit_pasien_frame, text="Keluhan : ").grid(row=4, column=0, sticky="ew")
    keluhan_entry = tk.Entry(edit_pasien_frame)
    keluhan_entry.insert(0, pasien[4])
    keluhan_entry.grid(row=4, column=1, sticky="ew")

    def update_data():
        nama = nama_entry.get()
        alamat = alamat_entry.get()
        no_telp = no_telp_entry.get()
        keluhan = keluhan_entry.get()

        if not nama or not alamat or not no_telp or not keluhan:
            messagebox.showerror("Failed", "All fields must be filled")
            return
        
        try:
            int(no_telp)
        except ValueError:
            messagebox.showerror("Failed", "No telp must be a number")
            no_telp_entry.delete(0, tk.END)
            return

        if nama and alamat and no_telp and keluhan:
            c.execute("UPDATE pasiens SET nama = ?, alamat = ?, no_telp = ?, keluhan = ? WHERE id = ?", (nama, alamat, no_telp, keluhan, pasien_id))
            conn.commit()
            messagebox.showinfo("Success", "Data has been updated")
            data_pasien()
        else:
            messagebox.showerror("Failed", "All fields must be filled")
    
    tk.Button(edit_pasien_frame, text="Update", command=update_data).grid(row=5, column=1, sticky="ewsn", pady=10)
    edit_pasien_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

def data_pasien():
    clear_window()
    menu = tk.Menu(root)
    root.config(menu=menu)
    root.minsize(1000,770)
    root.maxsize(1000, 770)
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get window width and height
    window_width = 1000
    window_height = 770

    # Calculate position x and y coordinates
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    
    root.config(menu=menu)
    menu.add_command(label="Data Managemant Dokter", command=data_dokter)
    menu.add_command(label="Change Password", command=change_password)
    menu.add_command(label="logout", command=logout)

    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    pasien_frame = tk.Frame(root)
    pasien_frame.grid(row=1, column=0, sticky="nsew")
    pasien_frame.rowconfigure(0, weight=0)
    pasien_frame.columnconfigure(0, weight=1)
    pasien_frame.columnconfigure(1, weight=0)
    pasien_frame.columnconfigure(2, weight=0)
    pasien_frame.columnconfigure(3, weight=0)
    pasien_frame.columnconfigure(4, weight=0)
    pasien_frame.columnconfigure(5, weight=1)

    tk.Label(root, text="Data Pasien", font=("Arial", 24), fg="brown").grid(row=0, column=0, pady=10)

    c.execute("SELECT * FROM pasiens")
    pasiens = c.fetchall()

    if pasiens:

        pasien_scroll = ttk.Scrollbar(pasien_frame, orient="vertical")
        pasien_scroll.grid(row=0, column=4, sticky="ns")

        pasien_table = ttk.Treeview(pasien_frame, columns=("Nama", "Alamat", "No Telp", "Keluhan"), yscrollcommand=pasien_scroll.set, height=30)
        pasien_table.heading("#0", text="No")
        pasien_table.column("#0", width=50, anchor="w")
        pasien_table.heading("#1", text="Nama")
        pasien_table.column("#1", width=200, anchor="w")
        pasien_table.heading("#2", text="Alamat")
        pasien_table.column("#2", width=200, anchor="w")
        pasien_table.heading("#3", text="No Telp")
        pasien_table.column("#3", width=200, anchor="w")
        pasien_table.heading("#4", text="Keluhan")
        pasien_table.column("#4", width=200, anchor="w")

        for i, pasien in enumerate(pasiens):
            pasien_table.insert("", "end", text=i+1, values=(pasien[1], pasien[2], pasien[3], pasien[4]), tags=(pasien[0],))

        pasien_table.grid(row=0, column=1, columnspan=3, sticky="nsew")
        pasien_scroll.config(command=pasien_table.yview)

        def on_edit_click():
            selected_items = pasien_table.selection()
            if selected_items:
                selected_item = selected_items[0]
                pasien_id = pasien_table.item(selected_item, "tags")[0]
                edit_pasien(pasien_id)
            else:
                messagebox.showerror("Error", "No data selected")
        
        def on_delete_click():
            selected_items = pasien_table.selection()
            if selected_items:
                selected_item = selected_items[0]
                pasien_id = pasien_table.item(selected_item, "tags")[0]
                c.execute("DELETE FROM pasiens WHERE id = ?", (pasien_id,))
                conn.commit()
                messagebox.showinfo("Success", "Data has been deleted")
                data_pasien()
            else:
                messagebox.showerror("Error", "No data selected")

        add_button = tk.Button(pasien_frame, text="Add", command=add_pasien, width=30, height=2)
        add_button.grid(row=1, column=1, pady=10)

        edit_button = tk.Button(pasien_frame, text="Edit", command=on_edit_click, width=30, height=2)
        edit_button.grid(row=1, column=2, pady=10)

        delete_button = tk.Button(pasien_frame, text="Delete", command=on_delete_click, width=30, height=2)
        delete_button.grid(row=1, column=3, pady=10)

    else:
        tk.Label(pasien_frame, text="No data available").grid(row=0, column=1, columnspan=2, sticky="nsew")



def main_menu():
    if logged_in:
        clear_window()
        data_pasien()
    else:
        login()

root = tk.Tk()
root.title("Managemant Rumah Sakit")
logged_in = False

add_admin()


main_menu()

root.mainloop()