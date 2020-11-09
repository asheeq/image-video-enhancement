import cv2
import os
from os.path import isfile, join
import time


def enhance_image(save_name, img):
    start_time = time.time()
    cv2.imwrite('/home/asheeq/Downloads/Video_Enhancement/Original/' + save_name, img)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(1, 1))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    print("Processing time is: %s seconds." % (time.time() - start_time))
    cv2.imwrite('/home/asheeq/Downloads/Video_Enhancement/Enhanced/' + save_name, final)


def convert_frames_to_video(pathIn, pathOut, fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]

    files.sort(key=lambda x: int(x[5:-4]))

    for i in range(len(files)):
        filename = pathIn + files[i]
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        print(filename)
        frame_array.append(img)

    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(frame_array)):
        out.write(frame_array[i])
    out.release()


vidcap = cv2.VideoCapture('/home/asheeq/Downloads/Video_Enhancement/Orginal.mp4')
video_start_time = time.time()
success, image = vidcap.read()
count = 0

while success:
    save_name = 'frame' + str(count) + '.jpg'
    enhance_image(save_name, image)
    success, image = vidcap.read()
    print('Read a new frame : ', success)
    count += 1

pathIn = '/home/asheeq/Downloads/Video_Enhancement/Enhanced/'
pathOut = '/home/asheeq/Downloads/Video_Enhancement/Enhanced.mp4'
fps = 15.0
convert_frames_to_video(pathIn, pathOut, fps)
video_process_time = time.time()
print("Processing time is: %s seconds." % (video_process_time - video_start_time))
