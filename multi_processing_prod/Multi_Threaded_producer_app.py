from glob import glob
import concurrent.futures
from util import *
from producer_config import config as producer_config
from confluent_kafka import Producer
import os
import time


class ProducerThread:
    def __init__(self, config):
        self.producer = Producer(config)

    def publishFrame(self, video_path):
        video = cv2.VideoCapture(video_path[0])
        video_name = os.path.basename(video_path[0]).split(".")[0]
        frame_no = 1
        while video.isOpened():
            _, frame = video.read()
            # pushing every 3rd frame
            if frame_no % 3 == 0:
                frame_bytes = serializeImg(frame)
                self.producer.produce(
                    topic=video_path[1],
                    value=frame_bytes,
                    on_delivery=delivery_report,
                    timestamp=frame_no,
                    headers={
                        "video_name": str.encode(video_name)
                    }
                )
                self.producer.poll(0)
            time.sleep(0.5)
            frame_no += 1
        video.release()

        return

    def start(self, vid_paths):
        # runs until the processes in all the threads are finished
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.publishFrame, vid_paths)

        self.producer.flush()  # push all the remaining messages in the queue
        print("Finished...")


if __name__ == "__main__":
    # video_dir = "/home/shekhar/mp_pr/multi_processing_prod/videos/"
    #
    # video_paths = glob(video_dir + "*.mp4")  # change extension here accordingly
    # print(video_paths)
    #
    video_paths = []

    for dirpath, dirs, files in os.walk('/home/shekhar/mp_pr/multi_processing_prod/videos/'):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            video_paths.append((fname, filename.split('.')[0]))

    producer_thread = ProducerThread(producer_config)
    producer_thread.start(video_paths)

