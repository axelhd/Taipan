import requests


def get_submitted_ip():
    url = 'https://axessiblestudios.pythonanywhere.com/get_submitted_string'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'submitted_string' in data:
            submitted_ip = data['submitted_string']
            return submitted_ip
        else:
            print("No submitted IP address found.")
    else:
        print(f"Request failed with status code: {response.status_code}")


if __name__ == '__main__':
    retrieved_ip = get_submitted_ip()
    if retrieved_ip:
        print(retrieved_ip)
