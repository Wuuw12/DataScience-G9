import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
from tqdm import tqdm

page_url = []
data = []

def find_date(url):
    target = url
    content = requests.get(target).text
    html = bs(content, 'lxml').find_all('article')
    for i in tqdm(range(len(html))):
        each = html[i]
        url = each.a['href']
        title = each.h5.text.split(',', 1)
        if len(title) == 1:
            name = title[0]
            location = 'location not found'
        else:
            name = title[0]
            location = title[1]
        Date = each.span.text
        Date = Date.replace('—','')

        # go inside every article
        entry_raw_page = requests.get(url)
        entry_parsed_page = bs(entry_raw_page.text, "lxml")
        # get the main content
        main_content = entry_parsed_page.find_all('div', {'kopa-single-1'})
        # count the number of images
        img = main_content[0].find_all('img')
        img_num = 0
        for i in img:
            img_num += 1
        # count the number of descriptions
        text = main_content[0].find_all('p')
        Text_num = 0
        for t in text:
            Text_num += len(t.text)

        # get all the date
        history = []
        all_blue_spans = entry_parsed_page.find_all('span', {"style": "color: #0000ff;"})
        for span in all_blue_spans:
            if span.text:
                potential_date = span.text
                # If that text starts with a number
                if potential_date[0].isnumeric():
                    # Add it to the list with the date
                    potential_date = potential_date.split('/')
                    temp = re.sub('[^0-9]', '', potential_date[len(potential_date) - 1])
                    if len(temp) > 4:
                        A = list(temp)
                        A.insert(4,'-')
                        temp = ''.join(A)
                    history.append(temp)
                    '''
                    if len(potential_date) > 1:
                        temp = re.sub('[^0-9]','', potential_date[len(potential_date)-1])
                        history.append(temp)
                    else:
                        temp = re.sub('[^0-9]','', potential_date[0])
                        history.append(temp)
                    '''
            '''
                else:
                    # Add it to the list, but say it doesn't contain a date
                    history.append('No Date found in text')
            else:
                # It contained no text at all
                history.append('No Text found')
            '''

        data.append(dict(Url=url, Name=name, Location=location, Date=Date, Text_num=Text_num, Img_num=img_num, History=history))

        '''
        print(f"Entry URL = {URL}")
        print(f"\tEntry title = {title}")
        print(f"\tDate added = {Date}")
        '''

def get_url(url):
    target = url
    content = requests.get(target).text
    html = bs(content, 'lxml')
    a = html.find_all('a', {'class': 'next page-numbers'})
    print(a)

for page_number in range(1,34):
    url = f'https://www.scottishbrickhistory.co.uk/category/brick-and-tile-works/page/{page_number}/'
    page_url.append(url)

for each_page in page_url:
    find_date(each_page)

data = pd.DataFrame(data)
data.to_csv('data.csv', encoding='utf-8')
print(data.head())



#find_date('https://www.scottishbrickhistory.co.uk/category/brick-and-tile-works/')