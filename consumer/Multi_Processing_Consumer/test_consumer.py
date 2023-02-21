import multiprocessing
from confluent_kafka import Consumer, KafkaError

def consumer_func(topic_name):
    conf = {'bootstrap.servers': 'localhost:9092', 'group.id': 'my_group', 'auto.offset.reset': 'earliest'}
    consumer = Consumer(conf)
    consumer.subscribe([topic_name])
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f'Reached end of {topic_name}')
            else:
                print(msg.error())
        else:
            # Do something with the message
            print(f'{topic_name}: {msg.value()}')

if __name__ == '__main__':
    topics = ['topic1', 'topic2', 'topic3']
    processes = []
    for topic in topics:
        process = multiprocessing.Process(target=consumer_func, args=(topic,))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
