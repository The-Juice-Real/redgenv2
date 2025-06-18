import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import streamlit as st
from simple_contact_enrichment import SimpleContactEnrichment

class LeadAnalyzer:
    """Specialized analyzer for B2B lead generation from Reddit content"""
    
    def __init__(self):
        self.contact_enricher = SimpleContactEnrichment()
        self.buying_intent_keywords = [
            # High intent
            'looking for', 'need to find', 'shopping for', 'considering', 'evaluating',
            'recommendations for', 'best tool for', 'which software', 'help me choose',
            'budget for', 'ready to buy', 'need asap', 'urgent need',
            
            # Medium intent
            'thinking about', 'exploring options', 'research', 'compare',
            'pros and cons', 'worth it', 'experience with', 'reviews',
            
            # Pain points
            'struggling with', 'problem with', 'frustrated', 'doesn\'t work',
            'looking to replace', 'current solution sucks', 'need better'
        ]
        
        self.business_size_indicators = {
            'enterprise': ['enterprise', 'corporation', 'fortune 500', 'large company', 'global team'],
            'mid_market': ['mid-size', 'growing company', '100+ employees', 'multiple offices'],
            'small_business': ['small business', 'startup', 'bootstrapped', 'solo founder', 'small team'],
            'freelancer': ['freelancer', 'solo', 'one-person', 'independent', 'consultant']
        }
        
        self.decision_maker_indicators = [
            'ceo', 'cto', 'founder', 'director', 'manager', 'head of',
            'vp', 'vice president', 'decision maker', 'in charge of',
            'responsible for', 'leading', 'managing team'
        ]
        
        self.urgency_indicators = [
            'asap', 'urgent', 'immediately', 'by end of month', 'deadline',
            'this week', 'this month', 'q1', 'q2', 'q3', 'q4',
            'budget approved', 'ready to implement', 'starting soon'
        ]
        
        self.budget_indicators = {
            'high_budget': ['unlimited budget', 'enterprise budget', '6 figures', '7 figures', 'well funded'],
            'medium_budget': ['budget of', 'allocated', 'approved budget', '5 figures', 'thousand'],
            'low_budget': ['tight budget', 'limited budget', 'bootstrap', 'cheap', 'free alternative'],
            'no_budget': ['no budget', 'broke', 'cant afford', 'too expensive']
        }
        
        self.timeline_indicators = {
            'immediate': ['today', 'tomorrow', 'this week', 'asap', 'urgent'],
            'short_term': ['this month', 'next month', 'within 30 days', '2-4 weeks'],
            'medium_term': ['this quarter', 'q1', 'q2', 'q3', 'q4', 'next quarter'],
            'long_term': ['next year', 'planning for', 'roadmap', 'future']
        }
        
        self.competitor_keywords = [
            # Project Management
            'monday.com', 'asana', 'trello', 'notion', 'clickup', 'jira', 'basecamp',
            # CRM
            'salesforce', 'hubspot', 'pipedrive', 'zoho', 'freshworks',
            # Communication
            'slack', 'discord', 'microsoft teams', 'zoom',
            # Development
            'github', 'gitlab', 'bitbucket', 'jenkins',
            # Analytics
            'google analytics', 'mixpanel', 'amplitude', 'hotjar'
        ]
        
        self.advanced_industry_keywords = {
            'saas_tech': ['saas', 'software as a service', 'api', 'cloud platform', 'microservices'],
            'fintech': ['fintech', 'payments', 'blockchain', 'cryptocurrency', 'trading'],
            'healthtech': ['healthtech', 'telemedicine', 'medical device', 'pharma', 'biotech'],
            'edtech': ['edtech', 'e-learning', 'lms', 'online courses', 'educational'],
            'ecommerce': ['ecommerce', 'shopify', 'woocommerce', 'online store', 'dropshipping', 'amazon fba', 'private label', 'product launch'],
            'marketing': ['martech', 'marketing automation', 'seo', 'sem', 'social media'],
            'hr_tech': ['hrtech', 'recruiting', 'talent acquisition', 'employee management'],
            'logistics': ['logistics', 'supply chain', 'warehouse', 'shipping', 'fulfillment'],
            'real_estate': ['proptech', 'real estate', 'property management', 'mls'],
            'media': ['media', 'content creation', 'streaming', 'publishing', 'advertising'],
            'manufacturing': ['manufacturing', 'factory', 'production', 'oem', 'odm', 'contract manufacturing'],
            'sourcing': ['sourcing', 'procurement', 'supplier', 'vendor', 'china sourcing', 'alibaba', 'wholesale', 'bulk buying']
        }
        
        # China sourcing specific indicators
        self.sourcing_pain_points = {
            'supplier_reliability': ['unreliable supplier', 'supplier issues', 'quality problems', 'communication problems', 'language barrier'],
            'quality_control': ['quality control', 'defective products', 'inspection needed', 'product quality', 'manufacturing defects'],
            'cost_reduction': ['high costs', 'expensive supplier', 'cost reduction', 'better pricing', 'cheaper alternative'],
            'moq_issues': ['minimum order', 'moq too high', 'small quantity', 'test order', 'sample order'],
            'shipping_logistics': ['shipping issues', 'long delivery', 'customs problems', 'import duties', 'logistics nightmare'],
            'supplier_search': ['find supplier', 'need manufacturer', 'looking for factory', 'supplier recommendations', 'trustworthy supplier'],
            'production_oversight': ['production monitoring', 'factory oversight', 'quality assurance', 'production timeline'],
            'documentation': ['import documentation', 'compliance issues', 'certifications needed', 'legal requirements']
        }
        
        self.sourcing_buying_signals = {
            'immediate': ['need urgently', 'asap production', 'rush order', 'immediate sourcing', 'quick turnaround'],
            'planning': ['planning to source', 'looking into', 'considering china', 'exploring options', 'research phase'],
            'budget_ready': ['budget approved', 'ready to order', 'have funding', 'investment ready', 'purchase budget'],
            'scaling': ['scaling production', 'increase volume', 'bulk order', 'mass production', 'large quantity'],
            'cost_focused': ['reduce costs', 'cheaper option', 'better pricing', 'cost optimization', 'margin improvement']
        }

    def analyze_lead_potential(self, content: Dict, content_type: str) -> Dict[str, Any]:
        """Analyze content for B2B lead generation potential"""
        
        if content_type == 'post':
            text = f"{content.get('title', '')} {content.get('content', '')}".strip()
            author = content.get('author', '')
        else:
            text = content.get('content', '').strip()
            author = content.get('author', '')
        
        if not text:
            return self._create_empty_lead_analysis()
        
        # Core lead analysis
        lead_score = self._calculate_lead_score(text, content)
        buying_intent = self._detect_buying_intent(text)
        business_context = self._extract_business_context(text)
        pain_points = self._identify_pain_points(text)
        urgency_level = self._assess_urgency(text)
        contact_hints = self._extract_contact_hints(text, author)
        
        # Enhanced analysis
        budget_analysis = self._analyze_budget_indicators(text)
        timeline_analysis = self._analyze_implementation_timeline(text)
        competitive_intel = self._analyze_competitive_mentions(text)
        enhanced_industry = self._classify_advanced_industry(text)
        
        # Enhanced contact enrichment
        enriched_contact_data = self.contact_enricher.enrich_contact_data(content, author)
        
        return {
            'lead_score': lead_score,
            'buying_intent': buying_intent,
            'business_context': business_context,
            'pain_points': pain_points,
            'urgency_level': urgency_level,
            'contact_hints': contact_hints,
            'enriched_contact': enriched_contact_data,
            'budget_analysis': budget_analysis,
            'timeline_analysis': timeline_analysis,
            'competitive_intel': competitive_intel,
            'enhanced_industry': enhanced_industry,
            'lead_quality': self._categorize_lead_quality(lead_score),
            'recommended_action': self._suggest_action(lead_score, buying_intent, urgency_level),
            'sales_notes': self._generate_enhanced_sales_notes(text, buying_intent, pain_points, budget_analysis, competitive_intel)
        }

    def _calculate_lead_score(self, text: str, content: Dict) -> float:
        """Calculate overall lead score (0-100)"""
        text_lower = text.lower()
        score = 0
        
        # Check if this is a sourcing-related lead for enhanced scoring
        is_sourcing_lead = any(keyword in text_lower for keyword_list in self.sourcing_pain_points.values() for keyword in keyword_list)
        is_sourcing_lead = is_sourcing_lead or any(keyword in text_lower for keyword_list in self.sourcing_buying_signals.values() for keyword in keyword_list)
        is_sourcing_lead = is_sourcing_lead or any(keyword in text_lower for keyword in ['china', 'alibaba', 'sourcing', 'supplier', 'manufacturer', 'factory', 'oem', 'odm', 'private label'])
        
        # Buying intent signals (0-40 points)
        intent_matches = sum(1 for keyword in self.buying_intent_keywords if keyword in text_lower)
        
        # Enhanced scoring for sourcing-specific buying signals
        if is_sourcing_lead:
            sourcing_intent_matches = 0
            for category, keywords in self.sourcing_buying_signals.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        sourcing_intent_matches += 1
                        if category in ['immediate', 'budget_ready']:
                            sourcing_intent_matches += 1  # Double weight for high-value signals
            
            intent_matches += sourcing_intent_matches
        
        intent_score = min(intent_matches * 6, 40)
        score += intent_score
        
        # Business context signals (0-25 points)
        business_matches = 0
        for category, keywords in self.business_size_indicators.items():
            if any(keyword in text_lower for keyword in keywords):
                business_matches += 1
        
        # Enhanced business context for sourcing leads
        if is_sourcing_lead:
            # Check for ecommerce and manufacturing indicators
            if any(keyword in text_lower for keyword in self.advanced_industry_keywords['ecommerce']):
                business_matches += 2
            if any(keyword in text_lower for keyword in self.advanced_industry_keywords['manufacturing']):
                business_matches += 2
            if any(keyword in text_lower for keyword in self.advanced_industry_keywords['sourcing']):
                business_matches += 2
        
        business_score = min(business_matches * 6, 25)
        score += business_score
        
        # Decision maker signals (0-20 points)
        decision_matches = sum(1 for indicator in self.decision_maker_indicators if indicator in text_lower)
        decision_score = min(decision_matches * 10, 20)
        score += decision_score
        
        # Engagement metrics (0-15 points)
        upvotes = content.get('score', 0)
        comments_count = content.get('num_comments', 0)
        engagement_score = min((upvotes * 0.1) + (comments_count * 0.5), 15)
        score += engagement_score
        
        return round(min(score, 100), 1)

    def _detect_buying_intent(self, text: str) -> Dict[str, Any]:
        """Detect and categorize buying intent"""
        text_lower = text.lower()
        
        high_intent = [kw for kw in self.buying_intent_keywords[:12] if kw in text_lower]
        medium_intent = [kw for kw in self.buying_intent_keywords[12:20] if kw in text_lower]
        pain_signals = [kw for kw in self.buying_intent_keywords[20:] if kw in text_lower]
        
        if high_intent:
            intent_level = "High"
            confidence = 0.9
        elif medium_intent:
            intent_level = "Medium"
            confidence = 0.6
        elif pain_signals:
            intent_level = "Low"
            confidence = 0.3
        else:
            intent_level = "None"
            confidence = 0.1
        
        return {
            'level': intent_level,
            'confidence': confidence,
            'signals': high_intent + medium_intent + pain_signals,
            'signal_count': len(high_intent + medium_intent + pain_signals)
        }

    def _extract_business_context(self, text: str) -> Dict[str, Any]:
        """Extract business size and industry context"""
        text_lower = text.lower()
        
        # Business size detection
        business_size = "Unknown"
        size_confidence = 0
        
        for size, keywords in self.business_size_indicators.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches > size_confidence:
                business_size = size
                size_confidence = matches
        
        # Industry indicators (basic)
        industry_keywords = {
            'technology': ['tech', 'software', 'saas', 'api', 'development'],
            'ecommerce': ['ecommerce', 'online store', 'shopify', 'amazon', 'retail'],
            'finance': ['fintech', 'banking', 'finance', 'accounting', 'payments'],
            'healthcare': ['healthcare', 'medical', 'hospital', 'clinic', 'pharma'],
            'education': ['education', 'school', 'university', 'learning', 'training']
        }
        
        industry = "Unknown"
        for ind, keywords in industry_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                industry = ind
                break
        
        return {
            'business_size': business_size,
            'size_confidence': size_confidence,
            'industry': industry,
            'decision_maker_signals': [dm for dm in self.decision_maker_indicators if dm in text_lower]
        }

    def _identify_pain_points(self, text: str) -> List[Dict[str, str]]:
        """Identify specific business pain points"""
        text_lower = text.lower()
        pain_points = []
        
        pain_patterns = {
            'inefficiency': ['slow', 'inefficient', 'takes forever', 'waste time', 'manual process'],
            'cost': ['expensive', 'costly', 'budget', 'cheap alternative', 'can\'t afford'],
            'integration': ['doesn\'t integrate', 'compatibility', 'data silos', 'multiple tools'],
            'scaling': ['can\'t scale', 'outgrew', 'too small', 'enterprise features'],
            'usability': ['difficult to use', 'confusing', 'user-friendly', 'learning curve'],
            'reliability': ['unreliable', 'downtime', 'crashes', 'bugs', 'unstable']
        }
        
        for category, keywords in pain_patterns.items():
            matched_keywords = [kw for kw in keywords if kw in text_lower]
            if matched_keywords:
                pain_points.append({
                    'category': category,
                    'description': f"{category.replace('_', ' ').title()} issues detected",
                    'signals': matched_keywords,
                    'severity': 'high' if len(matched_keywords) > 2 else 'medium'
                })
        
        return pain_points

    def _assess_urgency(self, text: str) -> Dict[str, Any]:
        """Assess urgency level of the need"""
        text_lower = text.lower()
        
        urgent_signals = [signal for signal in self.urgency_indicators if signal in text_lower]
        
        if any(signal in text_lower for signal in ['asap', 'urgent', 'immediately']):
            urgency = "High"
            timeline = "Immediate"
        elif any(signal in text_lower for signal in ['this week', 'this month', 'end of month']):
            urgency = "Medium"
            timeline = "Within 30 days"
        elif any(signal in text_lower for signal in ['q1', 'q2', 'q3', 'q4', 'budget approved']):
            urgency = "Medium"
            timeline = "Within quarter"
        else:
            urgency = "Low"
            timeline = "No specific timeline"
        
        return {
            'level': urgency,
            'timeline': timeline,
            'signals': urgent_signals
        }

    def _extract_contact_hints(self, text: str, author: str) -> Dict[str, Any]:
        """Extract potential contact information or hints"""
        
        # Email pattern (basic)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        # Company mentions
        company_pattern = r'\b(?:at|work for|company called|startup called)\s+([A-Za-z0-9\s]+)\b'
        companies = re.findall(company_pattern, text.lower())
        
        # LinkedIn/website mentions
        link_pattern = r'(linkedin\.com/[^\s]+|[a-zA-Z0-9-]+\.com)'
        links = re.findall(link_pattern, text.lower())
        
        return {
            'reddit_username': author,
            'emails': emails,
            'companies_mentioned': companies[:3],  # Limit to avoid noise
            'social_links': links[:2],
            'has_contact_info': bool(emails or companies or links)
        }

    def _categorize_lead_quality(self, lead_score: float) -> str:
        """Categorize lead quality based on score"""
        if lead_score >= 70:
            return "Hot Lead"
        elif lead_score >= 50:
            return "Warm Lead"
        elif lead_score >= 30:
            return "Cold Lead"
        else:
            return "Low Quality"

    def _suggest_action(self, lead_score: float, buying_intent: Dict, urgency: Dict) -> str:
        """Suggest next action for sales team"""
        if lead_score >= 70 and buying_intent['level'] == "High":
            return "🔥 Immediate outreach - High priority prospect"
        elif lead_score >= 50 and urgency['level'] in ["High", "Medium"]:
            return "📞 Contact within 24 hours - Good timing"
        elif lead_score >= 30:
            return "📧 Add to nurture campaign - Monitor activity"
        else:
            return "👀 Track for future opportunity"

    def _analyze_budget_indicators(self, text: str) -> Dict[str, Any]:
        """Analyze budget indicators and spending capacity"""
        text_lower = text.lower()
        
        budget_level = "unknown"
        budget_signals = []
        confidence = 0
        
        for level, keywords in self.budget_indicators.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if matches:
                budget_level = level
                budget_signals = matches
                confidence = len(matches) * 0.3
                break
        
        # Extract budget amounts using regex
        import re
        budget_amounts = []
        
        # Look for dollar amounts
        dollar_pattern = r'\$([0-9,]+(?:\.[0-9]{2})?)'
        dollar_matches = re.findall(dollar_pattern, text)
        budget_amounts.extend([f"${amount}" for amount in dollar_matches])
        
        # Look for "k" and "million" indicators
        amount_pattern = r'(\d+)\s*(k|thousand|million|m)\b'
        amount_matches = re.findall(amount_pattern, text_lower)
        for amount, unit in amount_matches:
            if unit in ['k', 'thousand']:
                budget_amounts.append(f"${amount}K")
            elif unit in ['million', 'm']:
                budget_amounts.append(f"${amount}M")
        
        return {
            'budget_level': budget_level,
            'budget_signals': budget_signals,
            'specific_amounts': budget_amounts[:3],
            'confidence': min(confidence, 1.0)
        }

    def _analyze_implementation_timeline(self, text: str) -> Dict[str, Any]:
        """Analyze implementation timeline and urgency"""
        text_lower = text.lower()
        
        timeline_category = "unknown"
        timeline_signals = []
        
        for category, keywords in self.timeline_indicators.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if matches:
                timeline_category = category
                timeline_signals = matches
                break
        
        # Extract specific dates/times
        import re
        date_patterns = [
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}\b',
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\bq[1-4]\s+20\d{2}\b'
        ]
        
        specific_dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text_lower)
            specific_dates.extend(matches[:2])
        
        return {
            'timeline_category': timeline_category,
            'timeline_signals': timeline_signals,
            'specific_dates': specific_dates,
            'urgency_score': self._calculate_urgency_score(timeline_category, timeline_signals)
        }

    def _analyze_competitive_mentions(self, text: str) -> Dict[str, Any]:
        """Analyze mentions of competitor tools and solutions"""
        text_lower = text.lower()
        
        mentioned_competitors = []
        competitor_context = {}
        
        for competitor in self.competitor_keywords:
            if competitor.lower() in text_lower:
                mentioned_competitors.append(competitor)
                
                # Extract context around competitor mention
                sentences = text.split('.')
                for sentence in sentences:
                    if competitor.lower() in sentence.lower():
                        context = sentence.strip()[:150]
                        
                        # Determine sentiment about competitor
                        negative_words = ['hate', 'sucks', 'terrible', 'awful', 'bad', 'worse', 'problems', 'issues']
                        positive_words = ['love', 'great', 'amazing', 'perfect', 'excellent', 'works well']
                        
                        sentiment = "neutral"
                        if any(word in context.lower() for word in negative_words):
                            sentiment = "negative"
                        elif any(word in context.lower() for word in positive_words):
                            sentiment = "positive"
                        
                        competitor_context[competitor] = {
                            'context': context,
                            'sentiment': sentiment
                        }
                        break
        
        return {
            'mentioned_competitors': mentioned_competitors,
            'competitor_count': len(mentioned_competitors),
            'competitor_context': competitor_context,
            'competitive_pressure': self._assess_competitive_pressure(mentioned_competitors, competitor_context)
        }

    def _classify_advanced_industry(self, text: str) -> Dict[str, Any]:
        """Advanced industry classification with sub-categories"""
        text_lower = text.lower()
        
        industry_matches = {}
        confidence_scores = {}
        
        for industry, keywords in self.advanced_industry_keywords.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if matches:
                industry_matches[industry] = matches
                confidence_scores[industry] = len(matches) * 0.2
        
        # Determine primary industry
        primary_industry = "unknown"
        if confidence_scores:
            primary_industry = max(confidence_scores.keys(), key=lambda k: confidence_scores[k])
        
        return {
            'primary_industry': primary_industry,
            'industry_matches': industry_matches,
            'confidence_scores': confidence_scores,
            'industry_signals': industry_matches.get(primary_industry, [])
        }

    def _calculate_urgency_score(self, timeline_category: str, signals: List[str]) -> float:
        """Calculate urgency score based on timeline"""
        if timeline_category == "immediate":
            return 1.0
        elif timeline_category == "short_term":
            return 0.8
        elif timeline_category == "medium_term":
            return 0.5
        elif timeline_category == "long_term":
            return 0.3
        else:
            return 0.1

    def _assess_competitive_pressure(self, competitors: List[str], context: Dict) -> str:
        """Assess competitive pressure level"""
        if len(competitors) == 0:
            return "low"
        
        negative_mentions = sum(1 for comp in competitors 
                              if context.get(comp, {}).get('sentiment') == 'negative')
        
        if negative_mentions >= 2:
            return "high"
        elif negative_mentions == 1 or len(competitors) >= 3:
            return "medium"
        else:
            return "low"

    def _generate_enhanced_sales_notes(self, text: str, buying_intent: Dict, pain_points: List, 
                                     budget_analysis: Dict, competitive_intel: Dict) -> str:
        """Generate enhanced actionable sales notes"""
        notes = []
        
        if buying_intent['level'] in ["High", "Medium"]:
            notes.append(f"Buying signals: {', '.join(buying_intent['signals'][:2])}")
        
        if pain_points:
            top_pain = pain_points[0]
            notes.append(f"Pain point: {top_pain['category']} issues")
        
        if budget_analysis['budget_level'] != 'unknown':
            budget_note = f"Budget: {budget_analysis['budget_level']}"
            if budget_analysis['specific_amounts']:
                budget_note += f" ({budget_analysis['specific_amounts'][0]})"
            notes.append(budget_note)
        
        if competitive_intel['mentioned_competitors']:
            comp_note = f"Uses: {', '.join(competitive_intel['mentioned_competitors'][:2])}"
            if competitive_intel['competitive_pressure'] == 'high':
                comp_note += " (dissatisfied)"
            notes.append(comp_note)
        
        # Extract key quotes
        sentences = text.split('.')
        relevant_quotes = []
        for sentence in sentences[:5]:
            if any(keyword in sentence.lower() for keyword in self.buying_intent_keywords[:10]):
                relevant_quotes.append(sentence.strip()[:80] + "...")
                break
        
        if relevant_quotes:
            notes.append(f"Quote: {relevant_quotes[0]}")
        
        return " | ".join(notes) if notes else "No specific sales notes available"

    def _generate_sales_notes(self, text: str, buying_intent: Dict, pain_points: List) -> str:
        """Generate actionable sales notes"""
        notes = []
        
        if buying_intent['level'] in ["High", "Medium"]:
            notes.append(f"🎯 Buying signals: {', '.join(buying_intent['signals'][:3])}")
        
        if pain_points:
            top_pain = pain_points[0]
            notes.append(f"😣 Key pain point: {top_pain['category']} issues")
        
        # Extract key quotes
        sentences = text.split('.')
        relevant_quotes = []
        for sentence in sentences[:5]:  # Check first 5 sentences
            if any(keyword in sentence.lower() for keyword in self.buying_intent_keywords[:10]):
                relevant_quotes.append(sentence.strip()[:100] + "...")
                break
        
        if relevant_quotes:
            notes.append(f"💬 Key quote: {relevant_quotes[0]}")
        
        return " | ".join(notes) if notes else "No specific sales notes available"

    def _create_empty_lead_analysis(self) -> Dict[str, Any]:
        """Create empty analysis for invalid content"""
        return {
            'lead_score': 0,
            'buying_intent': {'level': 'None', 'confidence': 0, 'signals': [], 'signal_count': 0},
            'business_context': {'business_size': 'Unknown', 'industry': 'Unknown', 'decision_maker_signals': []},
            'pain_points': [],
            'urgency_level': {'level': 'Low', 'timeline': 'No timeline', 'signals': []},
            'contact_hints': {'reddit_username': '', 'emails': [], 'companies_mentioned': [], 'social_links': [], 'has_contact_info': False},
            'budget_analysis': {'budget_level': 'unknown', 'budget_signals': [], 'specific_amounts': [], 'confidence': 0},
            'timeline_analysis': {'timeline_category': 'unknown', 'timeline_signals': [], 'specific_dates': [], 'urgency_score': 0},
            'competitive_intel': {'mentioned_competitors': [], 'competitor_count': 0, 'competitor_context': {}, 'competitive_pressure': 'low'},
            'enhanced_industry': {'primary_industry': 'unknown', 'industry_matches': {}, 'confidence_scores': {}, 'industry_signals': []},
            'lead_quality': 'Low Quality',
            'recommended_action': 'Track for future opportunity',
            'sales_notes': 'No content to analyze'
        }