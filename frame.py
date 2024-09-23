import appV2
import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox

class AppInterface:

    def __init__(self, root):
        self.dic_data = None
        self.root = root
        self.root.title("Amazon Scraper")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Seleccione una opción:")
        self.label.pack(pady=10)

        self.script_button = tk.Button(self.root, text="Scripting", command=self.run_scripting)
        self.script_button.pack(pady=5)

        self.create_csv_button = tk.Button(self.root, text="Create CSV", command=self.create_csv)
        self.create_csv_button.pack(pady=5)

        self.read_csv_button = tk.Button(self.root, text="Read CSV", command=self.read_csv)
        self.read_csv_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=5)

    def run_scripting(self):
        url = "https://www.amazon.com/s?k=samsung&ref=nb_sb_noss"
        end_page = simpledialog.askinteger("Input", "Number of pages:")
        if end_page:
            product = appV2.GetProducts()# Asegúrate de que GetProducts esté definido en app.py
            self.dic_data = product.products_amazon(url, start_page=0, end_page=end_page)
            messagebox.showinfo("Info", "Scripting completed")

    def create_csv(self):
        if hasattr(self, 'dic_data'):
            df = pd.DataFrame(self.dic_data)
            csv_name = simpledialog.askstring("Input", "CSV name:")
            if csv_name:
                df.to_csv(f"{csv_name}.csv", index=False)
                messagebox.showinfo("Info", "CSV created successfully")
        else:
            messagebox.showwarning("Warning", "No data to save. Run scripting first.")

    def read_csv(self):
        csv_name = simpledialog.askstring("Input", "CSV name:")
        if csv_name:
            try:
                df = pd.read_csv(f"{csv_name}.csv")
                messagebox.showinfo("CSV Content", df.to_string())
            except FileNotFoundError:
                messagebox.showerror("Error", "CSV file not found")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppInterface(root)
    root.mainloop()