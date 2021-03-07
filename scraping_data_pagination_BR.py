import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

class GetConntent:

    def __init__(self):
        self. companies = []
        self.url1 = "https://panoramafirm.pl/kancelaria_adwokacka/małopolska/firmy,"
        self.url2 = ".html?sort="
        self.content = ()

    def contents(self):
        for x in range(1, 2):
            url = self.url1 + str(x) + self.url2
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            # print(soup.title)
            self.content = soup.find_all('li', class_='card company-item py-2 container my-2')
        return self.content


class SelectContent:

    def __init__(self):
        self.score = ''

    # print(company.contents())
    def selectData(self):
        company = GetConntent()
        for property in company.contents():
            name = property.find('h2').text
            rating = property.find('div', {'class':'rater-review star-rating'})['data-rating']
            if float(rating) == 0.0 or float(rating) >= 4.0:
                self.score = rating
            try:
                web_address = property.find('a', {'class': 'icon-website addax addax-cs_hl_hit_homepagelink_click'})['href']

            except TypeError:
                web_address = None
            try:
                email = property.find('a', {'class': 'ajax-modal-link icon-envelope cursor-pointer addax addax-cs_hl_email_submit_click'})['data-company-email']
            except TypeError:
                email = None
            company_data = {
                'nazwa': name,
                'wynik': self.score,
                'www': web_address,
                'email': email,
            }
            company.companies.append(company_data)
            print("Liczna firm: ", len(company.companies))
        time.sleep(3)


        df = pd.DataFrame(company.companies)
        print(df.head())

        df.to_csv('companies.csv')


company_on = SelectContent()
company_on.selectData()
