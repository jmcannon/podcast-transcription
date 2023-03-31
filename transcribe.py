import json
import subprocess
import os
import sys
import shutil

# Whisper does not work on Python 3.11!

# source venv/bin/activate
# python transcribe.py audio/podcast.mp3 medium

# Currently the "medium" model seems to produce near 100% accuracy results on podcasts.
# Use "tiny" for testing.

# Whisper has a Python module, but it doesn't currently support outputting JSON or word level timestamps.
# Check if its updated in the future.

audio_path = sys.argv[1]
model = sys.argv[2] if len(sys.argv) == 3 else 'medium'

file_name = os.path.splitext(os.path.basename(audio_path))[0]

transcription = subprocess.run(['whisper',
                                audio_path,
                                '--language', 'Turkish',
                                '--model', model,
                                '--word_timestamps', 'True',
                                '--output_format', 'json',
                                ])

with open(file_name + '.json', 'r') as file:
    data = json.load(file)

segments = data["segments"]
result = {
    "showName": "",
    "episodeName": "",
    "publishDate": "",
    "transcription": "",
}

words = []
for segment in segments:
    for word in segment["words"]:
        words.append({"word": word["word"], "start": word["start"]})

result["transcription"] = words

with open('output/' + file_name + '.json', 'w') as file:
    json.dump(result, file)

# Save the raw Whisper output in case I ever want to process it again.
shutil.move(file_name + '.json', "whisper-results")


