import sys
import cv2
import os
import pathlib
from video_select import *

from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import QVideoWidget

from PyQt5.QtWidgets import QApplication, QMainWindow
from video_select import Ui_MainWindow
from myVideoWidget import myVideoWidget

class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.curId = 0
        self.sld_video_pressed=False  #判断当前进度条识别否被鼠标点击

        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.main_play)

        self.clip_suffix = "_clip_0%d.mp4"
        self.clip_players = []
        self.clip_player1 = QMediaPlayer()
        self.clip_player1.setVideoOutput(self.video1)
        self.clip_player2 = QMediaPlayer()
        self.clip_player2.setVideoOutput(self.video2)

        self.clip_player3 = QMediaPlayer()
        self.clip_player3.setVideoOutput(self.video3)
        self.clip_player4 = QMediaPlayer()
        self.clip_player4.setVideoOutput(self.video4)

        self.clip_player5 = QMediaPlayer()
        self.clip_player5.setVideoOutput(self.video5)
        self.clip_player6 = QMediaPlayer()
        self.clip_player6.setVideoOutput(self.video6)

        self.clip_player7 = QMediaPlayer()
        self.clip_player7.setVideoOutput(self.video7)
        self.clip_player8 = QMediaPlayer()
        self.clip_player8.setVideoOutput(self.video8)

        self.clip_player9 = QMediaPlayer()
        self.clip_player9.setVideoOutput(self.video9)

        self.clip_players.extend([self.clip_player1, self.clip_player2, self.clip_player3, self.clip_player4, self.clip_player5, self.clip_player6, self.clip_player7, self.clip_player8, self.clip_player9])


        #打开文件件
        self.open_dirs.clicked.connect(self.openDirsClicked)
        self.play_button.clicked.connect(self.click_play_button)
        self.pause_button.clicked.connect(self.click_play_pause)
        self.previous.clicked.connect(self.preVideoClick)
        self.next.clicked.connect(self.nextVideoClick)

        self.play_slide.setTracking(False)
        self.play_slide.sliderReleased.connect(self.releaseSlider)
        self.play_slide.sliderPressed.connect(self.pressSlider)
        self.play_slide.sliderMoved.connect(self.moveSlider)

    def click_play_button(self):
        self.player.play()

    def click_play_pause(self):
        self.player.pause()

    def openDirsClicked(self):
        self.videoFolder = QtWidgets.QFileDialog.getExistingDirectory(None, "选择文件夹", os.getcwd())
        if self.videoFolder != "":
            self.videoNameSet = [item for item in os.listdir(self.videoFolder) if item != ".DS_Store"]
            self.videoNameSet.sort()
            videoPath = os.path.join(self.videoFolder, self.videoNameSet[self.curId])

            self.player.setMedia(QMediaContent(QUrl("file://" + videoPath)))  # 选取视频文件
            self.player.play()  # 播放视频
            self.setWindowTitle(self.videoNameSet[self.curId])

            #裁剪视频
            videoPathObj = pathlib.Path(videoPath)
            output_dirs = str(videoPathObj.parent.parent / "output")
            video_to_clips(videoPath, output_dirs)
            p = 0
            for clip in self.clip_players:
                #print("file://" + output_dirs + "/" + videoPathObj.name[:-4]  + self.clip_suffix % p)
                clip.setMedia(QMediaContent(QUrl("file://" + output_dirs + "/" + videoPathObj.name[:-4]  + self.clip_suffix % p)))
                clip.play()
                p += 1

        else:
            print("请重新选择文件夹")


    def preVideoClick(self):
        self.curId -= 1
        if self.curId >= 0:
            videoPath = os.path.join(self.videoFolder, self.videoNameSet[self.curId])
            self.player.setMedia(QMediaContent(QUrl("file://" + videoPath)))  # 选取视频文件
            self.player.play()  # 播放视频
            self.setWindowTitle(self.videoNameSet[self.curId])


            #裁剪视频
            videoPathObj = pathlib.Path(videoPath)
            output_dirs = str(videoPathObj.parent.parent / "output")
            video_to_clips(videoPath, output_dirs)
            p = 0
            for clip in self.clip_players:
                #print("file://" + output_dirs + "/" + videoPathObj.name[:-4]  + self.clip_suffix % p)
                clip.setMedia(QMediaContent(QUrl("file://" + output_dirs + "/" + videoPathObj.name[:-4]  + self.clip_suffix % p)))
                clip.play()
                p += 1


    def nextVideoClick(self):
        self.curId += 1
        if self.curId < len(self.videoNameSet):
            videoPath = os.path.join(self.videoFolder, self.videoNameSet[self.curId])
            self.player.setMedia(QMediaContent(QUrl("file://" + videoPath)))  # 选取视频文件
            self.player.play()  # 播放视频
            self.setWindowTitle(self.videoNameSet[self.curId])


            #裁剪视频
            videoPathObj = pathlib.Path(videoPath)
            output_dirs = str(videoPathObj.parent.parent / "output")
            video_to_clips(videoPath, output_dirs)
            p = 0
            for clip in self.clip_players:
                #print("file://" + output_dirs + "/" + videoPathObj.name[:-4]  + self.clip_suffix % p)
                clip.setMedia(QMediaContent(QUrl("file://" + output_dirs + "/" + videoPathObj.name[:-4]  + self.clip_suffix % p)))
                clip.play()
                p += 1

    def pressSlider(self):
        self.sld_video_pressed = True
        print("pressed")

    def releaseSlider(self):
        self.sld_video_pressed = False

    def changeSlide(self, position):
        if not self.sld_video_pressed:  # 进度条被鼠标点击时不更新
            self.vidoeLength = self.player.duration()+0.1
            self.play_slide.setValue(round((position/self.vidoeLength)*100))
            self.lab_video.setText(str(round((position/self.vidoeLength)*100, 2))+'%')

    def moveSlider(self, position):
        if self.player.duration() > 0:  # 开始播放后才允许进行跳转
            video_position = int((position / 100) * self.player.duration())
            self.player.setPosition(video_position)
            self.lab_video.setText(str(round(position, 2)) + '%')



