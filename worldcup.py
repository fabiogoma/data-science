from bs4 import BeautifulSoup as bs
import sqlalchemy
import pandas as pd
import sqlite3
import requests
import os

base_url = "https://en.wikipedia.org"

def clean_content(data):
    if data.find("br"):
        items = []
        for item in data.stripped_strings:
            if 'goal' not in item:
                if '[' not in item:
                    items.append(item.strip())
        return items
    else:
        return data.get_text(" ", strip=True).replace('\xa0', ' ')

def get_infobox(url):
    req = requests.get(url)
    soup = bs(req.content, features="html.parser")
    infobox = soup.find(class_="infobox vcalendar")

    infobox_rows = infobox.find_all("tr")
    
    year = int(os.path.basename(url)[0:4])
    
    worldcup_info = {}
    worldcup_info['Year'] = year
    
    for index, row in enumerate(infobox_rows):
        if index > 1:
            if row.find('th'):
                if row.find('td'):
                    content_key = row.find('th').get_text(strip=True).replace('\xa0', ' ').strip()
                    if 'Venue' in content_key:
                        content_key = 'Stadiums'
                    if 'Host countries' in content_key:
                        content_key = 'Host country'
                    content_value = clean_content(row.find('td'))
                    worldcup_info[content_key] = content_value

    # Convert number fields to integer
    worldcup_info['Teams'] = int(worldcup_info.get('Teams',0).split(" ")[0])
    worldcup_info['Stadiums'] = int(worldcup_info.get('Stadiums',0).split(" ")[0])
    worldcup_info['Goals scored'] = int(worldcup_info.get('Goals scored',0).split(" ")[0])
    worldcup_info['Matches played'] = int(worldcup_info.get('Matches played',0).split(" ")[0])
    worldcup_info['Attendance'] = int(worldcup_info.get('Attendance',0).split(" ")[0].replace(',',"").replace(".",""))

    # Remove brackets from names
    worldcup_info['Best player(s)'] = worldcup_info.get('Best player(s)','N/A').split("[")[0].strip()
    worldcup_info['Best young player'] = worldcup_info.get('Best young player','N/A').split("[")[0].strip()
    worldcup_info['Bestgoalkeeper'] = worldcup_info.get('Bestgoalkeeper','N/A').split("[")[0].strip()
    worldcup_info['Third place'] = worldcup_info.get('Third place','N/A').split("[")[0].strip()
    worldcup_info['Fourth place'] = worldcup_info.get('Fourth place','N/A').split("[")[0].strip()

    # Remove parentheses from names
    worldcup_info['Champions'] = worldcup_info.get('Champions','N/A').split("(")[0].strip()

    # Convert string to List
    if isinstance(worldcup_info.get('Fair play award','N/A'), str):
        worldcup_info['Fair play award'] = [worldcup_info.get('Fair play award','N/A').split("[")[0].strip()]

    if isinstance(worldcup_info.get('Top scorer(s)','N/A'), str):
        worldcup_info['Top scorer(s)'] = [worldcup_info.get('Top scorer(s)','N/A').split("(")[0].strip()]
    else:
        if 'players' in worldcup_info['Top scorer(s)'][0]:
            worldcup_info['Top scorer(s)'] = ['N/A']

    month_of_the_year = ['January', 'February', 'March', 'Apr', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    months_of_the_worldcup = []

    # Convert date fields to a list of months
    if isinstance(worldcup_info.get('Dates','N/A'), str):
        for month in worldcup_info.get('Dates','N/A').split(" "):
            if month in month_of_the_year:
                months_of_the_worldcup.append(month)
            elif 'N/A' in month_of_the_year:
                months_of_the_worldcup.append('N/A')

    worldcup_info['Dates'] = months_of_the_worldcup

    return worldcup_info

initial_request = requests.get(f"{ base_url }/wiki/FIFA_World_Cup")

# Convert to a beautiful soup object
soup = bs(initial_request.content, features="html.parser")

# # Print out the HTML
# contents = soup.prettify()
# print(contents)

worldcup_years_table = soup.find_all(class_="infobox hlist nowraplinks")
worldcup_info_list = []

for item in worldcup_years_table:
    for index, link in enumerate(item.find_all("a", {"title" : True})):
        if index > 0:
            worldcup_year = int(link['title'][0:4])
            if worldcup_year < 2022:
                print(f"Fetching data from: { base_url + link['href'] }")
                worldcup_info_list.append(get_infobox(base_url + link['href']))

# print(len(worldcup_info_list))

worldcup_data_frame = pd.DataFrame(worldcup_info_list)

# Playing with pandas

# print(worldcup_data_frame.size)
# print(worldcup_data_frame.count)
# print(worldcup_data_frame.head)
# print(worldcup_data_frame.dtypes)
print(worldcup_data_frame.info())
worldcup_attendance = worldcup_data_frame.sort_values(['Attendance'], ascending=True)
print(worldcup_attendance.head(10))

# Create a connection to a new SQLite database file
sqlite_engine = sqlalchemy.create_engine('sqlite:///worldcup.db', echo=True)
mysql_engine = sqlalchemy.create_engine("mysql+mysqldb://metabase:password@127.0.0.1/metabase?charset=utf8mb4", echo=True)

sqlite_connection = sqlite_engine.connect()
sqlite_table = "worldcup"

mysql_connection = mysql_engine.connect()
mysql_table = "worldcup"

# Extract all "object" columns
column_names = worldcup_data_frame.select_dtypes(include=[object]).columns.values.tolist()

# Convert object columns type to String
for column in column_names:
    worldcup_data_frame[column] = worldcup_data_frame[column].astype('str')

# Save dataframe to SQL
worldcup_data_frame.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
worldcup_data_frame.to_sql(mysql_table, mysql_connection, if_exists='replace')

sqlite_connection.close()
mysql_connection.close()

# with open('teams.json', 'w', encoding='utf8') as outfile:
#     json.dump(all_teams, outfile, indent=4, sort_keys=True)
