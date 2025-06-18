import re
import requests
from typing import Dict, List, Any, Optional
import streamlit as st

class ContactEnrichment:
    """Contact enrichment and LinkedIn profile discovery"""
    
    def __init__(self):
        self.linkedin_patterns = [
            r'linkedin\.com/in/([a-zA-Z0-9\-]+)',
            r'linkedin\.com/pub/([a-zA-Z0-9\-]+)',
            r'/in/([a-zA-Z0-9\-]+)'
        ]
        
        self.email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'\b[A-Za-z0-9._%+-]+\s*\[\s*at\s*\]\s*[A-Za-z0-9.-]+\s*\[\s*dot\s*\]\s*[A-Z|a-z]{2,}\b'
        ]
        
        self.phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\(\d{3}\)\s*\d{3}[-.]?\d{4}\b'
        ]
        
        self.company_indicators = [
            r'\b(?:work at|working at|employed by|company:)\s+([A-Za-z0-9\s]+)\b',
            r'\b(?:founder of|ceo of|started)\s+([A-Za-z0-9\s]+)\b',
            r'\b([A-Za-z0-9\s]+)\s+(?:employee|team member|developer)\b'
        ]

    def enrich_contact_data(self, content: Dict, reddit_username: str) -> Dict[str, Any]:
        """Advanced contact enrichment with predictive intelligence and cross-platform discovery"""
        
        text = f"{content.get('title', '')} {content.get('content', '')}".strip()
        
        # Multi-source contact extraction
        emails = self._extract_emails(text)
        phones = self._extract_phones(text)
        linkedin_profiles = self._extract_linkedin_profiles(text)
        companies = self._extract_companies(text)
        social_links = self._extract_social_links(text)
        
        # Professional context analysis
        professional_context = self._extract_professional_context(text)
        
        # Enhanced enrichment scoring
        enrichment_score = self._calculate_enrichment_score(
            emails, phones, linkedin_profiles, companies, professional_context
        )
        
        return {
            'reddit_username': reddit_username,
            'emails_found': emails,
            'phones_found': phones,
            'linkedin_profiles': linkedin_profiles,
            'companies_mentioned': companies,
            'social_links': social_links,
            'professional_context': professional_context,
            'enrichment_score': enrichment_score,
            'contact_confidence': self._assess_contact_confidence(
                emails, linkedin_profiles, companies
            ),
            'outreach_strategies': self._generate_outreach_suggestions(
                reddit_username, emails, linkedin_profiles, companies, professional_context
            ),
            'seniority_level': self._assess_seniority_level(
                professional_context.get('roles', []),
                professional_context.get('experience_years', [])
            )
        }

    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text"""
        emails = []
        
        for pattern in self.email_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            emails.extend(matches)
        
        # Clean and deduplicate
        cleaned_emails = []
        for email in emails:
            # Handle obfuscated emails (e.g., "email [at] domain [dot] com")
            if '[at]' in email or '[dot]' in email:
                cleaned = email.replace('[at]', '@').replace('[dot]', '.').replace(' ', '')
                cleaned_emails.append(cleaned)
            else:
                cleaned_emails.append(email)
        
        return list(set(cleaned_emails))

    def _extract_phones(self, text: str) -> List[str]:
        """Extract phone numbers from text"""
        phones = []
        
        for pattern in self.phone_patterns:
            matches = re.findall(pattern, text)
            phones.extend(matches)
        
        return list(set(phones))

    def _extract_linkedin_profiles(self, text: str) -> List[str]:
        """Extract LinkedIn profile URLs and usernames"""
        profiles = []
        
        for pattern in self.linkedin_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            profiles.extend(matches)
        
        return list(set(profiles))

    def _extract_companies(self, text: str) -> List[str]:
        """Extract company names and affiliations"""
        companies = []
        
        for pattern in self.company_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            companies.extend([match.strip() for match in matches])
        
        # Also look for common company patterns
        company_patterns = [
            r'\b([A-Z][a-zA-Z]+\s+(?:Inc|LLC|Corp|Corporation|Ltd|Limited|Co|Company))\b',
            r'\b([A-Z][a-zA-Z]+(?:tech|Tech|TECH))\b'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            companies.extend(matches)
        
        # Filter out common false positives
        false_positives = ['Reddit Inc', 'Google Inc', 'Microsoft Corp', 'Apple Inc']
        companies = [comp for comp in companies if comp not in false_positives]
        
        return list(set(companies[:5]))  # Limit to top 5

    def _extract_social_links(self, text: str) -> List[str]:
        """Extract social media links and profiles"""
        social_patterns = [
            r'(?:https?://)?(?:www\.)?twitter\.com/([a-zA-Z0-9_]+)',
            r'(?:https?://)?(?:www\.)?github\.com/([a-zA-Z0-9\-]+)',
            r'(?:https?://)?(?:www\.)?instagram\.com/([a-zA-Z0-9_.]+)',
            r'(?:https?://)?([a-zA-Z0-9\-]+\.(?:com|org|net|io))'
        ]
        
        social_links = []
        for pattern in social_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            social_links.extend(matches)
        
        return list(set(social_links[:3]))  # Limit to top 3

    def _extract_professional_context(self, text: str) -> Dict[str, Any]:
        """Extract professional context and role information"""
        
        role_patterns = [
            r'\b(?:i am|i\'m)\s+(?:a|an)?\s*([a-zA-Z\s]+?)(?:\s+at|\s+for|\.|,)',
            r'\bmy role is\s+([a-zA-Z\s]+?)(?:\s+at|\.|,)',
            r'\bworking as\s+(?:a|an)?\s*([a-zA-Z\s]+?)(?:\s+at|\.|,)'
        ]
        
        roles = []
        for pattern in role_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            roles.extend([match.strip() for match in matches])
        
        # Extract years of experience
        experience_pattern = r'(\d+)\s*years?\s+(?:of\s+)?experience'
        experience_matches = re.findall(experience_pattern, text, re.IGNORECASE)
        experience_years = [int(match) for match in experience_matches]
        
        # Extract skills and technologies
        tech_keywords = [
            'python', 'javascript', 'react', 'node.js', 'sql', 'aws', 'docker',
            'kubernetes', 'machine learning', 'ai', 'data science', 'backend',
            'frontend', 'full stack', 'devops', 'cloud', 'api', 'microservices'
        ]
        
        mentioned_skills = [skill for skill in tech_keywords if skill.lower() in text.lower()]
        
        return {
            'roles_mentioned': roles[:3],
            'experience_years': max(experience_years) if experience_years else None,
            'skills_mentioned': mentioned_skills[:5],
            'seniority_level': self._assess_seniority_level(roles, experience_years)
        }

    def _generate_email_variations(self, username: str, companies: List[str]) -> List[str]:
        """Generate potential email variations based on username and companies"""
        
        if not username or not companies:
            return []
        
        variations = []
        clean_username = re.sub(r'[^a-zA-Z0-9]', '', username.lower())
        
        for company in companies[:2]:  # Use top 2 companies
            clean_company = re.sub(r'[^a-zA-Z0-9]', '', company.lower())
            
            # Common email patterns
            domain_variations = [
                f"{clean_company}.com",
                f"{clean_company}.org",
                f"{clean_company}.net"
            ]
            
            for domain in domain_variations:
                variations.extend([
                    f"{clean_username}@{domain}",
                    f"{clean_username[0]}.{clean_username[1:]}@{domain}",
                    f"{clean_username}.{clean_company}@gmail.com"
                ])
        
        return variations[:5]  # Limit to top 5 variations

    def _calculate_enrichment_score(self, emails: List[str], phones: List[str], 
                                  linkedin: List[str], companies: List[str], 
                                  context: Dict) -> float:
        """Calculate contact enrichment score (0-100)"""
        
        score = 0
        
        # Direct contact info
        score += len(emails) * 30  # Emails are most valuable
        score += len(phones) * 25  # Phone numbers are valuable
        score += len(linkedin) * 20  # LinkedIn profiles are good
        
        # Company context
        score += len(companies) * 10
        
        # Professional context
        if context.get('roles_mentioned'):
            score += 15
        if context.get('experience_years'):
            score += 10
        if context.get('skills_mentioned'):
            score += len(context['skills_mentioned']) * 2
        
        return min(score, 100)

    def _assess_contact_confidence(self, emails: List[str], linkedin: List[str], 
                                 companies: List[str]) -> str:
        """Assess confidence level for contact information"""
        
        if emails and linkedin:
            return "high"
        elif emails or linkedin:
            return "medium"
        elif companies:
            return "low"
        else:
            return "very_low"

    def _assess_seniority_level(self, roles: List[str], experience_years: List[int]) -> str:
        """Assess professional seniority level"""
        
        senior_keywords = ['senior', 'lead', 'principal', 'director', 'manager', 'head', 'vp', 'cto', 'ceo']
        junior_keywords = ['junior', 'intern', 'entry', 'associate', 'graduate']
        
        role_text = ' '.join(roles).lower()
        
        if any(keyword in role_text for keyword in senior_keywords):
            return "senior"
        elif any(keyword in role_text for keyword in junior_keywords):
            return "junior"
        elif experience_years and max(experience_years) >= 5:
            return "mid_to_senior"
        elif experience_years and max(experience_years) >= 2:
            return "mid_level"
        else:
            return "unknown"

    def _generate_outreach_suggestions(self, username: str, emails: List[str], 
                                     linkedin: List[str], companies: List[str], 
                                     context: Dict) -> List[str]:
        """Generate personalized outreach suggestions"""
        
        suggestions = []
        
        if emails:
            suggestions.append(f"✉️ Direct email outreach to {emails[0]}")
        
        if linkedin:
            suggestions.append(f"💼 LinkedIn connection request to linkedin.com/in/{linkedin[0]}")
        
        if not emails and not linkedin:
            suggestions.append(f"🔍 Research {username} on professional networks")
        
        if companies:
            suggestions.append(f"🏢 Company research: {companies[0]} for contact discovery")
        
        if context.get('roles_mentioned'):
            role = context['roles_mentioned'][0]
            suggestions.append(f"🎯 Role-specific messaging for {role} position")
        
        if context.get('skills_mentioned'):
            skills = ', '.join(context['skills_mentioned'][:2])
            suggestions.append(f"💡 Technical discussion opener about {skills}")
        
        return suggestions[:4]  # Limit to top 4 suggestions