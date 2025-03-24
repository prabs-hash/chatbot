import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk  # Importing Pillow library

# Function to run each script
def run_script(script_name):
    try:
        subprocess.run(['python3', script_name], check=True)
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", f"Failed to run {script_name}")
    else:
        messagebox.showinfo("Success", f"{script_name} ran successfully")

# Main window
root = tk.Tk()
root.title("Cybersecurity Tools")
root.geometry("500x400")
root.config(bg="#2c3e50")  # Set a background color

# Bakground image (JPG format)
bg_image = Image.open("bg.jpg")  # Replace 'bg.jpg' with your JPG image path
bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)  # Resize the image
bg_image_tk = ImageTk.PhotoImage(bg_image)  # Convert to Tkinter compatible format

# Canvas to display the image
canvas = tk.Canvas(root, width=500, height=400)
canvas.pack(fill="both", expand=True)

# Background image on the canvas
canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)

# Frame to hold the buttons and organize them neatly
frame = tk.Frame(root, bg="#2c3e50")
frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

# Title label
title_label = tk.Label(root, text="Information gathering tools", font=("Helvetica", 20, "bold"), fg="#ecf0f1", bg="#2c3e50")
title_label.place(relx=0.5, y=20, anchor="n")  # Position the title label

# Styled buttons
btn_style = {
    'font': ("Arial", 12, "bold"),
    'bg': "#2980b9",
    'fg': "#ecf0f1",
    'width': 40,
    'height': 2,
    'bd': 0,
    'relief': 'flat',
    'activebackground': "#3498db",
    'activeforeground': "#ecf0f1"
}

btn_mail = tk.Button(frame, text="Run Mail Info Gathering", **btn_style, command=lambda: run_script('mail.py'))
btn_mail.grid(row=0, column=0, padx=10, pady=10)

btn_gobuster = tk.Button(frame, text="Run Directory Enumeration", **btn_style, command=lambda: run_script('gobuster.py'))
btn_gobuster.grid(row=1, column=0, padx=10, pady=10)

btn_subdomain = tk.Button(frame, text="Run Subdomain Enumeration", **btn_style, command=lambda: run_script('subdomain.py'))
btn_subdomain.grid(row=2, column=0, padx=10, pady=10)

btn_portgui = tk.Button(frame, text="Run Port Scanning", **btn_style, command=lambda: run_script('portgui.py'))
btn_portgui.grid(row=3, column=0, padx=10, pady=10)

btn_whoisgui = tk.Button(frame, text="Run Whois Info", **btn_style, command=lambda: run_script('whoisgui.py'))
btn_whoisgui.grid(row=4, column=0, padx=10, pady=10)

# Footer with instructions
footer_label = tk.Label(root, text="Select a tool to run from the list above.", font=("Arial", 10), fg="#ecf0f1", bg="#2c3e50")
footer_label.pack(side=tk.BOTTOM, pady=20)

# Tkinter event loop
root.mainloop()
