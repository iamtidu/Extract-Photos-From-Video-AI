from flask import Flask, request
import os
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/extract_frames', methods=['POST'])
def extract_frames():
    video_file = request.files['video']
    video_path = 'temp_video.mp4'
    output_folder = 'extracted_frames'
    video_file.save(video_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    extract_frames_from_video(video_path, output_folder)
    return 'Frames extracted successfully!'

def extract_frames_from_video(video_path, output_path):
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    for frame_no in range(total_frames):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = video.read()

        if ret:
            frame_output_path = f"{output_path}/frame_{frame_no}.jpg"
            cv2.imwrite(frame_output_path, frame)
            print(f"Frame {frame_no} extracted and saved.")
        else:
            print(f"Error reading frame {frame_no}.")

    video.release()
    os.remove(video_path)

if __name__ == '__main__':
    app.run(debug=True)