"""
Improved lead scoring specifically for sourcing services
Focuses on actual buying signals rather than general business activity
"""

import re
from typing import Dict, List, Any

class ImprovedLeadScoring:
    def __init__(self):
        # Buying intent indicators for sourcing services
        self.buying_signals = {
            'urgent': ['urgent', 'asap', 'immediately', 'quickly', 'rush order', 'need now'],
            'seeking_quotes': ['quote', 'quotation', 'pricing', 'cost estimate', 'how much', 'price range'],
            'sourcing_needs': ['manufacturer', 'supplier', 'factory', 'wholesale', 'bulk order', 'private label'],
            'product_development': ['prototype', 'sample', 'custom design', 'oem', 'odm', 'specification'],
            'quality_concerns': ['quality control', 'inspection', 'certification', 'compliance', 'testing'],
            'logistics_needs': ['shipping', 'import', 'export', 'logistics', 'delivery', 'customs']
        }
        
        # Non-buyer indicators (content creators, advisors, etc.)
        self.non_buyer_signals = [
            'i help', 'i helped', 'consultant', 'here\'s how', 'advice', 'tips',
            'ama', 'ask me anything', 'sharing my experience', 'success story',
            'here\'s what i learned', 'my journey', 'how i made', 'tutorial'
        ]
        
        # Specific to China/Asia sourcing
        self.china_sourcing_signals = [
            'china', 'chinese', 'alibaba', 'guangzhou', 'shenzhen', 'yiwu',
            'guangdong', 'asia', 'asian suppliers', 'overseas', 'international sourcing'
        ]
        
    def score_lead_accurately(self, content: str, title: str, author: str, subreddit: str) -> Dict[str, Any]:
        """
        More accurate lead scoring focused on actual sourcing prospects
        """
        full_text = (title + ' ' + content).lower()
        
        # Start with base score
        score = 0
        intent_category = 'Low'
        urgency_level = 'Low'
        budget_category = 'Unknown'
        
        # Check if this is a content creator/advisor (should be filtered out)
        is_advisor = any(signal in full_text for signal in self.non_buyer_signals)
        if is_advisor:
            return {
                'lead_score': 10,  # Very low score for advisors
                'buying_intent': {'category': 'Content Creator'},
                'urgency': {'level': 'N/A'},
                'budget_indicators': {'category': 'N/A'},
                'is_qualified': False,
                'reason': 'Content creator/advisor, not a prospect'
            }
        
        # Buying intent scoring
        intent_score = 0
        for category, signals in self.buying_signals.items():
            matches = sum(1 for signal in signals if signal in full_text)
            if matches > 0:
                if category == 'urgent':
                    intent_score += matches * 25
                    urgency_level = 'High'
                elif category == 'seeking_quotes':
                    intent_score += matches * 30
                    intent_category = 'High'
                elif category == 'sourcing_needs':
                    intent_score += matches * 20
                    intent_category = 'Medium' if intent_category == 'Low' else intent_category
                else:
                    intent_score += matches * 10
        
        # China sourcing relevance bonus
        china_relevance = sum(1 for signal in self.china_sourcing_signals if signal in full_text)
        if china_relevance > 0:
            intent_score += china_relevance * 15
        
        # Budget indicators
        budget_signals = ['budget', 'investment', 'cost', 'price', 'afford', 'spend']
        budget_matches = sum(1 for signal in budget_signals if signal in full_text)
        if budget_matches > 0:
            budget_category = 'Budget-Aware'
            intent_score += budget_matches * 5
        
        # Question format bonus (indicates genuine inquiry)
        question_patterns = ['how do i', 'where can i', 'who knows', 'need help', 'looking for']
        question_matches = sum(1 for pattern in question_patterns if pattern in full_text)
        if question_matches > 0:
            intent_score += question_matches * 15
            intent_category = 'Medium' if intent_category == 'Low' else intent_category
        
        # Penalty for very short posts (likely low-effort)
        if len(full_text) < 50:
            intent_score = max(0, intent_score - 20)
        
        # Final score calculation
        score = min(100, intent_score)
        
        # Qualification threshold
        is_qualified = score >= 40 and not is_advisor
        
        # Intent categorization based on score
        if score >= 60:
            intent_category = 'High'
        elif score >= 35:
            intent_category = 'Medium'
        else:
            intent_category = 'Low'
        
        return {
            'lead_score': score,
            'buying_intent': {'category': intent_category},
            'urgency': {'level': urgency_level},
            'budget_indicators': {'category': budget_category},
            'is_qualified': is_qualified,
            'china_sourcing_relevance': china_relevance > 0,
            'reason': self._get_scoring_reason(score, is_advisor, china_relevance)
        }
    
    def _get_scoring_reason(self, score: int, is_advisor: bool, china_relevance: int) -> str:
        """Provide reasoning for the score"""
        if is_advisor:
            return "Content creator/advisor sharing experience"
        elif score >= 60:
            return "Strong buying signals detected"
        elif score >= 35:
            return "Moderate interest in sourcing services"
        elif china_relevance > 0:
            return "China-related but weak buying signals"
        else:
            return "Low buying intent"