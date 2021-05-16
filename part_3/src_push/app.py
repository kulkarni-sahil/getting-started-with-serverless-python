import json
import requests
import os

slack_endpoint = os.environ.get("slackEndpoint")


def lambda_handler(event, context):

    web_hook_event = json.loads(event.get('body'))

    repository = web_hook_event.get('repository')
    repo = repository.get('name')
    star_count = repository.get('stargazers_count')

    sender = web_hook_event.get('sender')
    username = sender.get('login')
    user_url = sender.get('url')
    user_avatar_url = sender.get('avatar_url')

    head_commit = web_hook_event.get('head_commit')
    commit_message = head_commit.get('message')
    commit_author_username = head_commit.get('author').get('username')

    message = {
        "attachments": [
            {
                "pretext": f"A new push has been made to {repo} !",
                # Special text for message
                "text": '\n'.join(
                    [
                        f"Message {commit_message}",
                        f"Made by <{user_url}|{commit_author_username}>."
                    ]
                ),
                "thumb_url": f"{user_avatar_url}",
                "footer": "Serverless App",
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            }
        ]
    }

    try:
        requests.post(url=slack_endpoint, data=json.dumps(message))
    except:
        print("some error while making post request")
        raise

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "done"
            }
        ),
    }
