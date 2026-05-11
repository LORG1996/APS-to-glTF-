APS (Forge) to glTF Converter GUI

A lightweight Python-based Graphical User Interface (GUI) for converting Autodesk Platform Services (formerly Forge) models to glTF format. This tool acts as a wrapper for the forge-convert-utils Node.js library, providing a seamless experience for users who prefer not to use the command line.
🚀 Features

    User-Friendly Interface: Built with Python's Tkinter for simplicity.

    Real-time Logging: Watch the conversion progress (downloading, mesh processing, etc.) directly in the app.

    Clipboard Support: Enhanced support for Ctrl+V (Paste) regardless of keyboard layout (works for English and Cyrillic).

    Built-in Guide: Integrated instructions on how to extract URNs and Tokens from the browser.

    Multi-threaded: The UI remains responsive while the conversion runs in the background.

🛠️ Prerequisites

Before using this tool, ensure you have the following installed:

    Node.js: Download and install Node.js.

    Conversion Library: Install the required Node.js package in your project folder:
    Bash

    npm install forge-convert-utils

    Python: (Only if running from source) Python 3.10 or higher.

📦 Installation & Setup

    Clone the repository:
    Bash

    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name

    Install Node.js dependencies:
    Bash

    npm install

    Run the application:
    Bash

    python ForgeConverterGUI.py

🖥️ How to Use

    Access Token: Open your model in the Autodesk Viewer, find the Authorization header in the Network tab (F12), and paste the Bearer token (without the word "Bearer").

    Model URN: Extract the Base64 URN of the model (instructions provided inside the app's Help button).

    Output Directory: Select where you want to save the converted glTF files.

    Convert: Click Start Conversion. You can monitor the progress in the log window.

🛠️ Building the Executable (Optional)

If you want to compile the script into a standalone Windows .exe file:
PowerShell

pip install pyinstaller
pyinstaller --noconsole --onefile ForgeConverterGUI.py

Note: The generated .exe in the dist folder must be placed in the root directory alongside the node_modules folder to function.
📂 Project Structure
Plaintext

.
├── ForgeConverterGUI.py     # Main Python script
├── node_modules/            # Node.js libraries (required)
├── README.md                # Documentation
└── package.json             # Node.js project file

📜 Credits

    GUI developed by [Your Name/Gemini AI].

    Powered by the forge-convert-utils library by Petr Broz.

⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.