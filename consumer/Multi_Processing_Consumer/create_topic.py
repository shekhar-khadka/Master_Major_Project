from confluent_kafka.admin import AdminClient, NewTopic

n_repicas = 1
n_partitions = 3

admin_client = AdminClient({
    "bootstrap.servers": "localhost:9092"
})

# topic_list = []
# topic_list.append(NewTopic("vehicle", n_partitions, n_repicas))
# fs = admin_client.create_topics(topic_list)
#
# for topic, f in fs.items():
#     try:
#         f.result()  # The result itself is None
#         print("Topic {} created".format(topic))
#     except Exception as e:
#         print("Failed to create topic {}: {}".format(topic, e))

topics = ['topic1', 'topic2', 'topic3']
topic_list = []


[topic_list.append(NewTopic(topic, n_partitions, n_repicas)) for topic in topics]
fs = admin_client.create_topics(topic_list)


for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print("Topic {} created".format(topic))
    except Exception as e:
        print("Failed to create topic {}: {}".format(topic, e))