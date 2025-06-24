@echo off
echo 🔧 Upgrading pip...
python -m pip install --upgrade pip

echo 📦 Installing required packages...
python -m pip install moviepy imageio-ffmpeg streamlit

echo 🚀 Running InstaReel Booster App...
python -m streamlit run streamlit_app.py

pause