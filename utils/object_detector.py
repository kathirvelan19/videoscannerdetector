from ultralytics import YOLO

model = YOLO("yolov8n.pt")


def detect_objects(frame, prev_count=0):

    results = model(frame)

    person_count = 0
    detections = []

    for r in results:

        for box in r.boxes:

            cls = int(box.cls[0])
            label = model.names[cls]

            if label == "person":
                person_count += 1

    # EVENT LOGIC (VERY IMPORTANT)

    if person_count > prev_count:
        detections.append("Person Entered Scene")

    elif person_count < prev_count:
        detections.append("Person Exited Scene")

    elif person_count >= 2:
        detections.append("Multiple Persons Detected")

    elif person_count == 1:
        detections.append("Single Person in Scene")

    return detections, person_count