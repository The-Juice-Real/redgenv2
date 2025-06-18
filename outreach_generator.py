import re
import random
from typing import Dict, List, Any, Optional

class OutreachGenerator:
    """Generate personalized, nonchalant outreach messages for Reddit leads"""
    
    def __init__(self):
        """Initialize with message templates and personalization strategies"""
        
        # Base message templates organized by lead type and context
        self.message_templates = {
            'business_owner': [
                "Interesting post about {topic}. We help {industry} businesses with {service_area} - mind if I share a quick case study?",
                "Saw your {context} - really solid approach. We've helped similar {industry} companies with {service_area}. Worth a quick chat?",
                "Your {topic} post caught my attention. We work with {industry} businesses on {service_area}. Would love to share what we've learned.",
                "Great insights on {topic}. We specialize in {service_area} for {industry} companies. Happy to share some strategies that might help.",
                "Really appreciate your perspective on {topic}. We've seen great results helping {industry} businesses with {service_area}. Open to a brief conversation?"
            ],
            
            'startup_founder': [
                "Love the {topic} approach! We help startups scale {service_area} - would you be interested in seeing how we've helped similar companies?",
                "Your {context} resonates with a lot of startups we work with. We specialize in {service_area} - mind if I share a relevant case study?",
                "Solid points on {topic}. We've helped several startups with {service_area} challenges. Worth connecting to share insights?",
                "Your {topic} post shows you get it. We work with startups on {service_area} - happy to share what's been working for similar companies.",
                "Great thread on {topic}. We help startups with {service_area} - would love to share some strategies that might be relevant."
            ],
            
            'pain_point_seeker': [
                "Saw your post about {pain_point} - we actually specialize in solving this for {industry} companies. Mind if I share how we've helped others?",
                "Your {pain_point} challenge is something we see a lot. We've developed solutions for {industry} businesses. Worth a quick conversation?",
                "Really relate to your {pain_point} situation. We help {industry} companies with exactly this - happy to share some insights.",
                "Your {topic} post highlights a common issue. We've helped {industry} businesses tackle {pain_point} - would love to share what works.",
                "Appreciate you sharing about {pain_point}. We work with {industry} companies on this exact challenge. Open to a brief chat?"
            ],
            
            'tech_focused': [
                "Nice post on {topic}. We help {industry} companies optimize their {tech_area} stack - would you be interested in seeing some results?",
                "Your {context} caught my attention. We specialize in {tech_area} solutions for {industry} businesses. Worth connecting?",
                "Solid insights on {topic}. We've helped similar companies with {tech_area} challenges - happy to share what we've learned.",
                "Great perspective on {topic}. We work with {industry} businesses on {tech_area} optimization. Mind if I share a case study?",
                "Really valuable post about {topic}. We help companies with {tech_area} solutions - would love to share some relevant strategies."
            ],
            
            'general_business': [
                "Interesting perspective on {topic}. We help {industry} businesses with {service_area} - would you be open to a quick conversation?",
                "Your {context} resonates with many of our clients. We specialize in {service_area} - mind if I share how we've helped similar businesses?",
                "Great post about {topic}. We work with {industry} companies on {service_area} - happy to share some insights that might help.",
                "Really appreciate your take on {topic}. We've seen success helping {industry} businesses with {service_area}. Worth connecting?",
                "Solid points on {topic}. We help companies with {service_area} challenges - would love to share what's been working."
            ],
            
            'sourcing_specialist': [
                "Saw your post about {topic} - we actually specialize in China sourcing for {industry} businesses. Mind if I share how we've helped others reduce costs?",
                "Your {pain_point} situation is exactly what we solve for ecommerce brands. We handle everything from supplier vetting to quality control. Worth a quick chat?",
                "Really relate to your supplier challenges. We're sourcing agents who help businesses find reliable manufacturers in China. Happy to share some insights.",
                "Your post about {topic} highlights common sourcing issues. We've helped {industry} companies navigate China manufacturing successfully. Open to connecting?",
                "Appreciate you sharing about {pain_point}. We specialize in China sourcing and quality control for businesses like yours. Would love to help."
            ],
            
            'manufacturing_expert': [
                "Nice post on {topic}. We help companies optimize their manufacturing in China - significant cost savings possible. Interested in seeing some results?",
                "Your manufacturing challenges caught my attention. We specialize in China production oversight and quality assurance. Worth connecting?",
                "Solid insights on {topic}. We've helped similar businesses reduce manufacturing costs by 30-50% through China sourcing. Happy to share details.",
                "Great perspective on production issues. We manage manufacturing partnerships in China for {industry} companies. Mind if I share a case study?",
                "Really valuable post about {topic}. We help businesses scale production in China while maintaining quality. Would love to share strategies."
            ],
            
            'supplier_consultant': [
                "Saw your supplier issues post - we actually audit and verify manufacturers in China for businesses. Could save you major headaches.",
                "Your {pain_point} with suppliers is something we solve daily. We're on-ground in China doing factory audits and quality control. Worth discussing?",
                "Really understand your supplier reliability concerns. We provide boots-on-ground sourcing support in China. Happy to share how we ensure quality.",
                "Your post about {topic} shows you need trustworthy suppliers. We've vetted thousands of Chinese manufacturers. Open to sharing our process?",
                "Appreciate your honesty about supplier challenges. We specialize in finding and managing reliable China suppliers for growing businesses."
            ]
        }
        
        # Follow-up templates for DM conversations
        self.follow_up_templates = [
            "Thanks for connecting! Here's that {resource_type} I mentioned: {link}. Would love to hear your thoughts.",
            "Appreciate you reaching out! I sent over that {resource_type} about {topic}. Happy to discuss how it might apply to your situation.",
            "Great connecting! Here's the {resource_type} we discussed. Let me know if you'd like to explore how this could work for your business.",
            "Thanks for the DM! I've shared that {resource_type} about {topic}. Would be happy to walk through how we've helped similar companies.",
            "Nice chatting! Here's the {resource_type} on {topic}. Feel free to ask any questions about implementation."
        ]
        
        # Context extractors for personalization
        self.business_indicators = {
            'saas': ['software', 'saas', 'platform', 'api', 'app', 'digital'],
            'ecommerce': ['store', 'shop', 'product', 'ecommerce', 'retail', 'sales', 'amazon fba', 'shopify', 'dropship'],
            'consulting': ['consultant', 'advisory', 'services', 'consulting', 'strategy'],
            'agency': ['agency', 'marketing', 'design', 'creative', 'advertising'],
            'restaurant': ['restaurant', 'food', 'dining', 'cafe', 'kitchen'],
            'real_estate': ['real estate', 'property', 'homes', 'realtor', 'broker'],
            'healthcare': ['health', 'medical', 'clinic', 'doctor', 'patient'],
            'education': ['education', 'school', 'training', 'course', 'learning'],
            'manufacturing': ['manufacturing', 'factory', 'production', 'assembly', 'industrial'],
            'sourcing': ['sourcing', 'supplier', 'vendor', 'procurement', 'import', 'export', 'china', 'alibaba']
        }
        
        self.pain_point_patterns = {
            'lead_generation': ['leads', 'customers', 'sales', 'conversion', 'prospects'],
            'marketing': ['marketing', 'traffic', 'visibility', 'brand', 'promotion'],
            'automation': ['manual', 'time', 'efficiency', 'automate', 'streamline'],
            'scaling': ['growth', 'scale', 'expand', 'bigger', 'volume'],
            'technology': ['tech', 'software', 'system', 'platform', 'integration'],
            'supplier_issues': ['supplier', 'quality', 'reliability', 'communication', 'delivery'],
            'cost_reduction': ['expensive', 'cost', 'pricing', 'margin', 'budget'],
            'quality_control': ['quality', 'defects', 'inspection', 'standards', 'compliance'],
            'sourcing_help': ['find supplier', 'manufacturer', 'factory', 'sourcing agent', 'procurement']
        }

    def generate_outreach_message(self, lead_data: Dict[str, Any], service_description: str) -> Dict[str, Any]:
        """Generate personalized outreach message for a lead"""
        
        # Extract context from lead
        context = self._extract_lead_context(lead_data)
        
        # Determine message type based on lead characteristics
        message_type = self._determine_message_type(lead_data, context)
        
        # Select and personalize template
        template = self._select_template(message_type, context)
        personalized_message = self._personalize_message(template, context, service_description)
        
        # Generate follow-up suggestions
        follow_up = self._generate_follow_up(context, service_description)
        
        return {
            'primary_message': personalized_message,
            'follow_up_message': follow_up,
            'context_used': context,
            'message_type': message_type,
            'personalization_score': self._calculate_personalization_score(context),
            'tone': 'professional_casual',
            'call_to_action': 'dm_conversation',
            'timing_suggestion': self._suggest_timing(lead_data)
        }

    def _extract_lead_context(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant context from lead data for personalization"""
        
        full_text = f"{lead_data.get('title', '')} {lead_data.get('content', '')}".lower()
        
        context = {
            'topic': self._extract_main_topic(lead_data),
            'industry': self._identify_industry(full_text),
            'pain_points': self._identify_pain_points(full_text),
            'business_type': self._identify_business_type(full_text),
            'context_type': self._identify_context_type(lead_data),
            'urgency_level': self._assess_urgency(full_text),
            'budget_indicators': self._identify_budget_signals(full_text),
            'author': lead_data.get('author', 'there'),
            'subreddit': lead_data.get('source_subreddit', 'business')
        }
        
        return context

    def _extract_main_topic(self, lead_data: Dict[str, Any]) -> str:
        """Extract the main topic from post title and content"""
        
        title = lead_data.get('title', '').lower()
        
        # Common business topics
        topic_keywords = {
            'marketing strategy': ['marketing', 'strategy', 'campaign', 'ads'],
            'business growth': ['growth', 'scaling', 'expand', 'revenue'],
            'lead generation': ['leads', 'customers', 'prospects', 'conversion'],
            'automation': ['automate', 'efficiency', 'workflow', 'system'],
            'website optimization': ['website', 'conversion', 'optimization', 'landing'],
            'social media': ['social', 'instagram', 'facebook', 'content'],
            'startup challenges': ['startup', 'founder', 'entrepreneur', 'launch'],
            'technology solutions': ['tech', 'software', 'platform', 'integration']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in title for keyword in keywords):
                return topic
                
        return 'business strategy'

    def _identify_industry(self, text: str) -> str:
        """Identify the industry from text content"""
        
        for industry, keywords in self.business_indicators.items():
            if any(keyword in text for keyword in keywords):
                return industry
                
        return 'business'

    def _identify_pain_points(self, text: str) -> List[str]:
        """Identify pain points mentioned in the text"""
        
        pain_points = []
        for pain_point, keywords in self.pain_point_patterns.items():
            if any(keyword in text for keyword in keywords):
                pain_points.append(pain_point)
                
        return pain_points[:2]  # Return top 2 pain points

    def _identify_business_type(self, text: str) -> str:
        """Identify if it's a startup, established business, etc."""
        
        if any(word in text for word in ['startup', 'co-founder', 'launch', 'mvp']):
            return 'startup'
        elif any(word in text for word in ['agency', 'consultant', 'freelance']):
            return 'service_provider'
        elif any(word in text for word in ['company', 'business', 'firm', 'corporation']):
            return 'established_business'
        else:
            return 'general_business'

    def _identify_context_type(self, lead_data: Dict[str, Any]) -> str:
        """Identify the type of post context"""
        
        title = lead_data.get('title', '').lower()
        
        if any(word in title for word in ['help', 'advice', 'how to', 'need']):
            return 'seeking_help'
        elif any(word in title for word in ['success', 'achieved', 'results', 'case study']):
            return 'sharing_success'
        elif any(word in title for word in ['question', 'ask', 'thoughts', 'opinion']):
            return 'asking_question'
        else:
            return 'general_discussion'

    def _assess_urgency(self, text: str) -> str:
        """Assess urgency level from text indicators"""
        
        high_urgency = ['urgent', 'asap', 'quickly', 'immediately', 'deadline', 'struggling']
        medium_urgency = ['soon', 'need', 'looking for', 'help', 'problem']
        
        if any(word in text for word in high_urgency):
            return 'high'
        elif any(word in text for word in medium_urgency):
            return 'medium'
        else:
            return 'low'

    def _identify_budget_signals(self, text: str) -> List[str]:
        """Identify budget-related signals in the text"""
        
        budget_indicators = []
        
        if any(word in text for word in ['budget', 'invest', 'spend', 'cost', 'price']):
            budget_indicators.append('budget_conscious')
        if any(word in text for word in ['revenue', 'profit', 'sales', 'income']):
            budget_indicators.append('revenue_generating')
        if any(word in text for word in ['funding', 'raised', 'investors']):
            budget_indicators.append('funded')
            
        return budget_indicators

    def _determine_message_type(self, lead_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Determine the best message template type for this lead"""
        
        business_type = context['business_type']
        context_type = context['context_type']
        industry = context['industry']
        
        # Check for sourcing-specific indicators first
        text = f"{lead_data.get('title', '')} {lead_data.get('content', '')}".lower()
        
        # Sourcing-specific message types
        if any(keyword in text for keyword in ['supplier', 'manufacturer', 'factory', 'quality control', 'inspection']):
            return 'supplier_consultant'
        elif any(keyword in text for keyword in ['manufacturing', 'production', 'oem', 'odm', 'tooling']):
            return 'manufacturing_expert'
        elif any(keyword in text for keyword in ['china sourcing', 'sourcing', 'procurement', 'alibaba', 'china', 'import']):
            return 'sourcing_specialist'
        
        # General business types
        elif business_type == 'startup':
            return 'startup_founder'
        elif context_type == 'seeking_help' and context['pain_points']:
            return 'pain_point_seeker'
        elif industry in ['saas', 'tech', 'software']:
            return 'tech_focused'
        elif business_type in ['service_provider', 'established_business']:
            return 'business_owner'
        else:
            return 'general_business'

    def _select_template(self, message_type: str, context: Dict[str, Any]) -> str:
        """Select appropriate template based on context"""
        
        templates = self.message_templates.get(message_type, self.message_templates['general_business'])
        return random.choice(templates)

    def _personalize_message(self, template: str, context: Dict[str, Any], service_description: str) -> str:
        """Personalize the template with context-specific information"""
        
        # Extract service area from description
        service_area = self._extract_service_area(service_description)
        
        # Prepare personalization variables
        personalization_vars = {
            'topic': context['topic'],
            'industry': context['industry'],
            'pain_point': context['pain_points'][0] if context['pain_points'] else 'business challenges',
            'service_area': service_area,
            'context': self._format_context_reference(context),
            'tech_area': self._extract_tech_area(service_description)
        }
        
        # Apply personalization
        try:
            personalized = template.format(**personalization_vars)
        except KeyError:
            # Fallback if template has missing variables
            personalized = template.replace('{topic}', context['topic'])
            personalized = personalized.replace('{industry}', context['industry'])
            personalized = personalized.replace('{service_area}', service_area)
        
        return personalized

    def _extract_service_area(self, service_description: str) -> str:
        """Extract the main service area from description"""
        
        desc_lower = service_description.lower()
        
        service_areas = {
            'web design': ['web design', 'website', 'web development'],
            'digital marketing': ['marketing', 'ads', 'social media', 'seo'],
            'automation': ['automation', 'workflow', 'integration'],
            'consulting': ['consulting', 'advisory', 'strategy'],
            'app development': ['app', 'mobile', 'development'],
            'lead generation': ['leads', 'prospect', 'sales']
        }
        
        for area, keywords in service_areas.items():
            if any(keyword in desc_lower for keyword in keywords):
                return area
                
        return 'business solutions'

    def _extract_tech_area(self, service_description: str) -> str:
        """Extract technology focus area"""
        
        desc_lower = service_description.lower()
        
        if any(word in desc_lower for word in ['web', 'website', 'frontend']):
            return 'web development'
        elif any(word in desc_lower for word in ['mobile', 'app', 'ios', 'android']):
            return 'mobile development'
        elif any(word in desc_lower for word in ['automation', 'workflow', 'integration']):
            return 'automation'
        else:
            return 'technology'

    def _format_context_reference(self, context: Dict[str, Any]) -> str:
        """Format a natural reference to the context"""
        
        context_type = context['context_type']
        
        references = {
            'seeking_help': 'question',
            'sharing_success': 'success story',
            'asking_question': 'post',
            'general_discussion': 'insights'
        }
        
        return references.get(context_type, 'post')

    def _generate_follow_up(self, context: Dict[str, Any], service_description: str) -> str:
        """Generate follow-up message for DM conversation"""
        
        template = random.choice(self.follow_up_templates)
        
        resource_types = ['case study', 'strategy guide', 'examples', 'insights', 'results']
        resource_type = random.choice(resource_types)
        
        topic = context['topic']
        
        return template.format(
            resource_type=resource_type,
            topic=topic,
            link='[relevant case study/resource]'
        )

    def _calculate_personalization_score(self, context: Dict[str, Any]) -> float:
        """Calculate how well the message can be personalized"""
        
        score = 0.0
        
        # Add points for available context
        if context['industry'] != 'business':
            score += 0.3
        if context['pain_points']:
            score += 0.3
        if context['business_type'] != 'general_business':
            score += 0.2
        if context['urgency_level'] != 'low':
            score += 0.1
        if context['budget_indicators']:
            score += 0.1
            
        return min(score, 1.0)

    def _suggest_timing(self, lead_data: Dict[str, Any]) -> str:
        """Suggest optimal timing for outreach"""
        
        lead_score = lead_data.get('lead_score', 0)
        urgency = lead_data.get('urgency', {}).get('level', 'low')
        
        if lead_score >= 80 or urgency == 'high':
            return 'immediate'
        elif lead_score >= 60:
            return 'within_24_hours'
        else:
            return 'within_3_days'

    def generate_bulk_outreach(self, leads: List[Dict[str, Any]], service_description: str) -> List[Dict[str, Any]]:
        """Generate outreach messages for multiple leads"""
        
        outreach_data = []
        
        for lead in leads:
            try:
                outreach = self.generate_outreach_message(lead, service_description)
                outreach_data.append({
                    'lead_id': lead.get('author', 'unknown'),
                    'lead_data': lead,
                    'outreach': outreach
                })
            except Exception as e:
                # Handle any errors gracefully
                outreach_data.append({
                    'lead_id': lead.get('author', 'unknown'),
                    'lead_data': lead,
                    'outreach': {
                        'primary_message': f"Interesting insights! We help businesses with {service_description.lower()}. Worth connecting?",
                        'error': str(e)
                    }
                })
                
        return outreach_data

    def get_outreach_statistics(self, outreach_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate statistics about outreach message generation"""
        
        total_messages = len(outreach_data)
        
        personalization_scores = []
        message_types = []
        timing_distribution = {}
        
        for item in outreach_data:
            outreach = item.get('outreach', {})
            if 'personalization_score' in outreach:
                personalization_scores.append(outreach['personalization_score'])
            if 'message_type' in outreach:
                message_types.append(outreach['message_type'])
            if 'timing_suggestion' in outreach:
                timing = outreach['timing_suggestion']
                timing_distribution[timing] = timing_distribution.get(timing, 0) + 1
        
        return {
            'total_messages_generated': total_messages,
            'average_personalization_score': sum(personalization_scores) / len(personalization_scores) if personalization_scores else 0,
            'message_type_distribution': {msg_type: message_types.count(msg_type) for msg_type in set(message_types)},
            'timing_distribution': timing_distribution,
            'high_priority_leads': len([item for item in outreach_data if item.get('outreach', {}).get('timing_suggestion') == 'immediate'])
        }