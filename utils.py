import pandas as pd
import re
import json
from typing import Any, Dict, List
from datetime import datetime
import streamlit as st

def format_text_preview(text: str, max_length: int = 200) -> str:
    """
    Format text for preview display
    
    Args:
        text: Text to format
        max_length: Maximum length of preview
        
    Returns:
        Formatted preview text
    """
    if not text:
        return "No content available"
    
    # Clean text
    text = clean_text(text)
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text

def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and special characters
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
    text = re.sub(r'~~(.*?)~~', r'\1', text)      # Strikethrough
    
    # Remove Reddit formatting
    text = re.sub(r'/u/\w+', '[username]', text)  # Username mentions
    text = re.sub(r'/r/\w+', '[subreddit]', text) # Subreddit mentions
    text = re.sub(r'https?://\S+', '[link]', text) # URLs
    
    # Remove excessive punctuation
    text = re.sub(r'[!]{2,}', '!', text)
    text = re.sub(r'[?]{2,}', '?', text)
    text = re.sub(r'[.]{3,}', '...', text)
    
    return text.strip()

def export_to_csv(df: pd.DataFrame, content_type: str) -> str:
    """
    Export DataFrame to CSV format
    
    Args:
        df: DataFrame to export
        content_type: Type of content ('posts' or 'comments')
        
    Returns:
        CSV string
    """
    try:
        # Select relevant columns for export
        if content_type == 'posts':
            export_columns = [
                'title', 'content', 'url', 'score', 'num_comments',
                'sentiment_score', 'sentiment_label', 'topics', 'intent',
                'relevance_score', 'created_utc', 'author', 'entities'
            ]
        else:  # comments
            export_columns = [
                'content', 'score', 'sentiment_score', 'sentiment_label',
                'topics', 'intent', 'relevance_score', 'created_utc',
                'author', 'post_id'
            ]
        
        # Filter columns that exist in the DataFrame
        available_columns = [col for col in export_columns if col in df.columns]
        export_df = df[available_columns].copy()
        
        # Convert list columns to strings
        for col in export_df.columns:
            if export_df[col].dtype == 'object':
                export_df[col] = export_df[col].apply(
                    lambda x: str(x) if isinstance(x, (list, dict)) else x
                )
        
        return export_df.to_csv(index=False)
        
    except Exception as e:
        st.error(f"Error exporting to CSV: {e}")
        return ""

def format_datetime(dt: datetime) -> str:
    """
    Format datetime for display
    
    Args:
        dt: Datetime object
        
    Returns:
        Formatted datetime string
    """
    if not dt:
        return "Unknown"
    
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_summary_stats(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate summary statistics for analyzed data
    
    Args:
        data: List of analyzed content dictionaries
        
    Returns:
        Summary statistics dictionary
    """
    if not data:
        return {}
    
    df = pd.DataFrame(data)
    
    stats = {
        'total_items': len(data),
        'avg_sentiment': df['sentiment_score'].mean() if 'sentiment_score' in df.columns else 0,
        'avg_relevance': df['relevance_score'].mean() if 'relevance_score' in df.columns else 0,
        'most_common_intent': df['intent'].mode().iloc[0] if 'intent' in df.columns and len(df['intent'].mode()) > 0 else 'unknown',
        'sentiment_distribution': df['sentiment_label'].value_counts().to_dict() if 'sentiment_label' in df.columns else {},
        'intent_distribution': df['intent'].value_counts().to_dict() if 'intent' in df.columns else {}
    }
    
    return stats

def extract_top_keywords(texts: List[str], top_n: int = 20) -> List[tuple]:
    """
    Extract top keywords from a list of texts
    
    Args:
        texts: List of text strings
        top_n: Number of top keywords to return
        
    Returns:
        List of (keyword, frequency) tuples
    """
    try:
        from collections import Counter
        import re
        
        # Combine all texts
        combined_text = ' '.join(texts).lower()
        
        # Extract words (removing common stop words)
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among', 'throughout',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
            'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
            'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his',
            'her', 'its', 'our', 'their'
        }
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', combined_text)
        words = [word for word in words if word not in stop_words]
        
        # Count frequencies
        word_freq = Counter(words)
        
        return word_freq.most_common(top_n)
        
    except Exception as e:
        return []

def format_score_display(score: float, score_type: str = "general") -> str:
    """
    Format scores for display with appropriate emoji and description
    
    Args:
        score: Numerical score
        score_type: Type of score ('sentiment', 'relevance', 'general')
        
    Returns:
        Formatted score string
    """
    if score_type == "sentiment":
        if score > 0.5:
            return f"😊 {score:.2f} (Positive)"
        elif score < -0.5:
            return f"😞 {score:.2f} (Negative)"
        else:
            return f"😐 {score:.2f} (Neutral)"
    
    elif score_type == "relevance":
        if score > 0.7:
            return f"🎯 {score:.2f} (Highly Relevant)"
        elif score > 0.4:
            return f"📌 {score:.2f} (Moderately Relevant)"
        else:
            return f"📍 {score:.2f} (Low Relevance)"
    
    else:
        return f"{score:.2f}"

def create_word_frequency_data(texts: List[str]) -> pd.DataFrame:
    """
    Create word frequency data for visualization
    
    Args:
        texts: List of text strings
        
    Returns:
        DataFrame with word frequency data
    """
    keywords = extract_top_keywords(texts, top_n=30)
    
    if not keywords:
        return pd.DataFrame(columns=['word', 'frequency'])
    
    return pd.DataFrame(keywords, columns=['word', 'frequency'])

def validate_subreddit_name(subreddit_name: str) -> bool:
    """
    Validate subreddit name format
    
    Args:
        subreddit_name: Name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not subreddit_name:
        return False
    
    # Remove r/ prefix if present
    if subreddit_name.startswith('r/'):
        subreddit_name = subreddit_name[2:]
    
    # Check format: alphanumeric and underscores, 3-21 characters
    pattern = r'^[A-Za-z0-9_]{3,21}$'
    return bool(re.match(pattern, subreddit_name))

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file export
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename

def parse_reddit_url(url: str) -> Dict[str, str]:
    """
    Parse Reddit URL to extract components
    
    Args:
        url: Reddit URL
        
    Returns:
        Dictionary with URL components
    """
    try:
        # Extract subreddit and post ID from URL
        pattern = r'reddit\.com/r/(\w+)/comments/(\w+)'
        match = re.search(pattern, url)
        
        if match:
            return {
                'subreddit': match.group(1),
                'post_id': match.group(2),
                'is_valid': True
            }
        else:
            return {'is_valid': False}
            
    except Exception as e:
        return {'is_valid': False, 'error': str(e)}

def format_large_number(number: int) -> str:
    """
    Format large numbers for display (e.g., 1.2K, 1.5M)
    
    Args:
        number: Number to format
        
    Returns:
        Formatted number string
    """
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(number)

def get_time_ago(dt: datetime) -> str:
    """
    Get human-readable time difference
    
    Args:
        dt: Datetime object
        
    Returns:
        Time ago string
    """
    try:
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"
            
    except Exception as e:
        return "Unknown time"
