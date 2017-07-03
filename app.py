from flask import Flask
import os
import socket
import boto3

queue_url = os.getenv("SQS_LOGGING_QUEUE_URL")

app = Flask(__name__)

template = "<h3>Hello Flask (Version 2.3)!</h3>" \
       "<b>Hostname:</b> {hostname}<br/>" \
       "<b>Queue Url:</b> {queue_url}<br>" \
       "<b>Message ID:</b> {message_id}<br>"

@app.route("/")
def hello():
    try:
        client = boto3.client('sqs')
        response = client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout=5,
            WaitTimeSeconds=20
        )
        message_id = response['Messages'][0]['MessageId'] if len(response['Messages']) > 0 else None
    except Exception as e:
        message_id = str(e)

    return template.format(hostname=socket.gethostname(), queue_url=queue_url, message_id=message_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
