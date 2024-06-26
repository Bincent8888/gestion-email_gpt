import tkinter as tk
from tkinter import filedialog, messagebox

class ScraperApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Web Scraper")

        self.url_label = tk.Label(master, text="URL:")
        self.url_label.grid(row=0, column=0, padx=5, pady=5)

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        self.scrape_button = tk.Button(master, text="Scrape", command=self.scrape_data)
        self.scrape_button.grid(row=1, column=1, padx=5, pady=5)

    def scrape_data(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file_path:
            return

        scrape_and_save(url, file_path)

def scrape_and_save(url, file_path):
    import requests
    from bs4 import BeautifulSoup
    import csv

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to retrieve webpage: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    data = []

    for item in soup.select('some_selector'):  # Change 'some_selector' to the actual CSS selector
        name = item.select_one('name_selector').text.strip()  # Change 'name_selector' to the actual CSS selector for names
        email = item.select_one('email_selector').text.strip()  # Change 'email_selector' to the actual CSS selector for emails
        phone = item.select_one('phone_selector').text.strip()  # Change 'phone_selector' to the actual CSS selector for phone numbers
        data.append([name, email, phone])

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Email', 'Phone'])
        writer.writerows(data)

    messagebox.showinfo("Success", f"Data saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()
