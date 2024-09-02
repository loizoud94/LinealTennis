# LinealTennis
A fun project to reimagine the tennis rankings in a 'lineal' system. If a player beats someone ranked above them, they assume their opponent's rank and everyone in between is pushed down one.

---

This repository contains scripts and data files for scraping tennis match results and updating ATP and WTA player rankings using a lineal ranking system. In this system, if a lower-ranked player defeats a higher-ranked player, they assume their opponent's ranking, pushing everyone else down a space.

## Project Overview

### Files in this Repository

- **`tnnslive_scraper.py`**: A web scraping script that extracts tennis match results from [tnnslive.com](https://tnnslive.com) and stores them in `tennis_matches.csv`.
- **`atp_rankings_updater.py`**: Updates the ATP rankings based on the results in `tennis_matches.csv`, using the initial rankings from `initial_atp_rankings.txt`.
- **`wta_rankings_updater.py`**: Similar to `atp_rankings_updater.py`, but for WTA rankings, using `initial_wta_rankings.txt`.
- **`initial_atp_rankings.txt`**: The initial ATP player rankings used as the starting point for the lineal ranking system.
- **`initial_wta_rankings.txt`**: The initial WTA player rankings used as the starting point for the lineal ranking system.
- **`tennis_matches.csv`**: A CSV file containing the scraped match results. This file is continually updated by `tnnslive_scraper.py`.
- **`updated_atp_rankings.csv`**: The CSV file where updated ATP rankings are stored after each script run.
- **`updated_wta_rankings.csv`**: The CSV file where updated WTA rankings are stored after each script run.

### Lineal Ranking System

The ranking system implemented here follows a lineal format:
- When a lower-ranked player defeats a higher-ranked player, they assume their opponent's ranking.
- All players between the original positions of the winner and loser are pushed down one rank.
- The rankings are updated in real-time based on the latest match results from `tennis_matches.csv`.

## How to Use

### Prerequisites

- **Python 3.6+**: Ensure you have Python installed on your system.
- **Required Libraries**: Install the required libraries using pip.

```bash
pip install pandas requests beautifulsoup4 selenium
```

### Running the Scripts

1. **Scrape the Latest Match Results:**
   - Run `tnnslive_scraper.py` to fetch the latest tennis match results and update `tennis_matches.csv`.

   ```bash
   python tnnslive_scraper.py
   ```

2. **Update ATP Rankings:**
   - Run `atp_rankings_updater.py` to update the ATP rankings based on the latest match results.

   ```bash
   python atp_rankings_updater.py
   ```

3. **Update WTA Rankings:**
   - Run `wta_rankings_updater.py` to update the WTA rankings based on the latest match results.

   ```bash
   python wta_rankings_updater.py
   ```

### Automating the Process

To automate the entire process, you can use cron jobs (Linux/Mac) or Task Scheduler (Windows) to run these scripts periodically. This will ensure your match results and rankings are always up-to-date.

## Visualization

If you would like to visualise the rankings over time, you can create a script that reads from the `updated_atp_rankings.csv` or `updated_wta_rankings.csv` files and generates line plots or other types of charts.

## Contributing

Feel free to fork this repository and submit pull requests if you have any improvements or additional features you would like to add.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
