from confluent_kafka import Consumer

################
c = Consumer({'bootstrap.servers': '192.168.0.4:9092', 'group.id': 'vehicle', 'auto.offset.reset': 'earliest'})
print('Kafka Consumer has been initiated...')

print('Available topics to consume: ', c.list_topics().topics)