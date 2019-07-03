import requests

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "http://www.dmmbus.us"
}



res = requests.get('http://www.dmmbus.us', headers=HEADERS, timeout=10)
res.encoding = 'utf-8'
print(res.text)