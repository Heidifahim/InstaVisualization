import json
import requests
import base64


def _convert_image_to_base64(image_filename):
    encoded_string = base64.b64encode(image_filename.read()).decode()

    return encoded_string



def call_vision_api(image_filename, api_keys):
    api_key = api_keys['google']
    post_url = "https://vision.googleapis.com/v1/images:annotate?key=" + api_key

    base64_image = image_filename

    post_payload = {
        "requests": [
            {
                "image": {
                    "source": {
                        "imageUri": image_filename
                    }
                },
                "features": [
                    {
                        "type": "LABEL_DETECTION",
                        "maxResults": 10
                    },
                    {
                        "type": "FACE_DETECTION",
                        "maxResults": 10
                    },
                    {
                        "type": "LANDMARK_DETECTION",
                        "maxResults": 10
                    },
                    {
                        "type": "LOGO_DETECTION",
                        "maxResults": 10
                    },
                    {
                        "type": "SAFE_SEARCH_DETECTION",
                        "maxResults": 10
                    },
                ]
            }
        ]
    }

    result = requests.post(post_url, json=post_payload)
    result.raise_for_status()

    return json.loads(result.text)


# See this function in microsoft.py for docs.
def get_standardized_result(api_result):
    output = {
        'tags': [],
    }

    api_result = api_result['responses'][0]

    if 'labelAnnotations' in api_result:
        for tag in api_result['labelAnnotations']:
            output['tags'].append((tag['description'], tag['score']))
    else:
        output['tags'].append(('none found', None))

    if 'logoAnnotations' in api_result:
        output['logo_tags'] = []
        for annotation in api_result['logoAnnotations']:
            output['logo_tags'].append((annotation['description'], annotation['score']))

    return output


def getUrls():
    access_token = ""
    url = "https://api.instagram.com/v1/users/self/media/recent/?access_token={}".format(access_token)
    response = requests.get(url)
    print("Status Code: {} ".format(response.status_code))
    data = json.loads(response.content)['data']
    datalinks = []
    for x in data:
        datalinks.append(x['images']['standard_resolution']['url'])
    return datalinks

from pprint import pprint

if __name__ == "__main__":
    images = getUrls()
    api_keys_filepath = './api_keys.json'
    with open(api_keys_filepath) as datafile:
        key = json.load(datafile)
        result = call_vision_api(images[0], api_keys=key)
    pprint(result)


