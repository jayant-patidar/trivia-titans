import boto3
import json

sqs_client = boto3.client('sqs')
ses_client = boto3.client('ses')

queue_url = "https://sqs.us-east-1.amazonaws.com/981263172079/NewGameQueue"
def lambda_handler(event, context):
    response = sqs_client.receive_message(
        QueueUrl = queue_url,
        MaxNumberOfMessages = 1,
        MessageAttributeNames=['All']
    )
    
    if 'Messages' in response:
        sqs_message_body = json.loads(response['Messages'][0]['Body'])
        required_json = json.loads(sqs_message_body['Message'])
        game_name = required_json['GameName']
        users = required_json['Users']
        
        receipt_handle = response['Messages'][0]['ReceiptHandle']
        
        email_subject = "New Game Alert!"
        email_body = f"A new trivia game named {game_name} has been added to the game! Please go to the dashboard to see it"
        
        ses_client.send_email(
            Source='TriviaTitansG7@proton.me',
            Destination={
                'ToAddresses': users
            },
            Message={
                'Subject': {'Data': email_subject},
                'Body': {'Text': {'Data': email_body}}
            }
        )

        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )