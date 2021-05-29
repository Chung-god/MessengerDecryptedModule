# 동영상 프로세싱
import cv2
import os
from ffpyplayer.player import MediaPlayer
import imutils

def video(videoName):
    if os.path.isfile(videoName) == False:
        videoName = 'image/noimage.png'
        image(videoName)
        return

    capture = cv2.VideoCapture(videoName)
    player = MediaPlayer(videoName)

    while capture.isOpened():
        run, frame = capture.read()
        audio_frame, val = player.get_frame()
        if not run:
            break
        
        # 높이 700으로 비율 맞춤
        frame = imutils.resize(frame, height=700)
        cv2.moveWindow('video', 400,100)
        cv2.imshow('video', frame)
        
        if cv2.waitKey(int(1000/30.0)) & 0xFF == ord('q'):
            break
        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame
        
    capture.release()
    cv2.destroyAllWindows()

def image(imageName):
    if os.path.isfile(imageName) == False:
        imageName = 'image/noimage.png'

    im_origin = cv2.imread(imageName, cv2.IMREAD_COLOR)

    im_origin = imutils.resize(im_origin, height=700)
    cv2.namedWindow('Image',cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Image', im_origin)
    cv2.moveWindow('Image', 400,100)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
