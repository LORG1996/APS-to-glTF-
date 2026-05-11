# APS (Forge) to glTF Converter GUI

<img width="700" height="350" alt="Gemini_Generated_Image_3tf8me3tf8me3tf8" src="https://github.com/user-attachments/assets/507b0115-1a87-4d8b-811d-afb44ba0ce03" />

A professional hybrid utility designed for architectural visualizers and 3D developers. This tool automates the extraction and conversion of **Autodesk Platform Services** (formerly Forge) models into high-quality **glTF** files, combining a user-friendly **Python GUI** with the powerful **Node.js** conversion engine.

## 🚀 Key Features

* **Auto-Manifest Retrieval:** Automatically fetches `manifest.json` from Autodesk servers—no more manual file hunting.
* **Intelligent URN Sanitizer:** Detects and fixes duplicated or malformed URNs during paste operations to prevent 401/404 errors.
* **Dynamic Export Organization:** Automatically creates structured sub-folders for each unique model URN.
* **Integrated Process Logs:** Real-time feedback via an embedded console to monitor conversion status and API responses.
* **Cross-Tool Workflow:** Optimized for assets destined for Blender, Unreal Engine 5, or 3ds Max.

## 🛠 Prerequisites

Ensure you have the following installed:

1.  **Node.js (LTS):** [Download](https://nodejs.org/)
2.  **Python 3.10+:** [Download](https://www.python.org/)
3.  **Python Requests Library:**
    ```bash
    pip install requests
    ```

## 📦 Quick Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/LORG1996/APS-to-glTF-](https://github.com/LORG1996/APS-to-glTF-)
    ```

2.  **Install the conversion engine:**
    ```bash
    npm init -y
    npm install forge-convert-utils axios
    ```

3.  **Verify core components:**
    The following files **must** copy from "FIX" folder to fix them for new Node.JS:
    * `node_modules/forge-convert-utils/bin/forge-convert.js`
    * `node_modules/forge-convert-utils/lib/svf/reader.js`
    * `node_modules/forge-convert-utils/lib/gltf/writer.js`

## 🖥 Usage

1.  **Run the GUI:**
    ```bash
    python ForgeConverterGUI.py  or ForgeConverterGUI.bat
    ```

2.  **Fill the credentials:**
    * **Access Token:** Paste your valid `Bearer` token from the Autodesk session.
    * **Model URN:** Paste the base64 URN (Auto-sanitizer will handle duplicates).

3.  **Start:**
    * Select an output directory.
    * Click **START CONVERSION** and wait for the "SUCCESS" message.

## 📂 Project Structure

```text
├── ForgeConverterGUI.py          # GUI Application logic
├── node_modules/             # Node.js engine & dependencies
├── package.json              # Node.js project configuration
└── README.md                 # Documentation
