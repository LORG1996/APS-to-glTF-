import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import subprocess
import os
import threading
import requests
import json

class ForgeConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("APS (Forge) to glTF Converter - Fixed v2.1")
        self.root.geometry("700x650")
        self.root.configure(bg="#2c3e50")

        label_style = {"bg": "#2c3e50", "fg": "white", "font": ("Arial", 10, "bold")}

        # Access Token
        tk.Label(root, text="Access Token:", **label_style).pack(pady=(10, 0))
        self.token_entry = tk.Entry(root, width=80)
        self.token_entry.pack(pady=5)
        
        # Model URN (з автоматичним очищенням)
        tk.Label(root, text="Model URN:", **label_style).pack(pady=(10, 0))
        self.urn_entry = tk.Entry(root, width=80)
        self.urn_entry.pack(pady=5)

        # Path
        tk.Label(root, text="Output Directory:", **label_style).pack(pady=(10, 0))
        self.path_entry = tk.Entry(root, width=60)
        self.path_entry.insert(0, os.getcwd())
        self.path_entry.pack(pady=5)
        tk.Button(root, text="Browse Folder", command=self.browse_folder).pack()

        # Log Area
        tk.Label(root, text="Process Log:", **label_style).pack(pady=(10, 0))
        self.log_area = scrolledtext.ScrolledText(root, width=80, height=15, bg="#1e272e", fg="#d2dae2", font=("Consolas", 9))
        self.log_area.pack(pady=10)

        # Main Button
        self.convert_btn = tk.Button(
            root, text="START CONVERSION",
            command=self.start_thread,
            bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
            padx=20, pady=10
        )
        self.convert_btn.pack(pady=10)

        self.add_clipboard_support(self.token_entry)
        self.add_clipboard_support(self.urn_entry)

    def log(self, text):
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.see(tk.END)

    def sanitize_urn(self, urn):
        """Видаляє дублікати URN, якщо вони склеїлися при вставці"""
        urn = urn.strip()
        # Якщо URN містить dXJuOm... посередині ще раз, відрізаємо другу частину
        parts = urn.split("dXJuOm")
        if len(parts) > 2:
            fixed_urn = "dXJuOm" + parts[1]
            return fixed_urn
        return urn

    def start_thread(self):
        self.convert_btn.config(state=tk.DISABLED, bg="#95a5a6")
        self.log_area.delete(1.0, tk.END)
        thread = threading.Thread(target=self.run_conversion, daemon=True)
        thread.start()

    def run_conversion(self):
        token = self.token_entry.get().strip()
        raw_urn = self.urn_entry.get().strip()
        urn = self.sanitize_urn(raw_urn) # Очищуємо від дублів
        base_output_dir = self.path_entry.get().strip()
        
        script_path = os.path.join("node_modules", "forge-convert-utils", "bin", "forge-convert.js")

        if not token or not urn:
            messagebox.showwarning("Warning", "Token or URN field is empty!")
            self.convert_btn.config(state=tk.NORMAL, bg="#27ae60")
            return

        # 1. Створення папки
        safe_urn = urn.replace(":", "_").replace("/", "_")[-20:] 
        model_dir = os.path.join(base_output_dir, f"export_{safe_urn}")

        try:
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            
            self.log(f"--- Process Started ---")
            self.log(f"Using URN: {urn}")
            self.log("Fetching manifest...")

            headers = {"Authorization": f"Bearer {token}"}
            manifest_url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/manifest"
            
            response = requests.get(manifest_url, headers=headers)

            if response.status_code == 200:
                manifest_path = os.path.join(model_dir, "manifest.json")
                with open(manifest_path, "w", encoding="utf-8") as f:
                    json.dump(response.json(), f, indent=4)
                self.log("✅ Manifest saved.")
            elif response.status_code == 401:
                self.log("❌ ERROR 401: Token is invalid or expired. Get a new one!")
                self.convert_btn.config(state=tk.NORMAL, bg="#c0392b")
                return
            else:
                self.log(f"❌ API Error: {response.status_code}")
                self.log(response.text)
                self.convert_btn.config(state=tk.NORMAL, bg="#c0392b")
                return

        except Exception as e:
            self.log(f"System Error: {str(e)}")
            self.convert_btn.config(state=tk.NORMAL, bg="#c0392b")
            return

        # 2. Конвертація
        self.log("--- Converting to glTF (Node.js) ---")
        env = os.environ.copy()
        env["FORGE_ACCESS_TOKEN"] = token

        try:
            # shell=True потрібен на Windows для запуску node
            process = subprocess.Popen(
                ["node", script_path, urn, "--output", model_dir, "--gltf"],
                env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, shell=True
            )

            for line in process.stdout:
                self.log(line.strip())
            
            process.wait()
            if process.returncode == 0:
                self.log("\n✅ SUCCESS! All files are in the output folder.")
                messagebox.showinfo("Success", "Conversion finished!")
            else:
                self.log(f"\n❌ Conversion failed with code {process.returncode}")

        except Exception as e:
            self.log(f"Error: {str(e)}")
        
        self.convert_btn.config(state=tk.NORMAL, bg="#27ae60")

    def add_clipboard_support(self, entry):
        entry.bind("<Control-v>", lambda e: self.force_paste(entry))
        entry.bind("<Control-V>", lambda e: self.force_paste(entry))

    def force_paste(self, entry):
        try:
            text = self.root.clipboard_get()
            entry.delete(0, tk.END)
            entry.insert(0, text.strip())
        except:
            pass
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