def video_to_clips(video_file, output_folder, resize=1, overlap=0, clip_length=90):

    os.makedirs(output_folder, exist_ok=True)

    video_cap = cv2.VideoCapture(video_file)
    fps = video_cap.get(cv2.CAP_PROP_FPS)
    vid_name = os.path.splitext(os.path.basename(video_file))[0]
    clip_name = os.path.join(output_folder, '%s_clip_%%02d.mp4' % vid_name)
    #fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_length = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    clip_num = 9
    chunk_num = int(video_length / clip_num)
    init = True

    clip_cap_list = []
    p = 0
    while video_cap.isOpened():
        # Get the next video frame
        _, frame = video_cap.read()
        # Resize the frame
        if resize != 1 and frame is not None:
            frame = cv2.resize(frame, (0, 0), fx=resize, fy=resize)
        if frame is None:
            print('There was a problem processing frame %d' %  p)
            for clip_cap_item in clip_cap_list:
                clip_cap_item.release()
            break

        if init:
            frame_size = frame.shape
            for i in range(clip_num):
                clip_cap = cv2.VideoWriter(clip_name % i,fourcc,fps,(frame_size[1], frame_size[0]))
                clip_cap_list.append(clip_cap)
            init = False

        if p >= 0 and p < chunk_num * 1:
            clip_cap_list[0].write(frame)
        elif p >= chunk_num and p < chunk_num* 2:
            clip_cap_list[1].write(frame)
        elif p >= 2 * chunk_num and p < chunk_num* 3:
            clip_cap_list[2].write(frame)
        elif p >= 3 * chunk_num and p < chunk_num* 4:
            clip_cap_list[3].write(frame)
        elif p >= 4 * chunk_num and p < chunk_num* 5:
            clip_cap_list[4].write(frame)
        elif p >= 5 * chunk_num and p < chunk_num* 6:
            clip_cap_list[5].write(frame)
        elif p >= 6 * chunk_num and p < chunk_num* 7:
            clip_cap_list[6].write(frame)
        elif p >= 7 * chunk_num and p < chunk_num* 8:
            clip_cap_list[7].write(frame)
        elif p >= 8 * chunk_num:
            clip_cap_list[8].write(frame)

        p+=1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())


