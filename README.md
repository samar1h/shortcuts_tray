# ![Icon](./icon.ico) Shortcuts Tray <a name="top"></a>
A simple tray application to quickly run Python code or CMD commands with a left-click. The right-click menu lets you add, edit, remove shortcuts, or set a default action.

---

## **Table of Contents**

1. **Introduction**  
   - Overview of the Shortcuts Tray

2. **Useful Shortcuts**
   - [Open Notepad](#1-open-notepad)  
   - [Take Screenshot](#2-take-screenshot)  
   - [Save Clipboard to Desktop](#3-save-clipboard-to-desktop)  
   - [Empty Recycle Bin](#4-empty-recycle-bin)  
   - [Create New Text File on Desktop](#5-create-new-text-file-on-desktop)  
   - [Battery Status](#8-battery-status)  
   - [System Stats](#9-system-stats)  
   - [Volume Up](#10-volume-up)  
   - [Quick Create and Open Text File](#11-quick-create-and-open-text-file)  
   - [Available WiFi Networks](#12-available-wifi-networks)  
   - [Clear Windows Temp](#13-clear-windows-temp)  
   - [Restart](#14-restart)  
   - [Lock Computer](#15-lock-computer)  
   - [Kill Chrome](#16-kill-chrome)
3. [Credit Section](#credit-section)
---

## **Useful Shortcuts**

### 1. **Open Notepad**  
**Description**: Opens the Windows Notepad application.  
**Code**:  
```bash
notepad.exe
```

---

### 2. **Take Screenshot**  
**Description**: Activates the Windows Snipping Tool shortcut to take a screenshot.  
**Code**:  
```python
import pyautogui
pyautogui.hotkey('win', 'shift', 's')
```

---

### 3. **Save Clipboard to Desktop**  
**Description**: Saves the current clipboard content to a text file on the desktop with a timestamp.  
**Code**:  
```python
import pyperclip
import datetime
import os

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
clip_content = pyperclip.paste()
if clip_content:
    filename = os.path.join(desktop, 'clipboard_history.txt')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f'\n--- {timestamp} ---\n{clip_content}\n')
    os.startfile(filename)
```

---

### 4. **Empty Recycle Bin**  
**Description**: Empties the Windows Recycle Bin after confirming with the user.  
**Code**:  
```python
import winshell
winshell.recycle_bin().empty(confirm=True)
```

---

### 5. **Create New Text File on Desktop**  
**Description**: Creates an empty text file on the desktop with a timestamp in its name.  
**Code**:  
```python
import os
import datetime

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename = os.path.join(desktop, f'note_{timestamp}.txt')
with open(filename, 'w') as f:
    f.write('')
os.startfile(filename)
```

---

### 8. **Battery Status**  
**Description**: Displays the current battery percentage, charging status, and estimated time remaining.  
**Code**:  
```python
import psutil
import pyautogui

battery = psutil.sensors_battery()
if battery:
    percent = battery.percent
    power_plugged = battery.power_plugged
    status = 'Plugged In' if power_plugged else 'On Battery'
    mins_left = battery.secsleft // 60 if battery.secsleft >= 0 else 'Unknown'
    msg = f'Battery: {percent}%\nStatus: {status}\nTime left: {mins_left} mins'
else:
    msg = 'No battery detected'
pyautogui.alert(msg, 'Battery Status')
```

---

### 9. **System Stats**  
**Description**: Shows system resource usage including CPU, memory, and disk usage.  
**Code**:  
```python
import psutil
import pyautogui

cpu = psutil.cpu_percent(interval=1)
mem = psutil.virtual_memory().percent
disk = psutil.disk_usage('/').percent
msg = f'CPU Usage: {cpu}%\nMemory Usage: {mem}%\nDisk Usage: {disk}%'
pyautogui.alert(msg, 'System Status')
```

---

### 10. **Volume Up**  
**Description**: Increases the system volume by a few steps.  
**Code**:  
```python
import pyautogui
pyautogui.press('volumeup', presses=5)
```

---

### 11. **Quick Create and Open Text File**  
**Description**: Creates a new text file with a unique name on the desktop and opens it in Notepad.  
**Code**:  
```python
import os
from pathlib import Path
import subprocess

def create_and_open_file():
    desktop_path = Path.home() / "Desktop"
    base_name = "new_file"
    counter = 0

    while True:
        filename = f"{base_name}_{counter}.txt" if counter > 0 else f"{base_name}.txt"
        file_path = desktop_path / filename
        if not file_path.exists():
            try:
                with open(file_path, 'w') as f:
                    f.write("")  # Empty file
                subprocess.Popen(['notepad.exe', str(file_path)])
                break
            except Exception as e:
                print(f"Error: {e}")
                break
        counter += 1

if __name__ == "__main__":
    create_and_open_file()
```

---

### 12. **Available WiFi Networks**  
**Description**: Shows Available WiFi Networks.  
**Code**:  
```python
import subprocess
import pyautogui

output = subprocess.check_output(['netsh', 'wlan', 'show', 'network']).decode('utf-8')
pyautogui.alert(output, 'Available WiFi Networks')
```

---

### 13. **Clear Windows Temp**  
**Description**: Clears temp storage.  
**Code**:  
```python
import os
import shutil
import pyautogui

temp_dir = os.environ.get('TEMP')
try:
    for item in os.listdir(temp_dir):
        item_path = os.path.join(temp_dir, item)
        try:
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except:
            continue
    pyautogui.alert('Temp files cleared!', 'Success')
except Exception as e:
    pyautogui.alert(f'Error: {str(e)}', 'Error')
```

---

### 14. **Restart**  
**Description**: Restarts computer.  
**Code**:  
```bash
shutdown /r /t 0
```

---

### 15. **Lock Computer**  
**Description**: Logs out current user.  
**Code**:  
```python
import ctypes
ctypes.windll.user32.LockWorkStation()
```

---

### 16. **Kill Chrome**  
**Description**: Kills Chrome process.  
**Code**:  
```python
import os
os.system('taskkill /f /im chrome.exe')
```

---

## Credit Section
- <a href="https://www.flaticon.com/free-icon/shortcut-script-app_3884552?term=shortcut&page=1&position=6&origin=search&related_id=3884552">Shortcut icon</a> created by <a href="https://www.flaticon.com/free-icons/shortcut" title="shortcut icons">Freepik - Flaticon</a>

---

[GO UP...](#top)
