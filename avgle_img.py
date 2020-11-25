import requests

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "https://www.fanbus.pw/"
}

default_path = "https://www.fanbus.pw/CEAD-324"
# default_path = "https://btsow.surf/search/HNDB-180"

res = requests.get(default_path, HEADERS, 10)
res.encoding = 'utf-8'
print(res.text)
