# MovieAnalytics

Analysis of movie ratings from Letterboxd.com for user **karavan0788**.

This tool scrapes movie ratings from Letterboxd, exports them to a pandas DataFrame, and performs statistical analysis to identify preferences such as best directors, favorite genres, and rating patterns.

## Features

- 🎬 Scrapes movie ratings from Letterboxd user profile
- 📊 Exports data to pandas DataFrame and CSV files
- 🎯 Statistical analysis including:
  - Rating distribution and statistics
  - Best directors (by average rating)
  - Genre preferences
  - Top rated movies
  - Year-based analysis
- 📈 Comprehensive analysis reports

## Installation

1. Clone the repository:
```bash
git clone https://github.com/karavan88/MovieAnalytics.git
cd MovieAnalytics
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script to fetch data from Letterboxd:
```bash
python movie_analytics.py
```

**Note:** This requires internet access to letterboxd.com.

To see a demo with sample data (works offline):
```bash
python demo.py
```

The script will:
1. Fetch movie ratings from Letterboxd for user karavan0788
2. Save all ratings to `movie_ratings.csv`
3. Perform statistical analysis
4. Generate detailed reports and export them to CSV files:
   - `best_directors.csv` - Directors ranked by average rating
   - `genre_preferences.csv` - Genres ranked by average rating
   - `movies_by_year.csv` - Year-based statistics

## Output Example

```
MOVIE RATINGS ANALYSIS REPORT
================================================================================

📊 RATING STATISTICS:
  Total Movies: 150
  Average Rating: 3.85
  Median Rating: 4.00
  Std Rating: 0.85
  Min Rating: 1.00
  Max Rating: 5.00

⭐ RATING DISTRIBUTION:
  5.0 ★★★★★: 45 movies
  4.5 ★★★★★: 32 movies
  4.0 ★★★★: 38 movies
  ...

🏆 TOP 10 RATED MOVIES:
  5.0★ - The Godfather (1972) - Francis Ford Coppola
  5.0★ - Pulp Fiction (1994) - Quentin Tarantino
  ...

🎬 BEST DIRECTORS (min 2 movies):
  4.75★ - Christopher Nolan (4 movies)
  4.50★ - Martin Scorsese (6 movies)
  ...
```

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- pandas
- numpy
- lxml

## Notes

- The script includes polite delays between requests to avoid overloading Letterboxd servers
- By default, the script limits scraping to 5 pages for demonstration purposes
- Modify `max_pages` parameter in `movie_analytics.py` to scrape more pages
- Letterboxd does not have an official API, so this tool uses web scraping

## License

MIT License

## Author

Created for analyzing movie preferences of Letterboxd user karavan0788.
