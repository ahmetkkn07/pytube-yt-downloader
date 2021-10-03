from PyQt5.QtWidgets import QMessageBox

import pytube
from pytube import YouTube


class YoutubeDownloader:

    def get_options(self, link):
        yt = YouTube(link, on_progress_callback=self.progress_function,
                     on_complete_callback=self.completed)
        self.videos = yt.streams.filter(audio_codec='mp4a.40.2')
        return self.videos
    filesize = 0

    def download_video(self, index):
        global filesize
        video: pytube.Stream
        video = self.videos[index]
        filesize = video.filesize
        video.download()

    def completed(self, stream, file_path):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(f"İndirme Tamamlandı.\nDosya Konumu: {file_path}")
        msgBox.setWindowTitle("Bilgi")
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            from videoDownloader import progressBar_download
            progressBar_download.setValue(0)

    def progress_function(self, chunk, file_handle, bytes_remaining):
        global filesize
        remaining = (100 * bytes_remaining) / filesize
        step = 100 - int(remaining)
        from videoDownloader import progressBar_download
        progressBar_download.setValue(step)
