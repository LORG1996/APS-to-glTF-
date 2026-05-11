import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import subprocess
import os
import threading

class ForgeConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("APS (Forge) to glTF Converter")
        self.root.geometry("700x750")
        self.root.configure(bg="#2c3e50")

        label_style = {"bg": "#2c3e50", "fg": "white", "font": ("Arial", 10, "bold")}

        # --- Top Panel with Help Button ---
        help_frame = tk.Frame(root, bg="#34495e", pady=5)
        help_frame.pack(fill=tk.X)
        tk.Button(help_frame, text="❓ How to get URN and Token?", command=self.show_guide, 
                  bg="#3498db", fg="white", font=("Arial", 9, "bold")).pack(pady=5)

        # Input Fields
        tk.Label(root, text="Access Token:", **label_style).pack(pady=(10, 0))
        self.token_entry = tk.Entry(root, width=80)
        self.token_entry.pack(pady=5)
        
        tk.Label(root, text="Model URN (Base64):", **label_style).pack(pady=(10, 0))
        self.urn_entry = tk.Entry(root, width=80)
        self.urn_entry.pack(pady=5)

        tk.Label(root, text="Output Directory:", **label_style).pack(pady=(10, 0))
        self.path_entry = tk.Entry(root, width=60)
        self.path_entry.insert(0, os.getcwd())
        self.path_entry.pack(pady=5)
        tk.Button(root, text="📁 Browse Folder", command=self.browse_folder).pack()

        # Log Window
        tk.Label(root, text="Process Log:", **label_style).pack(pady=(10, 0))
        self.log_area = scrolledtext.ScrolledText(root, width=80, height=18, bg="#1e272e", fg="#d2dae2", font=("Consolas", 9))
        self.log_area.pack(pady=10)

        # Start Button
        self.convert_btn = tk.Button(
            root, text="🚀 START CONVERSION", 
            command=self.start_thread,
            bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
            padx=40, pady=15
        )
        self.convert_btn.pack(pady=10)

        # Add clipboard support to all fields
        for e in [self.token_entry, self.urn_entry, self.path_entry]:
            self.add_clipboard_support(e)

    def show_guide(self):
        """Instructions Window"""
        guide_window = tk.Toplevel(self.root)
        guide_window.title("Guide: Where to get the data?")
        guide_window.geometry("600x520")
        guide_window.configure(bg="#ecf0f1")
        
        text_guide = scrolledtext.ScrolledText(guide_window, wrap=tk.WORD, font=("Arial", 10), padx=10, pady=10)
        text_guide.pack(expand=True, fill=tk.BOTH)
        
        instructions = """📌 HOW TO GET DATA FROM BROWSER (F12)

1. Open the model in Autodesk Viewer / BIM 360 / ACC.
2. Press F12 (Developer Console).

---
🔑 HOW TO FIND URN:
Option A (via Console):
Paste this code into the console and press Enter:
NOP_VIEWER.model.getData().urn

Option B (via Network tab):
- Go to the 'Network' tab.
- Type 'metadata' or 'urn' in the filter.
- Refresh the page (F5).
- Look for a string starting with 'dXJuOm...'

---
🎫 HOW TO FIND TOKEN:
1. In the 'Network' tab, find any request to 'developer.api.autodesk.com'.
2. Click on it, go to the 'Headers' section.
3. Look for 'Request Headers' -> 'Authorization'.
4. Copy the long text AFTER the word 'Bearer'.
   (Example: Bearer eyJhbGci... -> copy only eyJhbGci...)

⚠️ Reminder: Tokens usually expire after 60 minutes!
"""
        text_guide.insert(tk.END, instructions)
        text_guide.config(state=tk.DISABLED)

    def log(self, text):
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.see(tk.END)

    def start_thread(self):
        thread = threading.Thread(target=self.run_conversion)
        thread.start()

    def run_conversion(self):
        token = self.token_entry.get().strip()
        urn = self.urn_entry.get().strip()
        output_dir = self.path_entry.get().strip()
        script_path = os.path.join("node_modules", "forge-convert-utils", "bin", "forge-convert.js")

        if not os.path.exists(script_path):
            messagebox.showerror("Error", "node_modules not found! Make sure the folder is next to this program.")
            return

        if not token or not urn:
            messagebox.showerror("Error", "Please provide both Token and URN.")
            return

        self.convert_btn.config(state=tk.DISABLED)
        self.log("--- Conversion Started ---")
        
        env = os.environ.copy()
        env["FORGE_ACCESS_TOKEN"] = token

        try:
            process = subprocess.Popen(
                ["node", script_path, urn, "--output", output_dir, "--gltf"],
                env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                text=True, shell=True
            )

            for line in process.stdout:
                self.log(line.strip())
            
            process.wait()
            if process.returncode == 0:
                self.log("--- SUCCESS! ---")
                messagebox.showinfo("Done", "Model converted successfully!")
            else:
                self.log(f"--- FAILED (Exit Code: {process.returncode}) ---")
        except Exception as e:
            self.log(f"System Error: {str(e)}")
        
        self.convert_btn.config(state=tk.NORMAL)

    def add_clipboard_support(self, entry):
        entry.bind("<Control-v>", lambda e: entry.event_generate("<<Paste>>"))
        entry.bind("<Control-c>", lambda e: entry.event_generate("<<Copy>>"))
        entry.bind("<Control-a>", lambda e: self.select_all(entry))
        entry.bind("<Control-KeyPress>", self.handle_control_keys)

    def handle_control_keys(self, event):
        if event.state & 4:
            if event.keycode == 86: # V key
                event.widget.event_generate("<<Paste>>")
                return "break"
            elif event.keycode == 67: # C key
                event.widget.event_generate("<<Copy>>")
                return "break"
            elif event.keycode == 65: # A key
                self.select_all(event.widget)
                return "break"

    def select_all(self, widget):
        widget.selection_range(0, tk.END)
        widget.icursor(tk.END)
        return "break"

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)

if __name__ == "__main__":
    root = tk.Tk()
    app = ForgeConverterGUI(root)
    root.mainloop()