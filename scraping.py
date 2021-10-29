import requests
from bs4 import BeautifulSoup
from lxml import etree
from googleapiclient.discovery import build
from google.oauth2 import service_account
import time


# Google sheets creds
SERVICE_ACCOUNT_FILE = 'creds'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

spreadsheet_id = '1pNQhjBjjTSjjjc6m7Q5v9V2uMrvFiLJMP2y9aK7L3HQ'
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()




# URL'S GET FROM SHEET
# url = "https://www.markastok.com/buratti-slim-fit-fermuarli-dik-yaka-erkek-mont-556b79000-lacivert"
result = sheet.values().get(spreadsheetId=spreadsheet_id,
                            range="urls!A1:A1000").execute()
urls = list(result["values"])


payload={}
headers = {
  'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Upgrade-Insecure-Requests': '1',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
  'sec-ch-ua-platform': '"Windows"',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'same-origin',
  'Sec-Fetch-Dest': 'empty'
}


for i in range(0,len(urls)):
  values = None
  url = urls[i][0]
  product_availability = 0
  # time.sleep(1)
  try:
    response = requests.request("GET", url, headers=headers, data=payload)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Check
    # print(soup.title.text)

    product_name = soup.find("h1", {"id": "product-name"}).text.strip()

    # Product ID
    dom = etree.HTML(str(soup))
    try:
      product_id = dom.xpath('//*[@id="productRight"]/div/div[6]/div[2]/text()')[1].strip()
    except:
      product_id = 0


    # product_availability percentage calc
    product_availability_pure = soup.find("div", {"class": "new-size-variant fl col-12 ease variantList"})
    count_size = len(product_availability_pure.find_all("a"))
    count_availability = len(product_availability_pure.find_all("a", {"class": "col box-border"}))
    product_availability = round((count_availability * 100) / count_size, 2)
    if product_availability==0:
      # Write Data
      values = [[url, product_id, product_name, product_availability]]
      request = sheet.values().append(spreadsheetId=spreadsheet_id, range="Sayfa1", valueInputOption="USER_ENTERED",
                                      insertDataOption="INSERT_ROWS", body={"values": values})
      response = request.execute()
      print("Out of Stock:  ", url)
      continue


    offer = soup.find("div", {"class": "detay-indirim"}).text
    product_price = soup.find("span", {"class": "currencyPrice discountedPrice"}).text.strip()
    sale_price = soup.find("span", {"class": "discountPrice"}).text.strip()


    # Write Data
    values = [[url,product_id,product_name,product_availability,offer,product_price,sale_price]]
    request = sheet.values().append(spreadsheetId=spreadsheet_id, range="Sayfa1", valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values":values})
    response = request.execute()
    print(i ,"Succes:  " , url, product_availability)
  except AttributeError as error:
    # print(error)
    print(i ,"Error:  ", url, error)









