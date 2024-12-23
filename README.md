# WhatsApp Automator (Python)

This is a Python application with a GUI that allows you to schedule and send WhatsApp messages. It utilizes the Twilio API for sending messages.

## Features

*   Schedule WhatsApp messages.
*   Send messages through a user-friendly GUI.
*   Save settings for future use (account SID, auth token, phone number).
*   Option to implement a cache for previously sent messages (future enhancement).
*   Customizable UI (future enhancement).

## Prerequisites

*   Python 3.x installed.
*   A Twilio account with an active project (free trial available).

## Installation

1.  Clone this repository:

    ```bash
    git clone [invalid URL removed] # Replace YOUR_USERNAME
    ```

2.  Navigate to the project directory:

    ```bash
    cd whatsapp-automator
    ```

3.  Install dependencies (recommended to use a virtual environment):

    ```bash
    python3 -m venv venv        # Create a virtual environment
    source venv/bin/activate   # Activate on Linux/macOS
    venv\Scripts\activate      # Activate on Windows
    pip install PyQt6 twilio   # Install PyQt6 and Twilio
    ```

## Setup

1.  Create a Twilio account and create a new project.
2.  Obtain your Account SID, Auth Token, and WhatsApp phone number from your Twilio project dashboard.
3.  Run the application:

    ```bash
    python main.py
    ```

4.  Enter your Twilio credentials and WhatsApp phone number in the Settings dialog.

**Important Security Note:** **Never commit your Twilio credentials directly to your version control system.** Use environment variables or a secure configuration file if you need to store them outside the application's settings.

## Usage

1.  Open the "Settings" dialog from the menu bar.
2.  Enter your Twilio account credentials and WhatsApp phone number. Click "Save".
3.  Enter the recipient's phone number (including country code), message body, and the desired scheduled date and time.
4.  Click "Schedule Message".

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

## Future Enhancements

*   Implement a cache to store previously sent messages to avoid sending duplicates and improve performance.
*   Allow customization of the GUI appearance (themes, layouts).
*   Add features like sending images or other media.
*   Implement message delivery status tracking.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
