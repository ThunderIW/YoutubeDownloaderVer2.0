import os

import yt_dlp
from pathlib import Path,PureWindowsPath




class downloader:
    def  __init__(self,youtube_link):
        self.youtube_link = youtube_link
        self.title = None
        self.channel_url = None
        self.category = None
        self.thumbnail = None
        self.type= None
        self.uploader=None
        self.res= None

    def get_best_avc_formats_by_resolution(self, ydl_opts=None):
        with yt_dlp.YoutubeDL(ydl_opts or {'quiet': True}) as ydl:
            info = ydl.extract_info(self.youtube_link, download=False)
            formats = info.get('formats', [])

        res_map = {}

        for fmt in formats:
            video_codec = fmt.get('vcodec', '')
            height = fmt.get('height')
            fps = fmt.get('fps', '')
            bitrate = fmt.get('tbr')
            format_id = fmt.get('format_id')

            if (
                    'avc' in video_codec and bitrate and height and
                    fmt.get('filesize') and fmt.get('format_note')
            ):
                label = f"{height}p{int(fps) if fps else ''}"

                # Keep only the format with the highest bitrate for this resolution
                if label not in res_map or bitrate > res_map[label]['bitrate']:
                    res_map[label] = {
                        'format_id': format_id,
                        'bitrate': bitrate,
                        'vcodec': video_codec
                    }

        # Return a sorted list of (resolution label, format_id)
        return [(label, data['format_id']) for label, data in sorted(res_map.items())]


    def get_channel_avatar(self):
        channel_avatar_pic=""
        ydl_opts={
            'quiet': True,
            'extract_flat': True,
            'skip_download': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info=ydl.extract_info(self.channel_url,download=False)
            thumbnails=info.get('thumbnails')
            channels_official_url=info.get('uploader_url')
            for thumb in thumbnails:
                #print(thumb)
                if thumb.get('resolution')=='900x900':
                    channel_avatar_pic=thumb.get('url')

        return channel_avatar_pic,channels_official_url

    def download_video(self, format_id,folder_path,progress_callback=None):
        if not folder_path:
            folder_path = Path("videos")
        output_template=os.path.join(folder_path, '%(title)s.%(ext)s') if folder_path else '%(title)s.%(ext)s'
        ydl_opts = {
            'format': f'{format_id}+bestaudio',
            'merge_output_format': 'mp4',
            'outtmpl': output_template,
            'quiet': False
        }
        if progress_callback:
            ydl_opts['progress_hooks'] = [progress_callback]
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.youtube_link])


    def download_audio(self,folder_path,progress_callback=None):
        if not folder_path:
            folder_path = Path("audios")
        output_template = os.path.join(folder_path, '%(title)s.%(ext)s') if folder_path else '%(title)s.%(ext)s'
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'quiet': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        if progress_callback:
            ydl_opts['progress_hooks'] = [progress_callback]
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.youtube_link])




    def get_info(self, yld_opts=None):
        with yt_dlp.YoutubeDL(yld_opts) as ydl:
            info = ydl.extract_info(self.youtube_link, download=False)
            '''
            for key,value in info.items():
                print(f"key:{key}")
            '''
                


            self.channel_url= info.get('channel_url', None)
            self.category= info.get('categories', None)
            self.title=info.get ('title', None)
            self.thumbnail = info.get('thumbnail', None)
            self.type= info.get('media_type', None)
            self.uploader=info.get('uploader', None)


        return self.channel_url,self.title, self.category, self.thumbnail,self.type,self.uploader








ytDlp={
    'quiet': True,
    'skip_download':True
}

#youtube_link_to_find = downloader("https://www.youtube.com/watch?v=OcNZMW03318")

#channel_url,title, Category, thumbnail,media_type,uploader=youtube_link_to_find.get_info(ytDlp)
#res = youtube_link_to_find.get_best_avc_formats_by_resolution(ytDlp)




#path_to_save=PureWindowsPath(r'D:\Python Project\YoutubeDownloader_Ver2.0\Videos')
#youtube_link_to_find.download_video('137',path_to_save)
