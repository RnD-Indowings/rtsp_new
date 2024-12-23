import subprocess

def start_rtsp_server():
    command = [
        "ffmpeg",
        "-re",  # Read input in real-time
        "-i", "video.mp4",  # Use video file as input
        "-c:v", "libx264",  # Encode video using H.264
        "-preset", "ultrafast",  # Speed-optimized encoding
        "-f", "rtsp",
        "rtsp://192.168.2.95:8553/live/stream"
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    start_rtsp_server()
