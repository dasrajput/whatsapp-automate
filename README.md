WhatsApp Automator (Python)
This is a Python application with a GUI that allows you to schedule and send WhatsApp messages. It utilizes the Twilio API for sending messages.

Features
Schedule WhatsApp messages
Send messages through a user-friendly GUI
Save settings for future use (account SID, auth token, phone number)
Option to implement a cache for previously sent messages (future enhancement)
Customizable UI (future enhancement)
Prerequisites
Python 3.x installed
A Twilio account with an active project (free trial available)
Installation
Clone this repository:
Bash

git clone https://github.com/your-username/whatsapp-automator.git
Install dependencies:
Bash

pip install PyQt5 twilio
(Optional) Create a virtual environment to manage dependencies:
Bash

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install PyQt5 twilio
Setup
Create a Twilio account and create a new project.
Obtain your Account SID, Auth Token, and WhatsApp phone number from your Twilio project dashboard.
Run the application:
Bash

python main.py
Enter your Twilio credentials and configure your message settings in the Settings dialog.
Note: For security reasons, do not commit your Twilio credentials to your version control system.

Usage
Open the "Settings" dialog from the main window.
Enter your Twilio account credentials and WhatsApp phone number.
Schedule a message by entering the recipient's phone number, message body, and desired scheduled date and time.
Click "Send" to send the message immediately or wait for the scheduled time.
Contributing
We welcome contributions to improve this application. Feel free to fork the repository and submit pull requests with your enhancements.

Future Enhancements
Implement a cache to store previously sent messages (improve performance)
Allow customization of the GUI appearance
Add features like sending images or attachments
License
This project is licensed under the MIT License. See the LICENSE file for details.
