# backend/main.py

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
CORS(app)  # Allows your React Frontend to talk to this server

# Create 'media' folder to store your generated MP3s
MEDIA_FOLDER = os.path.join(os.getcwd(), 'media')
os.makedirs(MEDIA_FOLDER, exist_ok=True)

# LOAD ML MODEL (Task A Pre-load)
# We load KeyBERT once when the server starts to avoid delays later
print("Loading KeyBERT model... (This may take a minute)")
kw_model = KeyBERT()

# ==========================================
# HELPER: SERVE FILES
# ==========================================
# This allows the frontend to play audio via URL (e.g., localhost:5000/media/xyz.mp3)
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
        # Extract 1 keyword. keyphrase_ngram_range=(1,1) ensures single words.
        keywords = kw_model.extract_keywords(
            text_segment, 
            keyphrase_ngram_range=(1, 1), 
            stop_words='english', 
            top_n=1
        )
        # If KeyBERT finds a word, return it.
        if keywords:
            return keywords[0][0]
        
        # Fallback if the sentence is too short or weird
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
    # Use UUID to ensure every file has a unique name (no overwriting)
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(MEDIA_FOLDER, filename)
    
    # Generate audio
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
    
    # 1. Split script into segments (Scenes)
    # We split by periods to get sentences.
    raw_segments = full_script.split('.')
    # Filter out empty strings or very short fragments
    segments = [s.strip() for s in raw_segments if len(s) > 10]
    
    timeline = []
    print(f"Processing {len(segments)} scenes...")

    # 2. Process each segment through your pipeline
    for i, segment in enumerate(segments):
        
        # Run Task A: Get the visual keyword
        keyword = get_smart_image_keyword(segment)
        
        # Run Task B: Generate the audio file
        audio_filename = generate_audio(segment)
        
        # Run Task C: Package it all together
        scene = {
            "id": i,
            "text": segment,
            "image_keyword": keyword,
            # We construct a dynamic Unsplash URL using the keyword
            "image_url": f"https://source.unsplash.com/1600x900/?{keyword}",
            # We construct the local audio URL
            "audio_url": f"http://127.0.0.1:5000/media/{audio_filename}",
            "duration": 5 # Placeholder (Member 5 handles exact duration calculation)
        }
        
        timeline.append(scene)
        
    # Return the clean list to the Frontend
    return jsonify({"timeline": timeline})

if __name__ == "__main__":
    app.run(debug=True, port=5000)