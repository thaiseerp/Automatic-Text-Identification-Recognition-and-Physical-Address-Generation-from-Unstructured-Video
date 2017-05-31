import cv2
vidcap = cv2.VideoCapture('../Files/video.avi')
count = 0
success = True
fps = vidcap.get(cv2.CAP_PROP_FPS)

while success:
    frameId = int(round(vidcap.get(1)))                         # Getting current frames ID
    success, image = vidcap.read()

    if frameId == 0:                                            # Saving initial frame
        print('Read a new frame:  ' + str(frameId))
        cv2.imwrite("../Files/frames/%d.jpg" % count, image)    # save frame as JPEG file
        count += 1
    elif frameId % fps == 0:                                    # Making sure that only one image is saved per second
        print('Read a new frame:  ' + str(frameId))
        cv2.imwrite("../Files/frames/%d.jpg" % count, image)    # save frame as JPEG file
        count += 1

vidcap.release()
