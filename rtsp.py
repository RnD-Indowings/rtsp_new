import cv2
import subprocess

# RTSP Stream URL
rtsp_url = "rtsp://127.0.0.1:8554/live"

# Open the webcam or video
cap = cv2.VideoCapture("/home/indowings/rtsp/EO00006_00.mp4")

# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get the frame rate of the video (adjust FFmpeg settings accordingly)
fps = cap.get(cv2.CAP_PROP_FPS)
print("Frame rate of input video: ", fps)

# Start FFmpeg process for RTSP streaming
ffmpeg_command = [
    'ffmpeg',
    '-re',  # Read input at native frame rate
    '-y',  # Overwrite output files
    '-f', 'rawvideo',  # Input format
    '-vcodec', 'rawvideo',  # Codec
    '-pix_fmt', 'bgr24',  # Pixel format
    '-s', '1280x720',  # Resolution
    '-r', str(fps),  # Frame rate from input video
    '-i', '-',  # Input from stdin
    '-an',  # No audio
    '-vcodec', 'libx264',  # Video codec
    '-preset', 'fast',  # Adjust preset if needed
    '-tune', 'zerolatency',  # Minimize latency
    '-f', 'rtsp',  # RTSP format
    rtsp_url  # Output RTSP stream URL
]

# Start the FFmpeg process
process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Resize frame to match RTSP streaming requirements
    frame_resized = cv2.resize(frame, (1280, 720))
    
    # Write the frame to FFmpeg process (standard input)
    process.stdin.write(frame_resized.tobytes())

    # Display frame (for debugging)
    cv2.imshow("Frame", frame_resized)

    # Press 'q' to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and FFmpeg process
cap.release()
process.stdin.close()
process.wait()
cv2.destroyAllWindows()
