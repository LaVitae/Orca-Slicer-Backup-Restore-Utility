import os
import sys
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog

def getuser():
    user = os.getlogin()  # Get the current user's username.
    user_directory = f"C:/Users/{user}/AppData/Roaming/OrcaSlicer/user" # Define the directory to be restored to.
    return user_directory

# Function to get the directory of the executable file
def get_executable_directory():
    return os.path.dirname(sys.executable)

def restore(source_archive, target_directory):
        shutil.unpack_archive(source_archive, target_directory)  # Extract the zip archive.
        messagebox.showinfo("Restore Complete", f"Data restored to {target_directory}")

def browse_source_file():
    file_selected = filedialog.askopenfilename(filetypes=[('Zip files', '*.zip')])
    if file_selected:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, file_selected)

def browse_target_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, folder_selected)

def restore_default_source():
    default_directory = get_executable_directory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, "Choose .zip file")

def restore_default_target():
    default_directory = getuser()
    target_entry.delete(0, tk.END)
    target_entry.insert(0, default_directory)

def on_restore_button_click():
    # Retrieve the directories from the entry widgets
    restore_source_file_path = source_entry.get()
    restore_target_directory_path = target_entry.get()

    # Check if files and directories have been selected
    if not restore_source_file_path or not restore_target_directory_path:
        messagebox.showwarning("Warning", "Please select both a source file and target directory first!")
        return

    # Check if the source file is a zip file
    if not os.path.isfile(restore_source_file_path) or not restore_source_file_path.endswith('.zip'):
        messagebox.showwarning("Warning", "The selected source file must be a .zip file!")
        return

    restore(restore_source_file_path, restore_target_directory_path)

# Create the main window
root = tk.Tk()
root.title("OrcaSlicer Restore Utility v1.0 - by LaVitae")
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

# Frame to hold the file selection widgets for source
source_frame = tk.Frame(root)
source_frame.pack(padx=5, pady=7)

# Label for the source file path entry
source_label = tk.Label(source_frame, text="Source file:", width=12, anchor='w')
source_label.grid(row=0, column=0, padx=(0, 5))

# Entry widget to display and edit the source file path with default value from get_executable_directory()
default_source_file_path = "Choose .zip file"
source_entry = tk.Entry(source_frame, width=60)
source_entry.insert(0, default_source_file_path)
source_entry.grid(row=0, column=1, padx=(0, 5))

# Browse button for source
browse_source_button = tk.Button(source_frame, text="Browse...", command=browse_source_file)
browse_source_button.grid(row=0, column=2, padx=(0, 10))
# "Restore default" button for source
restore_source_button = tk.Button(source_frame, text="Restore default", command=restore_default_source)
restore_source_button.grid(row=0, column=3)

# Frame to hold the directory selection widgets for target
target_frame = tk.Frame(root)
target_frame.pack(padx=5, pady=7)

# Label for the target directory path entry
target_label = tk.Label(target_frame, text="Target directory:", width=12, anchor='w')
target_label.grid(row=0, column=0, padx=(0, 5))

# Entry widget to display and edit the target directory path with default value as user directory from getuser()
default_target_directory = getuser()
target_entry = tk.Entry(target_frame, width=60)
target_entry.insert(0, default_target_directory)
target_entry.grid(row=0, column=1, padx=(0, 5))

# Browse button for target
browse_target_button = tk.Button(target_frame, text="Browse...", command=browse_target_directory)
browse_target_button.grid(row=0, column=2, padx=(0, 10))

# "Restore default" button for target
restore_target_button = tk.Button(target_frame, text="Restore default", command=restore_default_target)
restore_target_button.grid(row=0, column=3)

# Labels to guide the user
label = tk.Label(root, text="Click the button to restore your OrcaSlicer user data from the source file to the target directory listed above.")
label.pack(pady=(10, 0))

# Restore button
restore_button = tk.Button(root, text="Restore", command=on_restore_button_click)
restore_button.pack(pady=(10,0))

# Run the application
root.mainloop()