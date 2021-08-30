import os
from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup as bs
with open('records.json') as json_file:
    records = json.load(json_file)


TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
MY_CHAT_ID = os.environ['MY_CHAT_ID']
def send_msg(text):

   url_req = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage" + "?chat_id=" + MY_CHAT_ID + "&text=" + text 
   results = requests.get(url_req)
   print(results.json())

## get current year and month

this_year =  datetime.now().year
this_month = datetime.now().month
url = f'http://jdih.kemendag.go.id/peraturan?tahunreg={this_year}&groupreg=4&jenisreg=&komoditireg=&search=Penetapan+Harga+Patokan+Ekspor+Atas+Produk+Pertanian+Dan+Kehutanan+Yang+Dikenakan+Bea+Keluar'

rs = requests.get(url)
html = rs.text
soup = bs(html, 'html.parser')

data = []
table = soup.find('table', attrs={'class':'table-bordered'})
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    # href = row.find_all('td')

    mylink = cols[1].find("a")["href"]  
    cols = [ele.text.strip() for ele in cols]
    cols.append(mylink)
    data.append([ele for ele in cols if ele]) # Get rid of empty values
#
recent_date =  data[-1][3]
converted_date = datetime.strptime(recent_date,'%Y-%m-%d')
recent_month = converted_date.month
recent_url = data[-1][-1]
final_message = f"export tax has been updated. url : {recent_url}"

if not any(record['date'] == recent_date for record in records) and recent_month==this_month :
    send_msg(final_message)
    new_entry = {}
    new_entry["date"] = recent_date
    records.append(new_entry)
    with open('records.json', 'w') as fp:
        json.dump(records, fp)
else:
    
    with open('tmp.json', 'w') as fp:
        a_datetime = datetime.datetime.now()
        formatted_datetime = a_datetime.isoformat()
        json_datetime = json.dumps(formatted_datetime)
        json.dump(json_datetime, fp)
