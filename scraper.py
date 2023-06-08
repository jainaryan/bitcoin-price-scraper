from bs4 import BeautifulSoup
import requests
import pandas as pd

# Initialize variables
count = 0
cryptonamelist = []
cryptopricelist = []
cryptodatelist = []
df = pd.DataFrame()

# Define the list of dates to scrape
# Dates are chosen between 5 April 2020 to 26 July 2020
dates = ['20200405/', '20200503/', '20200510/', '20200517/', '20200524/', '20200531/', '20200607/', '20200614/', '20200621/', '20200628/', '20200705/', '20200712/', '20200719/', '20200726/']

# Iterate over each date
for i in dates:
    # Send a GET request to the specified URL
    r = requests.get("https://coinmarketcap.com/historical/" + i)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find all rows with the specified class
    tr = soup.find_all('tr', attrs={'class': 'cmc-table-row'})

    # Iterate over each row
    for row in tr:
        # Check if the count is 1
        if count == 1:
            count = 0
            break

        # Increment the count
        count = count + 1

        # Find the cryptocurrency name
        cryptoname = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name'})
        finalname = cryptoname.find('a', attrs={'class': 'cmc-table__column-name--name cmc-link'}).text.strip()

        # Find the cryptocurrency price
        cryptoprice = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price'}).text.strip()

        # Append the date, price, and name to their respective lists
        cryptodatelist.append(i[:-1])
        cryptopricelist.append(cryptoprice[1:])
        cryptonamelist.append(finalname)

        # Print the cryptocurrency name and price (optional)
        print(finalname)
        print(cryptoprice)

# Assign the lists to the DataFrame columns
df['date'] = cryptodatelist
df['price'] = cryptopricelist
df['name'] = cryptonamelist

# Save the DataFrame to a CSV file
df.to_csv(r'C:\Projects\cryptoscraper\bitcoinhistory.csv')
