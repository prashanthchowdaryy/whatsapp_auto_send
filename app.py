import time
import threading
import urllib.parse
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

# Global variables
driver = None
driver_lock = threading.Lock()
is_logged_in = False

def init_whatsapp_driver():
    """Initializes Chrome and waits for WhatsApp Login"""
    global driver, is_logged_in
    with driver_lock:
        if driver is not None:
            return 

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get("https://web.whatsapp.com")
        print(">>> PLEASE SCAN THE QR CODE IN THE CHROME WINDOW <<<")
        
        try:
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
            )
            print(">>> Login Successful! <<<")
            is_logged_in = True
        except Exception:
            print("Login timed out.")
            if driver:
                driver.quit()
                driver = None

def send_whatsapp_message(phone, message):
    global driver, is_logged_in
    if not is_logged_in or driver is None:
        return False

    with driver_lock:
        try:
            encoded_msg = urllib.parse.quote(message)
            driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}")

            input_box = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            time.sleep(2) 
            input_box.send_keys(Keys.ENTER)
            print(f"Sent to {phone} at {datetime.now().strftime('%H:%M:%S')}")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Error sending to {phone}: {e}")
            return False

def schedule_messages(phone, message, interval_minutes, duration_hours, job_id):
    end_time = datetime.now() + timedelta(hours=duration_hours)

    def send():
        if datetime.now() >= end_time:
            # Job is done naturally
            try:
                scheduler.remove_job(job_id)
            except:
                pass
            return
        send_whatsapp_message(phone, message)

    scheduler.add_job(send, 'interval', minutes=interval_minutes, id=job_id, replace_existing=True)
    # Start first message in 10 seconds
    scheduler.add_job(send, 'date', run_date=datetime.now() + timedelta(seconds=10), id=f"{job_id}_init")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_sending():
    phone = request.form.get('phone')
    message = request.form.get('message')
    try:
        duration = int(request.form.get('duration'))
        interval = int(request.form.get('interval'))
    except:
        return "Invalid numbers", 400

    if driver is None:
        threading.Thread(target=init_whatsapp_driver, daemon=True).start()

    # Create a unique job ID
    job_id = f"job_{int(time.time())}"
    
    schedule_messages(phone, message, interval, duration, job_id)

    # Pass the job_id to the template so we can stop it later
    return render_template('success.html', 
                           phone=phone, 
                           message=message, 
                           duration=duration, 
                           interval=interval,
                           job_id=job_id)

@app.route('/stop/<job_id>', methods=['POST'])
def stop_job(job_id):
    global driver, is_logged_in
    
    # 1. Remove the scheduled job
    try:
        scheduler.remove_job(job_id)
    except Exception:
        pass # Job might have already finished
    
    try:
        scheduler.remove_job(f"{job_id}_init")
    except Exception:
        pass

    # 2. Close the browser (Optional: remove this block if you want to keep WhatsApp open)
    with driver_lock:
        if driver:
            driver.quit()
            driver = None
            is_logged_in = False
            print(">>> Driver stopped by user request. <<<")

    return render_template('stopped.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)