"""
Advanced Lead Scoring System V2.0
Implementing semantic understanding, context awareness, and nuanced scoring
"""

import re
import json
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import math

class AdvancedLeadScoringV2:
    def __init__(self):
        # Iteration 1 Improvements Implementation
        
        # Semantic scoring patterns (replacing simple keyword matching)
        self.semantic_patterns = {
            'urgent_intent': {
                'patterns': ['urgent', 'asap', 'immediately', 'rush', 'emergency', 'deadline', 'by [date]'],
                'weight': 35,
                'context_modifiers': {'business': 1.5, 'personal': 0.7}
            },
            'sourcing_need': {
                'patterns': ['manufacturer', 'supplier', 'factory', 'wholesale', 'oem', 'odm', 'private label'],
                'weight': 30,
                'context_modifiers': {'established_business': 1.3, 'startup': 1.1, 'individual': 0.8}
            },
            'budget_signals': {
                'patterns': ['budget', 'investment', 'funding', 'cost analysis', 'price comparison'],
                'weight': 25,
                'context_modifiers': {'specific_numbers': 1.4, 'ranges': 1.2, 'vague': 0.9}
            },
            'quality_focus': {
                'patterns': ['quality', 'certification', 'compliance', 'standards', 'inspection'],
                'weight': 20,
                'context_modifiers': {'regulated_industry': 1.6, 'consumer_goods': 1.0}
            }
        }
        
        # Geographic intelligence expansion
        self.manufacturing_hubs = {
            'china': {'weight': 1.0, 'keywords': ['china', 'chinese', 'guangzhou', 'shenzhen', 'yiwu']},
            'vietnam': {'weight': 0.9, 'keywords': ['vietnam', 'vietnamese', 'ho chi minh', 'hanoi']},
            'thailand': {'weight': 0.8, 'keywords': ['thailand', 'thai', 'bangkok']},
            'india': {'weight': 0.85, 'keywords': ['india', 'indian', 'mumbai', 'delhi', 'bangalore']},
            'taiwan': {'weight': 0.95, 'keywords': ['taiwan', 'taiwanese', 'taipei']},
            'south_korea': {'weight': 0.9, 'keywords': ['korea', 'korean', 'seoul']}
        }
        
        # Product category intelligence
        self.product_categories = {
            'electronics': {
                'complexity': 'high',
                'regulation_level': 'high',
                'keywords': ['electronic', 'pcb', 'circuit', 'chip', 'semiconductor'],
                'weight_modifier': 1.3
            },
            'textiles': {
                'complexity': 'medium',
                'regulation_level': 'medium',
                'keywords': ['fabric', 'clothing', 'textile', 'garment', 'apparel'],
                'weight_modifier': 1.0
            },
            'medical': {
                'complexity': 'very_high',
                'regulation_level': 'very_high',
                'keywords': ['medical', 'pharmaceutical', 'health', 'fda', 'ce mark'],
                'weight_modifier': 1.5
            },
            'consumer_goods': {
                'complexity': 'low',
                'regulation_level': 'low',
                'keywords': ['consumer', 'retail', 'household', 'lifestyle'],
                'weight_modifier': 0.9
            }
        }
        
        # Sentiment analysis patterns
        self.sentiment_patterns = {
            'positive': ['satisfied', 'great', 'excellent', 'recommend', 'successful', 'happy'],
            'negative': ['terrible', 'scam', 'avoid', 'worst', 'disappointed', 'fraud'],
            'neutral': ['okay', 'average', 'standard', 'normal']
        }
        
        # User credibility indicators
        self.credibility_indicators = {
            'high': ['verified', 'established', 'years of experience', 'track record'],
            'medium': ['some experience', 'learning', 'new to'],
            'low': ['first time', 'beginner', 'no experience']
        }
        
        # Competitor detection
        self.competitor_keywords = [
            'alibaba', 'made-in-china', 'globalsources', 'dhgate', 'indiamart',
            'thomasnet', 'ec21', 'trade key', 'exporters india'
        ]
        
        # Urgency timeline patterns
        self.urgency_patterns = {
            'immediate': ['today', 'tomorrow', 'this week', 'urgent', 'asap'],
            'short_term': ['this month', 'within 30 days', 'by end of month'],
            'medium_term': ['next quarter', 'within 3 months', 'by summer'],
            'long_term': ['next year', 'planning for', 'future project']
        }
        
    def analyze_lead_advanced(self, content: str, title: str, author: str, 
                            subreddit: str, created_utc: str = None,
                            comments: List[Dict] = None) -> Dict[str, Any]:
        """
        Advanced multi-dimensional lead analysis with semantic understanding
        """
        full_text = (title + ' ' + content).lower()
        
        # Initialize scoring components
        semantic_score = self._calculate_semantic_score(full_text)
        context_score = self._analyze_context_quality(full_text, comments or [])
        temporal_score = self._calculate_temporal_relevance(created_utc)
        credibility_score = self._assess_user_credibility(full_text, author)
        sentiment_score = self._analyze_sentiment(full_text)
        geographic_score = self._analyze_geographic_relevance(full_text)
        product_score = self._analyze_product_complexity(full_text)
        urgency_score = self._extract_urgency_timeline(full_text)
        competitor_score = self._analyze_competitor_mentions(full_text)
        
        # Advanced content creator detection (improved from iteration 1)
        is_content_creator = self._detect_content_creator_advanced(full_text, title)
        
        if is_content_creator:
            return {
                'lead_score': 5,
                'tier': 'Filtered',
                'buying_intent': {'category': 'Content Creator'},
                'is_qualified': False,
                'reason': 'Advanced content creator detection'
            }
        
        # Weighted composite scoring
        composite_score = (
            semantic_score * 0.25 +
            context_score * 0.15 +
            temporal_score * 0.10 +
            credibility_score * 0.15 +
            sentiment_score * 0.10 +
            geographic_score * 0.10 +
            product_score * 0.10 +
            urgency_score * 0.05
        )
        
        # Apply competitor intelligence modifier
        if competitor_score > 0:
            composite_score *= 1.1  # Slight boost for competitor awareness
        
        # Graduated tier system
        tier = self._determine_tier(composite_score)
        
        # Qualification logic
        is_qualified = composite_score >= 40 and tier != 'Cold'
        
        return {
            'lead_score': min(100, max(0, composite_score)),
            'tier': tier,
            'buying_intent': self._categorize_intent(composite_score),
            'urgency': self._categorize_urgency(urgency_score),
            'budget_indicators': self._categorize_budget(semantic_score),
            'geographic_relevance': geographic_score,
            'product_complexity': product_score,
            'user_credibility': credibility_score,
            'sentiment_quality': sentiment_score,
            'temporal_relevance': temporal_score,
            'competitor_awareness': competitor_score,
            'is_qualified': is_qualified,
            'reason': self._generate_detailed_reasoning(composite_score, tier),
            'analysis_components': {
                'semantic': semantic_score,
                'context': context_score,
                'temporal': temporal_score,
                'credibility': credibility_score,
                'sentiment': sentiment_score,
                'geographic': geographic_score,
                'product': product_score,
                'urgency': urgency_score,
                'competitor': competitor_score
            }
        }
    
    def _calculate_semantic_score(self, text: str) -> float:
        """Calculate semantic score using pattern matching with context"""
        score = 0
        for pattern_type, pattern_data in self.semantic_patterns.items():
            matches = sum(1 for pattern in pattern_data['patterns'] if pattern in text)
            if matches > 0:
                base_score = matches * pattern_data['weight']
                # Apply context modifiers based on surrounding text
                context_modifier = self._determine_context_modifier(text, pattern_type)
                score += base_score * context_modifier
        return min(score, 100)
    
    def _analyze_context_quality(self, text: str, comments: List[Dict]) -> float:
        """Analyze discussion context and engagement quality"""
        base_score = 0
        
        # Text quality indicators
        if len(text) > 100:
            base_score += 20
        if '?' in text:  # Questions indicate genuine inquiry
            base_score += 15
        if any(word in text for word in ['help', 'advice', 'guidance']):
            base_score += 10
            
        # Comment quality analysis
        if comments:
            authentic_comments = [c for c in comments if len(c.get('content', '')) > 20]
            if len(authentic_comments) > 2:
                base_score += 20
            if any('dm' in c.get('content', '').lower() or 'message' in c.get('content', '').lower() 
                  for c in authentic_comments):
                base_score += 15
                
        return min(base_score, 100)
    
    def _calculate_temporal_relevance(self, created_utc: str) -> float:
        """Weight recent posts higher"""
        if not created_utc:
            return 50  # Neutral if no timestamp
            
        try:
            if isinstance(created_utc, (int, float)):
                post_time = datetime.fromtimestamp(created_utc)
            else:
                post_time = datetime.fromisoformat(created_utc.replace('Z', '+00:00'))
            
            days_ago = (datetime.now() - post_time).days
            
            if days_ago <= 1:
                return 100
            elif days_ago <= 7:
                return 80
            elif days_ago <= 30:
                return 60
            elif days_ago <= 90:
                return 40
            else:
                return 20
        except:
            return 50
    
    def _assess_user_credibility(self, text: str, author: str) -> float:
        """Assess user credibility based on content and username"""
        score = 50  # Base neutral score
        
        for level, indicators in self.credibility_indicators.items():
            matches = sum(1 for indicator in indicators if indicator in text)
            if matches > 0:
                if level == 'high':
                    score += matches * 20
                elif level == 'medium':
                    score += matches * 10
                else:  # low
                    score -= matches * 10
        
        # Username analysis
        if any(term in author.lower() for term in ['ceo', 'founder', 'business', 'company']):
            score += 15
        if any(term in author.lower() for term in ['newbie', 'beginner', 'learner']):
            score -= 10
            
        return max(0, min(100, score))
    
    def _analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment to filter negative experiences"""
        positive_count = sum(1 for word in self.sentiment_patterns['positive'] if word in text)
        negative_count = sum(1 for word in self.sentiment_patterns['negative'] if word in text)
        
        if negative_count > positive_count and negative_count > 2:
            return 20  # Low score for negative sentiment
        elif positive_count > 0:
            return 80
        else:
            return 60  # Neutral
    
    def _analyze_geographic_relevance(self, text: str) -> float:
        """Analyze geographic manufacturing hub mentions"""
        max_score = 0
        for hub, data in self.manufacturing_hubs.items():
            matches = sum(1 for keyword in data['keywords'] if keyword in text)
            if matches > 0:
                score = matches * 30 * data['weight']
                max_score = max(max_score, score)
        return min(max_score, 100)
    
    def _analyze_product_complexity(self, text: str) -> float:
        """Analyze product category and complexity"""
        max_score = 0
        for category, data in self.product_categories.items():
            matches = sum(1 for keyword in data['keywords'] if keyword in text)
            if matches > 0:
                base_score = matches * 25
                weighted_score = base_score * data['weight_modifier']
                max_score = max(max_score, weighted_score)
        return min(max_score, 100)
    
    def _extract_urgency_timeline(self, text: str) -> float:
        """Extract and score urgency timeline"""
        for urgency_level, patterns in self.urgency_patterns.items():
            matches = sum(1 for pattern in patterns if pattern in text)
            if matches > 0:
                if urgency_level == 'immediate':
                    return 100
                elif urgency_level == 'short_term':
                    return 80
                elif urgency_level == 'medium_term':
                    return 60
                else:  # long_term
                    return 40
        return 50  # Default if no timeline detected
    
    def _analyze_competitor_mentions(self, text: str) -> float:
        """Detect competitor platform mentions"""
        mentions = sum(1 for competitor in self.competitor_keywords if competitor in text)
        return min(mentions * 25, 100)
    
    def _detect_content_creator_advanced(self, text: str, title: str) -> bool:
        """Advanced content creator detection"""
        creator_patterns = [
            'i help', 'i helped', 'consultant', 'here\'s how', 'my experience',
            'success story', 'ama', 'ask me anything', 'sharing my', 'tutorial',
            'guide to', 'how to', 'tips for', 'advice for', 'lessons learned'
        ]
        
        strong_indicators = sum(1 for pattern in creator_patterns if pattern in text)
        
        # Title analysis for content creation
        title_indicators = ['how i', 'my journey', 'success', 'tips', 'advice', 'guide']
        title_matches = sum(1 for indicator in title_indicators if indicator in title.lower())
        
        return strong_indicators >= 2 or title_matches >= 2
    
    def _determine_context_modifier(self, text: str, pattern_type: str) -> float:
        """Determine context modifier for semantic patterns"""
        # Simplified context analysis - can be expanded with NLP
        business_context = any(word in text for word in ['business', 'company', 'startup'])
        if business_context:
            return 1.2
        return 1.0
    
    def _determine_tier(self, score: float) -> str:
        """Determine lead tier based on composite score"""
        if score >= 80:
            return 'Burning'
        elif score >= 65:
            return 'Hot'
        elif score >= 45:
            return 'Warm'
        elif score >= 25:
            return 'Cool'
        else:
            return 'Cold'
    
    def _categorize_intent(self, score: float) -> Dict[str, str]:
        """Categorize buying intent"""
        if score >= 70:
            return {'category': 'Very High'}
        elif score >= 55:
            return {'category': 'High'}
        elif score >= 40:
            return {'category': 'Medium'}
        else:
            return {'category': 'Low'}
    
    def _categorize_urgency(self, urgency_score: float) -> Dict[str, str]:
        """Categorize urgency level"""
        if urgency_score >= 80:
            return {'level': 'Immediate'}
        elif urgency_score >= 60:
            return {'level': 'High'}
        elif urgency_score >= 40:
            return {'level': 'Medium'}
        else:
            return {'level': 'Low'}
    
    def _categorize_budget(self, semantic_score: float) -> Dict[str, str]:
        """Categorize budget indicators"""
        if semantic_score >= 60:
            return {'category': 'Budget-Defined'}
        elif semantic_score >= 40:
            return {'category': 'Budget-Aware'}
        else:
            return {'category': 'Budget-Unknown'}
    
    def _generate_detailed_reasoning(self, score: float, tier: str) -> str:
        """Generate detailed reasoning for the score"""
        if tier == 'Burning':
            return "Exceptional prospect with strong buying signals and urgency"
        elif tier == 'Hot':
            return "High-quality prospect with clear sourcing intent"
        elif tier == 'Warm':
            return "Qualified prospect showing sourcing interest"
        elif tier == 'Cool':
            return "Potential prospect requiring nurturing"
        else:
            return "Low priority or insufficient buying signals"