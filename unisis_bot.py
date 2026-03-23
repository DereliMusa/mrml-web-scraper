import tkinter as tk
from tkinter import ttk, messagebox
import json
import threading
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class UnisisBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unisis Veri Çekme Botu")
        self.root.geometry("600x400")
        
        # UI Elements
        self.setup_ui()

    def setup_ui(self):
        # URL Input
        url_frame = ttk.Frame(self.root, padding=10)
        url_frame.pack(fill=tk.X)
        
        ttk.Label(url_frame, text="URL:").pack(side=tk.LEFT, padx=5)
        self.url_var = tk.StringVar(value="https://unisis.ege.edu.tr/researcher=oguz.gurses")
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Options
        options_frame = ttk.LabelFrame(self.root, text="Çekilecek Veriler", padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=10)

        self.chk_profil = tk.BooleanVar(value=True)
        self.chk_metrikler = tk.BooleanVar(value=True)
        self.chk_kurum = tk.BooleanVar(value=True)

        ttk.Checkbutton(options_frame, text="Profil", variable=self.chk_profil).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(options_frame, text="Metrikleri", variable=self.chk_metrikler).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(options_frame, text="Kurum Bilgileri", variable=self.chk_kurum).pack(side=tk.LEFT, padx=10)

        # Action Button
        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(fill=tk.X)
        
        self.btn_fetch = ttk.Button(btn_frame, text="Getir", command=self.start_scraping)
        self.btn_fetch.pack(side=tk.RIGHT, padx=5)

        # Status output
        self.status_var = tk.StringVar(value="Hazır.")
        ttk.Label(self.root, textvariable=self.status_var, padding=10).pack(side=tk.BOTTOM, anchor=tk.W)

    def start_scraping(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Hata", "Lütfen bir URL girin.")
            return

        selected_options = {
            "profil": self.chk_profil.get(),
            "metrikler": self.chk_metrikler.get(),
            "kurum": self.chk_kurum.get()
        }

        if not any(selected_options.values()):
            messagebox.showwarning("Hata", "Lütfen en az bir veri alanı seçin.")
            return

        self.btn_fetch.config(state=tk.DISABLED)
        self.status_var.set("Veriler çekiliyor, lütfen bekleyin... (Bu işlem birkaç saniye sürebilir)")
        
        # Run scraping in a separate thread so UI doesn't freeze
        threading.Thread(target=self.scrape_unisis, args=(url, selected_options), daemon=True).start()

    def scrape_unisis(self, url, options):
        driver = None
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            # Use webdriver-manager
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            driver.get(url)
            
            # Wait for content to render (React app usually takes a few seconds)
            time.sleep(5)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            text_lines = soup.get_text(separator='\n', strip=True).split('\n')
            
            # Extract data
            result = {}
            if options["profil"]:
                result["Profil"] = self.extract_block(text_lines, "Profil", "Eğitim bilgileri", limit=10)
            
            if options["metrikler"]:
                result["Metrikleri"] = self.extract_block(text_lines, "Metrikler", "Kurum bilgileri", limit=30)
                
            if options["kurum"]:
                result["Kurum Bilgileri"] = self.extract_block(text_lines, "Kurum bilgileri", "Araştırma alanları", limit=20)
                
            # If our block extract didn't work well due to language or page structure changes, 
            # fallback to returning found items near the keywords
            
            self.root.after(0, self.show_result, result)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Hata", f"Veri çekilirken bir hata oluştu:\n{e}"))
        finally:
            if driver:
                driver.quit()
            self.root.after(0, self.reset_ui_state)

    def extract_block(self, lines, start_keyword, end_keyword, limit):
        # A simple extractor that grabs text lines between a start keyword and an end keyword or limit
        block = []
        capture = False
        count = 0
        for line in lines:
            if start_keyword.lower() == line.lower():
                capture = True
                continue
            if capture:
                if end_keyword and end_keyword.lower() in line.lower():
                    break
                # Only save specific generic metrics instead of garbage
                if line and len(line) > 1:
                    block.append(line)
                count += 1
                if count > limit:
                    break
        return block

    def show_result(self, data):
        result_win = tk.Toplevel(self.root)
        result_win.title("Çekilen Veriler (JSON)")
        result_win.geometry("700x500")

        # Create a text area like a terminal
        text_area = tk.Text(result_win, bg="black", fg="green", font=("Courier", 12))
        text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        text_area.insert(tk.END, json_data)
        text_area.config(state=tk.DISABLED)  # Read-only

    def reset_ui_state(self):
        self.btn_fetch.config(state=tk.NORMAL)
        self.status_var.set("Hazır.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnisisBotApp(root)
    root.mainloop()
