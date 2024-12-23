import cv2

cv2.namedWindow("RTSP View", cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture("rtsp://192.168.2.95:8553/video_stream")   #iwpl1u rpi5 address in correspondence to the drone's aviator
while True:
    
    ret, frame = cap.read()
    if ret:
        cv2.imshow("RTSP View", frame)
        cv2.waitKey(1)
    else:
        print("unable to open stream")
        break
cap.release()
cv2.destroyAllWindows()
