from flask import Flask, render_template, request, send_from_directory, url_for
from utils.video_processor import process_video
from utils.report_generator import generate_pdf_report
import os

app = Flask(__name__)

# ensure folders exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs/reports", exist_ok=True)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():

    video = request.files['video']
    case_id = request.form.get('case_id') or "CASE_001"

    path = "uploads/input.mp4"
    video.save(path)

    # PROCESS VIDEO
    events = process_video(path)

    # GENERATE REPORT
    report_file = generate_pdf_report(events, case_id)

    report_name = os.path.basename(report_file)

    return render_template(
        "result.html",
        events=events,
        report_file=report_name
    )


# DOWNLOAD ROUTE (IMPORTANT FIX)
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(
        'outputs/reports',
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)