import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
import json
import time


s3_client = boto3.client('s3')
s3 = boto3.resource('s3')
sqs_client = boto3.client('sqs')

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((128, 128))
        image.save(resized_path)

while True:
    try:
        queue_url = os.environ.get('SQS_QUEUE_URL')
        # Long poll for message on provided SQS queue
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            WaitTimeSeconds=20
        )

        event = response['Messages'][0]['Body']
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        try:
            bucket_name = json.loads(str(event))["Records"][0]["s3"]["bucket"]["name"]
            key = json.loads(str(event))["Records"][0]["s3"]["object"]["key"]
        except Exception as e:
            print("skipp")
            sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            print('Received and deleted message: %s' % message)
            continue
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key.split("/")[1])
        upload_path = '/tmp/mobile-{}'.format(key.split("/")[1])

        s3_client.download_file(bucket_name, key, download_path)
        resize_image(download_path, upload_path)
        s3.meta.client.upload_file(upload_path, bucket_name, 'thumbnail/Thumbail-'+key.split("/")[1]) #creates folder within ingest bucket
        print("Done for thumbnail/Thumbail-"+str(key.split("/")[1]))
        sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
    except Exception as e:
        print("waiting for new event....")