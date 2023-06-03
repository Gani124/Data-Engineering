#!/usr/bin/env python

import sys
import zlib
import time
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING
from google.cloud import storage
from google.api_core.exceptions import TooManyRequests

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    # Create Consumer instance
    consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # Subscribe to topic
    topic = "test1-topic"
    consumer.subscribe([topic], on_assign=reset_offset)
    count=0

    service_account_json = '/home/ps24/data-trimet-key.json'
    storage_client = storage.Client.from_service_account_json(service_account_json)

    bucket_name = 'triproj'
    file_name = 'result.json'


    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                # Extract the (optional) key and value, and print.
                key = msg.key()
                if key is not None :
                    count= count+1
                    print("Consumed message from topic {topic} with key={key} and event={event}".format(
                    topic=topic,
                    key=key.decode(),
                    event=msg.value().decode('utf-8')
                 ))
                with open('/home/ps24/result2.json','a') as f:
                    f.write(msg.value().decode('utf-8'))
                    f.close()


                compressed_data = zlib.compress(msg.value(), level=zlib.Z_BEST_COMPRESSION)

                while True:
                    try:
                        bucket = storage_client.get_bucket(bucket_name)
                        blob = bucket.blob(file_name)
                        blob.upload_from_string(compressed_data, content_type='application/octet-stream')
                        break
                    except TooManyRequests:
                        print("Rate limit exceeded. Retrying after backoff...")
                        time.sleep(1)  # Wait for 1 second before retrying

                #bucket = storage_client.get_bucket(bucket_name)
                #blob = bucket.blob(file_name)
                #blob.upload_from_string(msg.value().decode('utf-8'))

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
