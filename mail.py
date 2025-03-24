import requests
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import threading

# Backend API Key
API_KEY = "Your_api_key_here"  

def fetch_email_information(domain):
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "emails" in data["data"]:
                email_info_list = []
                for email_info in data["data"]["emails"]:
                    email_details = {
                        "email": email_info.get("value", "N/A"),
                        "first_name": email_info.get("first_name", "N/A"),
                        "last_name": email_info.get("last_name", "N/A"),
                        "position": email_info.get("position", "N/A"),
                        "department": email_info.get("department", "N/A"),
                        "linkedin": email_info.get("linkedin", "N/A"),
                        "source": email_info.get("sources", [{"uri": "N/A"}])[0].get("uri", "N/A"),
                    }
                    email_info_list.append(email_details)
                return email_info_list
            else:
                return [{"error": "No emails found."}]
        else:
            error_message = response.json().get("errors", [{"details": "Unknown error"}])[0]["details"]
            return [{"error": f"Error: {response.status_code} - {error_message}"}]
    except Exception as e:
        return [{"error": f"An error occurred: {str(e)}"}]

def start_email_collection():
    domain = domain_entry.get().strip()

    if not domain:
        messagebox.showerror("Error", "Please enter a domain to search.")
        return

    def email_thread():
        result_text.configure(state='normal')
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Fetching email information...\n")
        result_text.update()
        email_info_list = fetch_email_information(domain)
        result_text.delete(1.0, tk.END)

        result_text.insert(tk.END, f"Email information for {domain}:\n\n")
        for email_info in email_info_list:
            if "error" in email_info:
                result_text.insert(tk.END, f"{email_info['error']}\n\n")
            else:
                result_text.insert(tk.END, f"Email: {email_info['email']}\n")
                result_text.insert(tk.END, f"First Name: {email_info['first_name']}\n")
                result_text.insert(tk.END, f"Last Name: {email_info['last_name']}\n")
                result_text.insert(tk.END, f"Position: {email_info['position']}\n")
                result_text.insert(tk.END, f"Department: {email_info['department']}\n")
                result_text.insert(tk.END, f"LinkedIn: {email_info['linkedin']}\n")
                result_text.insert(tk.END, f"Source: {email_info['source']}\n")
                result_text.insert(tk.END, "-" * 40 + "\n")
        result_text.configure(state='disabled')

    threading.Thread(target=email_thread, daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("Email Information Gathering Tool")
root.geometry("800x600")

# Load Background Image
background_image = Image.open(r"C:\\Users\\prabu\\OneDrive\\Documents\\bg.jpg")
background_image = background_image.resize((1920, 1080), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Title Label
title_label = tk.Label(root, text="Email Information Gathering Tool", font=("Courier", 20, "bold"), bg="#000000", fg="#00FF00")
title_label.pack(pady=10)

# Frame for Inputs
input_frame = tk.Frame(root, bg="#111111", pady=10, padx=10, bd=3, relief="ridge")
input_frame.pack(pady=10, fill="x", padx=20)

# Domain Entry
domain_label = tk.Label(input_frame, text="Domain:", font=("Courier", 12), bg="#111111", fg="#00FF00")
domain_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
domain_entry = tk.Entry(input_frame, width=30, font=("Courier", 12), bg="#222222", fg="#00FF00")
domain_entry.grid(row=0, column=1, padx=10, pady=10)

# Start Button
start_button = tk.Button(root, text="Start Email Collection", font=("Courier", 12, "bold"), bg="#00FF00", fg="#000000", command=start_email_collection)
start_button.pack(pady=10)

# Result Text Area
result_frame = tk.Frame(root, bg="#111111", pady=10, padx=10, bd=3, relief="ridge")
result_frame.pack(pady=10, fill="both", expand=True, padx=20)
result_label = tk.Label(result_frame, text="Results:", font=("Courier", 12), bg="#111111", fg="#00FF00")
result_label.pack(anchor="w", padx=10, pady=5)
result_text = ScrolledText(result_frame, height=10, font=("Courier", 10), bg="#000000", fg="#00FF00", state='disabled', wrap="word")
result_text.pack(fill="both", expand=True, padx=10, pady=5)

root.mainloop()
