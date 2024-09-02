import pandas as pd
from datetime import datetime
import os

# Step 1: Read Initial Rankings from a text file
def read_initial_rankings(file_path):
    with open(file_path, 'r') as file:
        rankings = [line.strip() for line in file.readlines()]
    return rankings

# Step 2: Read Match Results from the CSV file
def read_match_results(csv_file):
    matches_df = pd.read_csv(csv_file)
    return matches_df

# Step 3: Update Rankings based on match results
def update_rankings(rankings, winner, loser):
    if winner in rankings and loser in rankings:
        winner_rank = rankings.index(winner)
        loser_rank = rankings.index(loser)
        
        if winner_rank > loser_rank:
            # Move the winner up to the loser's position
            rankings.pop(winner_rank)
            rankings.insert(loser_rank, winner)
    
    elif winner not in rankings and loser in rankings:
        # Winner enters the ranking and loser is pushed down
        loser_rank = rankings.index(loser)
        rankings.insert(loser_rank, winner)
        rankings = rankings[:100]  # Keep only the top 100
    
    elif winner in rankings and loser not in rankings:
        # Winner stays in the ranking, no change
        pass
    
    elif winner not in rankings and loser not in rankings:
        # Neither in the ranking, winner enters at the bottom if not full
        if len(rankings) < 100:
            rankings.append(winner)
    
    return rankings

# Step 4: Write Updated Rankings to a new file (appending new column for each update)
def write_updated_rankings(rankings, output_file, initial=False):
    if not os.path.exists(output_file):
        # File does not exist, create a new file with initial rankings
        rank_numbers = list(range(1, 101))
        if initial:
            initial_df = pd.DataFrame({'Rank': rank_numbers, 'Initial': rankings[:100]})
            initial_df.to_csv(output_file, index=False)
        else:
            initial_df = pd.DataFrame({'Rank': rank_numbers, 'Initial': rankings[:100]})
            initial_df.to_csv(output_file, index=False)
    else:
        # File exists, update it with new rankings
        existing_df = pd.read_csv(output_file)
        
        # Get the current date for the column header
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Create a new DataFrame with the updated rankings
        new_column = pd.DataFrame({'Rank': list(range(1, 101)), current_date: rankings[:100]})
        
        # Merge with the existing DataFrame to retain historical data
        updated_df = pd.merge(existing_df, new_column, on='Rank', how='outer')
        
        # Save the updated DataFrame back to the CSV file
        updated_df.to_csv(output_file, index=False)

# Main Function to Run the Process
def main():
    initial_rankings_file = 'initial_wta_rankings.txt'
    match_results_file = 'tennis_matches.csv'
    output_file = 'updated_wta_rankings.csv'
    
    # Read the initial rankings
    rankings = read_initial_rankings(initial_rankings_file)
    
    # Write initial rankings to the output file only if the file does not exist
    if not os.path.exists(output_file):
        write_updated_rankings(rankings, output_file, initial=True)
    
    # Read match results
    matches_df = read_match_results(match_results_file)
    
    # Update rankings based on each match result
    for index, row in matches_df.iterrows():
        winner = row['Winner']
        loser = row['Loser']
        rankings = update_rankings(rankings, winner, loser)
    
    # Write the updated rankings to the file
    write_updated_rankings(rankings, output_file)
    print(f"Updated rankings have been written to {output_file}")

# Run the main function
if __name__ == "__main__":
    main()