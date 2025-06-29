import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")

@function_tool
def send_email(subject: str, html_body: str, recipient_email: str) -> Dict[str, str]:
  """ Send an email with the given subject and HTML body """
  try:
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email(EMAIL_FROM)
    to_email = To(recipient_email)
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print(f"Email response: {response.status_code}")
    
    if response.status_code == 202:
      return {"status": f"Email sent successfully to {recipient_email}"}
    else:
      return {"status": f"Email sending failed with status {response.status_code}"}
  except Exception as e:
    print(f"Error sending email: {e}")
    return {"status": "error", "message": f"Email sending failed: {str(e)}"}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report and the recipient email address. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line and the recipient email address. If the email is not sent,
try again, but only once, if it fails again, stop the process. Do not try to send the email more than twice."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
