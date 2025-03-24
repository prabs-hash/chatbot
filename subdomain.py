import socket
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from concurrent.futures import ThreadPoolExecutor
import threading  # Missing import added

def resolve_subdomain(domain, subdomain, results):
    """Resolve a single subdomain."""
    full_domain = f"{subdomain}.{domain}"
    try:
        socket.gethostbyname(full_domain)
        results.append(full_domain)
    except socket.gaierror:
        pass

def enumerate_subdomains(domain, subdomain_list):
    """Perform concurrent subdomain resolution."""
    results = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(resolve_subdomain, domain, subdomain, results) for subdomain in subdomain_list]
        for future in futures:
            future.result()
    return results

def start_subdomain_enumeration():
    """Start subdomain enumeration with threading."""
    domain = domain_entry.get().strip()
    if not domain:
        messagebox.showerror("Error", "Please enter a domain to enumerate.")
        return

    if not subdomain_list:
        messagebox.showerror("Error", "Please upload a valid wordlist file.")
        return

    def subdomain_thread():
        result_text.configure(state='normal')
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Enumerating subdomains...\n")
        result_text.update()

        found_subdomains = enumerate_subdomains(domain, subdomain_list)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Found subdomains for {domain}:\n")
        result_text.insert(tk.END, '\n'.join(found_subdomains) + "\n")
        result_text.configure(state='disabled')

    # Run enumeration in a separate thread to keep the GUI responsive
    threading.Thread(target=subdomain_thread, daemon=True).start()

def upload_wordlist():
    """Upload and load the wordlist."""
    global subdomain_list
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'r') as f:
                subdomain_list = f.read().strip().split('\n')
                wordlist_label.config(text=f"Wordlist Loaded: {file_path.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the wordlist: {e}")

# Initialize the global subdomain list
subdomain_list = []

# GUI Setup
root = tk.Tk()
root.title("Subdomain Enumeration Tool")
root.geometry("800x600")

# Load Background Image
background_image = Image.open(r"C:\\Users\\prabu\\OneDrive\\Documents\\bg.jpg")
background_image = background_image.resize((1920, 1080), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Title Label
title_label = tk.Label(root, text="Subdomain Enumeration Tool", font=("Courier", 20, "bold"), bg="#000000", fg="#00FF00")
title_label.pack(pady=10)

# Frame for Inputs
input_frame = tk.Frame(root, bg="#111111", pady=10, padx=10, bd=3, relief="ridge")
input_frame.pack(pady=10, fill="x", padx=20)

# Domain Entry
domain_label = tk.Label(input_frame, text="Domain:", font=("Courier", 12), bg="#111111", fg="#00FF00")
domain_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
domain_entry = tk.Entry(input_frame, width=30, font=("Courier", 12), bg="#222222", fg="#00FF00")
domain_entry.grid(row=0, column=1, padx=10, pady=10)

# Wordlist Upload
wordlist_label = tk.Label(input_frame, text="Wordlist: Not loaded", font=("Courier", 12), bg="#111111", fg="#00FF00")
wordlist_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
upload_button = tk.Button(input_frame, text="Upload Wordlist", font=("Courier", 12, "bold"), bg="#00FF00", fg="#000000", command=upload_wordlist)
upload_button.grid(row=1, column=1, padx=10, pady=10)

# Start Button
start_button = tk.Button(root, text="Start Subdomain Enumeration", font=("Courier", 12, "bold"), bg="#00FF00", fg="#000000", command=start_subdomain_enumeration)
start_button.pack(pady=10)

# Result Text Area
result_frame = tk.Frame(root, bg="#111111", pady=10, padx=10, bd=3, relief="ridge")
result_frame.pack(pady=10, fill="both", expand=True, padx=20)
result_label = tk.Label(result_frame, text="Results:", font=("Courier", 12), bg="#111111", fg="#00FF00")
result_label.pack(anchor="w", padx=10, pady=5)
result_text = ScrolledText(result_frame, height=10, font=("Courier", 10), bg="#000000", fg="#00FF00", state='disabled', wrap="word")
result_text.pack(fill="both", expand=True, padx=10, pady=5)

root.mainloop()
