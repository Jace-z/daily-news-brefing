import requests
from typing import Dict, Optional

class EmailDistributor:
    """
    Distributes news briefings via email using Resend or SendGrid REST API.
    """

    def __init__(self, api_key: str, sender_email: str, provider: str = "resend"):
        self.api_key = api_key
        self.sender_email = sender_email
        self.provider = provider.lower()

    def send_briefing(self, to_email: str, subject: str, content: str) -> bool:
        """
        Sends an email briefing.
        """
        if self.provider == "resend":
            return self._send_via_resend(to_email, subject, content)
        elif self.provider == "sendgrid":
            return self._send_via_sendgrid(to_email, subject, content)
        else:
            print(f"Unsupported email provider: {self.provider}")
            return False

    def _send_via_resend(self, to_email: str, subject: str, content: str) -> bool:
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "from": self.sender_email,
            "to": [to_email],
            "subject": subject,
            "text": content
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"Resend error: {response.status_code} - {response.text}")
            return False

    def _send_via_sendgrid(self, to_email: str, subject: str, content: str) -> bool:
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "personalizations": [{"to": [{"email": to_email}]}],
            "from": {"email": self.sender_email},
            "subject": subject,
            "content": [{"type": "text/plain", "value": content}]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 202]:
            return True
        else:
            print(f"SendGrid error: {response.status_code} - {response.text}")
            return False

if __name__ == "__main__":
    # Test (requires API key)
    # distributor = EmailDistributor(api_key="your-api-key", sender_email="onboarding@resend.dev")
    # distributor.send_briefing("user@example.com", "Your Daily News Brief", "Hello World")
    pass
