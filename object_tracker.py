import cv2
import os, sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox
)
from PyQt5.QtCore import pyqtSlot, QDir
from PyQt5.QtGui import QImage, QPixmap
from tracker_processing import MultiTracker
from datetime import datetime
from utils import setUpLogger, print
import images.images_rc


# pyinstaller absolute path reference
os.chdir(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))
setUpLogger()


class ObjectTracker(QMainWindow):

    def __init__(self):
        super(ObjectTracker, self).__init__()
        loadUi('object_tracker.ui', self)
        self._connectSignals()
        self.enableRecord = False
        self._fps = 20.0
        self.multiTracker = None
        self.camWindowSize = None

    def _connectSignals(self):
        self.record.setShortcut('Ctrl+R')
        self.record.triggered.connect(self.startRecord)

        self.stopRecording.setShortcut('Ctrl+S')
        self.stopRecording.triggered.connect(self.stopRecord)

        self.clearCam.setShortcut('Ctrl+C')
        self.clearCam.triggered.connect(self._clearCam)

        self.openVideoPlayer.setShortcut('Ctrl+V')
        self.openVideoPlayer.triggered.connect(self._openVideoPlayer)

        self.selectTargets.setShortcut('Ctrl+A')
        self.selectTargets.triggered.connect(self._selectTargets)

        self.saveResults.setShortcut('Ctrl+S+L')
        self.saveResults.triggered.connect(self._saveResults)

        self.about.setShortcut('Ctrl+I')
        self.about.triggered.connect(self._about)

        trackersNames = MultiTracker.TrackersDict.keys()
        self.trackerType.addItems(trackersNames)

    @pyqtSlot()
    def startRecord(self):
        destDir = QFileDialog.getExistingDirectory(self, "Select Directory To Save Record")
        if destDir != '':
            self.enableRecord = True
            self._fps = float(self.fps.text())
            cap = cv2.VideoCapture(0)
            fourcc = cv2.VideoWriter_fourcc(*'X264')
            filePath = f'{destDir}/cam_record_{datetime.now().strftime("%d-%b-%Y_%H_%M_%S")}.mp4'
            out = cv2.VideoWriter(filePath,
                                  fourcc,
                                  self._fps,
                                  (self.videoStream.width(), self.videoStream.height()))
            print('Start Cam Recording...', consoleObj=self.outputConsole)

            while cap.isOpened():
                ret, frame = cap.read()
                if self.camWindowSize is not None:
                    frame = cv2.resize(frame, self.camWindowSize)
                
                if ret:
                    self.displayImage(frame)
                    cv2.waitKey()

                    if self.enableRecord:
                        out.write(frame)
                    elif not self.enableRecord:
                        print('Video Recording Stopped', consoleObj=self.outputConsole)
                        break
                else:
                    print('Camera Not Found!', consoleObj=self.outputConsole)
            
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            print(f'Saved to: {destDir}/cam_record_{datetime.now().strftime("%d-%b-%Y_%H_%M_%S")}.mp4', consoleObj=self.outputConsole)

    def stopRecord(self):
        self.enableRecord = False

    def displayImage(self, img):
        qFormat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qFormat = QImage.Format_RGBA888
            else:
                qFormat = QImage.Format_RGB888

        img = QImage(img, img.shape[1], img.shape[0], qFormat)
        img = img.rgbSwapped()

        self.videoStream.setPixmap(QPixmap.fromImage(img))

    def _clearCam(self):
        print('Clear camera stream...', consoleObj=self.outputConsole)
        self.videoStream.clear()

    def _openVideoPlayer(self):
        if self.multiTracker is not None:
            print('Playing processed video...', consoleObj=self.outputConsole)
            self.multiTracker.displayTracked()
        else:
            print('No vaild data provided for processing!', consoleObj=self.outputConsole)

    def _selectTargets(self):
        self.multiTracker = MultiTracker()

        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Open Video File",
                                                  QDir.homePath())
        print(f'Selected File: {fileName}', consoleObj=self.outputConsole)
        self.multiTracker.loadVideo(filePath=fileName)
        self.multiTracker.readFrame()
        selectedTracker = self.trackerType.currentText()
        numberOfObjects = self.numOfTargets.text()

        if not numberOfObjects.isnumeric():
            print(f'Wrong input: Number Of Targets -> {numberOfObjects}, Integers only allowed!',
                  consoleObj=self.outputConsole)
            return

        self.multiTracker.trackObjects(numberOfObjects=int(numberOfObjects),
                                       tracker=selectedTracker,
                                       consoleObj=self.outputConsole)

    def _saveResults(self):
        if self.multiTracker is not None:
            dirName = QFileDialog.getExistingDirectory(self,
                                                       "Select Directory",
                                                       QDir.homePath())
            self.multiTracker.saveResults(dirName=dirName)
            print(f'Data saved successfully to: {dirName}', consoleObj=self.outputConsole)
        else:
            print('No data to save! Select and track targets first...', consoleObj=self.outputConsole)

    def _about(self):
        info = "This application provides object tracking\nalgorithms analysis and comparison.\n"
        info += "\nDeveloped by Dmitry Borovensky"
        QMessageBox.information(self, "About", info, QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    size = app.primaryScreen().size()
    width, height = int(0.6 * size.width()), int(0.794 * size.height())
    mainwindow = ObjectTracker()
    mainwindow.camWindowSize = (int(0.6 * size.width()), int(0.6 * size.height()))
    mainwindow.setFixedSize(width, height)  # disable resize
    mainwindow.show()
    sys.exit(app.exec_())
