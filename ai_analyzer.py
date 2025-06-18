import os
import json
import re
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import streamlit as st
import requests
import hashlib
import time

class AIAnalyzer:
    """Advanced AI analyzer with sophisticated credit optimization strategies"""
    
    def __init__(self):
        """Initialize with aggressive credit conservation measures"""
        self.perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
        self.perplexity_base_url = "https://api.perplexity.ai/chat/completions"
        
        # Credit optimization settings
        self.api_call_count = 0
        self.max_api_calls = 12  # Conservative limit for $5 budget
        self.cache = {}  # Persistent cache to avoid duplicate calls
        self.batch_cache = {}  # Cache for batch processing
        
        # Advanced patterns for high-accuracy fallbacks
        self._initialize_advanced_patterns()
        
        # Track API efficiency
        self.successful_api_calls = 0
        self.cache_hits = 0
    
    def _initialize_advanced_patterns(self):
        """Initialize sophisticated pattern recognition systems"""
        
        # Advanced sentiment lexicon with weights
        self.sentiment_lexicon = {
            'extremely_positive': {'weight': 1.0, 'words': ['amazing', 'incredible', 'outstanding', 'exceptional', 'phenomenal', 'brilliant', 'perfect', 'flawless']},
            'positive': {'weight': 0.7, 'words': ['good', 'great', 'excellent', 'awesome', 'fantastic', 'wonderful', 'nice', 'helpful', 'useful', 'works', 'solved', 'fixed']},
            'moderately_positive': {'weight': 0.4, 'words': ['okay', 'decent', 'fine', 'acceptable', 'reasonable', 'satisfactory']},
            'neutral': {'weight': 0.0, 'words': ['maybe', 'perhaps', 'possibly', 'might', 'could']},
            'moderately_negative': {'weight': -0.4, 'words': ['disappointing', 'mediocre', 'poor', 'lacking', 'insufficient']},
            'negative': {'weight': -0.7, 'words': ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'broken', 'useless', 'failed', 'error', 'problem', 'issue', 'bug']},
            'extremely_negative': {'weight': -1.0, 'words': ['catastrophic', 'disastrous', 'abysmal', 'appalling', 'disgusting', 'revolting']}
        }
        
        # Sophisticated intent detection patterns
        self.intent_patterns = {
            'technical_help_seeking': {
                'patterns': [r'how\s+(?:do\s+i|to)', r'can\s+(?:someone|anyone)\s+help', r'need\s+help\s+with', r'stuck\s+on', r'error\s+when', r'problem\s+with'],
                'keywords': ['help', 'stuck', 'error', 'problem', 'issue', 'broken', 'not working', 'debug', 'fix'],
                'weight': 0.9
            },
            'advice_seeking': {
                'patterns': [r'should\s+i', r'what\s+do\s+you\s+think', r'any\s+(?:advice|suggestions)', r'recommend(?:ations?)?'],
                'keywords': ['advice', 'recommend', 'suggestion', 'opinion', 'thoughts', 'feedback'],
                'weight': 0.8
            },
            'information_sharing': {
                'patterns': [r'(?:fyi|for\s+your\s+information)', r'just\s+(?:found|discovered)', r'sharing\s+this', r'heads\s+up'],
                'keywords': ['fyi', 'sharing', 'found', 'discovered', 'news', 'update', 'announcement'],
                'weight': 0.7
            },
            'question_asking': {
                'patterns': [r'\?\s*$', r'^(?:what|how|why|when|where|who|which)', r'anyone\s+know'],
                'keywords': ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'question'],
                'weight': 0.8
            },
            'solution_providing': {
                'patterns': [r'(?:try|use)\s+this', r'here[\'s\s]+(?:how|what)', r'solution\s+is', r'fixed\s+by'],
                'keywords': ['solution', 'fix', 'solved', 'answer', 'try this', 'here is how'],
                'weight': 0.9
            },
            'experience_sharing': {
                'patterns': [r'i\s+(?:had|experienced|tried)', r'in\s+my\s+experience', r'when\s+i\s+(?:was|did)'],
                'keywords': ['experience', 'tried', 'when i', 'happened to me', 'i had'],
                'weight': 0.6
            },
            'complaint_expression': {
                'patterns': [r'(?:hate|can\'t\s+stand)', r'(?:terrible|awful|horrible)', r'worst\s+(?:thing|experience)'],
                'keywords': ['hate', 'terrible', 'awful', 'horrible', 'worst', 'frustrated', 'annoyed'],
                'weight': 0.8
            },
            'praise_expression': {
                'patterns': [r'(?:love|adore)\s+this', r'(?:amazing|incredible|fantastic)', r'best\s+(?:thing|feature)'],
                'keywords': ['love', 'amazing', 'incredible', 'fantastic', 'best', 'brilliant', 'excellent'],
                'weight': 0.8
            }
        }
        
        # Topic classification with domain expertise
        self.topic_domains = {
            'programming': {
                'primary': ['code', 'programming', 'development', 'coding', 'software', 'algorithm', 'function', 'variable', 'debug'],
                'secondary': ['github', 'api', 'database', 'framework', 'library', 'script', 'compile', 'syntax'],
                'languages': ['python', 'javascript', 'java', 'c++', 'react', 'node', 'html', 'css', 'sql']
            },
            'career': {
                'primary': ['job', 'career', 'work', 'employment', 'salary', 'interview', 'resume', 'hiring'],
                'secondary': ['manager', 'promotion', 'workplace', 'colleague', 'professional', 'industry'],
                'contexts': ['remote work', 'job search', 'career change', 'interview tips']
            },
            'technology': {
                'primary': ['tech', 'technology', 'digital', 'computer', 'device', 'software', 'hardware', 'system'],
                'secondary': ['innovation', 'startup', 'ai', 'machine learning', 'cloud', 'cybersecurity'],
                'trends': ['blockchain', 'cryptocurrency', 'metaverse', 'iot', 'quantum']
            },
            'education': {
                'primary': ['learn', 'study', 'education', 'course', 'tutorial', 'lesson', 'teaching', 'student'],
                'secondary': ['university', 'college', 'degree', 'certification', 'skill', 'knowledge'],
                'platforms': ['coursera', 'udemy', 'khan academy', 'edx', 'online learning']
            },
            'gaming': {
                'primary': ['game', 'gaming', 'play', 'player', 'gameplay', 'level', 'character', 'quest'],
                'secondary': ['console', 'pc gaming', 'mobile gaming', 'multiplayer', 'single player'],
                'genres': ['rpg', 'fps', 'strategy', 'puzzle', 'indie', 'aaa']
            }
        }
    
    def analyze_reddit_data(self, reddit_data: Dict, search_topic: str) -> Dict[str, Any]:
        """Analyze Reddit data with maximum accuracy and minimal API usage"""
        
        analyzed_posts = []
        analyzed_comments = []
        
        # Generate intelligent topic categories
        topic_categories = self._generate_intelligent_topic_categories(search_topic)
        
        st.sidebar.write("🧠 Analyzing with advanced AI (credit-optimized)...")
        
        # Pre-analysis: Score all content for relevance
        posts_with_scores = self._pre_score_content(reddit_data['posts'], search_topic, 'post')
        comments_with_scores = self._pre_score_content(reddit_data['comments'], search_topic, 'comment')
        
        # Strategic API allocation: Use API for highest-value content
        high_value_posts = [item for item, score in posts_with_scores if score > 0.6][:5]
        medium_value_posts = [item for item, score in posts_with_scores if 0.3 <= score <= 0.6][:10]
        
        # Batch process high-value content with API
        api_enhanced_posts = self._batch_process_with_api(high_value_posts, search_topic, topic_categories, 'post')
        
        # Process all posts with hybrid approach
        for i, post in enumerate(reddit_data['posts']):
            post_id = post.get('id', str(hash(str(post))))
            if post_id in api_enhanced_posts:
                analyzed_post = api_enhanced_posts[post_id]
            else:
                use_advanced_rules = post in [item for item, _ in posts_with_scores[:20]]
                analyzed_post = self._analyze_single_content_hybrid(
                    post, search_topic, topic_categories, 'post', use_advanced_rules
                )
            
            analyzed_posts.append(analyzed_post)
            
            if i % 10 == 0:
                st.sidebar.write(f"Processed {i+1}/{len(reddit_data['posts'])} posts")
        
        # Process comments with remaining API budget
        remaining_api_calls = self.max_api_calls - self.api_call_count
        high_value_comments = [item for item, score in comments_with_scores if score > 0.7][:remaining_api_calls]
        
        if high_value_comments and remaining_api_calls > 0:
            api_enhanced_comments = self._batch_process_with_api(high_value_comments, search_topic, topic_categories, 'comment')
        else:
            api_enhanced_comments = {}
        
        for i, comment in enumerate(reddit_data['comments']):
            comment_id = comment.get('id', str(hash(str(comment))))
            if comment_id in api_enhanced_comments:
                analyzed_comment = api_enhanced_comments[comment_id]
            else:
                analyzed_comment = self._analyze_single_content_hybrid(
                    comment, search_topic, topic_categories, 'comment', False
                )
            
            analyzed_comments.append(analyzed_comment)
            
            if i % 20 == 0:
                st.sidebar.write(f"Processed {i+1}/{len(reddit_data['comments'])} comments")
        
        # Display efficiency metrics
        efficiency = (self.cache_hits / max(self.api_call_count + self.cache_hits, 1)) * 100
        st.sidebar.write(f"API Efficiency: {efficiency:.1f}% cache hit rate")
        st.sidebar.write(f"Credits used: {self.api_call_count}/{self.max_api_calls} API calls")
        
        return {
            'posts': analyzed_posts,
            'comments': analyzed_comments,
            'analysis_metadata': {
                'search_topic': search_topic,
                'topic_categories': topic_categories,
                'analyzed_at': datetime.now(),
                'total_posts_analyzed': len(analyzed_posts),
                'total_comments_analyzed': len(analyzed_comments),
                'api_calls_used': self.api_call_count,
                'cache_hit_rate': efficiency
            }
        }
    
    def _pre_score_content(self, content_list: List[Dict], search_topic: str, content_type: str) -> List[Tuple[Dict, float]]:
        """Pre-score content to identify high-value items for API usage"""
        scored_content = []
        
        for content in content_list:
            if content_type == 'post':
                text = f"{content.get('title', '')} {content.get('content', '')}".strip()
            else:
                text = content.get('content', '').strip()
            
            if not text or len(text) < 10:
                scored_content.append((content, 0.0))
                continue
            
            # Multi-factor scoring
            relevance_score = self._calculate_advanced_relevance(text, search_topic)
            complexity_score = self._calculate_content_complexity(text)
            engagement_score = self._calculate_engagement_potential(content)
            
            # Weighted combined score
            combined_score = (relevance_score * 0.5 + complexity_score * 0.3 + engagement_score * 0.2)
            scored_content.append((content, combined_score))
        
        # Sort by score descending
        scored_content.sort(key=lambda x: x[1], reverse=True)
        return scored_content
    
    def _batch_process_with_api(self, content_list: List[Dict], search_topic: str, topic_categories: List[str], content_type: str) -> Dict[str, Dict]:
        """Batch process high-value content with API for maximum efficiency"""
        if not content_list or self.api_call_count >= self.max_api_calls:
            return {}
        
        enhanced_content = {}
        
        # Group similar content for batch processing
        content_groups = self._group_similar_content(content_list, content_type)
        
        for group in content_groups:
            if self.api_call_count >= self.max_api_calls:
                break
            
            # Process group with single API call when possible
            representative_content = group[0]
            if content_type == 'post':
                text = f"{representative_content.get('title', '')} {representative_content.get('content', '')}".strip()
            else:
                text = representative_content.get('content', '').strip()
            
            # Check cache first
            cache_key = self._generate_cache_key(text, search_topic)
            if cache_key in self.cache:
                self.cache_hits += 1
                api_result = self.cache[cache_key]
            else:
                api_result = self._call_advanced_perplexity_api(text, search_topic, topic_categories)
                if api_result:
                    self.cache[cache_key] = api_result
            
            # Apply API results to all items in group
            if api_result:
                for content in group:
                    enhanced = self._apply_api_results_to_content(content, api_result, search_topic, topic_categories, content_type)
                    # Use content ID as key instead of the dict object
                    content_id = content.get('id', str(hash(str(content))))
                    enhanced_content[content_id] = enhanced
        
        return enhanced_content
    
    def _call_advanced_perplexity_api(self, text: str, search_topic: str, topic_categories: List[str]) -> Optional[Dict]:
        """Advanced API call with sophisticated prompt engineering"""
        if not self.perplexity_api_key or self.api_call_count >= self.max_api_calls:
            return None
        
        # Craft intelligent prompt for maximum information extraction
        prompt = f"""Analyze this Reddit content about "{search_topic}":

TEXT: "{text[:600]}"

Provide a JSON response with:
{{
  "sentiment_score": <number from -1 to 1>,
  "sentiment_confidence": <0 to 1>,
  "primary_topics": [<top 3 relevant topics from: {', '.join(topic_categories[:10])}>],
  "intent": "<primary intent: help_seeking, advice_seeking, information_sharing, question_asking, solution_providing, experience_sharing, complaint, praise, discussion>",
  "complexity_level": "<basic, intermediate, advanced>",
  "key_entities": [<important entities mentioned>],
  "emotional_tone": "<calm, excited, frustrated, angry, happy, neutral>"
}}

Be precise and concise."""
        
        headers = {
            "Authorization": f"Bearer {self.perplexity_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(self.perplexity_base_url, headers=headers, json=data, timeout=12)
            if response.status_code == 200:
                self.api_call_count += 1
                self.successful_api_calls += 1
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    try:
                        parsed_result = json.loads(json_match.group())
                        return parsed_result
                    except json.JSONDecodeError:
                        pass
            
            return None
        except Exception:
            return None
    
    def _analyze_single_content_hybrid(self, content: Dict, search_topic: str, topic_categories: List[str], 
                                     content_type: str, use_advanced_rules: bool = False) -> Dict[str, Any]:
        """Hybrid analysis using advanced rule-based systems"""
        
        if content_type == 'post':
            text = f"{content.get('title', '')} {content.get('content', '')}".strip()
        else:
            text = content.get('content', '').strip()
        
        if not text or len(text) < 10:
            return self._create_minimal_analysis(content)
        
        analyzed = content.copy()
        
        # Advanced sentiment analysis
        sentiment_result = self._analyze_sentiment_advanced(text)
        analyzed.update(sentiment_result)
        
        # Sophisticated topic classification
        topics = self._classify_topics_advanced(text, topic_categories, use_advanced_rules)
        analyzed['topics'] = topics
        
        # Intent classification with pattern matching
        intent = self._classify_intent_advanced(text)
        analyzed['intent'] = intent
        
        # Multi-dimensional relevance scoring
        relevance_score = self._calculate_advanced_relevance(text, search_topic)
        analyzed['relevance_score'] = relevance_score
        
        # Entity extraction with context
        entities = self._extract_entities_advanced(text)
        analyzed['entities'] = entities
        
        # Emotional analysis
        emotions = self._detect_emotions_advanced(text)
        analyzed['emotions'] = emotions
        
        # Key phrase extraction with importance scoring
        key_phrases = self._extract_key_phrases_advanced(text)
        analyzed['key_phrases'] = key_phrases
        
        return analyzed
    
    def _analyze_sentiment_advanced(self, text: str) -> Dict[str, Any]:
        """Advanced sentiment analysis with nuanced understanding"""
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        total_score = 0.0
        word_count = 0
        confidence_factors = []
        
        # Process with weighted lexicon
        for category, data in self.sentiment_lexicon.items():
            weight = data['weight']
            category_words = data['words']
            
            matches = sum(1 for word in words if word in category_words)
            if matches > 0:
                contribution = matches * weight
                total_score += contribution
                word_count += matches
                confidence_factors.append(abs(weight) * matches)
        
        # Contextual modifiers
        negation_pattern = r'\b(not|no|never|none|nobody|nothing|neither|nowhere|isn\'t|aren\'t|wasn\'t|weren\'t|don\'t|doesn\'t|didn\'t|won\'t|wouldn\'t|can\'t|couldn\'t|shouldn\'t|mustn\'t)\b'
        negations = len(re.findall(negation_pattern, text_lower))
        
        # Apply negation adjustment
        if negations > 0:
            total_score *= (1 - (negations * 0.3))  # Reduce sentiment strength for negations
        
        # Intensity modifiers
        intensifiers = ['very', 'extremely', 'incredibly', 'absolutely', 'completely', 'totally', 'really']
        intensity_count = sum(1 for word in words if word in intensifiers)
        
        if intensity_count > 0:
            total_score *= (1 + (intensity_count * 0.2))  # Amplify sentiment
        
        # Normalize score
        if word_count > 0:
            final_score = total_score / max(len(words), 1) * 5  # Scale factor
            final_score = max(-1, min(1, final_score))
        else:
            final_score = 0.0
        
        # Determine label
        if final_score > 0.3:
            label = 'positive'
        elif final_score < -0.3:
            label = 'negative'
        else:
            label = 'neutral'
        
        # Calculate confidence
        confidence = min(sum(confidence_factors) / max(len(words), 1) * 3, 1.0) if confidence_factors else 0.5
        
        return {
            'sentiment_score': round(final_score, 3),
            'sentiment_label': label,
            'sentiment_confidence': round(confidence, 3)
        }
    
    def _classify_topics_advanced(self, text: str, categories: List[str], use_advanced: bool = False) -> List[str]:
        """Advanced topic classification with domain expertise"""
        text_lower = text.lower()
        topic_scores = {}
        
        # Domain-based classification
        for domain, keywords_data in self.topic_domains.items():
            if domain in categories:
                score = 0
                
                # Primary keywords (high weight)
                primary_matches = sum(1 for word in keywords_data['primary'] if word in text_lower)
                score += primary_matches * 3
                
                # Secondary keywords (medium weight)
                secondary_matches = sum(1 for word in keywords_data['secondary'] if word in text_lower)
                score += secondary_matches * 2
                
                # Specialized terms (context-dependent)
                if 'languages' in keywords_data:
                    lang_matches = sum(1 for word in keywords_data['languages'] if word in text_lower)
                    score += lang_matches * 2
                
                if 'contexts' in keywords_data:
                    context_matches = sum(1 for phrase in keywords_data['contexts'] if phrase in text_lower)
                    score += context_matches * 2
                
                if score > 0:
                    topic_scores[domain] = score
        
        # Fallback to keyword matching for other categories
        for category in categories:
            if category not in topic_scores:
                category_words = category.lower().split()
                matches = sum(1 for word in category_words if word in text_lower)
                if matches > 0:
                    topic_scores[category] = matches
        
        # Return top 3 topics
        sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
        return [topic for topic, _ in sorted_topics[:3]]
    
    def _classify_intent_advanced(self, text: str) -> str:
        """Advanced intent classification with pattern recognition"""
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, data in self.intent_patterns.items():
            score = 0
            weight = data['weight']
            
            # Pattern matching
            for pattern in data['patterns']:
                matches = len(re.findall(pattern, text_lower))
                score += matches * 2
            
            # Keyword matching
            keyword_matches = sum(1 for keyword in data['keywords'] if keyword in text_lower)
            score += keyword_matches
            
            # Apply weight
            final_score = score * weight
            
            if final_score > 0:
                intent_scores[intent] = final_score
        
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
            # Convert technical names to user-friendly names
            intent_mapping = {
                'technical_help_seeking': 'asking for help',
                'advice_seeking': 'seeking advice',
                'information_sharing': 'sharing information',
                'question_asking': 'asking question',
                'solution_providing': 'providing answer',
                'experience_sharing': 'sharing experience',
                'complaint_expression': 'complaining',
                'praise_expression': 'praising'
            }
            return intent_mapping.get(best_intent, best_intent)
        
        return 'general discussion'
    
    def _calculate_advanced_relevance(self, text: str, search_topic: str) -> float:
        """Multi-dimensional relevance calculation"""
        text_lower = text.lower()
        topic_lower = search_topic.lower()
        topic_words = topic_lower.split()
        
        # Exact matches (highest weight)
        exact_matches = sum(1 for word in topic_words if word in text_lower)
        exact_score = exact_matches / max(len(topic_words), 1)
        
        # Partial matches (medium weight)
        partial_matches = 0
        for topic_word in topic_words:
            for text_word in text_lower.split():
                if topic_word in text_word or text_word in topic_word:
                    partial_matches += 0.5
        
        partial_score = min(partial_matches / max(len(topic_words), 1), 1.0)
        
        # Semantic proximity (contextual)
        semantic_score = 0
        if 'programming' in topic_lower or 'code' in topic_lower:
            code_terms = ['function', 'variable', 'class', 'method', 'algorithm', 'syntax', 'debug', 'compile']
            semantic_matches = sum(1 for term in code_terms if term in text_lower)
            semantic_score = min(semantic_matches * 0.1, 0.3)
        
        # Combine scores with weights
        final_score = (exact_score * 0.6 + partial_score * 0.3 + semantic_score * 0.1)
        return round(min(final_score, 1.0), 3)
    
    def _extract_entities_advanced(self, text: str) -> List[Dict[str, Any]]:
        """Advanced entity extraction with context awareness"""
        entities = []
        
        # URLs and links
        urls = re.findall(r'https?://\S+', text)
        for url in urls[:3]:
            entities.append({'text': url, 'label': 'URL', 'confidence': 1.0, 'type': 'resource'})
        
        # Reddit-specific entities
        usernames = re.findall(r'/u/\w+', text)
        subreddits = re.findall(r'/r/\w+', text)
        
        for username in usernames[:2]:
            entities.append({'text': username, 'label': 'USERNAME', 'confidence': 1.0, 'type': 'social'})
        
        for subreddit in subreddits[:2]:
            entities.append({'text': subreddit, 'label': 'SUBREDDIT', 'confidence': 1.0, 'type': 'social'})
        
        # Technical terms (programming context)
        tech_patterns = {
            'programming_language': r'\b(python|javascript|java|c\+\+|react|node|html|css|sql|php|ruby|swift|kotlin)\b',
            'framework': r'\b(django|flask|express|angular|vue|spring|laravel|rails)\b',
            'tool': r'\b(git|docker|kubernetes|aws|azure|github|gitlab|vscode|intellij)\b'
        }
        
        for entity_type, pattern in tech_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:2]:
                entities.append({
                    'text': match,
                    'label': entity_type.upper(),
                    'confidence': 0.9,
                    'type': 'technical'
                })
        
        # Product names (capitalized sequences)
        products = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b', text)
        for product in products[:3]:
            if len(product) > 3 and len(product) < 30:
                entities.append({
                    'text': product,
                    'label': 'PRODUCT',
                    'confidence': 0.7,
                    'type': 'commercial'
                })
        
        return entities[:10]
    
    def _detect_emotions_advanced(self, text: str) -> List[Dict[str, Any]]:
        """Advanced emotion detection with intensity measurement"""
        emotion_patterns = {
            'excitement': {
                'patterns': [r'!{2,}', r'\b(wow|amazing|incredible|awesome)\b'],
                'keywords': ['excited', 'thrilled', 'pumped', 'stoked', 'ecstatic']
            },
            'frustration': {
                'patterns': [r'\b(ugh|argh|damn)\b', r'why\s+(?:is|does|do|can\'t)'],
                'keywords': ['frustrated', 'annoyed', 'irritated', 'fed up']
            },
            'confusion': {
                'patterns': [r'\?\?\+', r'\b(confused|lost|stuck)\b'],
                'keywords': ['confused', 'lost', 'bewildered', 'puzzled']
            },
            'satisfaction': {
                'patterns': [r'\b(finally|solved|worked|success)\b'],
                'keywords': ['satisfied', 'content', 'pleased', 'relieved']
            },
            'curiosity': {
                'patterns': [r'\b(wonder|curious|interesting)\b'],
                'keywords': ['curious', 'wondering', 'intrigued']
            }
        }
        
        detected_emotions = []
        text_lower = text.lower()
        
        for emotion, data in emotion_patterns.items():
            score = 0
            
            # Pattern matching
            for pattern in data['patterns']:
                matches = len(re.findall(pattern, text_lower))
                score += matches * 0.4
            
            # Keyword matching
            keyword_matches = sum(1 for keyword in data['keywords'] if keyword in text_lower)
            score += keyword_matches * 0.3
            
            if score > 0:
                intensity = min(score, 1.0)
                detected_emotions.append({
                    'emotion': emotion,
                    'score': round(intensity, 3),
                    'intensity': 'high' if intensity > 0.7 else 'medium' if intensity > 0.3 else 'low'
                })
        
        return sorted(detected_emotions, key=lambda x: x['score'], reverse=True)[:3]
    
    def _extract_key_phrases_advanced(self, text: str) -> List[str]:
        """Advanced key phrase extraction with importance scoring"""
        # Clean and tokenize
        text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text_clean.split()
        
        # Remove stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Generate bigrams and trigrams
        phrases = []
        
        # Bigrams
        for i in range(len(filtered_words) - 1):
            phrase = f"{filtered_words[i]} {filtered_words[i+1]}"
            if len(phrase) > 6:
                phrases.append(phrase)
        
        # Trigrams
        for i in range(len(filtered_words) - 2):
            phrase = f"{filtered_words[i]} {filtered_words[i+1]} {filtered_words[i+2]}"
            if len(phrase) > 10:
                phrases.append(phrase)
        
        # Score phrases by frequency and importance
        phrase_scores = {}
        for phrase in phrases:
            base_score = phrases.count(phrase)
            
            # Boost technical terms
            if any(tech in phrase for tech in ['code', 'program', 'function', 'error', 'debug', 'api']):
                base_score *= 1.5
            
            phrase_scores[phrase] = base_score
        
        # Return top unique phrases
        unique_phrases = list(set(phrases))
        scored_phrases = [(phrase, phrase_scores.get(phrase, 1)) for phrase in unique_phrases]
        scored_phrases.sort(key=lambda x: x[1], reverse=True)
        
        return [phrase for phrase, _ in scored_phrases[:8]]
    
    def _generate_intelligent_topic_categories(self, search_topic: str) -> List[str]:
        """Generate intelligent topic categories based on search context"""
        base_categories = list(self.topic_domains.keys())
        
        # Add search topic
        if search_topic and search_topic.lower() not in base_categories:
            base_categories.append(search_topic.lower())
        
        # Context-aware expansion
        search_lower = search_topic.lower() if search_topic else ""
        
        expansions = {
            'programming': ['web development', 'mobile development', 'data science', 'devops', 'testing'],
            'career': ['job interview', 'resume writing', 'networking', 'skill development', 'remote work'],
            'technology': ['artificial intelligence', 'cybersecurity', 'cloud computing', 'blockchain', 'iot'],
            'education': ['online learning', 'certification', 'bootcamp', 'university', 'self-taught']
        }
        
        for domain, related_topics in expansions.items():
            if domain in search_lower:
                base_categories.extend(related_topics)
                break
        
        return base_categories[:15]
    
    def _group_similar_content(self, content_list: List[Dict], content_type: str) -> List[List[Dict]]:
        """Group similar content for batch processing efficiency"""
        if len(content_list) <= 3:
            return [content_list]
        
        # Simple grouping by length and basic characteristics
        groups = []
        current_group = []
        
        for content in content_list:
            if content_type == 'post':
                text = f"{content.get('title', '')} {content.get('content', '')}".strip()
            else:
                text = content.get('content', '').strip()
            
            text_length = len(text)
            
            if not current_group:
                current_group.append(content)
            elif abs(len(text) - len(current_group[0])) < 200:  # Similar length
                current_group.append(content)
            else:
                groups.append(current_group)
                current_group = [content]
            
            # Limit group size for efficiency
            if len(current_group) >= 3:
                groups.append(current_group)
                current_group = []
        
        if current_group:
            groups.append(current_group)
        
        return groups
    
    def _apply_api_results_to_content(self, content: Dict, api_result: Dict, search_topic: str, 
                                    topic_categories: List[str], content_type: str) -> Dict[str, Any]:
        """Apply API results to content with fallback enhancement"""
        analyzed = content.copy()
        
        # Apply API results with validation
        analyzed['sentiment_score'] = max(-1, min(1, api_result.get('sentiment_score', 0.0)))
        analyzed['sentiment_label'] = api_result.get('sentiment_label', 'neutral')
        analyzed['sentiment_confidence'] = max(0, min(1, api_result.get('sentiment_confidence', 0.5)))
        
        analyzed['topics'] = api_result.get('primary_topics', [])[:3]
        analyzed['intent'] = api_result.get('intent', 'general discussion')
        
        # Calculate relevance independently
        if content_type == 'post':
            text = f"{content.get('title', '')} {content.get('content', '')}".strip()
        else:
            text = content.get('content', '').strip()
        
        analyzed['relevance_score'] = self._calculate_advanced_relevance(text, search_topic)
        
        # Enhanced entities from API
        api_entities = api_result.get('key_entities', [])
        basic_entities = self._extract_entities_advanced(text)
        
        # Combine and deduplicate
        all_entities = basic_entities.copy()
        for entity in api_entities:
            if isinstance(entity, str):
                all_entities.append({
                    'text': entity,
                    'label': 'MENTIONED',
                    'confidence': 0.8,
                    'type': 'api_extracted'
                })
        
        analyzed['entities'] = all_entities[:10]
        
        # Emotional tone from API
        emotional_tone = api_result.get('emotional_tone', 'neutral')
        analyzed['emotions'] = [{'emotion': emotional_tone, 'score': 0.7, 'source': 'api'}]
        
        # Key phrases
        analyzed['key_phrases'] = self._extract_key_phrases_advanced(text)
        
        return analyzed
    
    def _calculate_content_complexity(self, text: str) -> float:
        """Calculate content complexity for prioritization"""
        # Length factor
        length_score = min(len(text) / 1000, 1.0)
        
        # Technical term density
        tech_terms = ['algorithm', 'function', 'variable', 'method', 'class', 'object', 'array', 'loop', 'condition']
        tech_count = sum(1 for term in tech_terms if term in text.lower())
        tech_score = min(tech_count * 0.1, 0.3)
        
        # Question complexity
        question_marks = text.count('?')
        question_score = min(question_marks * 0.1, 0.2)
        
        return length_score * 0.5 + tech_score * 0.3 + question_score * 0.2
    
    def _calculate_engagement_potential(self, content: Dict) -> float:
        """Calculate engagement potential based on Reddit metrics"""
        score = max(content.get('score', 0), 0)
        num_comments = max(content.get('num_comments', 0), 0)
        
        # Normalize scores
        score_factor = min(score / 100, 1.0)  # Cap at 100 upvotes
        comments_factor = min(num_comments / 50, 1.0)  # Cap at 50 comments
        
        return score_factor * 0.6 + comments_factor * 0.4
    
    def _generate_cache_key(self, text: str, search_topic: str) -> str:
        """Generate cache key for content"""
        content_hash = hashlib.md5(f"{text[:200]}{search_topic}".encode()).hexdigest()
        return content_hash[:16]
    
    def _create_minimal_analysis(self, content: Dict) -> Dict[str, Any]:
        """Create minimal analysis for empty/short content"""
        analyzed = content.copy()
        analyzed.update({
            'sentiment_score': 0.0,
            'sentiment_label': 'neutral',
            'sentiment_confidence': 0.0,
            'topics': [],
            'intent': 'unknown',
            'relevance_score': 0.0,
            'entities': [],
            'emotions': [],
            'key_phrases': []
        })
        return analyzed