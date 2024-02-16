import requests
from lxml import html
import json

url = "https://mbasic.facebook.com/groups/?seemore&refid=27"

cookie = ""

payload = {}
headers = {
    'authority': 'mbasic.facebook.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
    'cookie': cookie
}

response = requests.request("GET", url, headers=headers, data=payload)
tree = html.fromstring(response.content)
links = tree.xpath('//a/@href')

new_links = []

for link in links:
    if "https://" in link:
        new_links.append(link)

groups = tree.xpath('//div//table[@role="presentation" and @align="center"]//tr')

groups_name = []

for group in groups:
    groups_name.append(group.xpath('./td//text()'))


for i in range(0, len(groups_name)):
    if len(groups_name[i]) == 1:
        groups_name[i].append(0)

data = []
for i in range(0, len(new_links)):
    data.append({
        'link: ': new_links[i],
        'name: ': groups_name[i][0],
        'num_unread_msg: ': int(groups_name[i][1])
    })

with open('group.json', 'w', encoding='UTF-8') as f:
    json.dump(data, f, indent=4, separators=(',', ': '), ensure_ascii=False)
