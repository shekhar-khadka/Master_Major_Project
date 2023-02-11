from confluent_kafka import Consumer

################
c = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'real-madrid', 'auto.offset.reset': 'earliest'})
print('Kafka Consumer has been initiated...')

print('Available topics to consume: ', c.list_topics().topics)
config = {
    'bootstrap.servers': '192.168.1.114:9092',
    'group.id': 'kafka-multi-video-stream',
    'enable.auto.commit': False,
    'default.topic.config': {'auto.offset.reset': 'earliest'}
}

c.subscribe(['real-madrid'])


#
#
################
def main():
    while True:
        msg = c.poll(5)  # timeout
        print(msg)
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data = msg.value().decode('utf-8')
        print(data)
    c.close()


main()

