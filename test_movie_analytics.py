"""
Unit tests for MovieAnalytics
"""

import unittest
import pandas as pd
from movie_analytics import MovieAnalyzer


class TestMovieAnalyzer(unittest.TestCase):
    """Test cases for MovieAnalyzer class."""
    
    def setUp(self):
        """Set up test data."""
        self.test_data = pd.DataFrame([
            {
                'title': 'The Godfather',
                'rating': 5.0,
                'director': 'Francis Ford Coppola',
                'year': 1972,
                'genres': ['Crime', 'Drama']
            },
            {
                'title': 'The Godfather Part II',
                'rating': 5.0,
                'director': 'Francis Ford Coppola',
                'year': 1974,
                'genres': ['Crime', 'Drama']
            },
            {
                'title': 'Pulp Fiction',
                'rating': 4.5,
                'director': 'Quentin Tarantino',
                'year': 1994,
                'genres': ['Crime', 'Drama']
            },
            {
                'title': 'Inception',
                'rating': 4.5,
                'director': 'Christopher Nolan',
                'year': 2010,
                'genres': ['Action', 'Sci-Fi', 'Thriller']
            },
            {
                'title': 'The Dark Knight',
                'rating': 4.0,
                'director': 'Christopher Nolan',
                'year': 2008,
                'genres': ['Action', 'Crime', 'Drama']
            }
        ])
        self.analyzer = MovieAnalyzer(self.test_data)
    
    def test_rating_statistics(self):
        """Test rating statistics calculation."""
        stats = self.analyzer.get_rating_statistics()
        
        self.assertEqual(stats['total_movies'], 5)
        self.assertAlmostEqual(stats['average_rating'], 4.6, places=1)
        self.assertEqual(stats['max_rating'], 5.0)
        self.assertEqual(stats['min_rating'], 4.0)
    
    def test_rating_distribution(self):
        """Test rating distribution."""
        dist = self.analyzer.get_rating_distribution()
        
        self.assertEqual(dist[5.0], 2)  # Two 5-star movies
        self.assertEqual(dist[4.5], 2)  # Two 4.5-star movies
        self.assertEqual(dist[4.0], 1)  # One 4-star movie
    
    def test_best_directors(self):
        """Test best directors analysis."""
        directors = self.analyzer.get_best_directors(min_movies=2)
        
        # Francis Ford Coppola should be top with 5.0 average
        self.assertEqual(directors.index[0], 'Francis Ford Coppola')
        self.assertEqual(directors.iloc[0]['avg_rating'], 5.0)
        self.assertEqual(directors.iloc[0]['movie_count'], 2)
    
    def test_top_rated_movies(self):
        """Test top rated movies retrieval."""
        top_movies = self.analyzer.get_top_rated_movies(3)
        
        self.assertEqual(len(top_movies), 3)
        # All top 3 should have rating >= 4.5
        self.assertTrue(all(top_movies['rating'] >= 4.5))
    
    def test_genre_preferences(self):
        """Test genre preferences analysis."""
        genres = self.analyzer.get_genre_preferences()
        
        # Check that we have genre data
        self.assertGreater(len(genres), 0)
        # Crime genre should appear most (4 times)
        self.assertIn('Crime', genres.index)
    
    def test_movies_by_year(self):
        """Test year-based analysis."""
        year_stats = self.analyzer.get_movies_by_year()
        
        self.assertEqual(len(year_stats), 5)  # 5 different years
        self.assertIn(1972, year_stats.index)
        self.assertIn(2010, year_stats.index)


class TestDataFrame(unittest.TestCase):
    """Test DataFrame structure."""
    
    def test_empty_dataframe(self):
        """Test analyzer with empty DataFrame."""
        df = pd.DataFrame(columns=['title', 'rating'])
        analyzer = MovieAnalyzer(df)
        stats = analyzer.get_rating_statistics()
        
        # Should handle empty DataFrame gracefully
        self.assertTrue('total_movies' in stats)
        self.assertEqual(stats['total_movies'], 0)


if __name__ == '__main__':
    unittest.main()
