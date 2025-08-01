import os
import sys
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog

def getuser():
    user = os.getlogin()  # Get the current user's username.
    user_directory = f"C:/Users/{user}/AppData/Roaming/OrcaSlicer/user" # Define the directory to be archived.
    return user_directory

# Function to get the directory of the executable file
def get_executable_directory():
    return os.path.dirname(sys.executable)

def backup(source_directory, target_directory):
    try:
        if not os.path.exists(source_directory):
            raise FileNotFoundError(f"The source directory {source_directory} does not exist.")
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        outputfile = os.path.join(target_directory, "user-backup-test")  # Define the name of the archive.
        shutil.make_archive(outputfile, 'zip', source_directory)  # Create the zip archive.
        messagebox.showinfo("Backup Complete", f"Backup saved as {outputfile}.zip")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_source_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, folder_selected)

def browse_target_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, folder_selected)

def restore_default_source():
    default_directory = getuser()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, default_directory)

def restore_default_target():
    default_directory = get_executable_directory()
    target_entry.delete(0, tk.END)
    target_entry.insert(0, default_directory)

def on_backup_button_click():
    # Retrieve the directories from the entry widgets
    backup_source_directory = source_entry.get()
    backup_target_directory = target_entry.get()

    # Check if directories have been selected
    if not backup_source_directory or not backup_target_directory:
        messagebox.showwarning("Warning", "Please select both a source and target directory first!")
        return

    # Extract the last folder name from the path
    last_folder_name = os.path.basename(os.path.normpath(backup_source_directory))
    if last_folder_name == "user":
        backup(backup_source_directory, backup_target_directory)
    else:
        messagebox.showwarning("Warning", "Please select a valid source directory. It has to contain the folder <user>")

# Create the main window
root = tk.Tk()
root.title("OrcaSlicer Backup Utility v1.0 - by LaVitae")
root.resizable(False, False)

# Set the width and height of the window
window_width = 650
window_height = 165

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the window
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the geometry of the window
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Frame to hold the directory selection widgets for source
source_frame = tk.Frame(root)
source_frame.pack(padx=5, pady=7)

# Label for the source directory path entry
source_label = tk.Label(source_frame, text="Source directory:")
source_label.grid(row=0, column=0, padx=(0, 5))

# Entry widget to display and edit the source directory path with default value from getuser()
default_source_directory = getuser()
source_entry = tk.Entry(source_frame, width=60)
source_entry.insert(0, default_source_directory)
source_entry.grid(row=0, column=1, padx=(0, 5))

# Browse button for source
browse_source_button = tk.Button(source_frame, text="Browse...", command=browse_source_directory)
browse_source_button.grid(row=0, column=2, padx=(0, 10))
# "Restore default" button for source
restore_source_button = tk.Button(source_frame, text="Restore default", command=restore_default_source)
restore_source_button.grid(row=0, column=3)

# Frame to hold the directory selection widgets for target
target_frame = tk.Frame(root)
target_frame.pack(padx=5, pady=7)

# Label for the target directory path entry
target_label = tk.Label(target_frame, text="Target directory:")
target_label.grid(row=1, column=0, padx=(0, 5))

# Entry widget to display and edit the target directory path with default value as script location
default_target_directory = get_executable_directory()
target_entry = tk.Entry(target_frame, width=60)
target_entry.insert(0, default_target_directory)
target_entry.grid(row=1, column=1, padx=(0, 5))

# Browse button for target
browse_target_button = tk.Button(target_frame, text="Browse...", command=browse_target_directory)
browse_target_button.grid(row=1, column=2, padx=(0, 10))

# "Restore default" button for target
restore_target_button = tk.Button(target_frame, text="Restore default", command=restore_default_target)
restore_target_button.grid(row=1, column=3)

# Labels to guide the user
label = tk.Label(root, text="Click the button to back up your OrcaSlicer user data from the source directory to the target directory listed above.")
label.pack(pady=(10, 0))

# Backup button
backup_button = tk.Button(root, text="Backup", command=on_backup_button_click)
backup_button.pack(pady=(10,0))

# Run the application
root.mainloop()