config = {
    'bootstrap.servers': '192.168.0.4:9092',
    'group.id': 'kafka-multi-video-stream',
    'enable.auto.commit': False,
    'default.topic.config': {'auto.offset.reset': 'earliest'}
}