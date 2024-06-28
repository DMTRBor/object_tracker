import os
import cv2
import numpy as np
from utils import print


class MultiTracker:
    TrackersDict = {'csrt': cv2.legacy.TrackerCSRT_create,
                    'kcf' : cv2.legacy.TrackerKCF_create,
                    'boosting' : cv2.legacy.TrackerBoosting_create,
                    'mil': cv2.legacy.TrackerMIL_create,
                    'tld': cv2.legacy.TrackerTLD_create,
                    'medianflow': cv2.legacy.TrackerMedianFlow_create,
                    'mosse': cv2.legacy.TrackerMOSSE_create}

    def __init__(self):
        self.trackers = cv2.legacy.MultiTracker_create()
    
    def loadVideo(self, filePath):
        self.video = cv2.VideoCapture(filePath)

    def readFrame(self):
        self.ret, self.frame = self.video.read()

    def trackObjects(self, numberOfObjects, tracker, consoleObj=None):
        print('Please select targets to process...', consoleObj=consoleObj)
        print("Select a ROI and then press SPACE or ENTER button!", consoleObj=consoleObj)
        for _ in range(numberOfObjects):
            cv2.imshow('Select Object', self.frame)
            boundBoxI = cv2.selectROI('Select Object', self.frame)
            trackerI = self.TrackersDict[tracker]()
            self.trackers.add(trackerI, self.frame, boundBoxI)
        print('Targets had been selected successfully!', consoleObj=consoleObj)
        cv2.destroyAllWindows()

    def displayTracked(self, frameNumber=2):
        # start from second frame
        # first frame used for manual tracking
        self.frameNumbers = []
        self.boxes = []

        while True:
            ret, frame = self.video.read()

            if not ret:
                break

            (success, boxes) = self.trackers.update(frame)
            self.frameNumbers.append(frameNumber)
            self.boxes.append(boxes)
            frameNumber += 1

            for box in boxes:
                (x, y, w, h) = [int(a) for a in box]
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
                
            cv2.imshow('Object Tracker', frame)
            key = cv2.waitKey(5) & 0xFF
            if key == ord('q'):
                break

        self.video.release()
        cv2.destroyAllWindows()

    def saveResults(self, dirName):
        os.makedirs(dirName, exist_ok=True)

        for i in range(len(self.frameNumbers)):
            np.savetxt(dirName + '/frame_'+str(self.frameNumbers[i])+'.txt', self.boxes[i], fmt='%f')
