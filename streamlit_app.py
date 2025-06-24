# InstaReel Booster - Streamlit Web App with AI Script, Style & Background Music

import os
import datetime
import textwrap
import random
import streamlit as st

# Direct imports for MoviePy components to avoid `moviepy.editor` issues
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip


def ai_generate_script(topic):
    prompts = {
        "motivation": [
            "Every step you take is progress. Keep going!",
            "Your only limit is you. Break it today!",
            "Dream big. Start now. Stay consistent."
        ],
        "healing": [
            "Healing isn’t linear, but every moment counts.",
            "Breathe. Accept. Let go. Grow.",
            "You’re allowed to rest and recover."
        ],
        "self-love": [
            "You are enough just as you are.",
            "Fall in love with taking care of yourself.",
            "Your worth is not up for debate."
        ],
        "spirituality": [
            "You are more than this moment. Trust the flow.",
            "The answers lie within your stillness.",
            "The universe responds to your energy."
        ]
    }
    return random.choice(prompts.get(topic, [f"This is a placeholder script about {topic}."]))


def generate_script(topic, custom_script):
    script = custom_script.strip() if custom_script else ai_generate_script(topic)
    return textwrap.fill(script, width=70)


def generate_hashtags(topic):
    base_tags = ["#reels", "#explore", f"#{topic}", "#viral", "#shorts"]
    if topic == "motivation":
        base_tags += ["#inspiration", "#dailyquotes"]
    elif topic == "healing":
        base_tags += ["#selfcare", "#mindfulness"]
    return base_tags


def save_log(timestamp, topic, script, hashtags, filename="reel_log.csv"):
    try:
        log_entry = f"{timestamp},{topic},\"{script.replace(',', ';')}\",{','.join(hashtags)}"
        with open(filename, "a", encoding="utf-8") as file:
            file.write(log_entry + "\n")
    except Exception as e:
        st.error(f"Failed to write log file: {e}")


def create_final_video(video_path, script_text, music_path, style):
    try:
        video = VideoFileClip(video_path)
        font_color = 'white'; bg_color = 'black'; fontsize = 40
        if style == "calm":
            font_color, fontsize = 'lightblue', 36
        elif style == "bold":
            font_color, bg_color, fontsize = 'yellow', 'darkred', 48
        elif style == "energetic":
            font_color, fontsize = 'lime', 50

        subtitle = TextClip(
            script_text,
            fontsize=fontsize,
            color=font_color,
            bg_color=bg_color,
            size=video.size,
            method='caption'
        )
        subtitle = subtitle.set_duration(video.duration).set_position(('center', 'bottom'))
        final = CompositeVideoClip([video, subtitle])

        if music_path:
            audio = AudioFileClip(music_path).subclip(0, video.duration)
            final = final.set_audio(audio)

        output_filename = "final_reel.mp4"
        final.write_videofile(output_filename, codec='libx264', audio_codec='aac')
        return output_filename
    except Exception as e:
        st.error(str(e))
        return None


def main():
    st.title("🎬 InstaReel Booster - Web App")
    st.markdown("Create AI-powered Instagram reels with background music and stylized captions.")

    topic = st.selectbox("Choose your topic", ["motivation", "healing", "self-love", "spirituality"])
    style = st.selectbox("Choose your style", ["calm", "bold", "energetic"])
    custom_script = st.text_area("Custom Script (optional)")
    video_file = st.file_uploader("Upload your video (MP4, under 30s)", type="mp4")
    music_file = st.file_uploader("Upload background music (MP3, optional)", type="mp3")

    if st.button("Generate Reel"):
        if not video_file:
            st.error("Please upload a video file.")
        else:
            with open("uploaded_video.mp4", "wb") as f:
                f.write(video_file.read())

            music_path = None
            if music_file:
                with open("uploaded_music.mp3", "wb") as f:
                    f.write(music_file.read())
                    music_path = "uploaded_music.mp3"

            script_text = generate_script(topic, custom_script)
            hashtags = generate_hashtags(topic)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_log(timestamp, topic, script_text, hashtags)
            output = create_final_video("uploaded_video.mp4", script_text, music_path, style)

            if output:
                st.success("Your reel has been created!")
                st.video(output)
                st.download_button("Download Final Reel", open(output, "rb"), file_name="final_reel.mp4")

if __name__ == "__main__":
    main()
