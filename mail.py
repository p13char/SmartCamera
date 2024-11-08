import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import cv2
import numpy as np

fromEmail = "p13chartestpi@gmail.com"
fromEmailPassword = "ggzw iqjd vuqk gulk"

# Recipient email
toEmail = "p13chartestpi@gmail.com"

def sendEmail(image):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Motion Detected'
    msgRoot['From'] = fromEmail
    msgRoot['To'] = toEmail

    # Add alternative plain-text and HTML parts to the message
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    # Plain text version
    text = "Motion detected. Please see the attached image for details."
    msgText = MIMEText(text, 'plain')
    msgAlternative.attach(msgText)

    # HTML version with inline image
    html = """
    <html>
    <body>
        <h3>Motion Detected</h3>
        <p>Please see the attached image for details:</p>
        <img src="cid:image1" style="width:100%; max-width:600px;">
    </body>
    </html>
    """
    msgText = MIMEText(html, 'html')
    msgAlternative.attach(msgText)

    # Encode the image to bytes
    _, image_encoded = cv2.imencode('.jpg', image)
    image_bytes = image_encoded.tobytes()

    # Attach the image with a Content-ID
    msgImage = MIMEImage(image_bytes)
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    # Set up the SMTP server and send the email
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(fromEmail, fromEmailPassword)
    smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
    smtp.quit()
    print("Email sent successfully.")
