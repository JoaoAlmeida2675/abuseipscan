import tkinter as tk
import re
import requests
import tkinter.filedialog as filedialog
from tkinter import messagebox


class AbuseIpScanner:
    api_key = None


def save_api_key():
    # Save the API key
    AbuseIpScanner.api_key = api_key_entry.get()
    api_key_window.destroy()


def enter_api_key():
    # Create a window for the user to enter their API key
    global api_key_window
    api_key_window = tk.Toplevel(window)
    api_key_window.geometry("250x100")
    api_key_window.title("API KEY")
    api_key_label = tk.Label(api_key_window, text="Enter your Abuseipdb API key:")
    api_key_label.pack()
    global api_key_entry
    api_key_entry = tk.Entry(api_key_window)
    api_key_entry.pack()
    save_api_key_button = tk.Button(api_key_window, text="Save", command=save_api_key)
    save_api_key_button.pack()


# Function to open a file
def open_file():
    filepath = filedialog.askopenfilename()
    global ips
    with open(filepath, 'r') as file:
        ips = file.read()
    ips = re.findall(r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}', ips)
    ips = list(set(ips))


def search_ips_button_clicked():
    # Clear the previous IP list
    ip_list_box.delete(0, tk.END)
    for ip in ips:
        try:
            response = requests.get(f'https://api.abuseipdb.com/api/v2/check',
                                    params={'ipAddress': ip, 'maxAgeInDays': 90},
                                    headers={'Key': AbuseIpScanner.api_key})
            data = response.json()
        except:
            ip_list_box.insert(tk.END, f'{ip} - API request error')
            return
        if data["data"]["abuseConfidenceScore"] >= 50:
            ip_list_box.insert(tk.END, f'{ip} - IP flagged as suspicious')


def save_to_file():
    # Ask user where they want to save the file
    filepath = tk.filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    # Open the file for writing and write the flagged IPs to it
    with open(filepath, "w") as file:
        for ip in ip_list_box.get(0, tk.END):
            if "suspicious" in ip:
                file.write(ip + "\n")

    # Inform the user that the file was saved
    messagebox.showinfo("Save to File", "File saved successfully!")


def close_button_clicked():
    window.destroy()


if __name__ == '__main__':
    # Create the main window
    window = tk.Tk()
    window.title("Abuse IP Scanner")
    window.geometry("500x400")
    window.configure(bg='lightblue')
    window.resizable(True, True)

    # Create the API key button
    enter_api_key_button = tk.Button(window, text="API KEY", command=enter_api_key)
    enter_api_key_button.pack()

    # Create the Open File button
    open_file_button = tk.Button(window, text="Choose File", command=open_file)
    open_file_button.pack()

    # Create the Search IPs button
    search_ips_button = tk.Button(window, text="Search AbuseIp", command=search_ips_button_clicked)
    search_ips_button.pack()

    # Create the IP list box
    global ip_list_box
    ip_list_box = tk.Listbox(window, width="45", height="15")
    ip_list_box.pack()

    # Create the Save to File button
    save_to_file_button = tk.Button(window, text="Save File", command=save_to_file)
    save_to_file_button.pack()

    # Create the Close button
    close_button = tk.Button(window, text="Close", command=close_button_clicked)
    close_button.pack()

    # Run the main loop.
    window.mainloop()
