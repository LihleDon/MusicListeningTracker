# Music Listening Tracker

An AWS data pipeline that tracks user music listening habits by processing CSV uploads and storing song play counts.

## Overview
- **Input**: CSV files (`user_id,song_id,timestamp`) uploaded to S3.
- **Processing**: Lambda parses CSV and updates DynamoDB.
- **Storage**: DynamoDB stores play counts per user.
- **Monitoring**: CloudWatch logs execution.

## Tech Stack
- AWS: S3, Lambda (Python 3.9), DynamoDB, CloudWatch
- Tools: AWS CLI, PowerShell

## Setup
1. **S3**: Create bucket `music-listening-bucket` (af-south-1).
2. **DynamoDB**: Create table `UserPreferences` (partition key: `user_id`, on-demand).
3. **Lambda**: Deploy `parse_listening_data.py`, set S3 trigger (all object creates).
4. **Test**: Run `aws s3 cp test_listening_data.csv s3://music-listening-bucket/ --region af-south-1`.

## Files
- `parse_listening_data.py`: Lambda function.
- `test_listening_data.csv`: Sample input.
- `key_user00X.json`: Delete scripts for reset.

## Key Lessons
- Handle DynamoDB attribute initialization.
- Debug with CloudWatch logs.
- Optimize for AWS Free Tier.

## Skills Demonstrated
- AWS Data Engineering
- NoSQL (DynamoDB)
- Python & boto3
- Event-driven architecture