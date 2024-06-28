# Object Tracker
# Introduction
Object tracking is a fundamental task in computer vision,
that involves the sequential estimation of an object’s position,
size, and orientation across multiple frames.

Tracking algorithms aim to maintain the identity of the object over time, enabling its continuous monitoring.

This 2D object tracking application, implemented with OpenCV, provides analysis and comparison for
common object tracking algorithms, such as CSRT, KCF, TLD, Mosse etc.

Following the comparative analysis of the algorithms, you can choose one that suites
the case by performance and accuracy.

The application supports single, as well as multiple objects tracking.


# User Instructions
* Select number of objects to track and tracker algorithm.
* Select the objects to track in bounding boxes, using the first frame.
* Play the processed video, to evaluate the efficiency of selected algorithm.
* Additional Options:
    * Save the results (bounding boxes coordinates) to *.txt file.
    * Live camera recording, to create data for future processing.
    * Configurable FPS for live camera recording.

![](https://github.com/DMTRBor/object_tracker/blob/master/demo.gif)


# Installation
To clone the repository:
```
git clone https://github.com/DMTRBor/object_tracker.git
```

Start with Python>=3.8 environment

To install virtual environment, use:
```
python -m venv .env
.env\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
compilation to *.exe:
```
pyinstaller object_tracker.spec
```
