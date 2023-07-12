import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
from datetime import datetime

def Flight_notify(Product_status_cmp):
    params = {"message" : '機票資訊更新' + '\r\n' + 'https://p-bandai.com/tw'}

    headers = {
            "Authorization": "Bearer " + "1NRWebAnozSCp3GZxlmMq4K9eyl44YPsjQonB8OwgcJ",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)

    headers = {
            "Authorization": "Bearer " + "QBTPesWGLk5yF7Jm1R4N06eQnxC9RusUWMEiuR3u9e5",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)

if __name__ == '__main__':

    user_agent = UserAgent()
    headers={ 'user-agent': user_agent.random }

    #建立session
    session_requests = requests.session()

    while True:
        try:
            now = datetime.now()
            cycle_time = int(now.strftime('%M%S'))
            if cycle_time % 1 == 0:
                PB_response_cmp = session_requests.get('https://p-bandai.com/tw', headers=headers)
                PB_soup_cmp = BeautifulSoup(PB_response_cmp.text, 'lxml')
                PB_Product_status_cmp = str(PB_soup_cmp.find_all('div'))
                PB_Product_status_cmp = PB_Product_status_cmp[PB_Product_status_cmp.find('m-card__thumb') : PB_Product_status_cmp.find('m-card__thumb') +10000]
                if PB_Product_status != PB_Product_status_cmp:
                    PB_Product_status = PB_Product_status_cmp
                    PB_Product_status_notify = PB_Product_status_cmp[26 : PB_Product_status_cmp.find('class') -2]
                    Flight_notify(PB_Product_status_notify)
                elif PB_Product_status == PB_Product_status_cmp:
                    print('PB No new product '+str(now))

        except:
            time.sleep(0.5)

        time.sleep(0.5)
