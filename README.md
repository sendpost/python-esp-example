# SendPost Python SDK - ESP Example

This project provides a comprehensive example demonstrating how Email Service Providers (ESPs) can use the SendPost Python SDK to manage email sending operations.

## Overview

The example demonstrates a complete ESP workflow including:

1. **Sub-Account Management** - Create and manage sub-accounts for different clients or use cases
2. **Webhook Setup** - Configure webhooks to receive real-time email event notifications
3. **Domain Management** - Add and verify sending domains
4. **Email Sending** - Send transactional and marketing emails
5. **Message Tracking** - Retrieve message details for tracking and debugging
6. **Statistics & Analytics** - Monitor email performance via sub-account stats, IP stats, and IP pool stats
7. **IP Pool Management** - Create and manage IP pools for better deliverability control

## Prerequisites

- Python 3.7 or higher
- pip 3 (Python 3 package installer)
- **Virtual environment (venv)** - Highly recommended for isolating project dependencies
- SendPost account with:
  - Account API Key (for account-level operations)
  - Sub-Account API Key (for sub-account-level operations)

**Note**: While not strictly required, using a virtual environment is a Python best practice and highly recommended. It keeps your project dependencies isolated and prevents conflicts with other Python projects on your system.

## Python Version Setup

### Check Your Python Version

First, verify that you have Python 3 installed:

```bash
python3 --version
```

You should see something like:
```
Python 3.9.0
```

**Important**: Make sure you're using Python 3.7 or higher. Python 2.7 is not supported.

### Verify pip Version

Check that you have pip3 (Python 3 package installer) installed:

```bash
pip3 --version
```

You should see something like:
```
pip 21.0.1 from /usr/local/lib/python3.9/site-packages/pip (python 3.9)
```

### Using the Correct Python and pip Commands

