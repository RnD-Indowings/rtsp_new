import cv2
import numpy as np
from flask import Flask, Response

app = Flask(__name__)

# RTSP stream URL
rtsp_url = "rtsp://65.0.71.42:8554/test"

# Initialize video capture from RTSP stream
cap = cv2.VideoCapture(rtsp_url)

def generate_frames():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Unable to open stream")
            break
        
        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        
        # Convert the frame to bytes and yield it for the stream
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start Flask server
    app.run(host='0.0.0.0', port=5000, debug=True)
