#  AI Video Generator (Automated Text-to-Video Engine)

An end-to-end automated video generation tool that converts text into professional, multi-scene videos. Built with Python and Flask, this engine uses Natural Language Processing (NLP) to understand the context of the text, fetches relevant stock footage, and overlays human-sounding Neural TTS (Text-to-Speech).

##  Key Features
* **Multi-Scene Generation:** Automatically splits long paragraphs into logical scenes based on sentence structure.
* **Smart Keyword Extraction (NLP):** Uses the NLTK library to analyze grammar and extract the most relevant noun (context) from each sentence to fetch accurate background videos.
* **Dynamic Stock Media:** Integrates with the Pexels API to download high-quality, context-aware stock footage on the fly.
* **Neural Voiceovers:** Utilizes `edge-tts` to generate professional, natural-sounding AI voiceovers.
* **Custom Audio Support:** Automatically detects and uses custom voice recordings (`my_voice.mp3`) if provided.
* **Interactive Web UI:** Clean and responsive frontend built with HTML/CSS/JS and served via Flask.

##  Tech Stack
* **Backend:** Python, Flask
* **Video Processing:** MoviePy, ImageMagick
* **AI & NLP:** NLTK (Natural Language Toolkit), Edge-TTS
* **External APIs:** Pexels API
* **Frontend:** HTML, CSS, JavaScript (Fetch API)

##  How to Run Locally

 * Install Required Libraries:
   pip install flask requests moviepy edge-tts pillow nltk

 * Set Up ImageMagick & Pexels API:
   * Install ImageMagick on your system and update the imagemagick_path in video_engine.py.
   * Get a free API key from Pexels and add it to the PEXELS_API_KEY variable in video_engine.py.
 * Run the Flask Server:
   python app.py

 * Generate Videos:
   Open your browser and navigate to http://127.0.0.1:5000. Enter your text and click "Video Banao"!

## Author
Subhash Chandra Soni
 * B.Tech Computer Science (2022-2026), Gopal Narayan Singh University
 * Passionate about Artificial Intelligence, Data Science, and Backend Development.