**Without a virtual environment:**
- Use `python3` instead of `python` (to avoid using Python 2.7)
- Use `pip3` instead of `pip` (to ensure you're installing packages for Python 3)

**With a virtual environment (recommended):**
- Once activated, you can use `python` and `pip` - the virtual environment ensures Python 3
- The virtual environment automatically uses Python 3, so `python` and `pip` are safe to use

### If Python 3 is Not Installed

#### macOS
```bash
# Using Homebrew
brew install python3

# Or download from python.org
# Visit https://www.python.org/downloads/
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### Linux (CentOS/RHEL)
```bash
sudo yum install python3 python3-pip
```

#### Windows
1. Download Python 3 from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Use `py` command or `python3` in Command Prompt/PowerShell

### Verify Installation

After installation, verify both Python and pip:

```bash
python3 --version
pip3 --version
```

Both should show version 3.x or higher.

## Setup

### 1. Clone or Download the Project

```bash
cd python-esp-example
```

### 2. Create a Virtual Environment (Recommended)

Using a virtual environment is the recommended best practice for Python development. It isolates your project dependencies and prevents conflicts with other Python projects.

#### Create the Virtual Environment

```bash
python3 -m venv venv
```

This creates a new directory called `venv` containing a fresh Python environment.

#### Activate the Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

After activation, you should see `(venv)` at the beginning of your command prompt, indicating the virtual environment is active.

#### Verify Virtual Environment is Active

```bash
which python3
# Should show: /path/to/your/project/venv/bin/python3

which pip3
# Should show: /path/to/your/project/venv/bin/pip3
```

#### Deactivate the Virtual Environment (when done)

When you're finished working on the project, you can deactivate the virtual environment:

```bash
deactivate
```

**Important**: Always activate your virtual environment before installing packages or running the example.

### 3. Install Dependencies

With your virtual environment activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install the SendPost Python SDK directly:

```bash
pip install sendpost-python-sdk
```

**Note**: When using a virtual environment, you can use `pip` instead of `pip3` since the virtual environment ensures you're using Python 3. However, `pip3` will also work.

### Why Use a Virtual Environment?

- **Isolation**: Keeps project dependencies separate from system-wide Python packages
- **Reproducibility**: Ensures consistent environments across different machines
- **Clean Management**: Easy to delete and recreate if something goes wrong
- **Best Practice**: Industry standard for Python development

### 3. Configure API Keys

You can set API keys in two ways:

#### Option A: Environment Variables (Recommended)

```bash
export SENDPOST_ACCOUNT_API_KEY="your_account_api_key_here"
export SENDPOST_SUB_ACCOUNT_API_KEY="your_sub_account_api_key_here"
```

#### Option B: Edit the Source Code

Edit `ESPExample.py` and update the constants:

```python
SUB_ACCOUNT_API_KEY = "your_sub_account_api_key_here"
ACCOUNT_API_KEY = "your_account_api_key_here"
```

### 4. Update Configuration Values

Edit `ESPExample.py` and update:

- `TEST_FROM_EMAIL` - Your verified sender email address
- `TEST_TO_EMAIL` - Recipient email address
- `TEST_DOMAIN_NAME` - Your sending domain
- `WEBHOOK_URL` - Your webhook endpoint URL

## Running the Example

### Run the Complete Workflow

**If using a virtual environment (recommended):**
1. Make sure your virtual environment is activated (you should see `(venv)` in your prompt)
2. Run the example:
   ```bash
   python ESPExample.py
   ```

**If not using a virtual environment:**
```bash
python3 ESPExample.py
```

This will execute the complete ESP workflow demonstrating all features.

**Note**: 
- With a virtual environment activated, you can use `python` (the venv ensures Python 3)
- Without a virtual environment, use `python3` to ensure you're running Python 3, not Python 2.7

## Project Structure

```
example-sdk-python/
├── ESPExample.py          # Main example class
├── README.md              # This file
├── requirements.txt       # Python dependencies
└── .gitignore             # Git ignore file (optional)
```

## Workflow Steps

The example demonstrates the following workflow:

### Step 1: Sub-Account Management
- List all sub-accounts
- Create new sub-accounts for different clients or use cases

### Step 2: Webhook Configuration
- Create webhooks to receive email event notifications
- Configure which events to receive (delivered, opened, clicked, bounced, etc.)
- Test webhooks locally using ngrok (see Testing Webhooks section below)

### Step 3: Domain Management
- Add sending domains
- View DNS records needed for domain verification
- List all domains

### Step 4: Email Sending
- Send transactional emails (order confirmations, receipts, etc.)
- Send marketing emails (newsletters, promotions, etc.)
- Configure tracking (opens, clicks)
- Add custom headers and fields

### Step 5: Message Tracking
- Retrieve message details by message ID
- View delivery information, IP used, submission time, etc.

### Step 6: Statistics & Analytics
- Get sub-account statistics (processed, delivered, opens, clicks, bounces, etc.)
- Get aggregate statistics
- Get account-level statistics across all sub-accounts

### Step 7: IP and IP Pool Management
- List all dedicated IPs
- Create IP pools for better deliverability control
- View IP pool configurations

## Key Features Demonstrated

### Email Sending
- **Transactional Emails**: Order confirmations, receipts, notifications
- **Marketing Emails**: Newsletters, promotions, campaigns
- **Tracking**: Open tracking, click tracking
- **Customization**: Custom headers, custom fields, groups

### Statistics & Monitoring
- **Sub-Account Stats**: Daily statistics for a specific sub-account
- **Aggregate Stats**: Overall performance metrics
- **Account Stats**: Statistics across all sub-accounts
- **Performance Metrics**: Open rates, click rates, delivery rates

### Infrastructure Management
- **Sub-Accounts**: Organize sending by client, product, or use case
- **Domains**: Add and verify sending domains
- **IPs**: Monitor dedicated IP addresses
- **IP Pools**: Group IPs for better deliverability control

### Event Handling
- **Webhooks**: Receive real-time notifications for email events
- **Event Types**: Processed, delivered, dropped, bounced, opened, clicked, unsubscribed, spam

## API Keys Explained

### Account API Key (`X-Account-ApiKey`)
Used for account-level operations:
- Creating and managing sub-accounts
- Managing IPs and IP pools
- Creating webhooks
- Getting account-level statistics
- Retrieving messages

### Sub-Account API Key (`X-SubAccount-ApiKey`)
Used for sub-account-level operations:
- Sending emails
- Managing domains
- Managing suppressions
- Getting sub-account statistics

## Example Output

When you run the example, you'll see output like:

```
╔═══════════════════════════════════════════════════════════════╗
║   SendPost Python SDK - ESP Example Workflow                    ║
╚═══════════════════════════════════════════════════════════════╝

=== Step 1: Listing All Sub-Accounts ===
Retrieving all sub-accounts...
✓ Retrieved 3 sub-account(s)
  - ID: 50441
    Name: API
    API Key: pR0YIuxYSbVwmQi2Y8Qs
    ...

=== Step 2: Creating Webhook ===
Creating webhook...
  URL: https://your-webhook-endpoint.com/webhook
✓ Webhook created successfully!
  ID: 12345
  ...

...
```

## Testing Webhooks with ngrok

When developing and testing webhooks locally, you need a way to expose your local webhook endpoint to the internet. **ngrok** is a popular tool that creates a secure tunnel to your localhost, allowing SendPost to send webhook events to your local development environment.

### What is ngrok?

ngrok is a reverse proxy that creates a secure tunnel from a public URL to your local machine. This allows you to:
- Test webhooks locally without deploying to a server
- Receive real-time email event notifications during development
- Debug webhook payloads in your local environment

### Installing ngrok

#### macOS
```bash
# Using Homebrew
brew install ngrok/ngrok/ngrok

# Or download from https://ngrok.com/download
```

#### Linux
```bash
# Download and install
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list && \
  sudo apt update && sudo apt install ngrok
```

#### Windows
1. Download from https://ngrok.com/download
2. Extract and add to PATH, or use the executable directly

### Setting Up ngrok

1. **Sign up for a free ngrok account** (optional but recommended):
   - Visit https://dashboard.ngrok.com/signup
   - Get your authtoken from the dashboard

2. **Configure ngrok** (if you signed up):
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN
   ```

### Running ngrok

1. **Start your local webhook server** (on port 8000, for example):
   ```bash
   # Example: Using Python's built-in HTTP server
   python3 -m http.server 8000
   
   # Or use Flask/FastAPI/your web framework
   # Your webhook endpoint should be accessible at http://localhost:8000/webhook
   ```

2. **Start ngrok** to create a tunnel:
   ```bash
   ngrok http 8000
   ```

3. **Copy the forwarding URL**:
   ```
   Forwarding  https://abc123.ngrok-free.app -> http://localhost:8000
   ```

4. **Update your webhook URL** in `ESPExample.py`:
   ```python
   WEBHOOK_URL = "https://abc123.ngrok-free.app/webhook"
   ```

### Example: Simple Webhook Server

Here's a minimal example to test webhooks locally:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Parse webhook payload
        webhook_data = json.loads(post_data.decode('utf-8'))
        
        print("Webhook received:")
        print(json.dumps(webhook_data, indent=2))
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), WebhookHandler)
    print("Webhook server running on http://localhost:8000/webhook")
    print("Start ngrok with: ngrok http 8000")
    server.serve_forever()
