# APS (Forge) to glTF Converter GUI

A lightweight Python-based Graphical User Interface (GUI) for converting **Autodesk Platform Services** (formerly Forge) models to glTF format. This tool acts as a wrapper for the `forge-convert-utils` Node.js library, providing a seamless experience for users who prefer not to use the command line.

## 🚀 Features

* **User-Friendly Interface**: Built with Python's Tkinter for simplicity and ease of use.
* **Real-time Logging**: Monitor the conversion progress (downloading, mesh processing, etc.) directly within the application window.
* **Enhanced Clipboard Support**: Full support for `Ctrl+V` (Paste), `Ctrl+C` (Copy), and `Ctrl+A` (Select All) that works across different keyboard layouts (English, Ukrainian, Russian).
* **Built-in Guide**: Integrated step-by-step instructions on how to extract **URNs** and **Access Tokens** using browser developer tools.
* **Multi-threaded**: The UI remains responsive and doesn't "freeze" while the conversion process runs in the background.

---

## 🛠️ Prerequisites

Before using this tool, ensure you have the following installed:

1.  **Node.js**: [Download and install Node.js](https://nodejs.org/).
2.  **Conversion Library**: Install the required Node.js package in your project folder:
    ```bash
    npm install forge-convert-utils
    ```
3.  **Python**: (Only if running from source) Python 3.10 or higher.

---

## 📦 Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/LORG1996/APS-to-glTF-](https://github.com/LORG1996/APS-to-glTF-)
    cd APS-to-glTF-
    ```
2.  **Install Node.js dependencies**:
    ```bash
    npm install
    ```
3.  **Apply the Required Fix**:
    > [!IMPORTANT]
    > If you reinstall `node_modules` or build the project on a new machine, you **must** manually apply the syntax fix to `node_modules/forge-convert-utils/dist/writers/writer.js` to ensure compatibility with modern Node.js versions. Keep a backup of your fixed `writer.js` file!

4.  **Run the application**:
    ```bash
    python ForgeConverterGUI.py
    ```

---

## 🖥️ How to Use

1.  **Access Token**: Open your model in the Autodesk Viewer, find the `Authorization` header in the **Network tab (F12)**, and paste the Bearer token (copy only the string after the word "Bearer").
2.  **Model URN**: Extract the Base64 URN of the model (detailed instructions are available via the **"How to get URN and Token?"** button in the app).
3.  **Output Directory**: Choose the destination folder where you want to save the converted glTF files.
4.  **Convert**: Click **🚀 START CONVERSION**. You can monitor the live output in the **Process Log** area.

---

## 🏗️ Building the Executable (Optional)

To compile the script into a standalone Windows `.exe` file, use PyInstaller:

```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile ForgeConverterGUI.py
