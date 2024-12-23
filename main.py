import json
import os
import io
import sys
import threading
import time
from PyQt6.QtWidgets import QTextEdit


from datetime import datetime

from PyQt6.QtWidgets import (QApplication, QDialog, QInputDialog, QListWidget,
                             QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QLineEdit, QDateTimeEdit, QTextEdit)
from twilio.rest import Client

from ui import Ui_MainWindow

SETTINGS_FILE = "settings.json"
HISTORY_FILE = "message_history.json"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # This will not be used in one-folder mode but keep it for consistency
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_settings():
    settings_path = resource_path(SETTINGS_FILE)
    print(f"Loading settings from: {settings_path}")
    try:
        with open(settings_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Settings file not found!")
        return {}

def save_settings(settings):
    settings_path = resource_path(SETTINGS_FILE)
    print(f"Saving settings to: {settings_path}")
    try:
        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"Error saving settings: {e}")

def load_history():
    history_path = resource_path(HISTORY_FILE)
    print(f"Loading history from: {history_path}")
    try:
        with open(history_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("History file not found!")
        return []

def save_history(history):
    history_path = resource_path(HISTORY_FILE)
    print(f"Saving history to: {history_path}")
    try:
        with open(history_path, "w") as f:
            json.dump(history, f, indent=4, default=str)
    except Exception as e:
        print(f"Error saving history: {e}")

def send_whatsapp_message(client, recipient_number, message_body, twilio_whatsapp_number):
    try:
        message = client.messages.create(
            from_=f'whatsapp:{twilio_whatsapp_number}',
            body=message_body,
            to=f'whatsapp:{recipient_number}'
        )
        print(f"Message sent Successfully to {recipient_number} ! Message SID: {message.sid}")
        return f"Message sent Successfully to {recipient_number} ! Message SID: {message.sid}"
    except Exception as e:
        error_message = f"Error sending message: {str(e)}"
        print(error_message)
        return error_message
    
class QtTextEditLogger(io.StringIO): #Custom class to redirect stdout and stderr
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def write(self, text):
        self.text_edit.append(text) #Append text to textedit
        return super().write(text) # Still print to console

    def flush(self):
        pass # To avoid errors

class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Twilio Settings")
        self.settings = settings

        layout = QVBoxLayout()

        self.account_sid_input = QLineEdit(self)
        self.account_sid_input.setPlaceholderText("Enter Account SID")
        self.account_sid_input.setText(settings.get("account_sid", ""))
        layout.addWidget(self.account_sid_input)

        self.auth_token_input = QLineEdit(self)
        self.auth_token_input.setPlaceholderText("Enter Auth Token")
        self.auth_token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.auth_token_input.setText(settings.get("auth_token", ""))
        layout.addWidget(self.auth_token_input)

        self.whatsapp_number_input = QLineEdit(self)
        self.whatsapp_number_input.setPlaceholderText("Enter Twilio WhatsApp Number (e.g., +14155238886)")
        self.whatsapp_number_input.setText(settings.get("twilio_whatsapp_number", ""))
        layout.addWidget(self.whatsapp_number_input)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_settings(self):
        self.settings["account_sid"] = self.account_sid_input.text()
        self.settings["auth_token"] = self.auth_token_input.text()
        self.settings["twilio_whatsapp_number"] = self.whatsapp_number_input.text()
        save_settings(self.settings)
        self.accept()

class HistoryDialog(QDialog):
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Message History")
        self.history_list = QListWidget()
        for entry in history:
            self.history_list.addItem(entry)
        layout = QVBoxLayout()
        layout.addWidget(self.history_list)
        self.setLayout(layout)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        print("Before setupUi")
        self.setupUi(self)
        print("After setupUi")
        self.terminal_text_edit = QTextEdit(self.centralwidget) #create textedit widget
        self.gridLayout.addWidget(self.terminal_text_edit, 6, 0, 1, 2) #add it to gridlayout
        sys.stdout = QtTextEditLogger(self.terminal_text_edit)
        sys.stderr = QtTextEditLogger(self.terminal_text_edit)

        print("Application started.")
        self.send_button.clicked.connect(self.schedule_message)
        self.actionTwilio_Settings.triggered.connect(self.open_settings)
        self.actionView_History.triggered.connect(self.open_history)

        settings_path = resource_path(SETTINGS_FILE)
        if not os.path.exists(settings_path):
            print("Creating settings.json")
            with open(settings_path, "w") as f:
                json.dump({}, f, indent=4)

        history_path = resource_path(HISTORY_FILE)
        if not os.path.exists(history_path):
            print("Creating message_history.json")
            with open(history_path, "w") as f:
                json.dump([], f, indent=4)

        self.settings = load_settings()
        self.history = load_history()

        self.initialize_twilio_client()
        if not self.settings:
            self.open_settings()
        

    def initialize_twilio_client(self):
        try:
            account_sid = self.settings.get("account_sid")
            auth_token = self.settings.get("auth_token")
            self.client = Client(account_sid, auth_token)
            self.twilio_whatsapp_number = self.settings.get("twilio_whatsapp_number")
            self.status_label.setText("Ready to send messages!")
        except Exception as e:
            error_message = f"Error initializing Twilio client: {str(e)}"
            print(error_message)
            self.status_label.setText(error_message)

    def open_settings(self):
        settings_dialog = SettingsDialog(self.settings)
        result = settings_dialog.exec()  # Use exec_() directly

        if result == QDialog.accepted:  # Check for Accepted on the instance
            self.settings = load_settings()
            self.initialize_twilio_client()

    def open_history(self):
        history_dialog = HistoryDialog(self.history)
        history_dialog.exec()

    def schedule_message(self):
        recipient_number = self.phone_number_line_edit.text()
        message_body = self.message_text_edit.toPlainText()
        scheduled_datetime = self.schedule_datetime_edit.dateTime().toPyDateTime()

        if not recipient_number or not message_body:
            self.status_label.setText("Please fill in all fields.")
            return

        now = datetime.now()
        if scheduled_datetime <= now:
            self.status_label.setText("Scheduled time must be in the future.")
            return

        self.status_label.setText(f"Message scheduled for {scheduled_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

        account_sid = self.settings.get("account_sid")
        auth_token = self.settings.get("auth_token")
        twilio_whatsapp_number = self.settings.get("twilio_whatsapp_number")

        threading.Thread(target=self.send_message_threaded, args=(recipient_number, message_body, scheduled_datetime, account_sid, auth_token, twilio_whatsapp_number)).start()

    def initialize_twilio_client(self):
        try:
            account_sid = self.settings.get("account_sid")
            auth_token = self.settings.get("auth_token")
            twilio_whatsapp_number = self.settings.get("twilio_whatsapp_number")

            self.status_label.setText(f"Initializing Twilio with SID: {account_sid}") # Display in UI
            print(f"Initializing Twilio with SID: {account_sid}")
            self.status_label.setText(f"Initializing Twilio with token: {auth_token}") # Display in UI
            print(f"Initializing Twilio with token: {auth_token}")
            self.status_label.setText(f"Initializing Twilio with number: {twilio_whatsapp_number}") # Display in UI
            print(f"Initializing Twilio with number: {twilio_whatsapp_number}")

            self.client = Client(account_sid, auth_token)
            self.twilio_whatsapp_number = twilio_whatsapp_number
            self.status_label.setText("Ready to send messages!")
        except Exception as e:
            error_message = f"Error initializing Twilio client: {str(e)}"
            self.status_label.setText(error_message) # Display error in UI
            print(error_message)

    def send_message_threaded(self, recipient_number, message_body, scheduled_datetime, account_sid, auth_token, twilio_whatsapp_number): # added arguments
        now = datetime.now()
        delay = (scheduled_datetime - now).total_seconds()
        time.sleep(delay)

        try:
            client = Client(account_sid, auth_token) # Initialize client INSIDE the thread
            message_status = send_whatsapp_message(client, recipient_number, message_body, twilio_whatsapp_number)
            self.status_label.setText(message_status)
            if "successfully" in message_status.lower():
                history_entry = {
                    "recipient_number": recipient_number,
                    "message_body": message_body,
                    "scheduled_datetime": str(scheduled_datetime),
                    "status": message_status
                }
                self.history.append(history_entry)
                save_history(self.history)
        except Exception as e:
            self.status_label.setText(f"Error in send_message_threaded: {e}")
            print(f"Error in send_message_threaded: {e}")

        if self.client and self.twilio_whatsapp_number:
            message_status = send_whatsapp_message(self.client, recipient_number, message_body, self.twilio_whatsapp_number)
            self.status_label.setText(message_status)
            if "successfully" in message_status.lower():
                history_entry = {
                    "recipient_number": recipient_number,
                    "message_body": message_body,
                    "scheduled_datetime": str(scheduled_datetime),
                    "status": message_status
                }
                self.history.append(history_entry)
                save_history(self.history)
        else:
            self.status_label.setText("Twilio client not initialized. Check settings.") # Display in UI
            print("Twilio client not initialized. Check settings.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



