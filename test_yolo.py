from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # load an official model

# Predict with the model
results = model('bus.jpg',show=False, 
                                save=True, 
                                show_labels=True, 
                                show_conf=True, 
                                conf=0.2, 
                                save_txt=True, 
                                line_width=2,)  # predict on an image
print(results)