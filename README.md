📲 WhatsApp Auto Message Sender

An automated WhatsApp message sender built using Python and Selenium that allows users to send scheduled or instant messages directly through WhatsApp Web.

🚀 Features

✅ Send messages automatically

✅ Send to saved contacts

✅ Custom message support

✅ Schedule messages

✅ Uses WhatsApp Web (no API required)

✅ Lightweight and easy to use

🛠 Tech Stack

Python

Selenium

WebDriver (ChromeDriver)

pywhatkit (optional alternative method)

📂 Project Structure
whatsapp-auto-send/
│
├── main.py
├── requirements.txt
├── README.md
└── driver/
    └── chromedriver.exe
⚙️ Installation

1️⃣ Clone the repository

git clone https://github.com/yourusername/whatsapp-auto-send.git
cd whatsapp-auto-send

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Download ChromeDriver
Make sure ChromeDriver version matches your Chrome browser version.

▶️ Usage

Run the script:

python main.py

The script will:

Open WhatsApp Web

Ask you to scan QR code

Automatically send your message

💻 Example Code Snippet
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")
time.sleep(20)

contact = "Contact Name"
message = "Hello, this is an automated message!"

search_box = driver.find_element(By.XPATH, '//div[@title="Search input textbox"]')
search_box.send_keys(contact)
time.sleep(3)

contact_click = driver.find_element(By.XPATH, f'//span[@title="{contact}"]')
contact_click.click()

msg_box = driver.find_element(By.XPATH, '//div[@title="Type a message"]')
msg_box.send_keys(message)
msg_box.send_keys("\n")
⚠️ Disclaimer

This project is for educational purposes only.
Excessive automation may violate WhatsApp’s terms of service.

📌 Future Improvements

📅 Advanced scheduler

📊 Message logging system

👥 Bulk message support

🧠 GUI interface

👨‍💻 Author

Prashanth
BCA Student | Aspiring Data Scientist
Passionate about automation & AI
