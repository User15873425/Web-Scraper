import requests

from bs4 import BeautifulSoup
from pathlib import Path
from string import punctuation

url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
pages_num, article_type = int(input('Number of pages: ')), input('Article Type: ')
for page in range(1, pages_num + 1):
    Path(f'./Page_{page}').mkdir(parents=True, exist_ok=True), print(f'Page {page} processing...')
    r = requests.get(url + f'&page={page}', headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')
    for article in soup.find_all('span', {'class': 'c-meta__type'}, text=article_type):
        anchor = article.find_parent('article').find('a', {'data-track': 'click'})
        r_next = requests.get(url[:22] + anchor.get('href'), headers={'Accept-Language': 'en-US,en;q=0.5'})
        body = BeautifulSoup(r_next.content, 'html.parser').find('div', {'class': 'c-article-body'})
        text = [i.text for i in body.find_all(('p', 'h2', 'h3')) if '\n' not in i]
        newlines = [[0] + [i[:(x+1)*110].rfind(' ') + 1 for x in range(len(i) // 110)] + [len(i)] for i in text]
        text = ['\n'.join(i[(n := newlines[text.index(i)])[x]:n[x+1]] for x in range(len(i) // 110 + 1)) for i in text]
        with open(f"./Page_{page}/{anchor.text.translate(str.maketrans(' ', '_', punctuation))}.txt", 'wb') as bf:
            bf.write('\n\n'.join(text).encode('UTF-8'))
print('Saved all articles.')
