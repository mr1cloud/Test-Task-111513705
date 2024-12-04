import argparse
from datetime import datetime
from confluent_kafka import Producer, Consumer


class KafkaClient:
    def __init__(self, kafka_server):
        self.kafka_server = kafka_server

    def produce_message(self, topic: str, message: str):
        """
        Produce a message to a Kafka topic
        :param topic:
        :param message:
        :return:
        """
        producer = Producer({'bootstrap.servers': self.kafka_server})
        producer.produce(topic, value=message)
        producer.flush()

    def consume_messages(self, topic: str, group_id: str = 'mygroup'):
        """
        Consume messages from a Kafka topic
        :param topic:
        :param group_id:
        :return:
        """
        consumer = Consumer({
            'bootstrap.servers': self.kafka_server,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT'
        })
        consumer.subscribe([topic])

        try:
            while True:
                message = consumer.poll(timeout=1.0)
                if message is None:
                    continue
                if message.error():
                    if message.error().code() == 3:
                        continue
                    print(f"Consumer error: {message.error()}")
                    continue

                print(f"{datetime.now().strftime('%d/%m/%Y, %H:%M:%S')} Message: {message.value().decode('utf-8')}")
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()


def main():
    parser = argparse.ArgumentParser(description="CLI Kafka Tool")
    subparsers = parser.add_subparsers(dest='command')

    produce_parser = subparsers.add_parser('produce', help='Produce a message to a Kafka topic')
    produce_parser.add_argument('--message', required=True, help='Message to send')
    produce_parser.add_argument('--topic', required=True, help='Kafka topic')
    produce_parser.add_argument('--kafka', required=True, help='Kafka server in the format ip:port')

    consume_parser = subparsers.add_parser('consume', help='Consume messages from a Kafka topic')
    consume_parser.add_argument('--topic', required=True, help='Kafka topic')
    consume_parser.add_argument('--kafka', required=True, help='Kafka server in the format ip:port')

    args = parser.parse_args()

    kafka_client = KafkaClient(args.kafka)

    if args.command == 'produce':
        kafka_client.produce_message(args.topic, args.message)
    elif args.command == 'consume':
        kafka_client.consume_messages(args.topic)


if __name__ == "__main__":
    main()
