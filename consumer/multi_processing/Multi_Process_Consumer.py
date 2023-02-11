import threading
from confluent_kafka import Consumer, KafkaError, KafkaException
from consumer_config import config as consumer_config
from datetime import datetime
import multiprocessing
import cv2
import numpy as np
import time



class MultiProcessConsumer:
    def __init__(self, config,topic,batch_size,model_onnx):
        self.config = config
        self.topic = topic
        self.batch_size = batch_size
        self.net = cv2.dnn.readNetFromONNX(model_onnx)


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
                    # img = cv2.resize(img, (224, 224))
                    self.detect_obj(img)

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

    # def start(self, numThreads):
    #     for _ in range(numThreads):
    #         t = threading.Thread(target=self.read_data)
    #         t.daemon = True
    #         t.start()
    #         while True: time.sleep(10)


    def detect_obj(self,img):

        # Load an color image in grayscale
        # img = cv2.imread('./test_images/Ratnapark.jpg')

        # cap = cv2.VideoCapture('/home/fm-pc-lt-197/mp_pr/Vehicle-Detection/test_images/v1.mp4')
        # net = cv2.dnn.readNetFromONNX("/home/shekhar/mp_pr/best.onnx")
        # file = open("coco.txt", "r")
        # net=self.net
        classes = ['Car', 'Motorcycle', 'Truck', 'Bus', 'Bicycle']

        img = cv2.resize(img, (640, 640))

        blob = cv2.dnn.blobFromImage(img, scalefactor=1 / 255, size=(640, 640), mean=[0, 0, 0], swapRB=True, crop=False)
        self.net.setInput(blob)
        detections = self.net.forward()[0]

        # cx,cy , w,h, confidence, 80 class_scores
        # class_ids, confidences, boxes

        classes_ids = []
        confidences = []
        boxes = []
        rows = detections.shape[0]

        img_width, img_height = img.shape[1], img.shape[0]
        x_scale = img_width / 640
        y_scale = img_height / 640

        for i in range(rows):
            row = detections[i]
            confidence = row[4]
            if confidence > 0.5:
                classes_score = row[5:]
                ind = np.argmax(classes_score)
                if classes_score[ind] > 0.5:
                    classes_ids.append(ind)
                    confidences.append(confidence)
                    cx, cy, w, h = row[:4]
                    x1 = int((cx - w / 2) * x_scale)
                    y1 = int((cy - h / 2) * y_scale)
                    width = int(w * x_scale)
                    height = int(h * y_scale)
                    box = np.array([x1, y1, width, height])
                    boxes.append(box)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.5)
        output = []
        for i in indices:
            x1, y1, w, h = boxes[i]
            label = classes[classes_ids[i]]
            conf = confidences[i]
            text = label + "{:.2f}".format(conf)
            output.append(f'Detected: {label} with confidence {conf}')

            # cv2.rectangle(img, (x1, y1), (x1 + w, y1 + h), (255, 0, 0), 2)
            # cv2.putText(img, text, (x1, y1 - 2), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)
        print(output)
        # cv2.imshow("VIDEO", img)
        # k = cv2.waitKey(10)
        # if k == ord('q'):
        #     break


if __name__ == "__main__":



    video_names = ["v1", "v2"]
    model_onnx='/home/fm-pc-lt-197/mp_pr/consumer/best.onnx'


    def worker(topic_name):
        t_name=[topic_name]
        print('Topic name is',t_name)
        consumer_thread = MultiProcessConsumer(consumer_config, t_name, 32, model_onnx)
        consumer_thread.read_data()

    #
    def main():
        start_time = datetime.now()
        topic_list = ['v1', 'v2']
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

