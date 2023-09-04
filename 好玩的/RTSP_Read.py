import cv2

cap = cv2.VideoCapture("rtsp://admin:password@192.168.10.20:554/Streaming/Channels/1")
ret, frame = cap.read()

while ret:
    ret, frame = cap.read()
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
