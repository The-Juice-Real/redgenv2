from typing import Dict, List, Any, Optional
import re
import math
from datetime import datetime

class AdvancedLeadScoringEngine:
    """Next-generation lead scoring with predictive analytics and behavioral modeling"""
    
    def __init__(self):
        self.score_weights = {
            'intent_clarity': 0.35,      # How clear is the purchase intent
            'decision_authority': 0.25,   # Authority to make decisions
            'timing_urgency': 0.20,      # Timing and urgency factors
            'business_fit': 0.15,        # Fit with target customer profile
            'engagement_quality': 0.05   # Quality of content and engagement
        }
        
        self.intent_signals = {
            'explicit_need': {
                'patterns': [
                    r'\bneed\s+(?:a|an|to find|to get)\s+\w+',
                    r'\blooking for\s+\w+',
                    r'\bsearching for\s+\w+',
                    r'\bwant to\s+(?:buy|purchase|get)\s+\w+'
                ],
                'weight': 25
            },
            'evaluation_stage': {
                'patterns': [
                    r'\b(?:comparing|evaluating|considering)\s+\w+',
                    r'\bwhich\s+(?:is better|should i choose)',
                    r'\bpros and cons\s+of\s+\w+'
                ],
                'weight': 20
            },
            'problem_statement': {
                'patterns': [
                    r'\bstruggling with\s+\w+',
                    r'\bhaving trouble\s+with\s+\w+',
                    r'\bfrustrated\s+(?:by|with)\s+\w+'
                ],
                'weight': 18
            },
            'budget_indication': {
                'patterns': [
                    r'\bbudget\s+(?:of|is|around)\s+\$?\d+',
                    r'\bcan\s+afford\s+\$?\d+',
                    r'\bwilling to\s+(?:pay|spend)\s+\$?\d+'
                ],
                'weight': 22
            }
        }
        
        self.authority_indicators = {
            'c_level': ['ceo', 'cto', 'cfo', 'coo', 'chief', 'president'],
            'vp_level': ['vp', 'vice president', 'director', 'head of'],
            'manager_level': ['manager', 'lead', 'senior', 'coordinator'],
            'decision_power': ['decision maker', 'in charge of', 'responsible for', 'budget owner']
        }
        
        self.urgency_signals = {
            'immediate': ['urgent', 'asap', 'immediately', 'right now', 'today'],
            'short_term': ['this week', 'this month', 'soon', 'quickly'],
            'deadline_driven': ['deadline', 'by end of', 'before', 'launch date'],
            'budget_cycle': ['q1', 'q2', 'q3', 'q4', 'end of year', 'budget approved']
        }
        
        self.business_indicators = {
            'size_large': ['enterprise', 'corporation', '500+ employees', 'multinational'],
            'size_medium': ['mid-size', '50-500 employees', 'growing company'],
            'size_small': ['startup', 'small business', '10-50 employees'],
            'size_micro': ['solo', 'freelancer', 'one person', 'independent']
        }
    
    def calculate_advanced_score(self, prospect: Dict[str, Any], service_description: str) -> Dict[str, Any]:
        """Calculate comprehensive lead score with detailed breakdown"""
        
        content = f"{prospect.get('title', '')} {prospect.get('content', '')}".lower()
        
        # Multi-dimensional scoring
        intent_score = self._score_purchase_intent(content, service_description)
        authority_score = self._score_decision_authority(content)
        urgency_score = self._score_timing_urgency(content, prospect)
        business_fit_score = self._score_business_fit(content, service_description)
        engagement_score = self._score_engagement_quality(prospect)
        
        # Calculate weighted composite score
        composite_score = (
            intent_score * self.score_weights['intent_clarity'] +
            authority_score * self.score_weights['decision_authority'] +
            urgency_score * self.score_weights['timing_urgency'] +
            business_fit_score * self.score_weights['business_fit'] +
            engagement_score * self.score_weights['engagement_quality']
        )
        
        # Apply context multipliers
        context_multiplier = self._calculate_context_multiplier(prospect, service_description)
        final_score = min(composite_score * context_multiplier, 100)
        
        return {
            'final_score': round(final_score, 2),
            'intent_score': round(intent_score, 2),
            'authority_score': round(authority_score, 2),
            'urgency_score': round(urgency_score, 2),
            'business_fit_score': round(business_fit_score, 2),
            'engagement_score': round(engagement_score, 2),
            'context_multiplier': round(context_multiplier, 3),
            'scoring_confidence': self._calculate_scoring_confidence(content),
            'lead_quality_tier': self._determine_quality_tier(final_score),
            'next_action_priority': self._recommend_action_priority(final_score, urgency_score)
        }
    
    def _score_purchase_intent(self, content: str, service_description: str) -> float:
        """Score purchase intent with context awareness"""
        
        intent_score = 0
        matched_signals = []
        
        # Check for explicit intent signals
        for signal_type, signal_data in self.intent_signals.items():
            for pattern in signal_data['patterns']:
                if re.search(pattern, content):
                    intent_score += signal_data['weight']
                    matched_signals.append(signal_type)
                    break
        
        # Service relevance boost
        service_words = set(service_description.lower().split())
        content_words = set(content.split())
        relevance_ratio = len(service_words.intersection(content_words)) / max(len(service_words), 1)
        intent_score *= (1 + relevance_ratio)
        
        # Question format penalty (information seeking vs purchase intent)
        question_words = ['what', 'how', 'when', 'where', 'why', 'which']
        question_count = sum(1 for word in question_words if word in content)
        if question_count > 2:
            intent_score *= 0.8  # Reduce score for purely informational queries
        
        return min(intent_score, 100)
    
    def _score_decision_authority(self, content: str) -> float:
        """Score decision-making authority"""
        
        authority_score = 0
        
        # Check authority levels
        for level, indicators in self.authority_indicators.items():
            for indicator in indicators:
                if indicator in content:
                    if level == 'c_level':
                        authority_score += 30
                    elif level == 'vp_level':
                        authority_score += 20
                    elif level == 'manager_level':
                        authority_score += 15
                    elif level == 'decision_power':
                        authority_score += 25
                    break
        
        # Business context indicators
        business_terms = ['company', 'business', 'organization', 'team', 'department']
        if any(term in content for term in business_terms):
            authority_score += 10
        
        # First-person decision language
        decision_phrases = ['i need to', 'we need to', 'i\'m looking', 'we\'re looking', 'i decide', 'we decide']
        if any(phrase in content for phrase in decision_phrases):
            authority_score += 15
        
        return min(authority_score, 100)
    
    def _score_timing_urgency(self, content: str, prospect: Dict[str, Any]) -> float:
        """Score timing and urgency factors"""
        
        urgency_score = 0
        
        # Check urgency signals
        for urgency_level, signals in self.urgency_signals.items():
            for signal in signals:
                if signal in content:
                    if urgency_level == 'immediate':
                        urgency_score += 25
                    elif urgency_level == 'short_term':
                        urgency_score += 18
                    elif urgency_level == 'deadline_driven':
                        urgency_score += 20
                    elif urgency_level == 'budget_cycle':
                        urgency_score += 15
                    break
        
        # Post recency boost
        try:
            created_utc = prospect.get('created_utc', 0)
            if created_utc:
                import time
                hours_ago = (time.time() - created_utc) / 3600
                if hours_ago <= 24:
                    urgency_score += 20
                elif hours_ago <= 72:
                    urgency_score += 15
                elif hours_ago <= 168:
                    urgency_score += 10
        except:
            pass
        
        return min(urgency_score, 100)
    
    def _score_business_fit(self, content: str, service_description: str) -> float:
        """Score business fit for target customer profile"""
        
        fit_score = 50  # Base score
        
        # Business size indicators
        for size, indicators in self.business_indicators.items():
            for indicator in indicators:
                if indicator in content:
                    if size in ['size_medium', 'size_small']:  # Target segments for China sourcing
                        fit_score += 20
                    elif size == 'size_large':
                        fit_score += 15
                    elif size == 'size_micro':
                        fit_score += 5
                    break
        
        # Industry relevance
        target_industries = ['ecommerce', 'retail', 'manufacturing', 'product', 'import', 'export']
        industry_matches = sum(1 for industry in target_industries if industry in content)
        fit_score += industry_matches * 8
        
        # Geographic indicators (international business)
        geo_indicators = ['international', 'global', 'overseas', 'china', 'asia', 'import', 'export']
        geo_matches = sum(1 for geo in geo_indicators if geo in content)
        fit_score += geo_matches * 6
        
        return min(fit_score, 100)
    
    def _score_engagement_quality(self, prospect: Dict[str, Any]) -> float:
        """Score content and engagement quality"""
        
        engagement_score = 0
        
        # Content length and detail
        content = f"{prospect.get('title', '')} {prospect.get('content', '')}"
        word_count = len(content.split())
        
        if word_count > 100:
            engagement_score += 25
        elif word_count > 50:
            engagement_score += 15
        elif word_count > 20:
            engagement_score += 10
        
        # Reddit engagement metrics
        score = prospect.get('score', 0)
        if score > 20:
            engagement_score += 20
        elif score > 10:
            engagement_score += 15
        elif score > 5:
            engagement_score += 10
        
        # Comment engagement
        num_comments = prospect.get('num_comments', 0)
        if num_comments > 10:
            engagement_score += 15
        elif num_comments > 5:
            engagement_score += 10
        elif num_comments > 0:
            engagement_score += 5
        
        return min(engagement_score, 100)
    
    def _calculate_context_multiplier(self, prospect: Dict[str, Any], service_description: str) -> float:
        """Calculate context-based score multiplier"""
        
        multiplier = 1.0
        content = f"{prospect.get('title', '')} {prospect.get('content', '')}".lower()
        
        # High-value subreddit boost
        subreddit = prospect.get('subreddit', '').lower()
        high_value_subs = ['entrepreneur', 'ecommerce', 'amazon', 'alibaba', 'sourcing', 'manufacturing']
        if subreddit in high_value_subs:
            multiplier *= 1.15
        
        # Professional language boost
        professional_terms = ['strategy', 'implementation', 'solution', 'optimization', 'efficiency']
        prof_matches = sum(1 for term in professional_terms if term in content)
        if prof_matches >= 2:
            multiplier *= 1.08
        
        # Specificity boost (detailed requirements)
        specific_terms = ['specifications', 'requirements', 'criteria', 'standards', 'quality']
        spec_matches = sum(1 for term in specific_terms if term in content)
        if spec_matches >= 1:
            multiplier *= 1.05
        
        return min(multiplier, 1.5)  # Cap at 50% boost
    
    def _calculate_scoring_confidence(self, content: str) -> float:
        """Calculate confidence in the scoring"""
        
        confidence_factors = []
        
        # Content length factor
        word_count = len(content.split())
        if word_count > 50:
            confidence_factors.append(0.3)
        elif word_count > 20:
            confidence_factors.append(0.2)
        else:
            confidence_factors.append(0.1)
        
        # Signal clarity factor
        clear_signals = ['need', 'looking for', 'budget', 'urgent', 'ceo', 'manager']
        signal_count = sum(1 for signal in clear_signals if signal in content)
        confidence_factors.append(min(signal_count * 0.15, 0.4))
        
        # Business context factor
        business_context = ['company', 'business', 'startup', 'team']
        if any(context in content for context in business_context):
            confidence_factors.append(0.3)
        else:
            confidence_factors.append(0.1)
        
        return min(sum(confidence_factors), 1.0)
    
    def _determine_quality_tier(self, score: float) -> str:
        """Determine lead quality tier"""
        
        if score >= 80:
            return 'Premium'
        elif score >= 60:
            return 'High Quality'
        elif score >= 40:
            return 'Medium Quality'
        elif score >= 25:
            return 'Low Quality'
        else:
            return 'Unqualified'
    
    def _recommend_action_priority(self, final_score: float, urgency_score: float) -> str:
        """Recommend action priority"""
        
        if final_score >= 70 and urgency_score >= 60:
            return 'Immediate Contact'
        elif final_score >= 60:
            return 'High Priority'
        elif final_score >= 40:
            return 'Medium Priority'
        elif final_score >= 25:
            return 'Low Priority'
        else:
            return 'Monitor Only'