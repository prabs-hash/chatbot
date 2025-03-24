import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import subprocess
import os

# Function to convert Windows path to WSL path
def convert_to_wsl_path(windows_path):
    # Convert "C:\Users\prabu" to "/mnt/c/Users/prabu"
    wsl_path = windows_path.replace("C:/", "/mnt/c/").replace("\\", "/")
    return wsl_path

# Function to perform the directory brute-forcing with gobuster
def perform_gobuster_scan():
    domain = domain_entry.get().strip()
    if not domain:
        messagebox.showerror("Error", "Please enter a domain to scan.")
        return

    if not wordlist_path.get():
        messagebox.showerror("Error", "Please upload a wordlist file.")
        return

    result_text.configure(state='normal')
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Starting directory brute-forcing for {domain} using wordlist {wordlist_path.get()}...\n")
    result_text.update()

    # Convert Windows path to WSL path
    wsl_wordlist_path = convert_to_wsl_path(wordlist_path.get())

    try:
        # Running gobuster through WSL with converted path
        process = subprocess.Popen(
            ['wsl', 'gobuster', 'dir', '-u', domain, '-w', wsl_wordlist_path, '-t', '10'],  # Using 50 threads for speed
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Read and display the output in the result text area
        for line in process.stdout:
            result_text.insert(tk.END, line)
            result_text.update()

        # Capture and display any errors from stderr
        stderr_output = process.stderr.read()
        if stderr_output:
            result_text.insert(tk.END, f"Error:\n{stderr_output}\n")

    except FileNotFoundError:
        result_text.insert(tk.END, "Error: gobuster tool not found. Make sure gobuster is installed and in your system's PATH.\n")
    except Exception as e:
        result_text.insert(tk.END, f"An unexpected error occurred: {e}\n")

    result_text.configure(state='disabled')

# Function to upload a wordlist file
def upload_wordlist():
    wordlist_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if wordlist_file:
        wordlist_path.set(wordlist_file)
        wordlist_label.config(text=f"Wordlist: {wordlist_file.split('/')[-1]}")

# GUI Setup
root = tk.Tk()
root.title("Directory Bruteforce with Gobuster")
root.geometry("600x500")

# Load Background Image
background_image = Image.open(r"C:\Users\prabu\OneDrive\Documents\bg.jpg")  # Update with your path
background_image = background_image.resize((1920, 1080), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Load Font
silkscreen_font = ("Silkscreen", 12)  # Ensure the font is available or use another font

# Title Label
title_label = tk.Label(root, text="Directory Bruteforce", font=("Silkscreen", 20, "bold"), bg="#000000", fg="#00FF00")
title_label.pack(pady=10)

# Frame for Inputs
input_frame = tk.Frame(root, bg="#111111", pady=10, padx=10, bd=3, relief="ridge")
input_frame.pack(pady=10, fill="x", padx=20)

# Domain Entry
domain_label = tk.Label(input_frame, text="Domain:", font=silkscreen_font, bg="#111111", fg="#00FF00")
domain_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
domain_entry = tk.Entry(input_frame, width=30, font=silkscreen_font, bg="#222222", fg="#00FF00")
domain_entry.grid(row=0, column=1, padx=10, pady=10)

# Wordlist Label & Entry (For Display Purpose)
wordlist_label = tk.Label(input_frame, text="Wordlist: Not selected", font=silkscreen_font, bg="#111111", fg="#00FF00")
wordlist_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Upload Button (Styled as a Pro-Level Button)
upload_button = tk.Button(
    input_frame, 
    text="Upload Wordlist", 
    font=("Silkscreen", 12, "bold"), 
    bg="#00FF00", 
    fg="#000000", 
    command=upload_wordlist,
    relief="solid", 
    bd=3, 
    padx=10, 
    pady=5
)
upload_button.grid(row=1, column=1, padx=10, pady=10)

# Scan Button
scan_button = tk.Button(root, text="Start Brute Force Scan", font=("Silkscreen", 12, "bold"), bg="#00FF00", fg="#000000", command=perform_gobuster_scan)
scan_button.pack(pady=10)

# Result Text Area
result_frame = tk.Frame(root, bg="#111111", pady=10, padx=10, bd=3, relief="ridge")
result_frame.pack(pady=10, fill="both", expand=True, padx=20)
result_label = tk.Label(result_frame, text="Scan Results:", font=silkscreen_font, bg="#111111", fg="#00FF00")
result_label.pack(anchor="w", padx=10, pady=5)
result_text = ScrolledText(result_frame, height=10, font=silkscreen_font, bg="#000000", fg="#00FF00", state='disabled', wrap="word")
result_text.pack(fill="both", expand=True, padx=10, pady=5)

# Tkinter StringVar for storing the wordlist path
wordlist_path = tk.StringVar()

# Run the GUI main loop
root.mainloop()
