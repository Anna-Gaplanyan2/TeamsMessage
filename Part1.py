import requests
import json
import os




def get_image():
    access_key = os.getenv('PEXELS_API_KEY')
    headers = {'Authorization': access_key}
    url = "https://api.pexels.com/v1/curated"
    response = requests.get(url, headers=headers)
    image_url = response.json()['photos'][0]['src']['original']
    return image_url


def get_quote():
    api_key = os.getenv('QUOTES_API_KEY')
    url = url = f"https://quotes.rest/qod.json?category=inspire&api_key={api_key}"
    response = requests.get(url)
    quote = response.json()['contents']['quotes'][0]['quote']
    return quote


def send_to_teams(image_url, quote):
    webhook_url = os.getenv('TEAMS_WEBHOOK_URL')
    headers = {
        'Content-Type': 'application/json'
    }
    message = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": "Daily Inspiration",
        "sections": [{
            "activityTitle": "Send by Anna Gaplanyan:",
            "text": quote,
            "images": [{
                "image": image_url
            }]
        }]
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(message))
    return response.text


def main():
    image_url = get_image()
    quote = get_quote()
    result = send_to_teams(image_url, quote)
    print(result)


if __name__ == "__main__":
    main()
