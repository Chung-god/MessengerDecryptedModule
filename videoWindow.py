# 동영상 프로세싱
import cv2
import os
from ffpyplayer.player import MediaPlayer

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
        img = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
        cv2.imshow('video', frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame
    capture.release()
    cv2.destroyAllWindows()

def image(imageName):
    if os.path.isfile(imageName) == False:
        imageName = 'image/noimage.png'

    im_origin = cv2.imread(imageName, cv2.IMREAD_COLOR)
    cv2.namedWindow('Image',cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Image', im_origin)
    #cv2.moveWindow('Image', 700,300)
    cv2.waitKey(0)
    cv2.destroyAllWindows()