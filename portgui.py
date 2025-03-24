import socket
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk, ImageFont

def is_port_open(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_ports(host, ports):
    open_ports = []
    closed_ports = []
    for port in ports:
        if is_port_open(host, port):
            open_ports.append(port)
        else:
            closed_ports.append(port)
    return open_ports, closed_ports

def start_scan():
    host = host_entry.get().strip()
    if not host:
        messagebox.showerror("Error", "Please enter a host to scan.")
        return

    scan_type = scan_type_var.get()
    if scan_type == "p":
        ports_input = ports_entry.get().strip()
        try:
            ports = [int(port.strip()) for port in ports_input.split(',')]
        except:
            messagebox.showerror("Error", "Invalid ports entered. Please use comma-separated integers.")
            return
    elif scan_type == "r":
        range_input = ports_entry.get().strip()
        try:
            start_port, end_port = map(int, range_input.split('-'))
            ports = list(range(start_port, end_port + 1))
        except:
            messagebox.showerror("Error", "Invalid range entered. Use the format start-end (e.g., 1-100).")
            return
    else:
        messagebox.showerror("Error", "Please select a valid scan type.")
        return

    result_text.configure(state='normal')
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Scanning...\n")
    result_text.update()
    open_ports, closed_ports = scan_ports(host, ports)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Open ports on {host}: {open_ports}\n")
    result_text.insert(tk.END, f"Closed ports on {host}: {closed_ports}\n")
    result_text.configure(state='disabled')

def on_scan_type_change(*args):
    if scan_type_var.get() == "p":
        ports_label.config(text="Enter Ports (comma-separated):")
    else:
        ports_label.config(text="Enter Port Range (e.g., 1-100):")

# GUI Setup
root = tk.Tk()
root.title("Professional Port Scanner")
root.geometry("600x400")

# Load Background Image
background_image = Image.open(r"C:\Users\prabu\OneDrive\Documents\bg.jpg")
background_image = background_image.resize((1920, 1080), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Load Silkscreen Font
font_path = r"C:\path\to\your\silkscreen.ttf"  # Replace with the actual path to your Silkscreen font
silkscreen_font = ("Courier", 12)  # Fallback if the custom font is not loaded properly

# Title Label
title_label = tk.Label(root, text="Port Scanner", font=("Courier", 20, "bold"), bg="#000000", fg="#00FF00")
title_label.pack(pady=10)

# Frame for Inputs
input_frame = tk.Frame(root, bg="#111111", pady=10, padx=10, bd=3, relief="ridge")
input_frame.pack(pady=10, fill="x", padx=20)

# Host Entry
host_label = tk.Label(input_frame, text="Host:", font=silkscreen_font, bg="#111111", fg="#00FF00")
host_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
host_entry = tk.Entry(input_frame, width=30, font=silkscreen_font, bg="#222222", fg="#00FF00")
host_entry.grid(row=0, column=1, padx=10, pady=10)

# Scan Type Selection
scan_type_var = tk.StringVar(value="p")
scan_type_var.trace("w", on_scan_type_change)

scan_type_label = tk.Label(input_frame, text="Scan Type:", font=silkscreen_font, bg="#111111", fg="#00FF00")
scan_type_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
scan_type_frame = tk.Frame(input_frame, bg="#111111")
scan_type_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
p_type_button = ttk.Radiobutton(scan_type_frame, text="Individual Ports", variable=scan_type_var, value="p")
p_type_button.pack(side="left", padx=5)
r_type_button = ttk.Radiobutton(scan_type_frame, text="Port Range", variable=scan_type_var, value="r")
r_type_button.pack(side="left", padx=5)

# Ports Entry
ports_label = tk.Label(input_frame, text="Enter Ports (comma-separated):", font=silkscreen_font, bg="#111111", fg="#00FF00")
ports_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
ports_entry = tk.Entry(input_frame, width=30, font=silkscreen_font, bg="#222222", fg="#00FF00")
ports_entry.grid(row=2, column=1, padx=10, pady=10)

# Scan Button
scan_button = tk.Button(root, text="Start Scan", font=("Courier", 12, "bold"), bg="#00FF00", fg="#000000", command=start_scan)
scan_button.pack(pady=10)

# Result Text Area
result_frame = tk.Frame(root, bg="#111111", pady=10, padx=10, bd=3, relief="ridge")
result_frame.pack(pady=10, fill="both", expand=True, padx=20)
result_label = tk.Label(result_frame, text="Scan Results:", font=silkscreen_font, bg="#111111", fg="#00FF00")
result_label.pack(anchor="w", padx=10, pady=5)
result_text = ScrolledText(result_frame, height=10, font=("Courier", 10), bg="#000000", fg="#00FF00", state='disabled', wrap="word")
result_text.pack(fill="both", expand=True, padx=10, pady=5)

root.mainloop()
