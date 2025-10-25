"""
MovieAnalytics - Letterboxd User Data Analysis
Fetches movie ratings from Letterboxd for user karavan0788 and performs statistical analysis.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from collections import Counter
from typing import List, Dict, Optional
import time


class LetterboxdScraper:
    """Scraper for Letterboxd user movie ratings."""
    
    BASE_URL = "https://letterboxd.com"
    
    def __init__(self, username: str):
        """
        Initialize the scraper for a specific user.
        
        Args:
            username: Letterboxd username
        """
        self.username = username
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_total_pages(self) -> int:
        """
        Get the total number of pages of ratings for the user.
        
        Returns:
            Number of pages
        """
        url = f"{self.BASE_URL}/{self.username}/films/"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find pagination
            pagination = soup.find('div', class_='pagination')
            if pagination:
                page_links = pagination.find_all('a', class_='paginate-page')
                if page_links:
                    # Get the last page number
                    last_page = max([int(link.text) for link in page_links if link.text.isdigit()])
                    return last_page
            return 1
        except Exception as e:
            print(f"Error getting total pages: {e}")
            return 1
    
    def scrape_ratings_page(self, page: int = 1) -> List[Dict]:
        """
        Scrape ratings from a specific page.
        
        Args:
            page: Page number to scrape
            
        Returns:
            List of movie dictionaries with ratings and metadata
        """
        url = f"{self.BASE_URL}/{self.username}/films/page/{page}/"
        movies = []
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all film posters/entries
            film_items = soup.find_all('li', class_='poster-container')
            
            for item in film_items:
                movie_data = {}
                
                # Get movie title and year
                film_div = item.find('div')
                if film_div and film_div.get('data-film-slug'):
                    slug = film_div['data-film-slug']
                    movie_data['slug'] = slug
                    
                    # Get film name from poster image
                    img = item.find('img')
                    if img and img.get('alt'):
                        movie_data['title'] = img['alt']
                
                # Get rating (stars)
                rating_span = item.find('span', class_='rating')
                if rating_span:
                    rating_class = rating_span.get('class', [])
                    for cls in rating_class:
                        if cls.startswith('rated-'):
                            # Extract rating from class like 'rated-10' (means 5 stars)
                            rating_num = int(cls.replace('rated-', ''))
                            movie_data['rating'] = rating_num / 2.0  # Convert to 0-5 scale
                            break
                
                # Only add if we have essential data
                if 'title' in movie_data and 'rating' in movie_data:
                    movies.append(movie_data)
            
            return movies
        except Exception as e:
            print(f"Error scraping page {page}: {e}")
            return []
    
    def scrape_movie_details(self, slug: str) -> Dict:
        """
        Scrape additional details for a specific movie.
        
        Args:
            slug: Movie slug from Letterboxd URL
            
        Returns:
            Dictionary with movie details (director, year, genres)
        """
        url = f"{self.BASE_URL}/film/{slug}/"
        details = {}
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get director
            director_link = soup.find('a', href=re.compile(r'/director/'))
            if director_link:
                details['director'] = director_link.text.strip()
            
            # Get year
            year_link = soup.find('a', href=re.compile(r'/films/year/'))
            if year_link:
                year_text = year_link.text.strip()
                if year_text.isdigit():
                    details['year'] = int(year_text)
            
            # Get genres
            genre_links = soup.find_all('a', href=re.compile(r'/films/genre/'))
            if genre_links:
                details['genres'] = [link.text.strip() for link in genre_links]
            
            return details
        except Exception as e:
            print(f"Error scraping details for {slug}: {e}")
            return {}
    
    def scrape_all_ratings(self, max_pages: Optional[int] = None, fetch_details: bool = True) -> pd.DataFrame:
        """
        Scrape all ratings for the user.
        
        Args:
            max_pages: Maximum number of pages to scrape (None for all)
            fetch_details: Whether to fetch detailed info for each movie
            
        Returns:
            DataFrame with all movie ratings and metadata
        """
        print(f"Scraping ratings for user: {self.username}")
        
        total_pages = self.get_total_pages()
        if max_pages:
            total_pages = min(total_pages, max_pages)
        
        print(f"Total pages to scrape: {total_pages}")
        
        all_movies = []
        for page in range(1, total_pages + 1):
            print(f"Scraping page {page}/{total_pages}...")
            movies = self.scrape_ratings_page(page)
            all_movies.extend(movies)
            time.sleep(1)  # Be polite to the server
        
        print(f"Found {len(all_movies)} rated movies")
        
        # Fetch detailed information if requested
        if fetch_details and all_movies:
            print("Fetching movie details...")
            for i, movie in enumerate(all_movies):
                if 'slug' in movie:
                    print(f"Fetching details for movie {i+1}/{len(all_movies)}: {movie['title']}")
                    details = self.scrape_movie_details(movie['slug'])
                    movie.update(details)
                    time.sleep(1)  # Be polite to the server
        
        # Convert to DataFrame
        df = pd.DataFrame(all_movies)
        return df


class MovieAnalyzer:
    """Analyzer for movie ratings data."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer with movie ratings DataFrame.
        
        Args:
            df: DataFrame with movie ratings
        """
        self.df = df
    
    def get_rating_statistics(self) -> Dict:
        """
        Get basic statistics about ratings.
        
        Returns:
            Dictionary with rating statistics
        """
        stats = {
            'total_movies': len(self.df),
            'average_rating': self.df['rating'].mean(),
            'median_rating': self.df['rating'].median(),
            'std_rating': self.df['rating'].std(),
            'min_rating': self.df['rating'].min(),
            'max_rating': self.df['rating'].max(),
        }
        return stats
    
    def get_rating_distribution(self) -> pd.Series:
        """
        Get the distribution of ratings.
        
        Returns:
            Series with rating counts
        """
        return self.df['rating'].value_counts().sort_index()
    
    def get_best_directors(self, min_movies: int = 2) -> pd.DataFrame:
        """
        Get directors sorted by average rating.
        
        Args:
            min_movies: Minimum number of movies to be included
            
        Returns:
            DataFrame with directors and their statistics
        """
        if 'director' not in self.df.columns:
            print("Director information not available")
            return pd.DataFrame()
        
        # Filter out movies without director info
        df_with_directors = self.df[self.df['director'].notna()].copy()
        
        # Group by director
        director_stats = df_with_directors.groupby('director').agg({
            'rating': ['mean', 'count', 'std']
        }).round(2)
        
        director_stats.columns = ['avg_rating', 'movie_count', 'std_rating']
        director_stats = director_stats[director_stats['movie_count'] >= min_movies]
        director_stats = director_stats.sort_values('avg_rating', ascending=False)
        
        return director_stats
    
    def get_movies_by_year(self) -> pd.DataFrame:
        """
        Get statistics grouped by year.
        
        Returns:
            DataFrame with year-based statistics
        """
        if 'year' not in self.df.columns:
            print("Year information not available")
            return pd.DataFrame()
        
        year_stats = self.df.groupby('year').agg({
            'rating': ['mean', 'count']
        }).round(2)
        
        year_stats.columns = ['avg_rating', 'movie_count']
        year_stats = year_stats.sort_values('year', ascending=False)
        
        return year_stats
    
    def get_genre_preferences(self) -> pd.DataFrame:
        """
        Get average ratings by genre.
        
        Returns:
            DataFrame with genre statistics
        """
        if 'genres' not in self.df.columns:
            print("Genre information not available")
            return pd.DataFrame()
        
        # Expand genres (each movie can have multiple genres)
        genre_ratings = []
        for _, row in self.df.iterrows():
            if isinstance(row.get('genres'), list):
                for genre in row['genres']:
                    genre_ratings.append({'genre': genre, 'rating': row['rating']})
        
        if not genre_ratings:
            return pd.DataFrame()
        
        genre_df = pd.DataFrame(genre_ratings)
        genre_stats = genre_df.groupby('genre').agg({
            'rating': ['mean', 'count']
        }).round(2)
        
        genre_stats.columns = ['avg_rating', 'movie_count']
        genre_stats = genre_stats.sort_values('avg_rating', ascending=False)
        
        return genre_stats
    
    def get_top_rated_movies(self, n: int = 10) -> pd.DataFrame:
        """
        Get top rated movies.
        
        Args:
            n: Number of top movies to return
            
        Returns:
            DataFrame with top rated movies
        """
        top_movies = self.df.nlargest(n, 'rating')
        columns = ['title', 'rating']
        if 'director' in self.df.columns:
            columns.append('director')
        if 'year' in self.df.columns:
            columns.append('year')
        
        return top_movies[columns]
    
    def print_analysis_report(self):
        """Print a comprehensive analysis report."""
        print("\n" + "="*80)
        print("MOVIE RATINGS ANALYSIS REPORT")
        print("="*80)
        
        # Basic statistics
        print("\n📊 RATING STATISTICS:")
        stats = self.get_rating_statistics()
        for key, value in stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
        
        # Rating distribution
        print("\n⭐ RATING DISTRIBUTION:")
        dist = self.get_rating_distribution()
        for rating, count in dist.items():
            stars = "★" * int(rating)
            print(f"  {rating:.1f} {stars}: {count} movies")
        
        # Top rated movies
        print("\n🏆 TOP 10 RATED MOVIES:")
        top_movies = self.get_top_rated_movies(10)
        for idx, row in top_movies.iterrows():
            title = row['title']
            rating = row['rating']
            director = row.get('director', 'Unknown')
            year = row.get('year', 'N/A')
            print(f"  {rating:.1f}★ - {title} ({year}) - {director}")
        
        # Best directors
        print("\n🎬 BEST DIRECTORS (min 2 movies):")
        best_directors = self.get_best_directors(min_movies=2)
        if not best_directors.empty:
            for director, row in best_directors.head(10).iterrows():
                print(f"  {row['avg_rating']:.2f}★ - {director} ({int(row['movie_count'])} movies)")
        
        # Genre preferences
        print("\n🎭 GENRE PREFERENCES:")
        genre_prefs = self.get_genre_preferences()
        if not genre_prefs.empty:
            for genre, row in genre_prefs.head(10).iterrows():
                print(f"  {row['avg_rating']:.2f}★ - {genre} ({int(row['movie_count'])} movies)")
        
        print("\n" + "="*80)


def main():
    """Main function to run the analysis."""
    username = "karavan0788"
    
    print("MovieAnalytics - Letterboxd User Analysis")
    print(f"User: {username}\n")
    
    # Scrape ratings
    scraper = LetterboxdScraper(username)
    df = scraper.scrape_all_ratings(max_pages=5, fetch_details=True)  # Limit to 5 pages for demo
    
    if df.empty:
        print("No data found. Please check if the username is correct.")
        return
    
    # Save to CSV
    output_file = "movie_ratings.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Data saved to {output_file}")
    
    # Perform analysis
    analyzer = MovieAnalyzer(df)
    analyzer.print_analysis_report()
    
    # Export analysis results
    print("\n📁 Exporting detailed analysis...")
    
    # Best directors
    best_directors = analyzer.get_best_directors(min_movies=2)
    if not best_directors.empty:
        best_directors.to_csv("best_directors.csv")
        print("  - best_directors.csv")
    
    # Genre preferences
    genre_prefs = analyzer.get_genre_preferences()
    if not genre_prefs.empty:
        genre_prefs.to_csv("genre_preferences.csv")
        print("  - genre_preferences.csv")
    
    # Movies by year
    year_stats = analyzer.get_movies_by_year()
    if not year_stats.empty:
        year_stats.to_csv("movies_by_year.csv")
        print("  - movies_by_year.csv")
    
    print("\n✨ Analysis complete!")


if __name__ == "__main__":
    main()
