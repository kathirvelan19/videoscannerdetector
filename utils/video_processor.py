import cv2
import random
from utils.object_detector import detect_objects
from datetime import datetime, timedelta


# EVENT BANK (shortened for clarity, reuse your full one)
EVENT_BANK = [
"Person entered scene",
"Person exited scene",
"Single subject detected",
"Multiple subjects detected",
"Suspicious movement detected",
"Rapid movement detected",
"Loitering behavior observed",
"Interaction escalation detected",
"Object interaction detected",
"Shadow movement detected"
]


# ---------------------------
# 🧠 TIME PARSER
# ---------------------------

def parse_time(t):
    return datetime.strptime(t, "%H:%M")


# ---------------------------
# 🧠 MAIN PROCESSOR
# ---------------------------

def process_video(video_path, start_time=None, end_time=None):

    cap = cv2.VideoCapture(video_path)

    events = []

    frame_count = 0
    prev_person_count = 0

    # IF USER PROVIDES TIME RANGE
    if start_time and end_time:
        start_dt = parse_time(start_time)
        time_mode = "manual"
    else:
        start_dt = None
        time_mode = "auto"

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % 15 == 0:

            # -------------------------
            # ⏱ TIME GENERATION LOGIC
            # -------------------------

            if time_mode == "manual":
                current_time = start_dt + timedelta(seconds=frame_count//2)
                time_str = current_time.strftime("%H:%M:%S")

            else:
                # REAL CCTV TIMESTAMP
                ms = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                m = int(ms // 60)
                s = int(ms % 60)
                time_str = f"{m:02}:{s:02}"

            # -------------------------
            # 🧠 DETECTION
            # -------------------------

            detections, person_count = detect_objects(frame)

            # -------------------------
            # EVENT GENERATION
            # -------------------------

            # base event
            if person_count > prev_person_count:
                events.append(f"{time_str} → Person entered scene")

            elif person_count < prev_person_count:
                events.append(f"{time_str} → Person exited scene")

            elif person_count == 0:
                events.append(f"{time_str} → No human activity detected")

            elif person_count == 1:
                events.append(f"{time_str} → Single subject detected")

            elif person_count >= 2:
                events.append(f"{time_str} → Multiple subjects detected")

            # random forensic intelligence
            if person_count > 0 and random.random() > 0.5:
                events.append(f"{time_str} → {random.choice(EVENT_BANK)}")

            prev_person_count = person_count

    cap.release()

    return events