```

### Testing Your Webhook

1. **Start your webhook server**:
   ```bash
   python3 webhook_server.py
   ```

2. **Start ngrok in another terminal**:
   ```bash
   ngrok http 8000
   ```

3. **Update `WEBHOOK_URL` in `ESPExample.py`** with your ngrok URL:
   ```python
   WEBHOOK_URL = "https://your-ngrok-url.ngrok-free.app/webhook"
   ```

4. **Run the example**:
   ```bash
   python3 ESPExample.py
   ```

5. **Watch your webhook server** - you should see webhook events being received!

### ngrok Tips

- **Free tier**: ngrok free tier provides a random URL each time you start it. For development, this is usually fine.
- **Paid tier**: For production or persistent URLs, consider ngrok's paid plans.
- **Web Interface**: ngrok provides a web interface at http://localhost:4040 to inspect requests
- **Request Replay**: Use the ngrok web interface to replay webhook requests for testing

### Alternative: Using RequestBin

For quick testing without setting up a local server, you can use [RequestBin](https://requestbin.com/):

1. Visit https://requestbin.com/
2. Create a new bin
3. Copy the bin URL
4. Use that URL as your `WEBHOOK_URL`
5. View incoming webhook requests in the RequestBin interface

**Note**: RequestBin bins expire after a certain time, so they're only suitable for quick testing.

## Error Handling

The example includes comprehensive error handling. If an operation fails, you'll see:
- HTTP status code
- Error response body
- Stack trace for debugging

Common issues:
- **401 Unauthorized**: Invalid or missing API key
- **403 Forbidden**: Resource already exists or insufficient permissions
- **404 Not Found**: Resource ID doesn't exist
- **422 Unprocessable Entity**: Invalid request body or parameters

## Python SDK Installation

### Install from PyPI (Recommended)

```bash
pip3 install sendpost-python-sdk
```

### Install from Source

If you're using the SDK from the local repository:

```bash
cd ../sendpost-python-sdk
pip3 install -e .
```

**Note**: Always use `pip3` to ensure you're installing packages for Python 3.

### Verify Installation

```python
import sendpost_python_sdk
print(sendpost_python_sdk.__version__)
```

## Code Examples

### Basic Email Sending

```python
from sendpost_python_sdk import Configuration, ApiClient
from sendpost_python_sdk.api import EmailApi
from sendpost_python_sdk.models import EmailMessageObject, EmailMessageFrom, EmailMessageToInner

