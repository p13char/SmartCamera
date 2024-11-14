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

# Track the last email sent timestamp
last_sent = 0
def check_for_objects():
    """Continuously checks for objects and sends an email alert if one is detected."""
    global last_sent
    confidence = 70
    suppression = 60
    while True:
         try:
            # Capture frame and check for objects
            frame, found_obj = video_camera.getObjects(thres =confidence/100,nms = suppression/100)
            if found_obj and (time.time() - last_sent) > email_update_interval:
                 last_sent = time.time()
                 sendEmail(frame)  # Sends the frame image via email

         except Exception as e:
             print("Error :", e)
             break
    cv2.destroyAllWindows()

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

@app.route('/video_feed')
def video_feed():
    """Route to stream the video feed."""
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start the object detection thread
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    # Run the Flask app
    app.run(host='0.0.0.0', debug=False)



