import requests
import json

def upload_medium(query: str, blog_content: str, api_key: str, image_url: str = None) -> str:
    BASE_URL = 'https://api.medium.com/v1'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    user_response = requests.get(f'{BASE_URL}/me', headers=headers)

    if user_response.status_code != 200:
        try:
            error_data = user_response.json()
            raise Exception(f"Failed to fetch user details: {error_data['errors'][0]['message']}")
        except json.JSONDecodeError:
            raise Exception(f"Failed to fetch user details: {user_response.text}")

    user_data = user_response.json()
    user_id = user_data['data']['id']

    post_data = {
        'title': query,
        'contentFormat': 'markdown',
        'content': blog_content,
        'publishStatus': 'draft',
    }

    if image_url:
        post_data['content'] = f'![Image]({image_url})\n\n' + post_data['content']

    response = requests.post(f'{BASE_URL}/users/{user_id}/posts', headers=headers, json=post_data)

    try:
        response_data = response.json()
        if response.status_code == 201:
            return response_data['data']['url']
        else:
            raise Exception(f"Failed to publish blog post: {response_data['errors'][0]['message']}")
    except json.JSONDecodeError:
        raise Exception(f"Failed to decode JSON response: {response.text}")