# Configure API key
config = Configuration(host="https://api.sendpost.io/api/v1")
config.api_key['subAccountAuth'] = "your_sub_account_api_key"

# Create email message
email_message = EmailMessageObject()
email_message.from_addr = EmailMessageFrom(email="sender@example.com", name="Sender")
email_message.to = [EmailMessageToInner(email="recipient@example.com", name="Recipient")]
email_message.subject = "Test Email"
email_message.html_body = "<h1>Hello!</h1>"
email_message.text_body = "Hello!"

# Send email
with ApiClient(config) as api_client:
    email_api = EmailApi(api_client)
    response = email_api.send_email(email_message)
    print(f"Message ID: {response[0].message_id}")
```

### Getting Statistics

```python
from sendpost_python_sdk import Configuration, ApiClient
from sendpost_python_sdk.api import StatsApi
from datetime import datetime, timedelta

# Configure API key
config = Configuration(host="https://api.sendpost.io/api/v1")
config.api_key['accountAuth'] = "your_account_api_key"

# Get stats for last 7 days
to_date = datetime.now().date()
from_date = to_date - timedelta(days=7)

with ApiClient(config) as api_client:
    stats_api = StatsApi(api_client)
    stats = stats_api.account_subaccount_stat_subaccount_id_get(
        from_date, to_date, sub_account_id
    )
    for stat in stats:
        print(f"Date: {stat.date}, Processed: {stat.stats.processed}")
```

## Next Steps

After running the example:

1. **Customize for Your Use Case**: Modify the example to match your specific requirements
2. **Integrate with Your Application**: Use the SDK in your own Python application
3. **Set Up Webhooks**: Configure your webhook endpoint to receive email events
4. **Monitor Statistics**: Set up regular monitoring of your email performance
5. **Optimize Deliverability**: Use IP pools and domain verification to improve deliverability

## Additional Resources

- [SendPost API Documentation](https://docs.sendpost.io)
- [SendPost Python SDK](https://github.com/sendpost/sendpost_python_sdk)
- [SendPost Developer Portal](https://app.sendpost.io)

## Support

For questions or issues:
- Email: hello@sendpost.io
- Website: https://sendpost.io
- Documentation: https://docs.sendpost.io

## License

This example is provided as-is for demonstration purposes.

