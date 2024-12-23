import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def create_rtsp_server():
    Gst.init(None)

    # Define pipeline
    pipeline = Gst.parse_launch(
        "appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=ultrafast ! "
        "rtph264pay config-interval=1 name=pay0 pt=96 ! udpsink host=127.0.0.1 port=8554"
    )
    
    # Start the pipeline
    pipeline.set_state(Gst.State.PLAYING)
    
    # Run loop
    loop = GLib.MainLoop()
    try:
        print("RTSP server running at rtsp://127.0.0.1:8554/")
        loop.run()
    except KeyboardInterrupt:
        print("Shutting down...")
        pipeline.set_state(Gst.State.NULL)

if __name__ == "__main__":
    create_rtsp_server()
