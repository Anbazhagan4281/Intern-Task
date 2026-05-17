import os
import csv
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from scanner import scan_folder
from reports import generate_report
from utils import search_files

# THEME
BG_COLOR = "#08080d"
BTN_COLOR = "#49C2E4"
TEXT_COLOR = "white"
FONT = ("Arial", 12)

# LOGIN SCREEN
def login_screen():
    root = tk.Tk()
    root.title("Login")
    root.geometry("400x300")
    root.configure(bg=BG_COLOR)

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(expand=True)

    tk.Label(frame, text="Login", font=("Arial", 18, "bold"),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    tk.Label(frame, text="Username", bg=BG_COLOR, fg=TEXT_COLOR).pack()
    username = tk.Entry(frame, font=FONT)
    username.pack(pady=5)

    tk.Label(frame, text="Password", bg=BG_COLOR, fg=TEXT_COLOR).pack()
    password = tk.Entry(frame, show="*", font=FONT)
    password.pack(pady=5)

    def check_login():
        if username.get() == "admin" and password.get() == "admin123":
            root.destroy()
            dashboard()
        else:
            messagebox.showerror("Error", "Invalid Login")

    tk.Button(frame, text="Login", bg=BTN_COLOR, fg="white",
              font=FONT, width=15, command=check_login).pack(pady=15)

    root.mainloop()


#  DASHBOARD
def dashboard():
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("500x400")
    root.configure(bg=BG_COLOR)

    tk.Label(root, text="Dashboard", font=("Arial", 18, "bold"),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack()

    def create_btn(text, cmd, row, col):
        tk.Button(frame, text=text, command=cmd,
                  width=18, height=2,
                  bg=BTN_COLOR, fg="white",
                  font=FONT).grid(row=row, column=col, padx=10, pady=10)

    create_btn("Add Folder", add_folder, 0, 0)
    create_btn("View Files", view_files, 0, 1)
    create_btn("Search", search_ui, 1, 0)
    create_btn("Report", show_report, 1, 1)
    create_btn("Exit", root.destroy, 2, 0)

    root.mainloop()


#  ADD FOLDER
def add_folder():
    path = filedialog.askdirectory()

    if path:
        new_files = scan_folder(path)

        os.makedirs("data", exist_ok=True)

        try:
            with open("data/monitored_files.json") as f:
                old_files = json.load(f)
        except:
            old_files = []

        all_files = old_files + new_files

        with open("data/monitored_files.json", "w") as f:
            json.dump(all_files, f, indent=4)

        messagebox.showinfo("Success", "Folder Added & Scanned")


#  VIEW FILES
def view_files():
    win = tk.Toplevel()
    win.title("Files")
    win.geometry("900x500")

    #  SEARCH BAR
    search_entry = tk.Entry(win, font=("Arial", 12))
    search_entry.pack(pady=5)

    columns = ("Name", "Size", "Type", "Modified", "Path")

    tree = ttk.Treeview(win, columns=columns, show="headings")

    def sort_column(col, reverse):
        data = [(tree.set(k, col), k) for k in tree.get_children('')]
        try:
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            data.sort(key=lambda t: t[0].lower(), reverse=reverse)

        for index, (_, k) in enumerate(data):
            tree.move(k, '', index)

        tree.heading(col, command=lambda: sort_column(col, not reverse))

    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_column(c, False))
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True)

    # LOAD DATA
    try:
        with open("data/monitored_files.json") as f:
            files_data = json.load(f)
        print("FILES:", files_data)
        
    except:
        messagebox.showerror("Error", "No files found")
        return

    def load_table(data):
        for row in tree.get_children():
            tree.delete(row)

        for item in data:
            tree.insert("", tk.END, values=(
                item.get("name", "N/A"),
                round(item.get("size", 0) / 1024, 2),
                item.get("type", "N/A"),
                item.get("modified", "N/A"),
                item.get("path", "N/A")
            ))

    load_table(files_data)

    #  LIVE SEARCH
    def filter_files(event):
        query = search_entry.get().lower()

        filtered = [
            f for f in files_data
            if query in f["name"].lower() or query in f["type"].lower()
        ]

        load_table(filtered)

    search_entry.bind("<KeyRelease>", filter_files)

    #  DOUBLE CLICK OPEN
    def open_file(event):
        selected = tree.focus()
        values = tree.item(selected, "values")

        if values:
            os.startfile(values[4])

    tree.bind("<Double-1>", open_file)

    # 📤 EXPORT
    def export_csv():
        with open("report.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(columns)

            for row in tree.get_children():
                writer.writerow(tree.item(row)["values"])

        messagebox.showinfo("Done", "CSV Exported")

    tk.Button(win, text="Export CSV", command=export_csv).pack(pady=5)

# SEARCH
def search_ui():
    win = tk.Toplevel()
    win.title("Search")
    win.geometry("350x300")

    tk.Label(win, text="Search File").pack(pady=10)

    entry = tk.Entry(win)
    entry.pack(pady=5)

    listbox = tk.Listbox(win, width=40)
    listbox.pack(pady=10)

    def search():
        listbox.delete(0, tk.END)

        try:
            with open("data/monitored_files.json") as f:
                files = json.load(f)

            result = search_files(entry.get(), files)

            for item in result:
                listbox.insert(tk.END, item["name"])

        except:
            messagebox.showerror("Error", "No files found")

    tk.Button(win, text="Search", command=search).pack()


# REPORT
def show_report():
    try:
        with open("data/monitored_files.json") as f:
            files = json.load(f)

        report = generate_report(files)

        msg = f"""
Total Files: {report['total_files']}
Largest File: {report['largest_file']}
Common Type: {report['common_extension']}
"""
        messagebox.showinfo("Report", msg)

    except:
        messagebox.showerror("Error", "No files found")


if __name__ == "__main__":
    login_screen()