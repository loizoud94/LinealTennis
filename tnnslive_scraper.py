from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
import time

# Path to my chromedriver
service = Service('/Users/loizoud94/Downloads/chromedriver-mac-arm64 2/chromedriver')
driver = webdriver.Chrome(service=service)

# Open TNNSLIVE page
driver.get('https://tnnslive.com/')

# Helper function to wait for an element to be clickable and click it
def wait_and_click(xpath, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    ).click()
    # Adding a small delay to ensure the click has the desired effect
    time.sleep(2)

# Click the necessary elements to navigate
try:
    wait_and_click('//*[@id="root"]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div/div/div[1]/div/div[1]/div/div/div')
except Exception as e:
    print(f"Error clicking on navigation elements: {e}")

try:
    wait_and_click('//*[@id="root"]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div/div')
except Exception as e:
    print(f"Error clicking on navigation elements: {e}")

# Adding a longer delay to ensure the page has time to fully load and update
time.sleep(3)  # Adjust as necessary

# Wait for the content to load
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div'))
    )
except Exception as e:
    print(f"Error waiting for content to load: {e}")

# Load the page source into BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the browser
driver.quit()

# Extract the match date from the webpage
date_element = soup.find('div', class_="css-1dbjc4n r-1awozwy r-13awgt0 r-1777fci")  # Replace with the correct class or identifier
match_date_text = date_element.get_text(strip=True) if date_element else "Unknown Date"

def parse_date(date_text):
    try:
        # Remove day names from the text
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Yesterday"]
        for day_name in day_names:
            date_text = date_text.replace(day_name, '').strip()
        
        # Split into day and month parts
        day_month = date_text.split()
        if len(day_month) == 2:
            day = day_month[0]
            month = day_month[1]
            
            # Map month abbreviations to full month names
            month_map = {
                'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April', 'May': 'May', 'Jun': 'June',
                'Jul': 'July', 'Aug': 'August', 'Sep': 'September', 'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
            }
            
            # If month abbreviation not found, use the raw month value
            month_full = month_map.get(month, month)
            
            # Convert to a date object; assume the current year
            today = datetime.today()
            date_str = f"{day} {month_full} {today.year}"
            date_obj = datetime.strptime(date_str, '%d %B %Y')
            return date_obj.strftime('%Y-%m-%d')  # Format for CSV
        else:
            print(f"Date parsing issue: {date_text}")
            return "Unknown Date"
    except Exception as e:
        print(f"Error parsing date: {e}")
        return "Unknown Date"

match_date = parse_date(match_date_text)

matches = []
players = soup.find_all('div', class_='css-901oao css-vcwn7f r-1wbh5a2')

# Helper function to get opacity from style attribute
def get_opacity(style):
    for part in style.split(';'):
        if 'opacity:' in part:
            return part.split(':')[1].strip()
    return None

# Temporary variables to hold players
current_match_players = []

# Iterate through players and group them into matches
for player in players:
    style = player.get('style', '')
    opacity = get_opacity(style)
    player_name = player.get_text(strip=True)
    
    current_match_players.append((player_name, opacity))
    
    # If two players are in the current match
    if len(current_match_players) == 2:
        winner = None
        loser = None
        
        for name, op in current_match_players:
            if op == '1':  # Winner
                winner = name
            elif op == '0.5':  # Loser
                loser = name
        
        # Only add match if both winner and loser are identified
        if winner and loser:
            matches.append((winner, loser, match_date))
        
        # Reset for the next match
        current_match_players = []

# Create a DataFrame from the matches list
df = pd.DataFrame(matches, columns=['Winner', 'Loser', 'Date'])

# Define the CSV file path
csv_file = 'tennis_matches.csv'

# Check if the file exists
if not os.path.isfile(csv_file):
    # If the file does not exist, create it and write the header
    df.to_csv(csv_file, index=False)
else:
    # If the file exists, append the new data without writing the header
    df.to_csv(csv_file, mode='a', header=False, index=False)

print(f"CSV file '{csv_file}' has been updated with new data.")