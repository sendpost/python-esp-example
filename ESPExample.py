#!/usr/bin/env python3
"""
Comprehensive SendPost Python SDK Example for Email Service Providers (ESPs)

This example demonstrates a complete workflow that an ESP would typically follow:
1. Create sub-accounts for different clients or use cases
2. Set up webhooks to receive email event notifications
3. Add and verify sending domains
4. Send transactional and marketing emails
5. Retrieve message details for tracking and debugging
6. Monitor statistics via IPs and IP pools
7. Manage IP pools for better deliverability control

To run this example:
1. Set environment variables:
   - SENDPOST_SUB_ACCOUNT_API_KEY: Your sub-account API key
   - SENDPOST_ACCOUNT_API_KEY: Your account API key
2. Or modify the API_KEY constants below
3. Update email addresses and domain names with your verified values
4. Run: python ESPExample.py
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Optional, List

# Add the parent directory to the path to import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sendpost-python-sdk'))

import sendpost_python_sdk
from sendpost_python_sdk import Configuration, ApiClient
from sendpost_python_sdk.api import (
    SubAccountApi, WebhookApi, DomainApi, EmailApi, MessageApi,
    StatsApi, StatsAApi, IPApi, IPPoolsApi
)
from sendpost_python_sdk.models import (
    CreateSubAccountRequest, CreateWebhookRequest, CreateDomainRequest,
    EmailMessageObject, EmailAddress, Recipient,
    IPPoolCreateRequest, EIP
)
from sendpost_python_sdk.exceptions import ApiException


class ESPExample:
    """SendPost Python SDK Example for Email Service Providers"""
    
    # API Configuration
    BASE_PATH = "https://api.sendpost.io/api/v1"
    
    # API Keys - Set these or use environment variables
    SUB_ACCOUNT_API_KEY = os.getenv("SENDPOST_SUB_ACCOUNT_API_KEY", "YOUR_SUB_ACCOUNT_API_KEY_HERE")
    ACCOUNT_API_KEY = os.getenv("SENDPOST_ACCOUNT_API_KEY", "YOUR_ACCOUNT_API_KEY_HERE")
    
    # Configuration - Update these with your values
    TEST_FROM_EMAIL = "sender@yourdomain.com"
    TEST_TO_EMAIL = "recipient@example.com"
    TEST_DOMAIN_NAME = "yourdomain.com"
    WEBHOOK_URL = "https://your-webhook-endpoint.com/webhook"
    
    def __init__(self):
        """Initialize the ESP example"""
        self.created_sub_account_id: Optional[int] = None
        self.created_sub_account_api_key: Optional[str] = None
        self.created_webhook_id: Optional[int] = None
        self.created_domain_id: Optional[str] = None
        self.created_ip_pool_id: Optional[int] = None
        self.sent_message_id: Optional[str] = None
    
    def _get_sub_account_config(self) -> Configuration:
        """Configure sub-account authentication"""
        config = Configuration(host=self.BASE_PATH)
        config.api_key['subAccountAuth'] = self.SUB_ACCOUNT_API_KEY
        return config
    
    def _get_account_config(self) -> Configuration:
        """Configure account authentication"""
        config = Configuration(host=self.BASE_PATH)
        config.api_key['accountAuth'] = self.ACCOUNT_API_KEY
        return config
    
    def list_sub_accounts(self):
        """Step 1: List all sub-accounts"""
        print("\n=== Step 1: Listing All Sub-Accounts ===")
        
        try:
            config = self._get_account_config()
            with ApiClient(config) as api_client:
                sub_account_api = SubAccountApi(api_client)
                
                print("Retrieving all sub-accounts...")
                sub_accounts = sub_account_api.get_all_sub_accounts()
                
                print(f"✓ Retrieved {len(sub_accounts)} sub-account(s)")
                for sub_account in sub_accounts:
                    print(f"  - ID: {sub_account.id}")
                    print(f"    Name: {sub_account.name}")
                    print(f"    API Key: {sub_account.api_key}")
                    account_type = "Plus" if (sub_account.type and sub_account.type == 1) else "Regular"
                    print(f"    Type: {account_type}")
                    blocked = "Yes" if (sub_account.blocked and sub_account.blocked) else "No"
                    print(f"    Blocked: {blocked}")
                    if sub_account.created:
                        print(f"    Created: {sub_account.created}")
                    print()
                    
                    # Use first sub-account if none selected
                    if self.created_sub_account_id is None and sub_account.id:
                        self.created_sub_account_id = sub_account.id
                        self.created_sub_account_api_key = sub_account.api_key
                        
        except ApiException as e:
            print(f"✗ Failed to list sub-accounts:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def create_sub_account(self):
        """Step 2: Create a new sub-account"""
        print("\n=== Step 2: Creating Sub-Account ===")
        
        try:
            config = self._get_account_config()
            with ApiClient(config) as api_client:
                sub_account_api = SubAccountApi(api_client)
                
                # Create new sub-account request
                new_sub_account = CreateSubAccountRequest()
                new_sub_account.name = f"ESP Client - {int(datetime.now().timestamp())}"
                
                print(f"Creating sub-account: {new_sub_account.name}")
                
                sub_account = sub_account_api.create_sub_account(new_sub_account)
                
                self.created_sub_account_id = sub_account.id
                self.created_sub_account_api_key = sub_account.api_key
                
                print("✓ Sub-account created successfully!")
                print(f"  ID: {self.created_sub_account_id}")
                print(f"  Name: {sub_account.name}")
                print(f"  API Key: {self.created_sub_account_api_key}")
                account_type = "Plus" if (sub_account.type and sub_account.type.value == 1) else "Regular"
                print(f"  Type: {account_type}")
                
        except ApiException as e:
            print(f"✗ Failed to create sub-account:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def create_webhook(self):
        """Step 3: Create a webhook"""
        print("\n=== Step 3: Creating Webhook ===")
        
        try:
            config = self._get_account_config()
            with ApiClient(config) as api_client:
                webhook_api = WebhookApi(api_client)
                
                # Create new webhook
                new_webhook = CreateWebhookRequest()
                new_webhook.url = self.WEBHOOK_URL
                new_webhook.enabled = True
                
                # Configure which events to receive
                new_webhook.processed = True      # Email processed
                new_webhook.delivered = True       # Email delivered
                new_webhook.dropped = True         # Email dropped
                new_webhook.soft_bounced = True    # Soft bounce
                new_webhook.hard_bounced = True    # Hard bounce
                new_webhook.opened = True           # Email opened
                new_webhook.clicked = True         # Link clicked
                new_webhook.unsubscribed = True     # Unsubscribed
                new_webhook.spam = True             # Marked as spam
                
                print("Creating webhook...")
                print(f"  URL: {new_webhook.url}")
                
                webhook = webhook_api.create_webhook(new_webhook)
                self.created_webhook_id = webhook.id
                
                print("✓ Webhook created successfully!")
                print(f"  ID: {self.created_webhook_id}")
                print(f"  URL: {webhook.url}")
                print(f"  Enabled: {webhook.enabled}")
                
        except ApiException as e:
            print(f"✗ Failed to create webhook:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def list_webhooks(self):
        """Step 4: List all webhooks"""
        print("\n=== Step 4: Listing All Webhooks ===")
        
        try:
            config = self._get_account_config()
            with ApiClient(config) as api_client:
                webhook_api = WebhookApi(api_client)
                
                print("Retrieving all webhooks...")
                webhooks = webhook_api.get_all_webhooks()
                
                print(f"✓ Retrieved {len(webhooks)} webhook(s)")
                for webhook in webhooks:
                    print(f"  - ID: {webhook.id}")
                    print(f"    URL: {webhook.url}")
                    print(f"    Enabled: {webhook.enabled}")
                    print()
                    
        except ApiException as e:
            print(f"✗ Failed to list webhooks:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def add_domain(self):
        """Step 5: Add a sending domain"""
        print("\n=== Step 5: Adding Domain ===")
        
        try:
            config = self._get_sub_account_config()
            with ApiClient(config) as api_client:
                domain_api = DomainApi(api_client)
                
                # Create domain request
                domain_request = CreateDomainRequest()
                domain_request.name = self.TEST_DOMAIN_NAME
                
                print(f"Adding domain: {self.TEST_DOMAIN_NAME}")
                
                domain = domain_api.subaccount_domain_post(domain_request)
                self.created_domain_id = str(domain.id) if domain.id else None
                
                print("✓ Domain added successfully!")
                print(f"  ID: {self.created_domain_id}")
                print(f"  Domain: {domain.name}")
                verified = "Yes" if (domain.verified and domain.verified) else "No"
                print(f"  Verified: {verified}")
                
                if domain.dkim:
                    print(f"  DKIM Record: {domain.dkim.text_value}")
                
                print("\n⚠️  IMPORTANT: Add the DNS records shown above to your domain's DNS settings to verify the domain.")
                
        except ApiException as e:
            print(f"✗ Failed to add domain:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def list_domains(self):
        """Step 6: List all domains"""
        print("\n=== Step 6: Listing All Domains ===")
        
        try:
            config = self._get_sub_account_config()
            with ApiClient(config) as api_client:
                domain_api = DomainApi(api_client)
                
                print("Retrieving all domains...")
                domains = domain_api.get_all_domains()
                
                print(f"✓ Retrieved {len(domains)} domain(s)")
                for domain in domains:
                    print(f"  - ID: {domain.id}")
                    print(f"    Domain: {domain.name}")
                    verified = "Yes" if (domain.verified and domain.verified) else "No"
                    print(f"    Verified: {verified}")
                    print()
                    
        except ApiException as e:
            print(f"✗ Failed to list domains:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def send_transactional_email(self):
        """Step 7: Send a transactional email"""
        print("\n=== Step 7: Sending Transactional Email ===")
        
        try:
            config = self._get_sub_account_config()
            with ApiClient(config) as api_client:
                email_api = EmailApi(api_client)
                
                # Create email message
                email_message = EmailMessageObject()
                
                # Set sender
                from_addr = EmailAddress()
                from_addr.email = self.TEST_FROM_EMAIL
                from_addr.name = "Your Company"
                email_message.var_from = from_addr
                
                # Set recipient
                recipient = Recipient()
                recipient.email = self.TEST_TO_EMAIL
                recipient.name = "Customer"
                
                # Add custom fields
                recipient.custom_fields = {
                    "customer_id": "67890",
                    "order_value": "99.99"
                }
                
                email_message.to = [recipient]
                
                # Set email content
                email_message.subject = "Order Confirmation - Transactional Email"
                email_message.html_body = "<h1>Thank you for your order!</h1><p>Your order has been confirmed and will be processed shortly.</p>"
                email_message.text_body = "Thank you for your order! Your order has been confirmed and will be processed shortly."
                
                # Enable tracking
                email_message.track_opens = True
                email_message.track_clicks = True
                
                # Add custom headers for tracking
                email_message.headers = {
                    "X-Order-ID": "12345",
                    "X-Email-Type": "transactional"
                }
                
                print("Sending transactional email...")
                print(f"  From: {self.TEST_FROM_EMAIL}")
                print(f"  To: {self.TEST_TO_EMAIL}")
                print(f"  Subject: {email_message.subject}")
                
                responses = email_api.send_email(email_message)
                
                if responses:
                    response = responses[0]
                    self.sent_message_id = response.message_id
                    
                    print("✓ Transactional email sent successfully!")
                    print(f"  Message ID: {self.sent_message_id}")
                    print(f"  To: {response.to}")
                    
        except ApiException as e:
            print(f"✗ Failed to send email:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def send_marketing_email(self):
        """Step 8: Send a marketing email"""
        print("\n=== Step 8: Sending Marketing Email ===")
        
        try:
            config = self._get_sub_account_config()
            with ApiClient(config) as api_client:
                email_api = EmailApi(api_client)
                
                # Create email message
                email_message = EmailMessageObject()
                
                # Set sender
                from_addr = EmailAddress()
                from_addr.email = self.TEST_FROM_EMAIL
                from_addr.name = "Marketing Team"
                email_message.var_from = from_addr
                
                # Set recipient
                recipient = Recipient()
                recipient.email = self.TEST_TO_EMAIL
                recipient.name = "Customer 1"
                
                email_message.to = [recipient]
                
                # Set email content
                email_message.subject = "Special Offer - 20% Off Everything!"
                email_message.html_body = (
                    "<html><body>"
                    "<h1>Special Offer!</h1>"
                    "<p>Get 20% off on all products. Use code: <strong>SAVE20</strong></p>"
                    "<p><a href=\"https://example.com/shop\">Shop Now</a></p>"
                    "</body></html>"
                )
                email_message.text_body = "Special Offer! Get 20% off on all products. Use code: SAVE20. Visit: https://example.com/shop"
                
                # Enable tracking
                email_message.track_opens = True
                email_message.track_clicks = True
                
                # Add group for analytics
                email_message.groups = ["marketing", "promotional"]
                
                # Add custom headers
                email_message.headers = {
                    "X-Email-Type": "marketing",
                    "X-Campaign-ID": "campaign-001"
                }
                
                print("Sending marketing email...")
                print(f"  From: {self.TEST_FROM_EMAIL}")
                print(f"  To: {self.TEST_TO_EMAIL}")
                print(f"  Subject: {email_message.subject}")
                
                responses = email_api.send_email(email_message)
                
                if responses:
                    response = responses[0]
                    if not self.sent_message_id:
                        self.sent_message_id = response.message_id
                    
                    print("✓ Marketing email sent successfully!")
                    print(f"  Message ID: {response.message_id}")
                    print(f"  To: {response.to}")
                    
        except ApiException as e:
            print(f"✗ Failed to send email:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def get_message_details(self):
        """Step 9: Retrieve message details"""
        print("\n=== Step 9: Retrieving Message Details ===")
        
        if not self.sent_message_id:
            print("✗ No message ID available. Please send an email first.")
            return
        
        try:
            config = self._get_account_config()
            with ApiClient(config) as api_client:
                message_api = MessageApi(api_client)
                
                print(f"Retrieving message with ID: {self.sent_message_id}")
                
                message = message_api.get_message_by_id(self.sent_message_id)
                
                print("✓ Message retrieved successfully!")
                print(f"  Message ID: {message.message_id}")
                print(f"  Account ID: {message.account_id}")
                print(f"  Sub-Account ID: {message.sub_account_id}")
                print(f"  IP ID: {message.ip_id}")
                print(f"  Public IP: {message.public_ip}")
                print(f"  Local IP: {message.local_ip}")
                print(f"  Email Type: {message.email_type}")
                
                if message.submitted_at:
                    print(f"  Submitted At: {message.submitted_at}")
                
                if message.var_from:
                    from_email = message.var_from.get('email', 'N/A') if isinstance(message.var_from, dict) else 'N/A'
                    print(f"  From: {from_email}")
                
                if message.to:
                    to_email = message.to.email if hasattr(message.to, 'email') else 'N/A'
                    print(f"  To: {to_email}")
                    if hasattr(message.to, 'name') and message.to.name:
                        print(f"    Name: {message.to.name}")
                
                if message.subject:
                    print(f"  Subject: {message.subject}")
                
                if message.ip_pool:
                    print(f"  IP Pool: {message.ip_pool}")
                
                if message.attempt:
                    print(f"  Delivery Attempts: {message.attempt}")
                    
        except ApiException as e:
            print(f"✗ Failed to get message:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def get_sub_account_stats(self):
        """Step 10: Get sub-account statistics"""
        print("\n=== Step 10: Getting Sub-Account Statistics ===")
        
        if not self.created_sub_account_id:
            print("✗ No sub-account ID available. Please create or list sub-accounts first.")
            return
        
        try:
            config = self._get_account_config()
            with ApiClient(config) as api_client:
                stats_api = StatsApi(api_client)
                
                # Get stats for the last 7 days
                to_date = datetime.now().date()
                from_date = to_date - timedelta(days=7)
                
                print(f"Retrieving stats for sub-account ID: {self.created_sub_account_id}")
                print(f"  From: {from_date}")
                print(f"  To: {to_date}")
                
                stats = stats_api.account_subaccount_stat_subaccount_id_get(
                    from_date, to_date, self.created_sub_account_id
                )
                
                print("✓ Stats retrieved successfully!")
                print(f"  Retrieved {len(stats)} stat record(s)")
                
                total_processed = 0
                total_delivered = 0
                
                for stat in stats:
                    print(f"\n  Date: {stat.date}")
                    if stat.stats:
                        stat_data = stat.stats
                        print(f"    Processed: {stat_data.processed or 0}")
                        print(f"    Delivered: {stat_data.delivered or 0}")
                        print(f"    Dropped: {stat_data.dropped or 0}")
                        print(f"    Hard Bounced: {stat_data.hard_bounced or 0}")
                        print(f"    Soft Bounced: {stat_data.soft_bounced or 0}")
                        print(f"    Unsubscribed: {stat_data.unsubscribed or 0}")
                        print(f"    Spam: {stat_data.spam or 0}")
                        
                        total_processed += stat_data.processed or 0
                        total_delivered += stat_data.delivered or 0
                
                print(f"\n  Summary (Last 7 days):")
                print(f"    Total Processed: {total_processed}")
                print(f"    Total Delivered: {total_delivered}")
                
        except ApiException as e:
            print(f"✗ Failed to get stats:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def get_aggregate_stats(self):
        """Step 11: Get aggregate statistics"""
        print("\n=== Step 11: Getting Aggregate Statistics ===")
        
        if not self.created_sub_account_id:
            print("✗ No sub-account ID available. Please create or list sub-accounts first.")
            return
        
        try:
            config = self._get_account_config()
            with ApiClient(config) as api_client:
                stats_api = StatsApi(api_client)
                
                # Get aggregate stats for the last 7 days
                to_date = datetime.now().date()
                from_date = to_date - timedelta(days=7)
                
                print(f"Retrieving aggregate stats for sub-account ID: {self.created_sub_account_id}")
                print(f"  From: {from_date}")
                print(f"  To: {to_date}")
                
                aggregate_stat = stats_api.account_subaccount_stat_subaccount_id_aggregate_get(
                    from_date, to_date, self.created_sub_account_id
                )
                
                print("✓ Aggregate stats retrieved successfully!")
                print(f"  Processed: {aggregate_stat.processed or 0}")
                print(f"  Delivered: {aggregate_stat.delivered or 0}")
                print(f"  Dropped: {aggregate_stat.dropped or 0}")
                print(f"  Hard Bounced: {aggregate_stat.hard_bounced or 0}")
                print(f"  Soft Bounced: {aggregate_stat.soft_bounced or 0}")
                print(f"  Unsubscribed: {aggregate_stat.unsubscribed or 0}")
                print(f"  Spam: {aggregate_stat.spam or 0}")
                
        except ApiException as e:
            print(f"✗ Failed to get aggregate stats:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def list_ips(self):
        """Step 12: List all IPs"""
        print("\n=== Step 12: Listing All IPs ===")
        
        try:
            config = self._get_account_config()
            with ApiClient(config) as api_client:
                ip_api = IPApi(api_client)
                
                print("Retrieving all IPs...")
                ips = ip_api.get_all_ips()
                
                print(f"✓ Retrieved {len(ips)} IP(s)")
                for ip in ips:
                    print(f"  - ID: {ip.id}")
                    print(f"    IP Address: {ip.public_ip}")
                    if ip.reverse_dns_hostname:
                        print(f"    Reverse DNS: {ip.reverse_dns_hostname}")
                    if ip.created:
                        print(f"    Created: {ip.created}")
                    print()
                    
        except ApiException as e:
            print(f"✗ Failed to list IPs:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def create_ip_pool(self):
        """Step 13: Create an IP Pool"""
        print("\n=== Step 13: Creating IP Pool ===")
        
        try:
            config = self._get_account_config()
            with ApiClient(config) as api_client:
                ip_pools_api = IPPoolsApi(api_client)
                
                # First, get available IPs
                ip_api = IPApi(api_client)
                ips = ip_api.get_all_ips()
                
                if not ips:
                    print("⚠️  No IPs available. Please allocate IPs first.")
                    return
                
                # Create IP pool request
                pool_request = IPPoolCreateRequest()
                pool_request.name = f"Marketing Pool - {int(datetime.now().timestamp())}"
                pool_request.routing_strategy = 0  # 0 = RoundRobin, 1 = EmailProviderStrategy
                
                # Add IPs to the pool (convert IP to EIP)
                pool_ips = []
                # Add first available IP (you can add more)
                if ips:
                    eip = EIP()
                    eip.public_ip = ips[0].public_ip
                    pool_ips.append(eip)
                pool_request.ips = pool_ips
                
                print(f"Creating IP pool: {pool_request.name}")
                print("  Routing Strategy: Round Robin")
                print(f"  IPs: {len(pool_ips)}")
                
                ip_pool = ip_pools_api.create_ip_pool(pool_request)
                self.created_ip_pool_id = ip_pool.id
                
                print("✓ IP pool created successfully!")
                print(f"  ID: {self.created_ip_pool_id}")
                print(f"  Name: {ip_pool.name}")
                print(f"  Routing Strategy: {ip_pool.routing_strategy}")
                print(f"  IPs in pool: {len(ip_pool.ips) if ip_pool.ips else 0}")
                
        except ApiException as e:
            print(f"✗ Failed to create IP pool:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def list_ip_pools(self):
        """Step 14: List all IP Pools"""
        print("\n=== Step 14: Listing All IP Pools ===")
        
        try:
            config = self._get_account_config()
            with ApiClient(config) as api_client:
                ip_pools_api = IPPoolsApi(api_client)
                
                print("Retrieving all IP pools...")
                ip_pools = ip_pools_api.get_all_ip_pools()
                
                print(f"✓ Retrieved {len(ip_pools)} IP pool(s)")
                for ip_pool in ip_pools:
                    print(f"  - ID: {ip_pool.id}")
                    print(f"    Name: {ip_pool.name}")
                    print(f"    Routing Strategy: {ip_pool.routing_strategy}")
                    print(f"    IPs in pool: {len(ip_pool.ips) if ip_pool.ips else 0}")
                    if ip_pool.ips:
                        for ip in ip_pool.ips:
                            print(f"      - {ip.public_ip}")
                    print()
                    
        except ApiException as e:
            print(f"✗ Failed to list IP pools:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def get_account_stats(self):
        """Step 15: Get account-level statistics"""
        print("\n=== Step 15: Getting Account-Level Statistics ===")
        
        try:
            config = self._get_account_config()
            with ApiClient(config) as api_client:
                stats_a_api = StatsAApi(api_client)
                
                # Get stats for the last 7 days
                to_date = datetime.now().date()
                from_date = to_date - timedelta(days=7)
                
                print("Retrieving account-level stats...")
                print(f"  From: {from_date}")
                print(f"  To: {to_date}")
                
                account_stats = stats_a_api.get_all_account_stats(from_date, to_date)
                
                print("✓ Account stats retrieved successfully!")
                print(f"  Retrieved {len(account_stats)} stat record(s)")
                
                for stat in account_stats:
                    print(f"\n  Date: {stat.var_date}")
                    if stat.stat:
                        stat_data = stat.stat
                        print(f"    Processed: {stat_data.processed or 0}")
                        print(f"    Delivered: {stat_data.delivered or 0}")
                        print(f"    Dropped: {stat_data.dropped or 0}")
                        print(f"    Hard Bounced: {stat_data.hard_bounced or 0}")
                        print(f"    Soft Bounced: {stat_data.soft_bounced or 0}")
                        print(f"    Opens: {stat_data.opened or 0}")
                        print(f"    Clicks: {stat_data.clicked or 0}")
                        print(f"    Unsubscribed: {stat_data.unsubscribed or 0}")
                        print(f"    Spams: {stat_data.spams or 0}")
                        
        except ApiException as e:
            print(f"✗ Failed to get account stats:")
            print(f"  Status code: {e.status}")
            print(f"  Response body: {e.body}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ Unexpected error:")
            import traceback
            traceback.print_exc()
    
    def run_complete_workflow(self):
        """Run the complete ESP workflow"""
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║   SendPost Python SDK - ESP Example Workflow                  ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        
        # Step 1: List existing sub-accounts (or create new one)
        self.list_sub_accounts()
        
        # Step 2: Create webhook for event notifications
        self.create_webhook()
        self.list_webhooks()
        
        # Step 3: Add and verify domain
        self.add_domain()
        self.list_domains()
        
        # Step 4: Send emails
        self.send_transactional_email()
        self.send_marketing_email()
        
        # Step 5: Retrieve message details
        self.get_message_details()
        
        # Step 6: Monitor statistics
        self.get_sub_account_stats()
        self.get_aggregate_stats()
        
        # Step 7: Manage IPs and IP pools
        self.list_ips()
        self.create_ip_pool()
        self.list_ip_pools()
        
        # Step 8: Get account-level overview
        self.get_account_stats()
        
        print("\n╔═══════════════════════════════════════════════════════════════╗")
        print("║   Workflow Complete!                                          ║")
        print("╚═══════════════════════════════════════════════════════════════╝")


def main():
    """Main entry point"""
    example = ESPExample()
    
    # Check if API keys are set
    if (example.SUB_ACCOUNT_API_KEY == "YOUR_SUB_ACCOUNT_API_KEY_HERE" or
        example.ACCOUNT_API_KEY == "YOUR_ACCOUNT_API_KEY_HERE"):
        print("⚠️  WARNING: Please set your API keys!")
        print("   Set environment variables:")
        print("   - SENDPOST_SUB_ACCOUNT_API_KEY")
        print("   - SENDPOST_ACCOUNT_API_KEY")
        print("   Or modify the constants in ESPExample.py")
        print()
    
    # Run the complete workflow
    example.run_complete_workflow()


if __name__ == "__main__":
    main()

