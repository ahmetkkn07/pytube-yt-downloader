import sys
from PyQt5.QtWidgets import QApplication
from videoDownloader import VideoDownloader


def main():
    app = QApplication(sys.argv)
    videoDownloader = VideoDownloader()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
