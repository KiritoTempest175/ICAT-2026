import requests

# This simulates data coming from Member 2 (The AI Engineer)
test_data = {
    "text": "Photosynthesis is the process by which plants make food. They use sunlight and water."
}

# Call your API
response = requests.post("http://127.0.0.1:5000/generate-video-assets", json=test_data)

# Check results
print("Status:", response.status_code)
data = response.json()
for scene in data['timeline']:
    print(f"Scene {scene['id']}: Keyword='{scene['image_keyword']}' | Audio={scene['audio_url']}")