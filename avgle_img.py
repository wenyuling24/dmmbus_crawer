import requests

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "https://www.dmmbus.cloud/"
}

res = requests.get('https://www.dmmbus.cloud/', headers=HEADERS, timeout=10)
res.encoding = 'utf-8'
print(res.text)
