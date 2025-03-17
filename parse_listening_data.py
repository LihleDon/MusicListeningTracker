import json
import boto3
import logging

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    table = dynamodb.Table('UserPreferences')
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        obj = s3.get_object(Bucket=bucket, Key=key)
        csv_content = obj['Body'].read().decode('utf-8')
        lines = csv_content.split('\n')[1:]
        for line in lines:
            if line:
                try:
                    user_id, song_id, timestamp = line.split(',')
                    table.update_item(
                        Key={'user_id': user_id},
                        UpdateExpression='SET #songs = if_not_exists(#songs, :empty_map)',
                        ExpressionAttributeNames={'#songs': 'songs'},
                        ExpressionAttributeValues={':empty_map': {}}
                    )
                    table.update_item(
                        Key={'user_id': user_id},
                        UpdateExpression='ADD #songs.#song :inc',
                        ExpressionAttributeNames={'#songs': 'songs', '#song': song_id},
                        ExpressionAttributeValues={':inc': 1}
                    )
                except ValueError as e:
                    logger.error(f"Invalid CSV line: {line} - {str(e)}")
                    continue
        logger.info("Successfully processed test_listening_data.csv")
        return {'statusCode': 200, 'body': json.dumps('Successfully processed test_listening_data.csv')}
    except Exception as e:
        logger.error(f"Error processing S3 event: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}