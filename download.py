import yt_dlp

def download_audio_as_mp3(video_url, output_path='.'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Ejemplo de uso:
video_url = 'https://www.youtube.com/watch?v=v2AC41dglnM'  # Reemplaza con la URL del video
output_path = './'  # Reemplaza con la ruta de la carpeta de destino
download_audio_as_mp3(video_url, output_path)
