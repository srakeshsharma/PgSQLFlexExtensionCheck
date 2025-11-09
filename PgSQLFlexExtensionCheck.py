import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psycopg2
import csv
import os

# Start with an empty set; will be populated from CSV
azure_supported_extensions = set()

def load_azure_extensions_from_csv():
    
    global azure_supported_extensions
    file_path = filedialog.askopenfilename(
        title="Select Azure Extensions CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not file_path:
        return  # user cancelled

    try:
        extensions = set()
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            # Read first row to check if header is present
            first_row = next(reader, None)
            if first_row is None:
                raise ValueError("CSV is empty.")
            first_cell = first_row[0].strip()
            # If first cell looks like a header (e.g., "Extension"), skip it
            if first_cell.lower() == "extension" or not first_cell.replace("_", "").replace("-", "").isalnum():
                # process remaining rows as data
                for row in reader:
                    if row:
                        ext = row[0].strip()
                        if ext:
                            extensions.add(ext.lower())
            else:
                # first row is data; include it
                if first_cell:
                    extensions.add(first_cell.lower())
                for row in reader:
                    if row:
                        ext = row[0].strip()
                        if ext:
                            extensions.add(ext.lower())

        azure_supported_extensions = extensions
        lbl_csv_status.config(text=f"Loaded {len(azure_supported_extensions)} extensions")
        messagebox.showinfo("Loaded", f"Loaded {len(azure_supported_extensions)} extensions from:\n{os.path.basename(file_path)}")

    except Exception as ex:
        messagebox.showerror("Error loading CSV", str(ex))

def check_extensions():
    host = host_entry.get().strip()
    port = port_entry.get().strip()
    database = db_entry.get().strip()
    user = user_entry.get().strip()
    password = pwd_entry.get()

    if not host:
        messagebox.showwarning("Input Required", "Please provide the Host.")
        return

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=host, port=port or "5432", database=database or "postgres", user=user, password=password
        )
        cursor = conn.cursor()

        # Query installed extensions
        cursor.execute("SELECT extname, extversion FROM pg_extension ORDER BY extname;")
        results = cursor.fetchall()

        # Clear previous results
        for row in tree.get_children():
            tree.delete(row)

        # Insert new results
        for extname, extversion in results:
            # Compare case-insensitively
            status = "✅ Supported" if extname.lower() in azure_supported_extensions else "❌ Not Supported"
            tree.insert("", "end", values=(extname, extversion, status))

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("PostgreSQL Extension Checker - Developed by Rakesh Sharma")
root.geometry("620x520")

# Input fields
tk.Label(root, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
host_entry = tk.Entry(root, width=40)
host_entry.insert(0, "localhost")
host_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(root, text="Port:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
port_entry = tk.Entry(root, width=40)
port_entry.insert(0, "5432")
port_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(root, text="Database:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
db_entry = tk.Entry(root, width=40)
db_entry.insert(0, "postgres")
db_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

tk.Label(root, text="User:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
user_entry = tk.Entry(root, width=40)
user_entry.insert(0, "postgres")
user_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

tk.Label(root, text="Password:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
pwd_entry = tk.Entry(root, show="*", width=40)
pwd_entry.insert(0, "c0NNECT@@8819")
pwd_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

# CSV loader button and status
btn_load_csv = tk.Button(root, text="Load Azure Extensions CSV", command=load_azure_extensions_from_csv)
btn_load_csv.grid(row=5, column=0, columnspan=1, padx=5, pady=8, sticky="e")

lbl_csv_status = tk.Label(root, text="No CSV loaded", anchor="w")
lbl_csv_status.grid(row=5, column=1, padx=5, pady=8, sticky="w")

# Check button
check_button = tk.Button(root, text="Check Extensions", command=check_extensions, width=30)
check_button.grid(row=6, column=0, columnspan=2, pady=10)

# Results Table
columns = ("Extension", "Version", "Azure Support")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180 if col == "Extension" else 120, anchor="w")
tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Make the# Make the grid expand nicely
root.grid_rowconfigure(7, weight=1)
root.grid_columnconfigure(1, weight=1)
root.mainloop()
