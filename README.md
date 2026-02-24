# VaaniSetu Backend Architecture

This repository contains the microservice backend architecture for VaaniSetu, consisting of 5 interconnected servers: a Node.js API Gateway and 4 Python Machine Learning/Logic engines.

## 🚀 Prerequisites
Before you begin, ensure you have the following installed on your machine:
* [Node.js](https://nodejs.org/) (v18 or higher)
* [Python](https://www.python.org/downloads/) (v3.10 or v3.12 recommended)
* Git

## 📦 1. Download Required ML Models (IMPORTANT)
Because machine learning models are too large for GitHub, you must download them manually before starting the servers.

1. Download the models from our Google Drive: **https://drive.google.com/drive/u/0/folders/1VWxalGTdxqFNyLU9nryvIykDFIKtLRxe**
2. Extract the downloaded files.
3. Place the `vectors` folder inside: `Named_Entity_Recognition/Google_Colab/vocab/`
4. Place the `intent_model_full.pkl` file inside: `VaaniSetu_NlpIntent_Backend/` (or wherever your code expects it).

*(Note: The PaddleOCR models do not need to be downloaded manually. They will automatically download from HuggingFace the first time you start the OCR server).*

## 🛠️ 2. Setup & Installation

**Main Node.js Gateway:**
```bash
cd MainBackend
npm install

**Python Sub-Backends (Run this for each Python folder):
You will need to create a virtual environment and install dependencies for the 4 Python backends (Named_Entity_Recognition, Govt_Scheme, VaaniSetu_NlpIntent_Backend, OCR_Backend).**

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt