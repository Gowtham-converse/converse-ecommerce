import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import EmailStr
from fastapi import HTTPException
import random
 

def generate_otp():
    otp = random.randint(100000, 999999)  # Generate a random 6-digit number
    return otp

def send_otp_email_for_login(recipient_email: EmailStr):

    OTP=generate_otp()

    sender_email = 'loggerkey314@gmail.com'  #our mail Id
    password = 'wgaw vdgv xxsc xwjw'  #our password
    subject = "OTP Verification"
    body = f"Your OTP for verification is: {OTP}"
 
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
 
    message.attach(MIMEText(body, "plain"))
 
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            return OTP
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send OTP email: {str(e)}")
    