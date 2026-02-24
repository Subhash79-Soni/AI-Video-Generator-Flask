from flask import Flask, request, jsonify, render_template, send_from_directory
from video_engine import create_video
import time
import os

app = Flask(__name__)

# NAYA: Frontend HTML page dikhane ke liye route
@app.route('/')
def home():
    return render_template('index.html')

# NAYA: Browser ko banayi hui MP4 video bhejne ke liye route
@app.route('/output/<path:filename>')
def serve_video(filename):
    return send_from_directory('output', filename)

@app.route('/api/generate', methods=['POST'])
def generate_lumen_video():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Kripya JSON mein 'text' provide karein"}), 400
        
    user_text = data['text']
    
    try:
        filename = f"lumen_video_{int(time.time())}.mp4"
        print("Video rendering start ho rahi hai...")
        
        # Video generate karna
        final_video_path = create_video(user_text, filename)
        
        return jsonify({
            "status": "success",
            "message": "Video successfully ban gayi hai!",
            "video_url": f"/output/{filename}" # NAYA: Browser ke liye URL bhejna
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)