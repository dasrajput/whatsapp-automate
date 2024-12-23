# WhatsApp Message Scheduler (Command-Line)

This Python script allows you to schedule WhatsApp messages to be sent at a specific date and time using the Twilio API.

## Prerequisites

- Python 3.6 or higher
- A Twilio account (with a WhatsApp Business API enabled number)
- Twilio Python library

## Setup

1.  **Clone the repository (or download the `main.py` file):**

    ```bash
    git clone [invalid URL removed] # Replace with your repo if you have one
    cd whatsapp-message-scheduler
    ```

2.  **Install the required Python library:**

    ```bash
    pip install twilio
    ```

3.  **Set up your Twilio credentials:**

    -   Obtain your Account SID and Auth Token from your Twilio Console ([https://www.twilio.com/console](https://www.twilio.com/console)).
    -   Replace the placeholders in the `main.py` file with your actual credentials:

    ```python
    account_sid = "YOUR_ACCOUNT_SID"
    auth_token = "YOUR_AUTH_TOKEN"
    ```

    **Important Security Note:** For production environments, it is highly recommended to store these credentials as environment variables instead of directly in the code.

## Usage

Run the script from your terminal:

```bash
python main.py



EXAMPLE : Enter the recipient name: John Doe
Enter the recipient whatsapp number with country code: +15551234567
Enter the message for John Doe: Hello John, this is a scheduled message!
Enter the date in YYYY-MM-DD format: 2024-12-26
Enter the time in HH:MM:SS format: 09:00:00
Message scheduled to be sent to John Doe at 2024-12-26 09:00:00.
(Script waits until the scheduled time and sends the message)
Message sent Successfully to +15551234567 ! Message SID: SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
