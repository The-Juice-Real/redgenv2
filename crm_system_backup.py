"""
CRM System with Exclusion Logic and User Research
Implements lightweight storage, exclusion tracking, and user profile analysis
"""

import json
import os
import requests
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

class CRMSystem:
    """Lightweight CRM with exclusion logic and user research capabilities"""
    
    def __init__(self):
        self.crm_file = 'crm_data.json'
        self.user_research_cache = 'user_research_cache.json'
        self.crm_data = self.load_crm_data()
        self.research_cache = self.load_research_cache()
        
        # Ensure required keys exist
        if 'saved_leads' not in self.crm_data:
            self.crm_data['saved_leads'] = []
        if 'saved_post_ids' not in self.crm_data:
            self.crm_data['saved_post_ids'] = []
        if 'user_research' not in self.crm_data:
            self.crm_data['user_research'] = {}
        if 'created_at' not in self.crm_data:
            self.crm_data['created_at'] = datetime.now().isoformat()
        if 'last_updated' not in self.crm_data:
            self.crm_data['last_updated'] = datetime.now().isoformat()
    
    def load_crm_data(self) -> Dict[str, Any]:
        """Load CRM data from file"""
        default_data = {
            'saved_leads': [],
            'saved_post_ids': [],
            'user_research': {},
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            with open(self.crm_file, 'r') as f:
                data = json.load(f)
                
                # Handle migration from old format
                if 'leads' in data and 'saved_leads' not in data:
                    # Convert old format to new format
                    old_leads = data.get('leads', {})
                    data['saved_leads'] = []
                    data['saved_post_ids'] = []
                    
                    # Convert old lead format to new simplified format
                    for lead_id, lead_data in old_leads.items():
                        if isinstance(lead_data, dict):
                            simplified_lead = {
                                'id': lead_id,
                                'reddit_username': lead_data.get('contact', {}).get('reddit_username', ''),
                                'post_url': lead_data.get('source_details', {}).get('post_url', ''),
                                'title': lead_data.get('lead_details', {}).get('title', ''),
                                'content': lead_data.get('lead_details', {}).get('content', ''),
                                'lead_score': lead_data.get('lead_details', {}).get('lead_score', 0),
                                'status': lead_data.get('status', 'new'),
                                'user_notes': '',
                                'created_date': lead_data.get('created_date', datetime.now().isoformat()),
                                'last_updated': lead_data.get('last_updated', datetime.now().isoformat())
                            }
                            data['saved_leads'].append(simplified_lead)
                            data['saved_post_ids'].append(lead_id)
                    
                    # Remove old leads structure
                    del data['leads']
                    
                    # Save the migrated data immediately
                    with open(self.crm_file, 'w') as f:
                        json.dump(data, f, indent=2)
                
                # Ensure all required keys exist
                for key in default_data:
                    if key not in data:
                        data[key] = default_data[key]
                        
                return data
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return default_data
    
    def load_research_cache(self) -> Dict[str, Any]:
        """Load user research cache"""
        try:
            with open(self.user_research_cache, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_lead_to_crm(self, post_data: Dict[str, Any], lead_score: float = None,
                        notes: str = "") -> Dict[str, Any]:
        """
        Save lead to CRM with lightweight storage
        Stores only: link, username, post description (text only)
        """
        
        # Extract essential data only
        lead_entry = {
            'id': post_data.get('id'),
            'saved_at': datetime.now().isoformat(),
            'reddit_link': post_data.get('url', ''),
            'username': post_data.get('author', ''),
            'post_title': post_data.get('title', ''),
            'post_description': post_data.get('content', ''),
            'subreddit': post_data.get('subreddit', ''),
            'lead_score': lead_score,
            'user_notes': notes,
            'status': 'new',
            'follow_up_date': None,
            'contacted': False
        }
        
        # Add to CRM data
        self.crm_data['saved_leads'].append(lead_entry)
        
        # Add to exclusion list
        post_id = post_data.get('id')
        if post_id and post_id not in self.crm_data['saved_post_ids']:
            self.crm_data['saved_post_ids'].append(post_id)
        
        # Update metadata
        self.crm_data['last_updated'] = datetime.now().isoformat()
        
        # Save to file
        self.save_crm_data()
        
        return {
            'success': True,
            'lead_id': lead_entry['id'],
            'message': f"Lead saved: {lead_entry['username']} from r/{lead_entry['subreddit']}",
            'exclusion_updated': True
        }
    
    def get_exclusion_list(self) -> List[str]:
        """Get list of post IDs to exclude from search results"""
        return self.crm_data.get('saved_post_ids', [])
    
    # User research functionality removed per user request
    
    def get_all_leads(self) -> List[Dict[str, Any]]:
        """Scrape user's posts and comments from Reddit"""
        
        posts = []
        comments = []
        subreddits = set()
        
        try:
            # Use Reddit's user API endpoint
            user_url = f"https://www.reddit.com/user/{username}.json"
            headers = {'User-Agent': 'CRM-Research/1.0'}
            
            response = requests.get(user_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for item in data.get('data', {}).get('children', []):
                    item_data = item.get('data', {})
                    
                    if item.get('kind') == 't3':  # Post
                        posts.append({
                            'title': item_data.get('title', ''),
                            'content': item_data.get('selftext', ''),
                            'subreddit': item_data.get('subreddit', ''),
                            'score': item_data.get('score', 0),
                            'created_utc': item_data.get('created_utc', 0)
                        })
                        subreddits.add(item_data.get('subreddit', ''))
                    
                    elif item.get('kind') == 't1':  # Comment
                        comments.append({
                            'content': item_data.get('body', ''),
                            'subreddit': item_data.get('subreddit', ''),
                            'score': item_data.get('score', 0),
                            'created_utc': item_data.get('created_utc', 0)
                        })
                        subreddits.add(item_data.get('subreddit', ''))
            
            # Get date range
            all_timestamps = []
            for post in posts:
                if post.get('created_utc'):
                    all_timestamps.append(post['created_utc'])
            for comment in comments:
                if comment.get('created_utc'):
                    all_timestamps.append(comment['created_utc'])
            
            date_range = {}
            if all_timestamps:
                date_range = {
                    'earliest': datetime.fromtimestamp(min(all_timestamps)).isoformat(),
                    'latest': datetime.fromtimestamp(max(all_timestamps)).isoformat()
                }
            
        except Exception as e:
            print(f"Error scraping user {username}: {e}")
        
        return {
            'posts': posts,
            'comments': comments,
            'subreddits': subreddits,
            'date_range': date_range
        }
    
    def _combine_user_content(self, user_content: Dict[str, Any]) -> str:
        """Combine all user posts and comments into single text block"""
        
        combined_parts = []
        
        # Add posts
        for post in user_content['posts']:
            post_text = f"POST in r/{post.get('subreddit', '')}: {post.get('title', '')} - {post.get('content', '')}"
            combined_parts.append(post_text)
        
        # Add comments
        for comment in user_content['comments']:
            comment_text = f"COMMENT in r/{comment.get('subreddit', '')}: {comment.get('content', '')}"
            combined_parts.append(comment_text)
        
        return "\n\n".join(combined_parts)
    
    def _analyze_user_profile(self, combined_text: str, user_content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user profile for interests, needs, and pain points"""
        
        analysis = {
            'business_indicators': self._detect_business_indicators(combined_text),
            'pain_points': self._extract_pain_points(combined_text),
            'interests': self._extract_interests(combined_text, user_content['subreddits']),
            'communication_style': self._analyze_communication_style(combined_text),
            'lead_potential': 0
        }
        
        # Calculate lead potential score
        business_score = len(analysis['business_indicators']) * 20
        pain_point_score = len(analysis['pain_points']) * 15
        activity_score = min(len(user_content['posts']) + len(user_content['comments']), 20)
        
        analysis['lead_potential'] = min(business_score + pain_point_score + activity_score, 100)
        
        return analysis
    
    def _detect_business_indicators(self, text: str) -> Dict[str, List[str]]:
        """Detect business-related indicators in user content"""
        
        text_lower = text.lower()
        indicators = {
            'business_ownership': [],
            'budget_mentions': [],
            'hiring_intent': [],
            'pain_points': [],
            'authority_signals': []
        }
        
        # Business ownership patterns
        ownership_patterns = ['my business', 'my company', 'my startup', 'we run', 'i own', 'ceo', 'founder']
        for pattern in ownership_patterns:
            if pattern in text_lower:
                indicators['business_ownership'].append(pattern)
        
        # Budget patterns
        import re
        budget_patterns = re.findall(r'\$[\d,]+', text)
        indicators['budget_mentions'] = budget_patterns
        
        # Hiring intent
        hiring_patterns = ['looking to hire', 'need help with', 'seeking', 'outsource', 'freelancer']
        for pattern in hiring_patterns:
            if pattern in text_lower:
                indicators['hiring_intent'].append(pattern)
        
        return indicators
    
    def _extract_pain_points(self, text: str) -> List[str]:
        """Extract pain points and problems mentioned by user"""
        
        pain_indicators = [
            'struggling with', 'having trouble', 'difficult to', 'cant figure out',
            'overwhelming', 'time consuming', 'expensive', 'too complex',
            'need help', 'frustrated', 'challenge', 'problem'
        ]
        
        pain_points = []
        sentences = text.split('.')
        
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            for indicator in pain_indicators:
                if indicator in sentence_lower and len(sentence) > 20:
                    pain_points.append(sentence.strip())
                    break
        
        return pain_points[:10]  # Limit to top 10
    
    def _extract_interests(self, text: str, subreddits: set) -> List[str]:
        """Extract interests and topics based on content and subreddits"""
        
        interests = []
        
        # Add subreddits as interests
        business_subreddits = {
            'entrepreneur', 'smallbusiness', 'startups', 'marketing', 'socialmedia',
            'webdev', 'freelance', 'ecommerce', 'advertising', 'sales'
        }
        
        for subreddit in subreddits:
            if subreddit.lower() in business_subreddits:
                interests.append(f"Business: {subreddit}")
            else:
                interests.append(subreddit)
        
        # Extract topic keywords
        topic_keywords = [
            'video editing', 'social media', 'marketing', 'website', 'design',
            'programming', 'photography', 'content creation', 'e-commerce'
        ]
        
        text_lower = text.lower()
        for keyword in topic_keywords:
            if keyword in text_lower:
                interests.append(keyword)
        
        return list(set(interests))[:15]  # Unique interests, limit to 15
    
    def _analyze_communication_style(self, text: str) -> str:
        """Analyze user's communication style"""
        
        if len(text) < 100:
            return "Limited content for analysis"
        
        # Simple analysis based on patterns
        if 'thank you' in text.lower() and 'please' in text.lower():
            return "Polite and professional"
        elif '!' in text and text.count('!') > 5:
            return "Enthusiastic and expressive"
        elif len(text.split()) / len(text.split('.')) > 20:
            return "Detailed and thorough"
        else:
            return "Direct and concise"
    
    def _update_crm_with_research(self, username: str, profile: Dict[str, Any]):
        """Update CRM leads with research data"""
        
        for lead in self.crm_data['saved_leads']:
            if lead.get('username') == username:
                lead['user_research'] = {
                    'researched_at': profile['researched_at'],
                    'lead_potential': profile['lead_potential'],
                    'pain_points_count': len(profile['pain_points']),
                    'business_indicators_count': len(profile['business_indicators']),
                    'interests': profile['interests'][:5]  # Top 5 interests
                }
        
        self.save_crm_data()
    
    def get_all_leads(self) -> List[Dict[str, Any]]:
        """Get all saved leads from CRM"""
        return self.crm_data.get('saved_leads', [])
    
    def update_lead_status(self, lead_id: str, status: str, notes: str = "") -> bool:
        """Update lead status and notes"""
        
        for lead in self.crm_data['saved_leads']:
            if lead.get('id') == lead_id:
                lead['status'] = status
                lead['user_notes'] = notes
                lead['last_updated'] = datetime.now().isoformat()
                self.save_crm_data()
                return True
        
        return False
    
    def delete_lead(self, lead_id: str) -> bool:
        """Delete lead from CRM and remove from exclusion list"""
        
        # Remove from leads
        original_count = len(self.crm_data['saved_leads'])
        self.crm_data['saved_leads'] = [
            lead for lead in self.crm_data['saved_leads'] 
            if lead.get('id') != lead_id
        ]
        
        # Remove from exclusion list
        if lead_id in self.crm_data['saved_post_ids']:
            self.crm_data['saved_post_ids'].remove(lead_id)
        
        if len(self.crm_data['saved_leads']) < original_count:
            self.save_crm_data()
            return True
        
        return False
    
    def get_crm_stats(self) -> Dict[str, Any]:
        """Get CRM statistics and metrics"""
        
        leads = self.crm_data.get('saved_leads', [])
        
        status_counts = defaultdict(int)
        for lead in leads:
            status_counts[lead.get('status', 'unknown')] += 1
        
        return {
            'total_leads': len(leads),
            'status_breakdown': dict(status_counts),
            'exclusion_list_size': len(self.crm_data.get('saved_post_ids', [])),
            'last_updated': self.crm_data.get('last_updated', ''),
            'research_cache_size': len(self.research_cache),
            'top_subreddits': self._get_top_subreddits(leads)
        }
    
    def _get_top_subreddits(self, leads: List[Dict[str, Any]]) -> List[Dict[str, int]]:
        """Get top subreddits by lead count"""
        
        subreddit_counts = defaultdict(int)
        for lead in leads:
            subreddit = lead.get('subreddit', '')
            if subreddit:
                subreddit_counts[subreddit] += 1
        
        return [
            {'subreddit': sub, 'count': count}
            for sub, count in sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
    
    def save_crm_data(self):
        """Save CRM data to file"""
        try:
            with open(self.crm_file, 'w') as f:
                json.dump(self.crm_data, f, indent=2)
        except Exception as e:
            print(f"Error saving CRM data: {e}")
    
    def save_research_cache(self):
        """Save research cache to file"""
        try:
            with open(self.user_research_cache, 'w') as f:
                json.dump(self.research_cache, f, indent=2)
        except Exception as e:
            print(f"Error saving research cache: {e}")