import os
import time

import streamlit as st
from pathlib import Path
from downloader import downloader
import streamlit_shadcn_ui as ui
def main():
    ytDlp = {
    'quiet': True,
    'skip_download': True
}


    youtube_link=st.text_input("Enter the YouTube video link:")
    if youtube_link:
        available_res = [""]
        youtube_to_find= downloader(youtube_link)
        channel_url, title, category, thumbnail, media_type, uploader = youtube_to_find.get_info(yld_opts=ytDlp)
        res= youtube_to_find.get_best_avc_formats_by_resolution()
        for resolution, format_id in res:
            available_res.append(f'{resolution} - Format ID: {format_id}')
        st.subheader("Video Information")
        st.write(f"**Title:** {title}")
        st.image(thumbnail, caption=f"Thumbnail for {title}", use_container_width=True)
        st.write(f"**Uploader:** {uploader}")
        st.write(f"**Uploader Channel URL:** [Link]({channel_url})")
        st.write(f"**Category:** {', '.join(category) if category else 'N/A'}")
        st.subheader("Available Resolutions and Formats")
        chosen_resolution = st.selectbox("Select Resolution", available_res)
        download_button = ui.button("Download Video",key="download_button", class_name="bg-green-800 text-white")
        #confirm_download = ui.alert_dialog(show=download_button, title="Confirm Download",confirm_label="Download",cancel_label="Cancel",description=f"Are you sure you want to download the video '{title}' in resolution '{chosen_resolution}'?",key='confirm_download_dialog')

        if download_button:
            chosen_res=chosen_resolution.split(" - ")[1].split(": ")[1]
            youtube_to_find.download_video(str(chosen_res), folder_path=None)
            st.success(f"Video '{title}' downloaded successfully to application")


            found_file= None
            expected_tile=title
            for filename in os.listdir('videos'):
                if expected_tile in filename  and filename.endswith('.mp4'):
                    video_path = os.path.join('videos', filename)
                    st.write(f"Video found: {filename}")
                    break
                found_file=os.path.join('videos', filename)

       
            with open(found_file,'rb') as f:
                video_bytes = f.read()

            st.download_button(label="Download Video",
                           data=video_bytes,
                           file_name=f"{title}.mp4",
                           mime="video/mp4")
            time.sleep(2)
            os.remove(found_file)




if __name__ == "__main__":
    main()





