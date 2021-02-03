import re
import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup

today = date.today()

# This should output an array json data object that we can then send to react


def get_news(epic: str):
    beforedate = today.strftime('%Y%m%d')
    afterdate = (today - timedelta(days=1)).strftime('%Y%m%d')
    url = f'https://www.londonstockexchange.com/news?tab=news-explorer&period=custom&beforedate={beforedate}&afterdate={afterdate}&namecode={epic}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='news-table-results')
    rows = results.find_all('td', class_='news-title')

    if not rows:
        print(f'No news for {epic}.')
    else:
        print(f'{epic} announced: ', end='\n' * 2)
        for row in rows:
            company = row.text.strip()
            p = '-\s+([\w]+)'
            re_result = re.search(p, company)
            if re_result and re_result.group(1) != epic:
                continue
            title = row.find('a', class_='dash-link').text.strip()
            href = row.find('a', class_='dash-link')['href']
            link = f'https://www.londonstockexchange.com/{href}'
            source = row.find('div', class_='rns-source')

            if not source:
                source = row.find('div', class_='source-label')
                if not source:
                    source = 'NA'
                else:
                    source = source.text.strip()
            else:
                source = source.text.strip()

            slug = row.find(
                'div', class_='td-column-content flex-wrapper spaced-flex-container mobile-flex-container flex-align-center')
            infos = slug.find_all('div')
            date = infos[0].text.strip()
            time = infos[1].text.strip()
            # price = infos[2].text.strip()
            # change = infos[3].text.strip()
            print(f'{date} {time}', end='\n')
            print(f'{title} - {source}', end='\n')
            print(f'{link}', end='\n' * 2)
        print('- - -', end='\n' * 2)


epics = ['ITV', 'BP']
epics.sort()

for epic in epics:
    get_news(epic)
