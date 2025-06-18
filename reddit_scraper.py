import praw
import os
from datetime import datetime
import time
import streamlit as st
from typing import Dict, List, Any

class RedditScraper:
    """Reddit scraper using PRAW to fetch posts and comments"""
    
    def __init__(self):
        """Initialize Reddit API connection"""
        # Reddit configuration - using provided credentials
        self.reddit_config = {
            'client_id': os.getenv('REDDIT_CLIENT_ID', 'iuRk8bamt7Zj6Vi4uPwr5Q'),
            'client_secret': os.getenv('REDDIT_CLIENT_SECRET', 'bhrgHoMkQONKvT9zGaETC8i4iZYjRg'),
            'user_agent': os.getenv('REDDIT_USER_AGENT', 'Tom')
        }
        
        try:
            self.reddit = praw.Reddit(
                client_id=self.reddit_config['client_id'],
                client_secret=self.reddit_config['client_secret'],
                user_agent=self.reddit_config['user_agent']
            )
            # Test the connection
            self.reddit.user.me()
        except Exception as e:
            # If authenticated user fails, continue with read-only access
            self.reddit = praw.Reddit(
                client_id=self.reddit_config['client_id'],
                client_secret=self.reddit_config['client_secret'],
                user_agent=self.reddit_config['user_agent']
            )
    
    def scrape_subreddit(self, subreddit_name: str, limit: int = 100, 
                        include_comments: bool = True, max_comments_per_post: int = 20) -> Dict[str, List[Any]]:
        """
        Scrape posts and comments from a specified subreddit
        
        Args:
            subreddit_name: Name of the subreddit to scrape
            limit: Number of posts to scrape
            include_comments: Whether to include comments
            max_comments_per_post: Maximum comments to scrape per post
            
        Returns:
            Dictionary containing posts and comments data
        """
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            posts_data = []
            comments_data = []
            
            # Fetch most recent posts (new posts sorted by recency)
            posts = list(subreddit.new(limit=limit))
            
            for i, post in enumerate(posts):
                # Update progress
                if i % 10 == 0:
                    progress = min(90, (i / len(posts)) * 90)  # Max 90% for scraping
                    st.sidebar.write(f"Processing post {i+1}/{len(posts)}")
                
                try:
                    # Extract post data
                    post_data = {
                        'id': post.id,
                        'title': post.title,
                        'content': post.selftext or post.title,  # Use title if no selftext
                        'url': f"https://reddit.com{post.permalink}",
                        'score': post.score,
                        'upvote_ratio': post.upvote_ratio,
                        'num_comments': post.num_comments,
                        'created_utc': datetime.fromtimestamp(post.created_utc),
                        'author': str(post.author) if post.author else '[deleted]',
                        'subreddit': str(post.subreddit),
                        'flair': post.link_flair_text,
                        'is_video': post.is_video,
                        'is_self': post.is_self,
                        'domain': post.domain
                    }
                    
                    posts_data.append(post_data)
                    
                    # Scrape comments if requested
                    if include_comments and post.num_comments > 0:
                        comments = self._scrape_post_comments(post, max_comments_per_post)
                        comments_data.extend(comments)
                    
                    # Rate limiting to avoid hitting API limits
                    time.sleep(0.1)
                    
                except Exception as e:
                    st.sidebar.warning(f"Error processing post {post.id}: {str(e)}")
                    continue
            
            return {
                'posts': posts_data,
                'comments': comments_data,
                'scraped_at': datetime.now(),
                'subreddit': subreddit_name,
                'total_posts': len(posts_data),
                'total_comments': len(comments_data)
            }
            
        except Exception as e:
            # Handle 404 and other errors gracefully
            error_msg = str(e).lower()
            if '404' in error_msg or 'not found' in error_msg or 'private' in error_msg:
                return {
                    'posts': [],
                    'comments': [],
                    'scraped_at': datetime.now(),
                    'subreddit': subreddit_name,
                    'total_posts': 0,
                    'total_comments': 0,
                    'error': f"Subreddit r/{subreddit_name} not accessible"
                }
            else:
                raise Exception(f"Error scraping subreddit r/{subreddit_name}: {str(e)}")
    
    def _scrape_post_comments(self, post, max_comments: int) -> List[Dict[str, Any]]:
        """
        Scrape comments from a specific post
        
        Args:
            post: Reddit post object
            max_comments: Maximum number of comments to scrape
            
        Returns:
            List of comment dictionaries
        """
        
        comments_data = []
        
        try:
            # Expand all comments
            post.comments.replace_more(limit=0)
            
            comment_count = 0
            for comment in post.comments.list():
                if comment_count >= max_comments:
                    break
                
                try:
                    # Skip deleted/removed comments
                    if comment.body in ['[deleted]', '[removed]']:
                        continue
                    
                    comment_data = {
                        'id': comment.id,
                        'post_id': post.id,
                        'content': comment.body,
                        'score': comment.score,
                        'created_utc': datetime.fromtimestamp(comment.created_utc),
                        'author': str(comment.author) if comment.author else '[deleted]',
                        'parent_id': comment.parent_id,
                        'is_submitter': comment.is_submitter,
                        'depth': comment.depth if hasattr(comment, 'depth') else 0,
                        'permalink': f"https://reddit.com{comment.permalink}"
                    }
                    
                    comments_data.append(comment_data)
                    comment_count += 1
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            st.sidebar.warning(f"Error scraping comments for post {post.id}: {str(e)}")
        
        return comments_data
    
    def search_subreddit(self, subreddit_name: str, query: str, limit: int = 50, max_comments_per_post: int = 20) -> Dict[str, List[Any]]:
        """
        Search for specific content within a subreddit, including both posts and comments
        
        Args:
            subreddit_name: Name of the subreddit
            query: Search query
            limit: Number of results to return
            max_comments_per_post: Maximum comments to scrape per post
            
        Returns:
            Dictionary containing search results with both posts and comments
        """
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts_data = []
            comments_data = []
            
            # Search within the subreddit, sorted by most recent
            # Add time restriction to get only recent posts (last 30 days)
            search_results = list(subreddit.search(query, limit=limit, sort='new', time_filter='month'))
            
            for post in search_results:
                try:
                    post_data = {
                        'id': post.id,
                        'title': post.title,
                        'content': post.selftext or post.title,
                        'url': f"https://reddit.com{post.permalink}",
                        'score': post.score,
                        'upvote_ratio': post.upvote_ratio,
                        'num_comments': post.num_comments,
                        'created_utc': datetime.fromtimestamp(post.created_utc),
                        'author': str(post.author) if post.author else '[deleted]',
                        'subreddit': str(post.subreddit),
                        'post_id': post.id
                    }
                    
                    posts_data.append(post_data)
                    
                    # Also scrape comments from this post
                    if max_comments_per_post > 0:
                        post_comments = self._scrape_post_comments(post, max_comments_per_post)
                        comments_data.extend(post_comments)
                    
                except Exception as e:
                    continue
            
            return {
                'posts': posts_data,
                'comments': comments_data,
                'query': query,
                'subreddit': subreddit_name,
                'total_results': len(posts_data),
                'total_comments': len(comments_data)
            }
            
        except Exception as e:
            # Handle 404 and other errors gracefully - return empty results instead of failing
            error_msg = str(e).lower()
            if '404' in error_msg or 'not found' in error_msg or 'private' in error_msg:
                return {
                    'posts': [],
                    'comments': [],
                    'query': query, 
                    'subreddit': subreddit_name,
                    'total_results': 0,
                    'total_comments': 0,
                    'error': f"Subreddit r/{subreddit_name} not accessible"
                }
            else:
                raise Exception(f"Error searching r/{subreddit_name} for '{query}': {str(e)}")
    
    def get_subreddit_info(self, subreddit_name: str) -> Dict[str, Any]:
        """
        Get basic information about a subreddit
        
        Args:
            subreddit_name: Name of the subreddit
            
        Returns:
            Dictionary containing subreddit information
        """
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            return {
                'name': subreddit.display_name,
                'title': subreddit.title,
                'description': subreddit.public_description,
                'subscribers': subreddit.subscribers,
                'created_utc': datetime.fromtimestamp(subreddit.created_utc),
                'over18': subreddit.over18,
                'active_users': subreddit.active_user_count
            }
            
        except Exception as e:
            raise Exception(f"Error getting info for r/{subreddit_name}: {str(e)}")
