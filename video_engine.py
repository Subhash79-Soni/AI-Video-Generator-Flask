import os
import requests
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import edge_tts
import PIL.Image
import nltk

# 1. NLTK AI Models Load Karna
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

# 2. Pillow Error Fix
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

from moviepy.config import change_settings

# 3. ImageMagick Path
imagemagick_path = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
change_settings({"IMAGEMAGICK_BINARY": imagemagick_path})

from moviepy.editor import *

# 4. Pexels API Key - YAHAN APNI KEY DAALEIN
PEXELS_API_KEY = "your_pexels_api_key_here"

async def generate_audio(text, output_file):
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save(output_file)

def get_smart_keyword(sentence):
    """NLP ka use karke sentence se sabse best Noun (keyword) nikalta hai"""
    try:
        tokens = nltk.word_tokenize(sentence)
        tags = nltk.pos_tag(tokens)
        for word, tag in tags:
            if tag in ['NN', 'NNS', 'NNP', 'NNPS']: 
                clean_word = "".join(e for e in word if e.isalnum())
                if len(clean_word) > 2:
                    return clean_word
    except Exception as e:
        print(f"NLP Error: {e}")
    return "technology"

def get_pexels_video(keyword, index):
    url = f"https://api.pexels.com/videos/search?query={keyword}&per_page=1"
    headers = {"Authorization": PEXELS_API_KEY}
    try:
        response = requests.get(url, headers=headers).json()
        if response.get('videos'):
            video_url = response['videos'][0]['video_files'][0]['link']
            video_data = requests.get(video_url).content
            temp_path = f"temp_bg_{index}.mp4"
            with open(temp_path, "wb") as f:
                f.write(video_data)
            return temp_path
    except Exception as e:
        print(f"Pexels Error: {e}")
    return None

def create_video(text_content, output_filename):
    if not os.path.exists("output"):
        os.makedirs("output")
    output_path = os.path.join("output", output_filename)

    raw_sentences = text_content.replace('\n', '.').split('.')
    sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 2]
    
    if not sentences:
        sentences = ["No valid text provided."]

    video_clips = []
    temp_files_to_delete = []

    print(f"Total Scenes Banenge: {len(sentences)}")

    for idx, sentence in enumerate(sentences):
        print(f"--- Scene {idx + 1} processing ---")
        temp_audio_path = f"temp_audio_{idx}.mp3"
        
        # ASYNCIO THREAD FIX (Jo galti se mit gaya tha)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(generate_audio(sentence, temp_audio_path))
        loop.close()
        
        temp_files_to_delete.append(temp_audio_path)
        
        audio_clip = AudioFileClip(temp_audio_path)
        audio_duration = audio_clip.duration

        # Naya AI Keyword Logic
        keyword = get_smart_keyword(sentence)
        print(f"AI Selected Keyword: '{keyword}' for sentence: {sentence[:30]}...")
        
        bg_path = get_pexels_video(keyword, idx)

        if bg_path:
            temp_files_to_delete.append(bg_path)
            bg_clip = VideoFileClip(bg_path).subclip(0, min(audio_duration, 15)).resize(height=1080).crop(x_center=960, y_center=540, width=1920, height=1080)
        else:
            bg_clip = ColorClip(size=(1920, 1080), color=(30, 30, 30)).set_duration(audio_duration)

        txt_clip = TextClip(sentence, fontsize=70, color='white', font='Arial-Bold', method='caption', size=(1500, None))
        txt_clip = txt_clip.set_position('center').set_duration(audio_duration)

        scene_video = CompositeVideoClip([bg_clip, txt_clip]).set_audio(audio_clip)
        video_clips.append(scene_video)

    print("Sabhi scenes ko ek sath jod rahe hain...")
    final_video = concatenate_videoclips(video_clips, method="compose")
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

    final_video.close()
    for clip in video_clips:
        clip.close()
    
    for file_path in temp_files_to_delete:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
    
    return output_path