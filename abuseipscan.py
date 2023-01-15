import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import requests
import re


class AbuseIpScanner:
    """
    This class holds the API key for the Abuse IP Scanner
    """
    api_key = None


def save_api_key():
    """
    Save the API key
    """
    AbuseIpScanner.api_key = API_KEY_ENTRY.get()
    API_KEY_WINDOW.destroy()


def enter_api_key():
    """
    Create a window for the user to enter their API key
    """
    global API_KEY_WINDOW
    API_KEY_WINDOW = tk.Toplevel(window)
    API_KEY_WINDOW.geometry("250x100")
    API_KEY_WINDOW.title("API KEY")
    api_key_label = tk.Label(API_KEY_WINDOW, text="Enter your Abuseipdb API key:")
    api_key_label.pack()
    global API_KEY_ENTRY
    API_KEY_ENTRY = tk.Entry(API_KEY_WINDOW)
    API_KEY_ENTRY.pack()
    save_api_key_button = tk.Button(API_KEY_WINDOW, text="Save", command=save_api_key)
    save_api_key_button.pack()


# Function to open a file.
def open_file():
    """
    Open a file
    """
    filepath = filedialog.askopenfilename()
    global IPS
    with open(filepath, 'r', encoding='utf-8') as file:
        IPS = file.read()
    IPS = re.findall(r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}', IPS)
    IPS = list(set(IPS))


def search_ips_button_clicked():
    """
    Search the IPs in the file
    """
    # Clear the previous IP list
    IP_LIST_BOX.delete(0, tk.END)
    for ip in IPS:
        try:
            response = requests.get(f'https://api.abuseipdb.com/api/v2/check',
                                    params={'ipAddress': ip, 'maxAgeInDays': 90},
                                    headers={'Key': AbuseIpScanner.api_key}, timeout=5)
            data = response.json()
        except requests.exceptions.RequestException as e:
            IP_LIST_BOX.insert(tk.END, f'{ip} - API request error')
            return
        if data["data"]["abuseConfidenceScore"] >= 50:
            IP_LIST_BOX.insert(tk.END, f'{ip} - IP flagged as suspicious')


def save_to_file():
    """
    Save the flagged IPs to a file
    """
    # Ask user where they want to save the file
    filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    # Open the file for writing and write the flagged IPs to it
    with open(filepath, "w", encoding='utf-8') as file:
        for ip in IP_LIST_BOX.get(0, tk.END):
            if "suspicious" in ip:
                file.write(ip + "\n")

    # Inform the user that the file was saved
    messagebox.showinfo("Save to File", "File saved successfully!")


def close_button_clicked():
    """
    Close the main window
    """
    window.destroy()


if __name__ == '__main__':
    # Create the main window
    window = tk.Tk()
    window.title("Abuse IP Scanner")
    window.geometry("500x500")
    window.configure(bg='lightblue')
    window.resizable(True, True)

    # Create the API key button
    enter_api_key_button = tk.Button(window, text="API KEY", command=enter_api_key)
    enter_api_key_button.pack()

    # Create the Open File button
    open_file_button = tk.Button(window, text="Choose File", command=open_file)
    open_file_button.pack()

    # Create the Search IPs button
    search_ips_button = tk.Button(window, text="Search Abusedb", command=search_ips_button_clicked)
    search_ips_button.pack()

    # Create the IP list box
    IP_LIST_BOX = tk.Listbox(window, height=20, width=35)
    IP_LIST_BOX.pack()

    # Create the Save to File button
    save_to_file_button = tk.Button(window, text="Save to File", command=save_to_file)
    save_to_file_button.pack()

    # Create the Close button
    close_button = tk.Button(window, text="Close", command=close_button_clicked)
    close_button.pack()

    # Start the main event loop
    window.mainloop()
