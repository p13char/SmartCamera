import cv2
import sys
from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera 
from flask_basicauth import BasicAuth
import time


# Set email update interval
email_update_interval = 30  # 1/2 minute
video_camera = VideoCamera()

# Initialize Flask app with basic authentication
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'user'
app.config['BASIC_AUTH_PASSWORD'] = 'pass'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)




@app.route('/')
@basic_auth.required
def index():
    """Render the main page."""
    return render_template('index.html')

def gen(camera):
    """Generator function for streaming the video frame by frame."""
    while True:
        frame = camera.get_frame()
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            exit()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

if __name__ == '__main__':
app.run(host='0.0.0.0', debug=False)

