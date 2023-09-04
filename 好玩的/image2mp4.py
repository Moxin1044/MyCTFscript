import cv2
import numpy as np


def image_to_video(image_path, video_name, duration):
    frame = cv2.imread(image_path)
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width,height))
    for _ in range(60 * duration):
        video.write(frame)
    cv2.destroyAllWindows()
    video.release()


# Example usage
image_to_video('image.jpg', 'output.mp4', 60)
