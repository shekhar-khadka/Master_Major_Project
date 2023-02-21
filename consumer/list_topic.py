from confluent_kafka import Consumer

################
c = Consumer({'bootstrap.servers': '192.168.0.3:9092', 'group.id': 'real_madrid', 'auto.offset.reset': 'earliest'})
print('Kafka Consumer has been initiated...')

print('Available topics to consume: ', c.list_topics().topics)




