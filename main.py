import json
import os
import subprocess
import sys
import traceback
from pathlib import Path
import pystray
from PIL import Image
import customtkinter as ctk
from threading import Thread
import tkinter as tk


class ShortcutManager:
    def update_menu(self):
        self.icon.menu = pystray.Menu(*self.get_menu_items())

    def get_menu_items(self):
        items = []

        def create_command_handler(shortcut_name):
            def handle_command(icon, item):
                self.run_command(shortcut_name)

            return handle_command

        def create_checked_handler(shortcut_name):
            def check_default(item):
                return self.shortcuts[shortcut_name]["is_default"]

            return check_default

        # First pass to find the default shortcut
        for name, data in self.shortcuts.items():
            if data.get("is_default"):
                default_shortcut = name
                break
        else:
            default_shortcut = None

        # Create menu items with proper default handling
        for name, data in self.shortcuts.items():
            is_default = name == default_shortcut
            item = pystray.MenuItem(
                name,
                create_command_handler(name),
                default=is_default,
                checked=create_checked_handler(name)
            )
            items.append(item)

        # Rest of the menu items...
        items.append(pystray.Menu.SEPARATOR)
        items.append(pystray.MenuItem("Add Shortcut", lambda icon, item: self.root.after(0, self.show_add_dialog)))
        items.append(pystray.MenuItem("Edit Shortcuts", lambda icon, item: self.root.after(0, self.show_edit_dialog)))
        items.append(pystray.Menu.SEPARATOR)
        items.append(pystray.MenuItem("Exit", lambda icon, item: self.on_exit()))

        return items

    def setup_tray(self):
        icon_path = "icon.png"
        if not os.path.exists(icon_path):
            img = Image.new('RGB', (64, 64), color='blue')
            img.save(icon_path)

        self.icon = pystray.Icon(
            "ShortcutManager",
            Image.open(icon_path),
            "Shortcut Manager",
            menu=pystray.Menu(*self.get_menu_items())
        )
    def __init__(self):
        self.shortcuts_file = "shortcuts.json"
        self.default_shortcuts = {
            "Open Notepad": {
                "command": "notepad.exe",
                "is_python": False,
                "is_default": False
            },
            "Take Screenshot": {
                "command": """import pyautogui\npyautogui.hotkey('win', 'shift', 's')""",
                "is_python": True,
                "is_default": True
            },
        }
        self.shortcuts = self.load_shortcuts()
        self.icon = None
        self.root = ctk.CTk()
        self.root.iconbitmap("icon.ico")
        self.root.iconphoto(True, tk.PhotoImage(file="icon.png"))
        self.root.withdraw()  # Hide the root window
        self.setup_tray()

    def load_shortcuts(self):
        if os.path.exists(self.shortcuts_file):
            with open(self.shortcuts_file, 'r') as f:
                shortcuts = json.load(f)
                # Ensure only one default
                default_found = False
                for name, data in shortcuts.items():
                    if data.get("is_default"):
                        if default_found:
                            data["is_default"] = False
                        default_found = True
                return shortcuts
        else:
            with open(self.shortcuts_file, 'w') as f:
                json.dump(self.default_shortcuts, f, indent=4)
        return self.default_shortcuts.copy()

    def save_shortcuts(self):
        with open(self.shortcuts_file, 'w') as f:
            json.dump(self.shortcuts, f, indent=4)
        self.update_menu()

    def run_command(self, name):
        shortcut = self.shortcuts[name]
        if shortcut["is_python"]:
            thread = Thread(target=self._run_python_code, args=(shortcut["command"],))
        else:
            thread = Thread(target=self._run_system_command, args=(shortcut["command"],))
        thread.daemon = True
        thread.start()

    def _run_python_code(self, code):
        try:
            exec(code)
        except Exception as e:
            error_traceback = traceback.format_exc()
            self.root.after(0, lambda: self.show_error(str(e), error_traceback))

    def _run_system_command(self, command):
        try:
            subprocess.Popen(command, shell=True)
        except Exception as e:
            error_traceback = traceback.format_exc()
            self.root.after(0, lambda: self.show_error(str(e), error_traceback))

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'+{x}+{y}')

    def show_error(self, message, traceback_text=None):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Error")
        dialog.geometry("500x300")
        dialog.lift()

        self.center_window(dialog)

        # Main error message
        label = ctk.CTkLabel(dialog, text=f"Error: {message}")
        label.pack(pady=10, padx=10)

        if traceback_text:
            # Create a collapsible frame for traceback
            def toggle_traceback():
                if traceback_frame.winfo_viewable():
                    traceback_frame.pack_forget()
                    toggle_btn.configure(text="Show Traceback")
                else:
                    traceback_frame.pack(fill="both", expand=True, padx=10, pady=5)
                    toggle_btn.configure(text="Hide Traceback")

            toggle_btn = ctk.CTkButton(dialog, text="Show Traceback", command=toggle_traceback)
            toggle_btn.pack(pady=5)

            traceback_frame = ctk.CTkFrame(dialog)
            traceback_text_widget = ctk.CTkTextbox(traceback_frame, height=150)
            traceback_text_widget.pack(fill="both", expand=True, padx=5, pady=5)
            traceback_text_widget.insert("1.0", traceback_text)
            traceback_text_widget.configure(state="disabled")

        ok_button = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
        ok_button.pack(pady=10)

    def show_add_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.after(250, lambda: dialog.iconbitmap('icon.ico'))
        dialog.after(250, lambda: dialog.iconphoto(True, tk.PhotoImage(file="icon.png")))
        dialog.title("Add Shortcut")
        dialog.geometry("400x350")
        dialog.lift()

        self.center_window(dialog)
        dialog.transient(self.root)
        dialog.grab_set()

        name_label = ctk.CTkLabel(dialog, text="Shortcut Name:")
        name_label.pack(pady=5)
        name_entry = ctk.CTkEntry(dialog)
        name_entry.pack(pady=5)

        command_label = ctk.CTkLabel(dialog, text="Command/Python Code:")
        command_label.pack(pady=5)
        command_entry = ctk.CTkTextbox(dialog, height=100)
        command_entry.pack(pady=5)

        is_python_var = ctk.BooleanVar()
        is_python_check = ctk.CTkCheckBox(dialog, text="Is Python Code", variable=is_python_var)
        is_python_check.pack(pady=5)

        is_default_var = ctk.BooleanVar()
        is_default_check = ctk.CTkCheckBox(dialog, text="Set as Default (Runs on Left Click)", variable=is_default_var)
        is_default_check.pack(pady=5)

        def save():
            try:
                name = name_entry.get().strip()
                command = command_entry.get("1.0", "end-1c").strip()

                if not name or not command:
                    self.show_error("Name and command are required!")
                    return

                if is_default_var.get():
                    # Clear previous defaults
                    for shortcut in self.shortcuts.values():
                        shortcut["is_default"] = False

                self.shortcuts[name] = {
                    "command": command,
                    "is_python": is_python_var.get(),
                    "is_default": is_default_var.get()
                }

                self.save_shortcuts()
                dialog.destroy()
            except Exception as e:
                error_traceback = traceback.format_exc()
                self.show_error(str(e), error_traceback)

        save_button = ctk.CTkButton(dialog, text="Save", command=save)
        save_button.pack(pady=10)

    def show_edit_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Edit Shortcuts")
        dialog.geometry("400x500")
        dialog.lift()
        dialog.after(250, lambda: dialog.iconbitmap('icon.ico'))
        dialog.after(250, lambda: dialog.iconphoto(True, tk.PhotoImage(file="icon.png")))

        self.center_window(dialog)
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ctk.CTkScrollableFrame(dialog)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        def update_checkboxes():
            for cb in default_checkboxes:
                name, checkbox = cb
                checkbox.configure(state="normal")
                if self.shortcuts[name]["is_default"]:
                    checkbox.select()
                else:
                    checkbox.deselect()

        default_checkboxes = []

        for name, data in self.shortcuts.items():
            shortcut_frame = ctk.CTkFrame(frame)
            shortcut_frame.pack(fill="x", pady=5)

            name_label = ctk.CTkLabel(shortcut_frame, text=name)
            name_label.pack(side="left", padx=5)

            is_default_var = ctk.BooleanVar(value=data["is_default"])
            is_default_check = ctk.CTkCheckBox(shortcut_frame, text="Default",
                                               variable=is_default_var)
            is_default_check.pack(side="right", padx=5)
            default_checkboxes.append((name, is_default_check))

            def on_default_change(n=name):
                # Clear all other defaults
                for shortcut_name, shortcut_data in self.shortcuts.items():
                    shortcut_data["is_default"] = (shortcut_name == n)
                self.save_shortcuts()
                update_checkboxes()

            is_default_check.configure(command=lambda n=name: on_default_change(n))

            def delete_shortcut(n=name):
                del self.shortcuts[n]
                self.save_shortcuts()
                dialog.destroy()
                self.show_edit_dialog()

            def edit_shortcut(n=name):
                dialog.destroy()
                self.show_edit_shortcut_dialog(n)

            edit_btn = ctk.CTkButton(shortcut_frame, text="Edit", width=60,
                                     command=lambda n=name: edit_shortcut(n))
            edit_btn.pack(side="right", padx=5)

            delete_btn = ctk.CTkButton(shortcut_frame, text="Delete", width=60,
                                       command=lambda n=name: delete_shortcut(n))
            delete_btn.pack(side="right", padx=5)

    def show_edit_shortcut_dialog(self, name):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(f"Edit Shortcut: {name}")
        dialog.geometry("400x300")
        dialog.after(250, lambda: dialog.iconbitmap('icon.ico'))
        dialog.after(250, lambda: dialog.iconphoto(True, tk.PhotoImage(file="icon.png")))
        dialog.lift()

        self.center_window(dialog)
        dialog.transient(self.root)
        dialog.grab_set()

        shortcut = self.shortcuts[name]

        command_label = ctk.CTkLabel(dialog, text="Command/Python Code:")
        command_label.pack(pady=5)
        command_entry = ctk.CTkTextbox(dialog, height=100)
        command_entry.insert("1.0", shortcut["command"])
        command_entry.pack(pady=5)

        is_python_var = ctk.BooleanVar(value=shortcut["is_python"])
        is_python_check = ctk.CTkCheckBox(dialog, text="Is Python Code", variable=is_python_var)
        is_python_check.pack(pady=5)

        is_default_var = ctk.BooleanVar(value=shortcut["is_default"])
        is_default_check = ctk.CTkCheckBox(dialog, text="Set as Default (Runs on Left Click)", variable=is_default_var)
        is_default_check.pack(pady=5)

        def save():
            try:
                command = command_entry.get("1.0", "end-1c").strip()

                if not command:
                    self.show_error("Command is required!")
                    return

                if is_default_var.get():
                    # Clear previous defaults
                    for s in self.shortcuts.values():
                        s["is_default"] = False

                self.shortcuts[name].update({
                    "command": command,
                    "is_python": is_python_var.get(),
                    "is_default": is_default_var.get()
                })

                self.save_shortcuts()
                dialog.destroy()
            except Exception as e:
                error_traceback = traceback.format_exc()
                self.show_error(str(e), error_traceback)

        save_button = ctk.CTkButton(dialog, text="Save", command=save)
        save_button.pack(pady=10)

    def on_exit(self):
        self.icon.stop()
        self.root.destroy()
        exit(0)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    manager = ShortcutManager()

    icon_thread = Thread(target=manager.icon.run)
    icon_thread.daemon = True
    icon_thread.start()

    manager.root.mainloop()
