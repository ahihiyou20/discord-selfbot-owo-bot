from ultralytics import YOLO


############ NEW MODEL ############
# model = YOLO('yolov8m.pt')

# results = model.train(
#     data=r'C:\Users\ducna\Desktop\huntbot.v2-ver1.yolov5pytorch\data.yaml',
#     device="cpu",
#     weight_decay=0.0010,
#     epochs=50,
#     imgsz=640)

# ############ RESUME TRAINING ############
# model = YOLO(
#     r"C:\Users\ducna\Desktop\huntbot.v2-ver1.yolov5pytorch\runs\detect\train\weights\last.pt")

# results = model.train(resume=True)

############ PREDICT ############
model = YOLO(
    r"C:\Users\ducna\Desktop\huntbot.v2-ver1.yolov5pytorch\runs\detect\train\weights\best.pt")

results = model.predict(r"C:\Users\ducna\Desktop\huntbot\captchas",
                        visualize=True,
                        augment=True,
                        conf=0.15,
                        max_det=5,
                        save=True,
                        show_conf=False,
                        show_boxes=True,
                        save_txt=True
                        )
