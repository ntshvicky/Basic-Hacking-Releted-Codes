import cv2

# Define the RTSP URL
username = "camerausername"
password = "camerapassword"
ip_address = "cameraipaddress"
port = "80"
channel = "1"  # Channel, choose between based on nos of cameras you have connected, you can use loop also to see all cameras
subtype = "0"  # Stream Type, choose Main Stream (0) or Sub Stream (1)

rtsp_url = f"rtsp://{username}:{password}@{ip_address}:{port}/cam/realmonitor?channel={channel}&subtype={subtype}"

# Create a VideoCapture object for the RTSP stream
cap = cv2.VideoCapture(rtsp_url)

# Check if the stream is opened successfully
if not cap.isOpened():
    print("Error: Could not open RTSP stream.")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Display the video frame
        cv2.imshow("RTSP Stream", frame)

        # Exit when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()
