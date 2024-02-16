import time
import requests
from lxml import html
import json

id = "thienan1105"

url = f"https://mbasic.facebook.com/{id}/?v=timeline"

cookie = ""


def get_link(url):
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
    return tree

def get_article_link(article):
    for a in article.xpath('.//a'):
        if a.text == "Xem thêm":
            return a.attrib['href']
    return None

def get_article_contents(articles):
    for article in articles:
        time.sleep(1)
        isMore = False
        
        for a in article.xpath('.//a'):
            if a.text == "Toàn bộ tin":
                isMore = True
                linkArticle = a.attrib['href']
                treeArticle = get_link("https://mbasic.facebook.com" + linkArticle)
                links.append("https://mbasic.facebook.com" + linkArticle)
                contents.append(treeArticle.xpath('//p//text()'))
                for img in treeArticle.xpath('//a'):
                    if "photo.php" in img.attrib['href']:
                        images.append(img.xpath('.//img')[0].attrib['src'])
                        break 

        if isMore == False:
            links.append("https://mbasic.facebook.com")
            contents.append(article.xpath('.//div[@class="story_body_container"]//div//div[1]//span//text()'))
            for img in article.xpath('.//a'):
                if "photo.php" in img.attrib['href']:
                    images.append(img.xpath('.//img')[0].attrib['src'])
                    break
                else:
                    images.append(None)


tree = get_link(url)

articles = tree.xpath('//article')
nextLink = tree.xpath('//a//span[text()="Xem tin khác"]')
count = 0
links = []
contents = []
images = []

get_article_contents(articles)

while nextLink:
    nextLink = nextLink[0].getparent().attrib['href']
    tree = get_link("https://mbasic.facebook.com" + nextLink)
    articles = tree.xpath('//article')
    get_article_contents(articles)
    nextLink = tree.xpath('//a//span[text()="Xem tin khác"]')
    time.sleep(1)

data = []
for i in range(0, len(links)):
    data.append({
        'link: ': links[i],
        'content: ': contents[i],
        'images: ': images.pop(0) if images else None
    })

with open('posts.json', 'w', encoding='UTF-8') as f:
    json.dump(data, f, indent=4, separators=(',', ': '), ensure_ascii=False)
