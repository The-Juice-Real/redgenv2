import re
from typing import Dict, List, Any

class SimpleContactEnrichment:
    """Simple contact enrichment for lead analysis"""
    
    def __init__(self):
        pass

    def enrich_contact_data(self, content: Dict, reddit_username: str) -> Dict[str, Any]:
        """Basic contact enrichment"""
        
        text = f"{content.get('title', '')} {content.get('content', '')}".strip()
        
        # Basic contact extraction
        emails = self._extract_emails(text)
        companies = self._extract_companies(text)
        
        return {
            'reddit_username': reddit_username,
            'emails_found': emails,
            'companies_mentioned': companies,
            'enrichment_score': len(emails) * 30 + len(companies) * 20,
            'contact_confidence': 'High' if emails else 'Medium' if companies else 'Low'
        }

    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return list(set(re.findall(email_pattern, text)))

    def _extract_companies(self, text: str) -> List[str]:
        """Extract company names and affiliations"""
        companies = []
        
        # Common company indicators
        company_patterns = [
            r'(?:work at|working at|employed by|company called)\s+([A-Z][a-zA-Z\s&]{2,20})',
            r'([A-Z][a-zA-Z\s&]{2,20})\s+(?:Inc|LLC|Corp|Company|Ltd)',
            r'(?:CEO|founder|owner) of\s+([A-Z][a-zA-Z\s&]{2,20})'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            companies.extend([match.strip() for match in matches if len(match.strip()) > 2])
        
        return list(set(companies[:5]))