# 🛡️ Cloudwalk | Real-Time Telegram Fraud Monitor 
This repository contains the solution for the Cloudwalk Security Engineer Challenge.

This project is a containerized automation that monitors specific Telegram groups for financial fraud keywords. It saves all relevant messages to a persistent database and performs Optical Character Recognition (OCR) on images to detect brand mentions or fraud terms in real-time.

<br>

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) 
![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white) 
![Google Gemini](https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white) 
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

</div>

---

## ✨ Core Features 
* **Real-Time Monitoring:** Uses modern asyncio libraries (Pyrogram) to listen to new messages instantly via Telegram's streaming API, with no polling.

* **Text & Image Analysis:** Detects a configurable list of fraud keywords in both plain text messages and text embedded within images.

* **High-Performance OCR:** Integrates EasyOCR, a modern, deep-learning-based OCR engine.

* **Persistent Storage:** All processed messages (including OCR results and alert status) are saved to a local SQLite database for logging and analysis.

* **100% Dockerized:** The entire application and all its complex dependencies (including the PyTorch AI framework) are containerized for one-command, reproducible deployment.

## 📂 Project Structure

Here’s an overview of the repository and the files generated during execution:  

```
telegram-monitor/
│
├── .env # [IGNORED] Your secret keys and configuration
├── .env.example # Template for your .env file
├── .gitignore # Tells Git to ignore secrets, logs, and generated files
├── Dockerfile # Recipe to build the production Docker image
├── main.py # Main Python application (listener, OCR, DB logic)
├── README.md # This file
└── requirements.txt # Python dependencies list

```

### 🗂️ Generated Files *(Ignored by Git)* 

These files will be automatically created when you run the application:  

```
│
├── my_account.session # [GENERATED] Telegram authentication session file
└── fraud_database.db # [GENERATED] SQLite database file
```

## 🚀 How to Run This Project 

You only need Git, Docker Desktop, and Python 3.9+ (Python is only for the one-time login step).

### Step 1: Configuration
#### 1. Clone the Repository:

```
git clone https://github.com/CamilaSCodes/telegram-monitor.git
cd telegram-monitor
```

#### 2. Get API Credentials:

- Log in to my.telegram.org.

- Go to "API development tools" and create an app.

- You will get your api_id and api_hash.

#### 3. Create .env File:

- Copy the example file: cp .env.example .env (or just rename it).

```
copy .env.example .env
```
```
notepad .env
```

- Edit the .env file with your credentials:

```
API_ID=YOUR_API_ID_HERE

API_HASH=YOUR_API_HASH_HERE

MONITOR_GROUP_ID=-100123456789

FRAUD_KEYWORDS="pix,urubu do pix,retorno garantido,pirâmide,investimento seguro"
```

> [!TIP]
> To find your MONITOR_GROUP_ID, you can add a bot like @meuchatid_bot to the target group. It will post a message with the chat.id.

### Step 2: One-Time Authentication (Local)
To allow Docker to log in non-interactively, we must first create a session file locally. This is only done once.

#### 1. Install local dependencies:

```
pip install -r requirements.txt
```

#### 2. Run the script to log in:

```
python main.py
```

> [!NOTE]  
> The script will ask for your phone number, a login code from Telegram, and your 2FA password (if set).

A new file, my_account.session, now exists in your folder. This is your saved login.

Once you see `Monitor online. Listening for new messages...`, you can stop the script with `Ctrl+C`.

### Step 3: Launch with Docker 🐳
Now for the final step. With [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install) running, execute the following commands:

#### 1. Build the Docker Image:

```
docker build -t telegram-monitor .
```

> [!IMPORTANT]  
> The first build is **slow** (it can take an hour depending on your internet connection). This is a one-time cost. Thanks to Docker's caching, all subsequent builds will be almost instant.

#### 2. Run the Container:

This command starts the monitor in the background (-d) and mounts (-v) your project folder. This allows the container to read your .env/.session files and write back to the fraud_database.db file.

* **On Windows (PowerShell):**
  
```
docker run -d --name fraud_app --env-file .env -v "${PWD}:/app" telegram-monitor
```

* **On Windows (CMD):**

```
docker run -d --name fraud_app --env-file .env -v "%cd%:/app" telegram-monitor
```

* **On macOS / Linux / Git Bash:**
```
docker run -d --name fraud_app --env-file .env -v "$(pwd):/app" telegram-monitor
```

That's it! The automation is now running.

### 🔎 Verifying the Results

#### 1. Viewing Real-Time Logs
To see the monitor in action (including new messages and 🚨 FRAUD ALERT 🚨 logs), run:

```
docker logs -f fraud_app
```

#### 2. Inspecting the Database
All messages and alerts are saved to the fraud_database.db file in your project folder.

| Column       | Type      | Description                                         |
| :------------ | :--------- | :-------------------------------------------------- |
| `id`          | INTEGER    | Primary Key                                         |
| `timestamp`   | DATETIME   | When the message was processed                      |
| `message_text`| TEXT       | The content of the text message (if any)           |
| `ocr_result`  | TEXT       | The full text extracted from the image (if any)    |
| `is_alert`    | BOOLEAN    | `1` (True) if a keyword was found, `0` (False) otherwise |

---

### 📊 Project Stats
<br>

<div align="center">
  
**🤖 AI Assisted:** Development and debugging assisted by ChatGPT & Gemini

**🐍 Code:** 1 Python application file

**📄 Configuration:** 3 supporting files (Dockerfile, requirements.txt, .env.example)

**⚙️ Key Libraries:** Pyrogram, EasyOCR, SQLite

**✅ Challenge Complete:** All prompt requirements met
</div>
