import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from plotly import plotly
from plotly.offline import init_notebook_mode, iplot
plotly.offline.init_notebook_mode()
init_notebook_mode()
import plotly.graph_objs as go
plotly.offline.iplot(Frame)
import cufflinks
cufflinks.go_offline()

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/74.0.3729.169 Safari/537.36'}

base_url = 'https://tver.hh.ru/search/vacancy?area=89&text=Python'


def Parser(base_url, headers):
    global title, company, href, compensation, i
    data = []

    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})

        print('По запросу найдено: ', len(divs), '\n')
        for div in divs:
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            compensation = div.find('div', class_="vacancy-serp-item__sidebar").text

            #print(company)
            #print(href)
            #print(title)
            #print(compensation, '\n')

        print("Connection is OK! \n")
    else:
        print("Connection denied! \n")

    data.append({
        'title': title,
        'href': href,
        'company': company,
        'compensation': compensation
    })


Frame = pd.DataFrame({'title': ['Software developer',                   # 1
                                'Lead Mobile Networking Architect',     # 2
                                'Developer-analyst',                    # 3
                                'Python-developer',                     # 4
                                'Python-developer',                     # 5
                                'Python&JS-developer',                  # 6
                                'DevOps Engineer Linux',                # 7
                                'Python teacher',                       # 8
                                'Senior QA Engineer',                   # 9
                                'DB-developer',                         # 10
                                'Software Engineer',                    # 11
                                'Senior system analyst',                # 12
                                'DB-developer',                         # 13
                                'BigData-developer',                    # 14
                                ],

                      'href': ['https://tver.hh.ru/vacancy/32843807?query=Python',
                               'https://tver.hh.ru/vacancy/33321515?query=Python',
                               'https://tver.hh.ru/vacancy/32790471?query=Python',
                               'https://tver.hh.ru/vacancy/31510872?query=Python',
                               'https://tver.hh.ru/vacancy/32730086?query=Python',
                               'https://tver.hh.ru/vacancy/30693999?query=Python',
                               'https://tver.hh.ru/vacancy/33009714?query=Python',
                               'https://tver.hh.ru/vacancy/32856867?query=Python',
                               'https://tver.hh.ru/vacancy/32849995?query=Python',
                               'https://tver.hh.ru/vacancy/31510793?query=Python',
                               'https://tver.hh.ru/vacancy/31510904?query=Python',
                               'https://tver.hh.ru/vacancy/31452735?query=Python',
                               'https://tver.hh.ru/vacancy/31510838?query=Python',
                               'https://tver.hh.ru/vacancy/32803116?query=Python'],

                      'company': ['OOO Integer',
                                  'Nokia Networks',
                                  'OOO Alpha Company',
                                  'RuBaseIT',
                                  'RuBaseIT',
                                  'RuBaseIT',
                                  'OOO Telecontact',
                                  'techno-land Quantorium',
                                  'Studio-Evolution',
                                  'RuBaseIT',
                                  'RuBaseIT',
                                  'Accenture',
                                  'RuBaseIT',
                                  'EPAM System Inc',
                                  ],

                      'compensation': [30000,
                                       None,
                                       55000,
                                       52500,
                                       60000,
                                       70000,
                                       50000,
                                       33000,
                                       95000,
                                       None,
                                       None,
                                       None,
                                       None,
                                       None]})

Frame.to_csv('OutputData.csv', sep='\t', header=True, index=True)
print(Frame)


Frame['compensation'].iplot(kind='hist', xTitle='Linear Distribution',
                            yTitle='Increase', title='Salary Distribution')


diff = Frame['compensation'].diff().hist()
print('Discrete difference: ', diff)
compensation_mean = Frame.get('compensation')
print('Mean Salary (Rub/M): ',compensation_mean.mean())


Frame.iplot(
    x='title',
    y='compensation',
    # Указываем категорию
    xTitle='Position',
    yTitle='Salary',
    title='Dependence of salary on position')


Parser(base_url, headers)
