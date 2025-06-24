import os
import time

import streamlit as st
from pathlib import Path

from docutils.nodes import label
from nicegui.functions.download import download

from downloader import downloader
import streamlit_shadcn_ui as ui

def download_video_with_progress(youtube_to_find, chosen_res):
    progress_bar_video = st.progress(0)
    progress_text_video = st.empty()
    def progress_hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                percent = int(downloaded / total * 100)
                progress_bar_video.progress(percent)
                progress_text_video.text(f"Downloading video: {percent}%")
        elif d['status'] == 'finished':
            progress_bar_video.progress(100)
            progress_text_video.text("Progress: 100% - Download finished!")

    youtube_to_find.download_video(str(chosen_res), folder_path=None, progress_callback=progress_hook)
    progress_bar_video.empty()



def download_audio_with_progress(youtube_to_find):
    progress_bar_audio = st.progress(0)
    progress_text_audio = st.empty()
    def progress_hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                percent = int(downloaded / total * 100)
                progress_bar_audio.progress(percent)
                progress_text_audio.text(f"Downloading audio: {percent}%")
        elif d['status'] == 'finished':
            progress_bar_audio.progress(100)
            progress_text_audio.text("Progress: 100% - Download finished!")
    youtube_to_find.download_audio(folder_path=None, progress_callback=progress_hook)
    progress_bar_audio.empty()



def main():
    ytDlp = {
    'quiet': True,
    'skip_download': True
}






    st.header("YouTube Downloader 🎬")
    youtube_link = st.text_input("Enter the YouTube video link:",key='youtube_link_input')
    if youtube_link:
        available_res = [""]
        youtube_to_find= downloader(youtube_link)
        channel_url, title, category, thumbnail, media_type, uploader = youtube_to_find.get_info(yld_opts=ytDlp)
        channel_profile_avatar_link,official_link=youtube_to_find.get_channel_avatar()
        res= youtube_to_find.get_best_avc_formats_by_resolution()
        for resolution, format_id in res:
            available_res.append(f'{resolution} - Format ID: {format_id}')
        st.subheader("Video Information")
        st.write(f"**Title:** {title}")
        st.image(thumbnail, caption=f"Thumbnail for {title}", use_container_width=True)

        st.markdown(f"""
        <a href="{official_link}" target="_blank">
            <img src="{channel_profile_avatar_link}"
                style="width:120px; height:120px; border-radius:50%; border:2px solid #ccc;">
        </a>
        
        """,unsafe_allow_html=True)
        st.write(f"**Uploader:** {uploader}")
        #st.write(f"**Uploader Channel URL:** [Link]({channel_url})")
        st.write(f"**video Category:** {', '.join(category) if category else 'N/A'}")
        download_type = st.segmented_control("Select Download Type", options=["Video 🎬", "Audio 🎶"])

        #confirm_download = ui.alert_dialog(show=download_button, title="Confirm Download",confirm_label="Download",cancel_label="Cancel",description=f"Are you sure you want to download the video '{title}' in resolution '{chosen_resolution}'?",key='confirm_download_dialog')
        if download_type == "Video 🎬":
            chosen_resolution = st.selectbox("Select Resolution", available_res)
            download_button_video = ui.button("Download Video", key="download_button", class_name="bg-green-800 text-white")
            if download_button_video:
                st.subheader("Available Resolutions and Formats")
                chosen_res=chosen_resolution.split(" - ")[1].split(": ")[1]
                download_video_with_progress(youtube_to_find, str(chosen_res))
                #youtube_to_find.download_video(str(chosen_res), folder_path=None)
                st.success(f"Video '{title}' downloaded successfully to application")


                found_file= None

                expected_title = str(title).replace(":",": ")

                for filename in os.listdir('videos'):
                    normalized_filename = filename.replace(":",": ")
                    print("Normalized filename:", normalized_filename)
                    if normalized_filename.endswith('.mp4'):
                        print("found")
                        video_path = os.path.join('videos', filename)
                        found_file = os.path.join('videos', filename)
                    if found_file and os.path.exists(found_file):
                        with open(found_file, 'rb') as f:
                            with open(found_file, 'rb') as f:
                                video_bytes = f.read()

                        st.download_button(label=f"⬇️ Download {title} (🎬 video)",
                                       data=video_bytes,
                                       file_name=f"{title}.mp4",
                                       mime="video/mp4",key='download_video_button',type='primary')

                        time.sleep(2)
                        os.remove(found_file)



        if  download_type =='Audio 🎶':
            download_button_audio = ui.button("Download Audio", key="download_button_audio", class_name="bg-green-800 text-white")
            if download_button_audio:
                #chosen_res = chosen_resolution.split(" - ")[1].split(": ")[1]
                download_audio_with_progress(youtube_to_find)
                #youtube_to_find.download_audio(folder_path=None)
                st.success(f"Audio '{title}' downloaded successfully to application")

                found_file = None

                expected_title = str(title).replace(":", ": ")

                for filename in os.listdir('audios'):
                    normalized_filename = filename.replace(":", ": ")
                    print("Normalized filename:", normalized_filename)
                    if normalized_filename.endswith('.mp3'):
                        print("found")
                        audio_path = os.path.join('audios', filename)
                        found_file = os.path.join('audios', filename)
                    if found_file and os.path.exists(found_file):

                        with open(found_file, 'rb') as f:
                            audio_bytes = f.read()

                        st.download_button(label=f"⬇️Download {title} (🎶 audio) ",
                                       data=audio_bytes,
                                       file_name=f"{title}.mp3",
                                       mime="audio/mp3",key='download_audio_button',type='primary')

                        time.sleep(2)
                        os.remove(found_file)














if __name__ == "__main__":
    main()





