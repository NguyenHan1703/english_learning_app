import requests

def translate_word(word):
    response = requests.get(f"https://api.mymemory.translated.net/get?q={word}&langpair=en|vi")
    if response.status_code == 200:
        data = response.json()
        return data['responseData']['translatedText']
    return None
