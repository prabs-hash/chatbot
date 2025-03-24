import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import whois
import subprocess 

def fetch_whois_info(): 
    domain = domain_entry.get().strip()
    if not domain:
        messagebox.showerror("Error", "Please enter a domain to fetch WHOIS information.")
        return

    result_text.configure(state='normal')
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Fetching WHOIS information...\n")
    result_text.update()

    try:
        whois_data = whois.whois(domain)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"WHOIS Information for {domain}:\n")
        for key, value in whois_data.items():
            result_text.insert(tk.END, f"{key}: {value}\n")
    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Failed to fetch WHOIS information. Error: {e}\n")

    result_text.configure(state='disabled')

# GUI Setup
root = tk.Tk()
root.title("WHOIS Information Fetcher")
root.geometry("600x400")

# Load Background Image
background_image = Image.open(r"C:\Users\prabu\OneDrive\Documents\bg.jpg")  
background_image = background_image.resize((1920, 1080), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Load Font
font_path = r"C:\Users\prabu\Downloads\Oswald,Silkscreen\Silkscreen\Silkscreen-Bold.ttf" 
silkscreen_font = ("Courier", 12)  

# Title Label
title_label = tk.Label(root, text="WHOIS Information", font=("Courier", 20, "bold"), bg="#000000", fg="#00FF00")
title_label.pack(pady=10)

# Frame for Inputs
input_frame = tk.Frame(root, bg="#111111", pady=10, padx=10, bd=3, relief="ridge")
input_frame.pack(pady=10, fill="x", padx=20)

# Domain Entry
domain_label = tk.Label(input_frame, text="Domain:", font=silkscreen_font, bg="#111111", fg="#00FF00")
domain_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
domain_entry = tk.Entry(input_frame, width=30, font=silkscreen_font, bg="#222222", fg="#00FF00")
domain_entry.grid(row=0, column=1, padx=10, pady=10)

# Fetch Button
fetch_button = tk.Button(root, text="Fetch WHOIS Info", font=("Courier", 12, "bold"), bg="#00FF00", fg="#000000", command=fetch_whois_info)
fetch_button.pack(pady=10)

# Result Text Area
result_frame = tk.Frame(root, bg="#111111", pady=10, padx=10, bd=3, relief="ridge")
result_frame.pack(pady=10, fill="both", expand=True, padx=20)
result_label = tk.Label(result_frame, text="WHOIS Results:", font=silkscreen_font, bg="#111111", fg="#00FF00")
result_label.pack(anchor="w", padx=10, pady=5)
result_text = ScrolledText(result_frame, height=10, font=("Courier", 10), bg="#000000", fg="#00FF00", state='disabled', wrap="word")
result_text.pack(fill="both", expand=True, padx=10, pady=5)

root.mainloop()
