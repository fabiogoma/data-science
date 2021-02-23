from bs4 import BeautifulSoup
import sqlalchemy
import pandas as pd
import requests
import json
import time

base_url = "https://www.louwman.nl/index.php?mact=Occasions,cntnt01,ajaxDoAdvancedSearch,0&cntnt01returnid=1&pagina="

def get_cars_from_page(url):
    get_cars_page_request = requests.get(url)
    page_cars_json = json.loads(get_cars_page_request.content)

    # Convert to a beautiful soup object
    soup = BeautifulSoup(page_cars_json['occasions_html'], features="html.parser")

    # # Print out the HTML
    # contents = soup.prettify()
    # print(contents)

    all_cars_columns = soup.find_all(class_="column")

    all_cars_details = []
    for car in all_cars_columns:
        car_details = {}
        favAuto_div = car.find(class_="favAuto")
        wrap_div = car.find(class_="wrap")
        car_details['brand'] = favAuto_div['data-merk'].strip()
        car_details['model'] = favAuto_div['data-model'].strip()
        car_details['version'] = favAuto_div['data-uitvoering'].strip()
        car_details['license'] = favAuto_div['data-kenteken'].strip()
        car_details['price'] = int(favAuto_div['data-prijs'].strip())

        car_details['year'] = int(wrap_div.text.split("|")[0].strip())
        car_details['engine'] = wrap_div.text.split("|")[1].strip()
        car_details['mileage'] = int(wrap_div.text.split("|")[2].replace("km", "").replace(".","").strip())

        car_details['link'] = favAuto_div['data-url'].strip()

        all_cars_details.append(car_details)
    return all_cars_details

total_pages = 181
page = 1
all_cars_list = []

while page <= total_pages:
    time.sleep(1)
    url_page = base_url + str(page)
    print(f"Fetching data from: { url_page }")
    all_cars_list += get_cars_from_page(url_page)
    page += 1

# Create a panda data frame
cars_data_frame = pd.DataFrame(all_cars_list)
print(cars_data_frame.head())
print(cars_data_frame.info())

# Create a connection to a new SQLAlchemy engine
sqlite_engine = sqlalchemy.create_engine('sqlite:///cars.db', echo=True)
mysql_engine = sqlalchemy.create_engine("mysql+mysqldb://metabase:password@127.0.0.1/metabase?charset=utf8mb4", echo=True)

sqlite_connection = sqlite_engine.connect()
sqlite_table = "cars"

mysq_connection = mysql_engine.connect()
mysql_table = "cars"

# Save dataframe to SQL
cars_data_frame.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
cars_data_frame.to_sql(mysql_table, mysq_connection, if_exists='replace')

sqlite_connection.close()
mysq_connection.close()
