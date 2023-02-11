import multiprocessing
import time
from confluent_kafka import Producer, KafkaError

def produce_func(topic_name):
    conf = {'bootstrap.servers': 'localhost:9092'}
    producer = Producer(conf)
    while True:
        # Generate message
        message = f'Hello from {topic_name}'
        # Produce message
        producer.produce(topic_name, key='key', value=message)
        producer.flush()
        print(f'Sent message to {topic_name}: {message}')
        time.sleep(5)


if __name__ == '__main__':
    topics = ['topic1', 'topic2', 'topic3']
    processes = []
    for topic in topics:
        process = multiprocessing.Process(target=produce_func, args=(topic,))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
