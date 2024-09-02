from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd

# Path to your chromedriver
service = Service('/Users/loizoud94/Downloads/chromedriver-mac-arm64 2/chromedriver')
driver = webdriver.Chrome(service=service)

# Navigate to the desired page
driver.get('https://www.atptour.com/en/scores/current')

# Load the page source into BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the browser
driver.quit()

print(soup.get_text())

# Initialize lists to store data
winners = []
losers = []

# Find all match result sections (adjust the selector as needed)
matches = soup.find_all('div', class_='player-info')  # Update to match actual HTML

# Function to clean player names
def clean_name(name):
    # Remove anything after the first parenthesis including the parenthesis
    if '(' in name:
        return name.split('(')[0].strip()
    return name.strip()

# Extract winner and loser
for match in matches:
    players = match.find_all('div', class_='name')
    for player in players:
        # Clean the player name to remove seeds
        player_name = clean_name(player.text.strip())
        
        # Check if player has a sibling with class 'winner'
        if player.find_next_sibling('div', class_='winner'):
            winners.append(player_name)  # This player is the winner
        else:
            losers.append(player_name)  # This player is the loser
            
# Create DataFrame
df = pd.DataFrame({
    'Winner': winners,
    'Loser': losers
})

# Display DataFrame
print(df)