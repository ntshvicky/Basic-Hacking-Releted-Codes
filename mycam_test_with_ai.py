import cv2
from flask import Flask, Response, render_template
from ultralytics import YOLO
import cv2
import math 

# object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

# Define your camera parameters
username = "camerausername"
password = "camerapassword"
ip_address = "cameraipaddress"
port = "80"

cameras = [
    {
        "username": username,
        "password": password,
        "ip_address": ip_address,
        "port": port,
        "channel": "1",
        "subtype": "0",
    },
    {
        "username": username,
        "password": password,
        "ip_address": ip_address,
        "port": port,
        "channel": "2",
        "subtype": "0",
    },
    {
        "username": username,
        "password": password,
        "ip_address": ip_address,
        "port": port,
        "channel": "3",
        "subtype": "0",
    },
    {
        "username": username,
        "password": password,
        "ip_address": ip_address,
        "port": port,
        "channel": "4",
        "subtype": "0",
    },
]

app = Flask(__name__)

model = YOLO("yolov8n.pt")

def generate_frames(camera_params):
    rtsp_url = f"rtsp://{camera_params['username']}:{camera_params['password']}@{camera_params['ip_address']}:{camera_params['port']}/cam/realmonitor?channel={camera_params['channel']}&subtype={camera_params['subtype']}"
    cap = cv2.VideoCapture(rtsp_url)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, stream=True, conf=0.1)

        # coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                # put box in cam
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confidence
                confidence = math.ceil((box.conf[0]*100))/100
                print("Confidence --->",confidence)

                # class name
                cls = int(box.cls[0])
                print("Class name -->", classNames[cls])

                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (90, 219, 61)
                thickness = 2

                cv2.putText(frame, classNames[cls], org, font, fontScale, color, thickness)


        # Encode the frame as JPEG
        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            continue

        # Yield the frame in bytes
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video/<int:camera_id>")
def video(camera_id):
    if 0 <= camera_id < len(cameras):
        return Response(generate_frames(cameras[camera_id]), mimetype="multipart/x-mixed-replace; boundary=frame")
    else:
        return "Camera ID not found."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
