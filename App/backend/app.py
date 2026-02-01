from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from keybert import KeyBERT
from gtts import gTTS
import os
import uuid

# ==========================================
# SETUP & CONFIGURATION
# ==========================================
app = Flask(__name__)
CORS(app)

MEDIA_FOLDER = os.path.join(os.getcwd(), 'media')
os.makedirs(MEDIA_FOLDER, exist_ok=True)

kw_model = KeyBERT()

# ==========================================
# HELPER: SERVE FILES
# ==========================================
@app.route('/media/<path:filename>')
def serve_media(filename):
    return send_from_directory(MEDIA_FOLDER, filename)

# ==========================================
# TASK A: SMART VISUALS (KeyBERT)
# Responsibility: Find the best noun for Unsplash
# ==========================================
def get_smart_image_keyword(text_segment):
    """
    Analyzes the text segment and extracts the single most relevant noun.
    """
    try:
        keywords = kw_model.extract_keywords(
            text_segment, 
            keyphrase_ngram_range=(1, 1), 
            stop_words='english', 
            top_n=1
        )
        if keywords:
            return keywords[0][0]
        
        return "education"
        
    except Exception as e:
        print(f"KeyBERT Error: {e}")
        return "abstract"

# ==========================================
# TASK B: AUDIO SYNTHESIS (gTTS)
# Responsibility: Create temporary MP3 files
# ==========================================
def generate_audio(text_segment):
    """
    Converts text to speech and saves it with a unique ID.
    """
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(MEDIA_FOLDER, filename)
    
    tts = gTTS(text=text_segment, lang='en')
    tts.save(filepath)
    
    return filename

# ==========================================
# TASK C: ASSET PACKAGING (API Endpoint)
# Responsibility: Bundle Audio/Video data for Frontend
# ==========================================
@app.route("/generate-video-assets", methods=['POST'])
def generate_assets():
    """
    Accepts a full script, breaks it into scenes, and runs the ML/Audio pipeline.
    """
    data = request.json
    full_script = data.get('text', '')

    if not full_script:
        return jsonify({"error": "No text provided"}), 400
    
    raw_segments = full_script.split('.')
    segments = [s.strip() for s in raw_segments if len(s) > 10]
    
    timeline = []
    print(f"Processing {len(segments)} scenes...")

    for i, segment in enumerate(segments):
        
        keyword = get_smart_image_keyword(segment)
        
        audio_filename = generate_audio(segment)
        
        scene = {
            "id": i,
            "text": segment,
            "image_keyword": keyword,
            "image_url": f"https://source.unsplash.com/1600x900/?{keyword}",
            "audio_url": f"http://127.0.0.1:5000/media/{audio_filename}",
            "duration": 5
        }
        
        timeline.append(scene)
        
    return jsonify({"timeline": timeline})

if __name__ == "__main__":
    app.run(debug=True, port=5000)