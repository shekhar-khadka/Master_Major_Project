import threading
from confluent_kafka import Consumer, KafkaError, KafkaException
from consumer_config import config as consumer_config
# from util import *
# from single_image import detect_obj
from datetime import datetime
import multiprocessing
import cv2
import numpy as np
import time
from process_frames import DetectFrames



class MultiProcessConsumer:
    def __init__(self, config,topic,weight,conf,img_size,device,conf_thres,iou_thres):
        self.config = config
        self.topic = topic
        self.obj =DetectFrames(weight,conf,img_size,device,conf_thres,iou_thres)


    def read_data(self):
        consumer = Consumer(self.config)

        consumer.subscribe(self.topic)

        self.run(consumer, 0, [], [])
        print('ok*******************')

    def run(self, consumer, msg_count, msg_array, metadata_array):
        try:
            while True:
                msg = consumer.poll(0.5)
                if msg == None:
                    print(msg)
                    continue
                elif msg.error() == None:
                    print('got data')

                    # convert image bytes data to numpy array of dtype uint8
                    nparr = np.frombuffer(msg.value(), np.uint8)

                    # decode image
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    img = cv2.resize(img, (640, 640))
                    self.obj.detect(img)

                elif msg.error().code() == KafkaError._PARTITION_EOF:
                    print('End of partition reached {0}/{1}'
                          .format(msg.topic(), msg.partition()))
                else:
                    print('Error occured: {0}'.format(msg.error().str()))

        except KeyboardInterrupt:
            print("Detected Keyboard Interrupt. Quitting...")
            pass

        finally:
            consumer.close()

    def start(self, numThreads):
        # Note that number of consumers in a group shouldn't exceed the number of partitions in the topic
        for _ in range(numThreads):
            t = threading.Thread(target=self.read_data)
            t.daemon = True
            t.start()
            while True: time.sleep(10)



if __name__ == "__main__":



    video_names = ["Putalisadak", "Baluwatar"]
    # model_onnx='/home/fm-pc-lt-197/mp_pr/consumer/best.onnx'
    # image_source = '1225.jpg'
    conf = 0.5
    img_size = 640,
    device = 'cpu'
    weight = 'weights/best.pt'
    conf_thres = 0.25
    iou_thres = 0.45


    def worker(topic_name):
        # subprocess.call(f"./mp_column_spliter.sh {x[0]}  {x[1]}", shell=True)
        t_name=[topic_name]
        print('Topic name is',t_name)
        consumer_thread = MultiProcessConsumer(consumer_config, t_name,weight,conf,img_size,device,conf_thres,iou_thres)
        consumer_thread.read_data()

    #
    def main():
        start_time = datetime.now()
        topic_list = ["Putalisadak", "Baluwatar"]
        # with Pool(processes=2) as pool:
        #     print(pool.map(worker, topic_list))
        # topics = ['topic1', 'topic2', 'topic3']
        processes = []
        for topic in topic_list:
            process = multiprocessing.Process(target=worker, args=(topic,))
            process.start()
            processes.append(process)
        for process in processes:
            process.join()


    main()
    # consumer_thread = MultiProcessConsumer(consumer_config, topic, 32,model_onnx)
    # consumer_thread.start(2)

