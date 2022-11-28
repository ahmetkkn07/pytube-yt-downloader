from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QImage, QPixmap

import pytube
from pytube.streams import Stream
from pytube import YouTube
import requests

from youtubeDownloader import YoutubeDownloader

HEADERS = ["Boyut", "Format", "Çözünürlük", "Progressive", "Tür", "fps/kbps"]

progressBar_download = None


class VideoDownloader(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.youtubeDownloader = YoutubeDownloader()
        self.init_ui()

    def init_ui(self):
        global progressBar_download
        self.setWindowTitle("YouTube Downloader v1.0")

        self.label_enterLink = QtWidgets.QLabel("Video linkini giriniz")
        self.lineEdit_link = QtWidgets.QLineEdit()

        self.pushButton_download = QtWidgets.QPushButton("İndir")
        self.pushButton_download.setMinimumWidth(200)
        self.pushButton_download.setEnabled(False)

        self.pushButton_list = QtWidgets.QPushButton("Listele")
        self.pushButton_list.setMinimumWidth(200)

        self.label_videoName = QtWidgets.QLabel()
        self.label_videoName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_thumbnail = QtWidgets.QLabel()
        self.label_thumbnail.setAlignment(QtCore.Qt.AlignCenter)
        self.label_thumbnail.setStyleSheet("background-color: lightgray")
        self.label_thumbnail.setFixedHeight(200)
        self.label_thumbnail.setFixedWidth(300)

        self.tableView_options = QtWidgets.QTableView()
        self.tableView_options.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableView_options.setDisabled(False)
        self.standardItemModel = QStandardItemModel()
        self.standardItemModel.setHorizontalHeaderLabels(HEADERS)

        self.tableView_options.setModel(self.standardItemModel)

        progressBar_download = QtWidgets.QProgressBar()
        progressBar_download.setValue(0)

        v_box = QVBoxLayout()
        v_box.addWidget(self.label_enterLink)
        v_box.addWidget(self.lineEdit_link)

        h_box1 = QHBoxLayout()
        h_box1.addStretch()
        h_box1.addWidget(self.pushButton_list)
        h_box1.addStretch()
        v_box.addLayout(h_box1)

        h_box3 = QHBoxLayout()
        v_box2 = QVBoxLayout()
        v_box2.addWidget(self.label_thumbnail, alignment=QtCore.Qt.AlignCenter)
        v_box2.addWidget(self.label_videoName, alignment=QtCore.Qt.AlignCenter)
        h_box3.addStretch()
        h_box3.addLayout(v_box2)
        h_box3.addStretch()
        v_box.addLayout(h_box3)

        v_box.addWidget(self.tableView_options)
        h_box2 = QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.pushButton_download)
        h_box2.addStretch()
        v_box.addLayout(h_box2)
        v_box.addWidget(progressBar_download)

        h_box = QHBoxLayout()
        h_box.addLayout(v_box)

        self.setLayout(h_box)

        self.setMinimumHeight(800)
        self.setMinimumWidth(800)

        self.pushButton_download.clicked.connect(self.download)
        self.lineEdit_link.returnPressed.connect(self.get_list)
        self.pushButton_list.clicked.connect(self.get_list)

    def get_list(self):
        link = self.lineEdit_link.text()
        self.standardItemModel.clear()
        self.standardItemModel.setHorizontalHeaderLabels(HEADERS)
        self.label_thumbnail.clear()
        self.label_thumbnail.setStyleSheet("background-color: lightgray")
        self.label_videoName.clear()
        try:
            options = self.youtubeDownloader.get_options(link)
        except:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Lütfen geçerli bir link giriniz!")
            msgBox.setWindowTitle("Hata")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                self.clear_ui()
        else:
            option: pytube.Stream
            first_video: pytube.Stream
            first_video = options[0]
            self.label_videoName.setText(first_video.title)

            image = QImage()

            image.loadFromData(requests.get(
                YouTube(self.lineEdit_link.text()).thumbnail_url).content)

            self.label_thumbnail.setPixmap(QPixmap(image))

            for index, option in enumerate(options):
                try:
                    standardItem_size = QStandardItem(str(option.filesize))
                    standardItem_mimeType = QStandardItem(
                        str(option.mime_type))
                    standardItem_resolution = QStandardItem(
                        str(option.resolution))
                    standardItem_progressive = QStandardItem(
                        str(option.is_progressive))
                    standardItem_type = QStandardItem(str(option.type))
                    standardItem_fps_abr = QStandardItem(
                        str(option.fps) + "fps")
                except AttributeError:
                    standardItem_fps_abr = QStandardItem(str(option.abr))
                finally:
                    items = [standardItem_size, standardItem_mimeType, standardItem_resolution,
                             standardItem_progressive, standardItem_type, standardItem_fps_abr]
                    self.standardItemModel.appendRow(items)
            self.pushButton_download.setEnabled(True)

    def download(self):
        self.pushButton_download.setEnabled(False)
        selectedIndex = self.tableView_options.selectedIndexes()[0].row()
        self.youtubeDownloader.download_video(selectedIndex)
        self.clear_ui()

    def clear_ui(self):
        self.label_thumbnail.clear()
        self.label_thumbnail.setStyleSheet("background-color: lightgray")
        self.label_videoName.clear()
        self.lineEdit_link.clear()
        self.standardItemModel.clear()
        self.standardItemModel.setHorizontalHeaderLabels(HEADERS)
        self.lineEdit_link.setFocus()
