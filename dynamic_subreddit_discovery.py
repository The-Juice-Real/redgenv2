"""
Dynamic Subreddit Discovery System
Combines AI-powered analysis with Reddit's native search capabilities
"""

import os
import re
import json
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import time

class DynamicSubredditDiscovery:
    """Intelligent subreddit discovery using AI + Reddit Search API"""
    
    def __init__(self):
        self.perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
        self.discovery_cache = {}
        self.reddit_cache = {}
        
        # Community quality thresholds
        self.min_subscribers = 500
        self.min_activity_score = 0.1
        
    def discover_optimal_subreddits(self, service_description: str, max_subreddits: int = 15) -> Dict[str, Any]:
        """
        Main discovery function combining AI analysis and Reddit search
        """
        print(f"🔍 Discovering optimal subreddits for: {service_description}")
        
        # Step 1: AI-powered service analysis
        service_analysis = self._analyze_service_with_ai(service_description)
        
        # Step 2: Reddit native subreddit discovery
        reddit_communities = self._discover_reddit_communities(service_analysis)
        
        # Step 3: Combine and optimize results
        optimized_strategy = self._create_optimized_strategy(
            service_analysis, reddit_communities, max_subreddits
        )
        
        print(f"✅ Found {len(optimized_strategy['subreddits'])} optimal communities")
        return optimized_strategy
    
    def _analyze_service_with_ai(self, service_description: str) -> Dict[str, Any]:
        """Use AI to analyze service and extract targeting intelligence"""
        
        cache_key = f"ai_analysis_{hash(service_description)}"
        if cache_key in self.discovery_cache:
            return self.discovery_cache[cache_key]
        
        if not self.perplexity_api_key:
            return self._fallback_service_analysis(service_description)
        
        prompt = f"""
        Analyze this service request for Reddit lead generation targeting:
        
        Service: "{service_description}"
        
        Provide a JSON response with:
        1. primary_service: Main service category
        2. industry_vertical: Specific industry/niche
        3. target_keywords: List of 15-20 relevant search keywords
        4. subreddit_suggestions: List of 25-30 relevant subreddit names (without r/)
        5. urgency_indicators: Phrases that indicate urgency
        6. budget_signals: Phrases that indicate budget/investment readiness
        7. search_strategies: Different approaches to find leads
        
        Focus on active, business-oriented communities where people discuss real problems and seek solutions.
        Include both obvious and non-obvious subreddits (e.g., for video editing: not just r/VideoEditing but also r/YouTubeCreators, r/SmallBusiness, r/Podcasting)
        """
        
        try:
            response = requests.post(
                'https://api.perplexity.ai/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.perplexity_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'llama-3.1-sonar-small-128k-online',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'temperature': 0.3,
                    'max_tokens': 2000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                    self.discovery_cache[cache_key] = analysis
                    return analysis
                    
        except Exception as e:
            print(f"⚠️ AI analysis failed: {e}")
        
        return self._fallback_service_analysis(service_description)
    
    def _discover_reddit_communities(self, service_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Discover Reddit communities using multiple search strategies"""
        
        all_communities = []
        keywords = service_analysis.get('target_keywords', [])
        suggested_subreddits = service_analysis.get('subreddit_suggestions', [])
        
        # Strategy 1: Direct subreddit name validation
        validated_subreddits = self._validate_subreddit_names(suggested_subreddits)
        all_communities.extend(validated_subreddits)
        
        # Strategy 2: Keyword-based subreddit discovery
        keyword_communities = self._search_subreddits_by_keywords(keywords[:10])
        all_communities.extend(keyword_communities)
        
        # Strategy 3: Related community discovery
        related_communities = self._find_related_communities(validated_subreddits[:5])
        all_communities.extend(related_communities)
        
        # Remove duplicates and score communities
        unique_communities = self._deduplicate_and_score_communities(all_communities)
        
        return sorted(unique_communities, key=lambda x: x['score'], reverse=True)
    
    def _validate_subreddit_names(self, subreddit_names: List[str]) -> List[Dict[str, Any]]:
        """Validate that suggested subreddit names actually exist and are active"""
        
        validated = []
        
        for subreddit in subreddit_names:
            if not subreddit:
                continue
                
            # Clean subreddit name
            clean_name = subreddit.lower().replace('r/', '').strip()
            
            try:
                # Check if subreddit exists using Reddit's JSON API
                url = f"https://www.reddit.com/r/{clean_name}/about.json"
                headers = {'User-Agent': 'LeadDiscovery/1.0'}
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    subreddit_data = data.get('data', {})
                    
                    subscribers = subreddit_data.get('subscribers', 0)
                    if subscribers >= self.min_subscribers:
                        validated.append({
                            'name': clean_name,
                            'subscribers': subscribers,
                            'score': min(subscribers / 10000, 10),  # Cap at 10
                            'source': 'ai_suggested',
                            'description': subreddit_data.get('public_description', ''),
                            'active_users': subreddit_data.get('active_user_count', 0)
                        })
                
                time.sleep(0.1)  # Rate limiting
                
            except Exception:
                continue
        
        return validated
    
    def _search_subreddits_by_keywords(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Search for subreddits using keywords via Reddit search"""
        
        found_communities = []
        
        for keyword in keywords[:5]:  # Limit to avoid rate limits
            try:
                # Use Reddit search API
                url = f"https://www.reddit.com/subreddits/search.json"
                params = {
                    'q': keyword,
                    'type': 'sr',
                    'limit': 10
                }
                headers = {'User-Agent': 'LeadDiscovery/1.0'}
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for item in data.get('data', {}).get('children', []):
                        subreddit_data = item.get('data', {})
                        subscribers = subreddit_data.get('subscribers', 0)
                        
                        if subscribers >= self.min_subscribers:
                            found_communities.append({
                                'name': subreddit_data.get('display_name', '').lower(),
                                'subscribers': subscribers,
                                'score': min(subscribers / 20000, 8),  # Lower score for search results
                                'source': 'keyword_search',
                                'description': subreddit_data.get('public_description', ''),
                                'keyword_match': keyword
                            })
                
                time.sleep(0.2)  # Rate limiting
                
            except Exception:
                continue
        
        return found_communities
    
    def _find_related_communities(self, seed_subreddits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find related communities based on seed subreddits"""
        
        related = []
        
        for subreddit in seed_subreddits:
            try:
                # Get subreddit sidebar info which often contains related communities
                url = f"https://www.reddit.com/r/{subreddit['name']}/about.json"
                headers = {'User-Agent': 'LeadDiscovery/1.0'}
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    description = data.get('data', {}).get('description', '')
                    
                    # Extract subreddit mentions from description
                    subreddit_mentions = re.findall(r'r/([a-zA-Z0-9_]+)', description)
                    
                    for mentioned in subreddit_mentions[:5]:  # Limit to 5 per subreddit
                        if mentioned.lower() not in [s['name'] for s in seed_subreddits]:
                            # Quick validation
                            validation_result = self._validate_subreddit_names([mentioned])
                            if validation_result:
                                related.extend(validation_result)
                
                time.sleep(0.1)
                
            except Exception:
                continue
        
        return related
    
    def _deduplicate_and_score_communities(self, communities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicates and enhance scoring"""
        
        seen_names = set()
        unique_communities = []
        
        for community in communities:
            name = community['name'].lower()
            if name not in seen_names:
                seen_names.add(name)
                
                # Enhance scoring based on multiple factors
                base_score = community.get('score', 1)
                
                # Boost for high activity
                if community.get('active_users', 0) > 100:
                    base_score *= 1.2
                
                # Boost for business-oriented keywords in description
                description = community.get('description', '').lower()
                business_keywords = ['business', 'professional', 'industry', 'commercial', 'service']
                for keyword in business_keywords:
                    if keyword in description:
                        base_score *= 1.1
                        break
                
                community['final_score'] = base_score
                unique_communities.append(community)
        
        return unique_communities
    
    def _create_optimized_strategy(self, service_analysis: Dict[str, Any], 
                                 communities: List[Dict[str, Any]], 
                                 max_subreddits: int) -> Dict[str, Any]:
        """Create optimized search strategy from discovered data with robust fallbacks"""
        
        # Select top communities
        top_communities = communities[:max_subreddits]
        subreddit_names = [c['name'] for c in top_communities]
        
        # If no communities found, use AI-suggested subreddits as fallback
        if not subreddit_names:
            ai_suggested = service_analysis.get('subreddit_suggestions', [])
            if ai_suggested:
                subreddit_names = ai_suggested[:max_subreddits]
            
            # Service-specific fallbacks if AI suggestions also empty
            service_type = service_analysis.get('primary_service', '').lower()
            if not subreddit_names:
                if 'website' in service_type or 'web' in service_type:
                    subreddit_names = [
                        'smallbusiness', 'entrepreneur', 'startups', 'business', 'webdev',
                        'web_design', 'WordPress', 'shopify', 'freelance', 'digitalmarketing'
                    ][:max_subreddits]
                elif 'video' in service_type:
                    subreddit_names = [
                        'videoediting', 'youtubers', 'contentcreators', 'filmmakers', 'entrepreneur'
                    ][:max_subreddits]
                elif 'manufacturing' in service_type:
                    subreddit_names = [
                        'manufacturing', 'entrepreneur', 'business', 'startups', 'hardware'
                    ][:max_subreddits]
                else:
                    subreddit_names = ['entrepreneur', 'smallbusiness', 'business', 'startups'][:max_subreddits]
        
        return {
            'subreddits': subreddit_names,
            'search_terms': service_analysis.get('target_keywords', [])[:20],
            'urgency_patterns': service_analysis.get('urgency_indicators', []),
            'budget_patterns': service_analysis.get('budget_signals', []),
            'min_score': 25,  # Dynamic based on service complexity
            'target_tiers': ['Platinum', 'Gold', 'Silver', 'Bronze'],
            'discovery_metadata': {
                'primary_service': service_analysis.get('primary_service', ''),
                'industry_vertical': service_analysis.get('industry_vertical', ''),
                'total_communities_found': len(communities),
                'community_sources': self._analyze_community_sources(top_communities),
                'average_community_size': sum(c.get('subscribers', 0) for c in top_communities) // len(top_communities) if top_communities else 0,
                'used_fallback_subreddits': len(communities) == 0
            }
        }
    
    def _analyze_community_sources(self, communities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze sources of discovered communities"""
        sources = {}
        for community in communities:
            source = community.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        return sources
    
    def _fallback_service_analysis(self, service_description: str) -> Dict[str, Any]:
        """Fallback analysis when AI is unavailable"""
        
        desc_lower = service_description.lower()
        
        # Website development services
        if any(word in desc_lower for word in ['website', 'web', 'local business', 'site', 'online']):
            return {
                'primary_service': 'website development',
                'industry_vertical': 'web development',
                'target_keywords': [
                    'website development', 'web design', 'local business website', 'small business website',
                    'wordpress', 'shopify', 'ecommerce website', 'business website', 'online presence',
                    'website designer', 'web developer', 'responsive website', 'mobile website'
                ],
                'subreddit_suggestions': [
                    'smallbusiness', 'entrepreneur', 'startups', 'business', 'LocalBusiness',
                    'webdev', 'web_design', 'WordPress', 'shopify', 'freelance',
                    'restaurantowners', 'realestate', 'fitness', 'healthcare', 'legal'
                ],
                'urgency_indicators': ['website urgently needed', 'website asap', 'business opening soon', 'website down'],
                'budget_signals': ['website budget', 'web development cost', 'website investment', 'affordable website']
            }
        
        # Video editing services
        elif any(word in desc_lower for word in ['video', 'edit', 'youtube', 'content']):
            return {
                'primary_service': 'video editing',
                'industry_vertical': 'content creation',
                'target_keywords': ['video editing', 'youtube', 'content creation', 'video production'],
                'subreddit_suggestions': ['videoediting', 'youtubers', 'contentcreators', 'filmmakers'],
                'urgency_indicators': ['urgent', 'asap', 'deadline', 'rush'],
                'budget_signals': ['budget', 'pay', 'cost', 'price', 'investment']
            }
        
        # Manufacturing services
        elif any(word in desc_lower for word in ['manufacturing', 'production', 'supplier', 'factory']):
            return {
                'primary_service': 'manufacturing',
                'industry_vertical': 'manufacturing',
                'target_keywords': ['manufacturing', 'production', 'supplier', 'factory', 'sourcing'],
                'subreddit_suggestions': ['manufacturing', 'entrepreneur', 'business', 'startups'],
                'urgency_indicators': ['urgent production', 'manufacturing asap', 'supplier needed'],
                'budget_signals': ['manufacturing budget', 'production cost', 'supplier pricing']
            }
        
        # General business fallback
        else:
            words = desc_lower.split()
            return {
                'primary_service': 'general business service',
                'industry_vertical': 'business',
                'target_keywords': words + ['business service', 'entrepreneur', 'small business'],
                'subreddit_suggestions': ['entrepreneur', 'smallbusiness', 'business', 'startups'],
                'urgency_indicators': ['urgent', 'asap', 'deadline'],
                'budget_signals': ['budget', 'pay', 'cost', 'price']
            }