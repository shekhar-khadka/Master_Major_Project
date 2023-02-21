from confluent_kafka import Consumer
group_id='vehicle'

################
c = Consumer({'bootstrap.servers': '192.168.0.4:9092', 'group.id': group_id, 'auto.offset.reset': 'earliest'})
print('Kafka Consumer has been initiated...')

print('Available topics to consume: ', c.list_topics().topics)

# c.subscribe([group_id])
#
#
# #
# #
# ################
# def main():
#     while True:
#         msg = c.poll(.5)  # timeout
#         # print(msg)
#         if msg is None:
#             continue
#         if msg.error():
#             print('Error: {}'.format(msg.error()))
#             continue
#         # print(msg)
#         data = msg.value().decode('utf-8')
#         print(data)
#
#     c.close()


#
# main()