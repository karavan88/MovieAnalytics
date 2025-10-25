"""
Demo script showing MovieAnalytics functionality with sample data.
This demonstrates what the tool would do when run with real Letterboxd data.
"""

import pandas as pd
from movie_analytics import MovieAnalyzer


def create_sample_data():
    """Create sample movie ratings data."""
    return pd.DataFrame([
        {
            'title': 'The Godfather',
            'rating': 5.0,
            'director': 'Francis Ford Coppola',
            'year': 1972,
            'genres': ['Crime', 'Drama'],
            'slug': 'the-godfather'
        },
        {
            'title': 'The Godfather Part II',
            'rating': 5.0,
            'director': 'Francis Ford Coppola',
            'year': 1974,
            'genres': ['Crime', 'Drama'],
            'slug': 'the-godfather-part-ii'
        },
        {
            'title': 'Pulp Fiction',
            'rating': 5.0,
            'director': 'Quentin Tarantino',
            'year': 1994,
            'genres': ['Crime', 'Drama'],
            'slug': 'pulp-fiction'
        },
        {
            'title': 'The Shawshank Redemption',
            'rating': 5.0,
            'director': 'Frank Darabont',
            'year': 1994,
            'genres': ['Drama'],
            'slug': 'the-shawshank-redemption'
        },
        {
            'title': 'Inception',
            'rating': 4.5,
            'director': 'Christopher Nolan',
            'year': 2010,
            'genres': ['Action', 'Sci-Fi', 'Thriller'],
            'slug': 'inception'
        },
        {
            'title': 'The Dark Knight',
            'rating': 4.5,
            'director': 'Christopher Nolan',
            'year': 2008,
            'genres': ['Action', 'Crime', 'Drama'],
            'slug': 'the-dark-knight'
        },
        {
            'title': 'Interstellar',
            'rating': 4.5,
            'director': 'Christopher Nolan',
            'year': 2014,
            'genres': ['Adventure', 'Drama', 'Sci-Fi'],
            'slug': 'interstellar'
        },
        {
            'title': 'Fight Club',
            'rating': 4.5,
            'director': 'David Fincher',
            'year': 1999,
            'genres': ['Drama'],
            'slug': 'fight-club'
        },
        {
            'title': 'Se7en',
            'rating': 4.5,
            'director': 'David Fincher',
            'year': 1995,
            'genres': ['Crime', 'Drama', 'Mystery'],
            'slug': 'se7en'
        },
        {
            'title': 'The Matrix',
            'rating': 4.5,
            'director': 'The Wachowskis',
            'year': 1999,
            'genres': ['Action', 'Sci-Fi'],
            'slug': 'the-matrix'
        },
        {
            'title': 'Goodfellas',
            'rating': 4.5,
            'director': 'Martin Scorsese',
            'year': 1990,
            'genres': ['Biography', 'Crime', 'Drama'],
            'slug': 'goodfellas'
        },
        {
            'title': 'Taxi Driver',
            'rating': 4.0,
            'director': 'Martin Scorsese',
            'year': 1976,
            'genres': ['Crime', 'Drama'],
            'slug': 'taxi-driver'
        },
        {
            'title': 'The Departed',
            'rating': 4.0,
            'director': 'Martin Scorsese',
            'year': 2006,
            'genres': ['Crime', 'Drama', 'Thriller'],
            'slug': 'the-departed'
        },
        {
            'title': 'Forrest Gump',
            'rating': 4.0,
            'director': 'Robert Zemeckis',
            'year': 1994,
            'genres': ['Drama', 'Romance'],
            'slug': 'forrest-gump'
        },
        {
            'title': 'The Green Mile',
            'rating': 4.0,
            'director': 'Frank Darabont',
            'year': 1999,
            'genres': ['Crime', 'Drama', 'Fantasy'],
            'slug': 'the-green-mile'
        },
        {
            'title': 'Django Unchained',
            'rating': 4.0,
            'director': 'Quentin Tarantino',
            'year': 2012,
            'genres': ['Drama', 'Western'],
            'slug': 'django-unchained'
        },
        {
            'title': 'Inglourious Basterds',
            'rating': 4.0,
            'director': 'Quentin Tarantino',
            'year': 2009,
            'genres': ['Adventure', 'Drama', 'War'],
            'slug': 'inglourious-basterds'
        },
        {
            'title': 'Parasite',
            'rating': 4.5,
            'director': 'Bong Joon-ho',
            'year': 2019,
            'genres': ['Comedy', 'Drama', 'Thriller'],
            'slug': 'parasite'
        },
        {
            'title': 'Whiplash',
            'rating': 4.5,
            'director': 'Damien Chazelle',
            'year': 2014,
            'genres': ['Drama', 'Music'],
            'slug': 'whiplash'
        },
        {
            'title': 'The Prestige',
            'rating': 4.0,
            'director': 'Christopher Nolan',
            'year': 2006,
            'genres': ['Drama', 'Mystery', 'Sci-Fi'],
            'slug': 'the-prestige'
        }
    ])


def main():
    """Run demo analysis with sample data."""
    print("="*80)
    print("MovieAnalytics Demo - Sample Data Analysis")
    print("="*80)
    print("\nNote: This demo uses sample data to show functionality.")
    print("To analyze real Letterboxd data, run: python movie_analytics.py\n")
    
    # Create sample data
    df = create_sample_data()
    
    # Save to CSV
    output_file = "demo_movie_ratings.csv"
    df.to_csv(output_file, index=False)
    print(f"✅ Sample data saved to {output_file}")
    print(f"   Total movies: {len(df)}\n")
    
    # Perform analysis
    analyzer = MovieAnalyzer(df)
    analyzer.print_analysis_report()
    
    # Export analysis results
    print("\n📁 Exporting detailed analysis...")
    
    # Best directors
    best_directors = analyzer.get_best_directors(min_movies=2)
    if not best_directors.empty:
        best_directors.to_csv("demo_best_directors.csv")
        print("  - demo_best_directors.csv")
    
    # Genre preferences
    genre_prefs = analyzer.get_genre_preferences()
    if not genre_prefs.empty:
        genre_prefs.to_csv("demo_genre_preferences.csv")
        print("  - demo_genre_preferences.csv")
    
    # Movies by year
    year_stats = analyzer.get_movies_by_year()
    if not year_stats.empty:
        year_stats.to_csv("demo_movies_by_year.csv")
        print("  - demo_movies_by_year.csv")
    
    print("\n" + "="*80)
    print("✨ Demo complete!")
    print("="*80)
    print("\nTo run with real data from Letterboxd:")
    print("  1. Ensure you have internet access")
    print("  2. Run: python movie_analytics.py")
    print("\nThe script will:")
    print("  - Fetch ratings from https://letterboxd.com/karavan0788/films/")
    print("  - Extract movie details (director, year, genres)")
    print("  - Perform comprehensive statistical analysis")
    print("  - Export results to CSV files")


if __name__ == "__main__":
    main()
