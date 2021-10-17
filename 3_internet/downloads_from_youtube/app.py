import ffmpeg
from pytube import YouTube

URL = 'https://www.youtube.com/watch?v=7jLEVrH4Bhg'
DOWNLOAD_DIR = 'data'


def download_video(url):
    # Скачивает первое видео с самым высоким разрешением
    yt = YouTube(url)
    stream_video = yt.streams.filter(file_extension='mp4').order_by(
        'resolution').desc().first()
    stream_video.download(DOWNLOAD_DIR, 'video.mp4')

    # Если у видео нет звука то скачивает audio
    if not stream_video.is_progressive:
        stream_audio = yt.streams.get_audio_only()
        stream_audio.download(DOWNLOAD_DIR, 'audio')
        # Склеиваем дорожки
        combine(audio=DOWNLOAD_DIR + '/audio',
                video=DOWNLOAD_DIR + '/video.mp4')


def combine(*, audio, video):
    # берет Аудио и Видео файлы
    audio_stream = ffmpeg.input(audio)
    video_stream = ffmpeg.input(video)
    # Склеивает видео и аудио дорожки, не меняя кодека
    # codec="copy" - Без перекодирования
    ffmpeg.output(video_stream,
                  audio_stream,
                  codec="copy",
                  filename=DOWNLOAD_DIR + '/result.mp4'
                  ).overwrite_output().run()


if __name__ == '__main__':
    download_video(URL)
