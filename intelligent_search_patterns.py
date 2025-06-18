from typing import Dict, List, Any, Tuple
import re
from collections import defaultdict

class IntelligentSearchPatterns:
    """Advanced pattern recognition for Reddit lead discovery"""
    
    def __init__(self):
        self.intent_pattern_library = {
            # Social Media Posting Service Patterns
            'social_media_growth': {
                'patterns': [
                    r'\b(?:grow|increase|boost)\s+(?:followers|engagement|reach)\b',
                    r'\b(?:social media|instagram|tiktok|youtube)\s+(?:management|growth|strategy)\b',
                    r'\b(?:content|posting)\s+(?:schedule|calendar|consistency)\b',
                    r'\balgorithm\s+(?:changes|updates|struggles)\b',
                    r'\b(?:brand|influencer)\s+(?:partnerships|collaborations)\b'
                ],
                'intent_score': 90,
                'priority': 'high'
            },
            'content_creation_burnout': {
                'patterns': [
                    r'\b(?:burnt out|exhausted|overwhelmed)\s+(?:creating|posting|content)\b',
                    r'\b(?:need help|looking for)\s+(?:content creator|social media manager)\b',
                    r'\b(?:posting|content)\s+(?:consistency|regularly|daily)\s+(?:struggle|hard|difficult)\b',
                    r'\b(?:running out|lack)\s+(?:ideas|content|creativity)\b'
                ],
                'intent_score': 85,
                'priority': 'immediate'
            },
            'monetization_ready': {
                'patterns': [
                    r'\b(?:monetize|make money|revenue)\s+(?:from|through)\s+(?:social media|content)\b',
                    r'\b(?:brand deals|sponsorships|partnerships)\b',
                    r'\b(?:affiliate marketing|product placement)\b',
                    r'\b(?:10k|100k|million)\s+(?:followers|subscribers|views)\b'
                ],
                'intent_score': 95,
                'priority': 'immediate'
            },
            
            # Video Editing Service Patterns
            'video_editing_overwhelm': {
                'patterns': [
                    r'\b(?:video editing|post production)\s+(?:taking|consuming)\s+(?:too long|forever|hours)\b',
                    r'\b(?:need|looking for|want)\s+(?:video editor|editing help)\b',
                    r'\b(?:premiere|after effects|davinci)\s+(?:crashing|slow|problems)\b',
                    r'\b(?:render|export)\s+(?:time|speed|taking forever)\b'
                ],
                'intent_score': 88,
                'priority': 'high'
            },
            'professional_video_needs': {
                'patterns': [
                    r'\b(?:4k|8k|high resolution)\s+(?:video|footage|editing)\b',
                    r'\b(?:color grading|color correction)\s+(?:help|services|needed)\b',
                    r'\b(?:wedding|event|corporate)\s+(?:video|videography)\b',
                    r'\b(?:multi-camera|multicam)\s+(?:editing|sync)\b',
                    r'\b(?:motion graphics|after effects|animation)\b'
                ],
                'intent_score': 92,
                'priority': 'high'
            },
            'video_turnaround_pressure': {
                'patterns': [
                    r'\b(?:urgent|rush|asap|deadline)\s+(?:video|editing)\b',
                    r'\b(?:client|project)\s+(?:deadline|due|waiting)\b',
                    r'\b(?:same day|24 hour|quick)\s+(?:turnaround|editing)\b',
                    r'\b(?:event|wedding)\s+(?:tomorrow|this week|soon)\b'
                ],
                'intent_score': 95,
                'priority': 'immediate'
            },
            
            # Drone Trading/Selling Service Patterns
            'drone_commercial_use': {
                'patterns': [
                    r'\b(?:commercial|business)\s+(?:drone|drones|uav)\b',
                    r'\b(?:part 107|faa certification|drone license)\b',
                    r'\b(?:real estate|aerial|inspection)\s+(?:photography|videography)\b',
                    r'\b(?:agriculture|mapping|surveying)\s+(?:drone|drones)\b',
                    r'\b(?:fleet|multiple|several)\s+(?:drones|units)\b'
                ],
                'intent_score': 95,
                'priority': 'immediate'
            },
            'drone_repair_upgrade': {
                'patterns': [
                    r'\b(?:drone|dji|phantom|mavic)\s+(?:repair|broken|crashed|damaged)\b',
                    r'\b(?:gimbal|camera|motor|propeller)\s+(?:replacement|broken|damaged)\b',
                    r'\b(?:upgrade|modify|customize)\s+(?:drone|drones)\b',
                    r'\b(?:parts|components|accessories)\s+(?:needed|looking for)\b'
                ],
                'intent_score': 85,
                'priority': 'high'
            },
            'drone_investment_scaling': {
                'patterns': [
                    r'\b(?:buying|purchasing|investing in)\s+(?:multiple|fleet of)\s+(?:drones|units)\b',
                    r'\b(?:expanding|scaling|growing)\s+(?:drone|aerial)\s+(?:business|operation)\b',
                    r'\b(?:insurance|liability)\s+(?:drone|aerial|commercial)\b',
                    r'\b(?:training|certification|education)\s+(?:drone|pilot|operator)\b'
                ],
                'intent_score': 90,
                'priority': 'high'
            },
            
            # Universal High-Value Patterns
            'explicit_sourcing': {
                'patterns': [
                    r'\b(?:need|looking for|searching for)\s+(?:supplier|manufacturer|factory)\b',
                    r'\bchina\s+(?:sourcing|manufacturing|supplier)\b',
                    r'\b(?:alibaba|made in china|sourcing agent)\b',
                    r'\bmanufacturing\s+(?:in china|overseas|abroad)\b'
                ],
                'intent_score': 95,
                'priority': 'immediate'
            },
            'quality_issues': {
                'patterns': [
                    r'\b(?:quality|defective|poor|terrible)\s+(?:products|items|goods)\b',
                    r'\bsupplier\s+(?:problems|issues|scam)\b',
                    r'\b(?:received|got)\s+(?:wrong|damaged|fake)\s+product\b'
                ],
                'intent_score': 85,
                'priority': 'high'
            },
            'cost_optimization': {
                'patterns': [
                    r'\b(?:reduce|lower|cheaper)\s+(?:costs|pricing|price)\b',
                    r'\bsave\s+money\s+on\s+(?:manufacturing|production)\b',
                    r'\bbetter\s+(?:pricing|rates|deal)\b'
                ],
                'intent_score': 75,
                'priority': 'medium'
            },
            'scaling_production': {
                'patterns': [
                    r'\b(?:scale|increase|expand)\s+(?:production|manufacturing)\b',
                    r'\bbulk\s+(?:orders|production|manufacturing)\b',
                    r'\bhigh\s+volume\s+(?:production|orders)\b'
                ],
                'intent_score': 80,
                'priority': 'high'
            }
        }
        
        self.business_context_patterns = {
            'startup_indicators': [
                r'\bstartup\b', r'\bbootstrap\b', r'\bfounding\b', r'\bearly stage\b',
                r'\bpre-revenue\b', r'\bmvp\b', r'\bminimum viable product\b'
            ],
            'ecommerce_indicators': [
                r'\becommerce\b', r'\be-commerce\b', r'\bonline store\b', r'\bshopify\b',
                r'\bamazon\s+(?:fba|seller)\b', r'\betsy\b', r'\bebay\b'
            ],
            'enterprise_indicators': [
                r'\benterprise\b', r'\bcorporation\b', r'\bfortune\s+\d+\b',
                r'\bmultinational\b', r'\bglobal\s+company\b'
            ]
        }
        
        self.urgency_detection_patterns = {
            'immediate': [
                r'\burgent\b', r'\basap\b', r'\bimmediately\b', r'\bright now\b',
                r'\btoday\b', r'\bthis week\b'
            ],
            'deadline_driven': [
                r'\bdeadline\b', r'\bby\s+(?:end of|next)\b', r'\bbefore\s+\w+\b',
                r'\blaunch\s+date\b', r'\btime\s+sensitive\b'
            ],
            'budget_cycle': [
                r'\bq[1-4]\b', r'\bquarter\b', r'\bfiscal\s+year\b',
                r'\bbudget\s+(?:approved|allocated)\b'
            ]
        }
    
    def analyze_search_intent(self, content: str, title: str = '') -> Dict[str, Any]:
        """Advanced intent analysis with pattern matching"""
        
        full_text = f"{title} {content}".lower()
        detected_intents = []
        max_intent_score = 0
        primary_intent = None
        
        for intent_type, intent_data in self.intent_pattern_library.items():
            for pattern in intent_data['patterns']:
                if re.search(pattern, full_text):
                    detected_intents.append({
                        'intent': intent_type,
                        'score': intent_data['intent_score'],
                        'priority': intent_data['priority'],
                        'pattern_matched': pattern
                    })
                    
                    if intent_data['intent_score'] > max_intent_score:
                        max_intent_score = intent_data['intent_score']
                        primary_intent = intent_type
                    break
        
        return {
            'detected_intents': detected_intents,
            'primary_intent': primary_intent,
            'intent_confidence': max_intent_score,
            'business_context': self._detect_business_context(full_text),
            'urgency_level': self._detect_urgency(full_text),
            'qualification_score': self._calculate_qualification_score(detected_intents, full_text)
        }
    
    def _detect_business_context(self, text: str) -> Dict[str, Any]:
        """Detect business context and company size"""
        
        context = {
            'business_type': 'unknown',
            'size_estimate': 'unknown',
            'industry_indicators': []
        }
        
        for business_type, patterns in self.business_context_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    context['business_type'] = business_type.replace('_indicators', '')
                    break
        
        # Size estimation based on language patterns
        if any(term in text for term in ['enterprise', 'corporation', 'large company']):
            context['size_estimate'] = 'large'
        elif any(term in text for term in ['startup', 'small business', 'growing']):
            context['size_estimate'] = 'small_medium'
        elif any(term in text for term in ['solo', 'freelancer', 'one person']):
            context['size_estimate'] = 'micro'
        
        return context
    
    def _detect_urgency(self, text: str) -> Dict[str, Any]:
        """Detect urgency and timing indicators"""
        
        urgency_data = {
            'level': 'low',
            'indicators': [],
            'estimated_timeline': 'long_term'
        }
        
        for urgency_type, patterns in self.urgency_detection_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    urgency_data['indicators'].append(urgency_type)
                    
                    if urgency_type == 'immediate':
                        urgency_data['level'] = 'high'
                        urgency_data['estimated_timeline'] = 'immediate'
                    elif urgency_type == 'deadline_driven':
                        urgency_data['level'] = 'medium'
                        urgency_data['estimated_timeline'] = 'short_term'
                    break
        
        return urgency_data
    
    def _calculate_qualification_score(self, detected_intents: List[Dict], text: str) -> float:
        """Calculate overall qualification score"""
        
        base_score = 0
        
        # Intent scoring
        if detected_intents:
            max_intent_score = max(intent['score'] for intent in detected_intents)
            base_score += max_intent_score * 0.4
        
        # Content quality scoring
        word_count = len(text.split())
        if word_count > 100:
            base_score += 20
        elif word_count > 50:
            base_score += 15
        elif word_count > 20:
            base_score += 10
        
        # Professional language indicators
        professional_terms = ['solution', 'requirements', 'specifications', 'strategy', 'implementation']
        prof_score = sum(5 for term in professional_terms if term in text)
        base_score += min(prof_score, 25)
        
        # Business context bonus
        business_terms = ['company', 'business', 'organization', 'team']
        if any(term in text for term in business_terms):
            base_score += 15
        
        return min(base_score, 100)
    
    def generate_optimized_search_terms(self, service_description: str, detected_intent: str = None) -> List[str]:
        """Generate optimized search terms based on service and intent"""
        
        base_terms = []
        
        # Intent-based terms
        if detected_intent:
            intent_term_map = {
                # Social Media Posting Service Terms
                'social_media_growth': ['grow followers', 'increase engagement', 'social media strategy', 'content calendar', 'algorithm help'],
                'content_creation_burnout': ['content help', 'social media manager', 'posting consistency', 'content ideas', 'creator burnout'],
                'monetization_ready': ['monetize social media', 'brand partnerships', 'influencer marketing', 'sponsored content', 'affiliate marketing'],
                
                # Video Editing Service Terms
                'video_editing_overwhelm': ['video editor needed', 'editing help', 'post production', 'video editing service', 'premiere help'],
                'professional_video_needs': ['4k video editing', 'color grading', 'wedding videography', 'corporate video', 'motion graphics'],
                'video_turnaround_pressure': ['urgent video editing', 'rush editing', 'quick turnaround', 'same day editing', 'deadline help'],
                
                # Drone Service Terms
                'drone_commercial_use': ['commercial drone', 'drone business', 'aerial photography', 'drone services', 'part 107'],
                'drone_repair_upgrade': ['drone repair', 'dji repair', 'drone parts', 'gimbal repair', 'drone upgrade'],
                'drone_investment_scaling': ['drone fleet', 'commercial drones', 'drone business', 'aerial services', 'drone training'],
                
                # Universal High-Value Terms
                'explicit_sourcing': ['supplier needed', 'manufacturer search', 'sourcing help'],
                'quality_issues': ['quality problems', 'supplier issues', 'product defects'],
                'cost_optimization': ['reduce costs', 'cheaper manufacturing', 'better pricing'],
                'scaling_production': ['scale production', 'bulk manufacturing', 'high volume']
            }
            base_terms.extend(intent_term_map.get(detected_intent, []))
        
        # Service-specific terms
        service_lower = service_description.lower()
        
        # Social Media Posting Services
        if any(term in service_lower for term in ['social media', 'posting', 'content creation', 'instagram', 'tiktok', 'youtube']):
            base_terms.extend([
                'social media help', 'content strategy', 'posting schedule', 'engagement boost',
                'algorithm changes', 'content ideas', 'social media manager', 'brand partnerships',
                'influencer growth', 'monetize content', 'follower growth', 'content calendar'
            ])
        
        # Video Editing Services
        elif any(term in service_lower for term in ['video editing', 'video', 'editing', 'post production']):
            base_terms.extend([
                'video editor', 'editing help', 'premiere pro', 'after effects', 'color grading',
                'video production', 'wedding video', 'youtube editing', 'corporate video',
                'motion graphics', 'render time', 'video turnaround', 'editing workflow'
            ])
        
        # Drone Services
        elif any(term in service_lower for term in ['drone', 'drones', 'aerial', 'uav']):
            base_terms.extend([
                'drone services', 'aerial photography', 'commercial drone', 'drone repair',
                'dji drone', 'drone parts', 'part 107', 'drone business', 'aerial videography',
                'drone fleet', 'drone training', 'gimbal repair', 'fpv drone', 'drone upgrade'
            ])
        
        # China Sourcing Services (original)
        elif any(term in service_lower for term in ['sourcing', 'manufacturing', 'supplier']):
            base_terms.extend(['china sourcing', 'supplier vetting', 'manufacturing partner'])
            if 'quality' in service_lower:
                base_terms.extend(['quality control', 'inspection services', 'product testing'])
            if 'logistics' in service_lower:
                base_terms.extend(['shipping from china', 'import logistics', 'customs clearance'])
        
        # Default high-value terms if no specific service detected
        else:
            base_terms.extend([
                'need help', 'looking for service', 'business solution',
                'professional service', 'service provider', 'business help'
            ])
        
        return list(set(base_terms))  # Remove duplicates
    
    def rank_subreddits_by_intent(self, intent_type: str) -> List[Tuple[str, float]]:
        """Rank subreddits by relevance to detected intent"""
        
        subreddit_scores = defaultdict(float)
        
        # Intent-specific subreddit mapping
        intent_subreddit_map = {
            # Social Media Service Patterns
            'social_media_growth': {
                'socialmedia': 0.99, 'instagram': 0.95, 'tiktok': 0.93, 'youtube': 0.91,
                'influencer': 0.89, 'contentcreator': 0.87, 'marketing': 0.82, 'entrepreneur': 0.78
            },
            'content_creation_burnout': {
                'contentcreator': 0.98, 'youtube': 0.94, 'smallyoutuber': 0.96, 'instagram': 0.88,
                'tiktok': 0.85, 'freelance': 0.83, 'socialmedia': 0.80
            },
            'monetization_ready': {
                'influencer': 0.97, 'youtube': 0.95, 'instagram': 0.92, 'entrepreneur': 0.88,
                'socialmedia': 0.85, 'onlinebusiness': 0.83, 'affiliate': 0.90
            },
            
            # Video Editing Service Patterns
            'video_editing_overwhelm': {
                'videoediting': 0.99, 'youtube': 0.95, 'premiere': 0.93, 'aftereffects': 0.91,
                'videography': 0.89, 'contentcreator': 0.87, 'filmmakers': 0.85
            },
            'professional_video_needs': {
                'videography': 0.98, 'filmmakers': 0.96, 'weddingvideography': 0.94, 'corporatevideo': 0.92,
                'videoediting': 0.90, 'cinematography': 0.88, 'realestate': 0.75
            },
            'video_turnaround_pressure': {
                'videography': 0.97, 'freelance': 0.94, 'weddingvideography': 0.96, 'videoediting': 0.89,
                'events': 0.92, 'youtube': 0.80, 'entrepreneur': 0.75
            },
            
            # Drone Service Patterns
            'drone_commercial_use': {
                'drones': 0.99, 'commercialdrone': 0.98, 'uav': 0.96, 'realestate': 0.92,
                'aerial': 0.90, 'photography': 0.85, 'surveying': 0.88, 'agriculture': 0.86
            },
            'drone_repair_upgrade': {
                'drones': 0.98, 'dji': 0.96, 'phantom': 0.94, 'mavic': 0.92,
                'fpv': 0.90, 'droneracing': 0.88, 'repair': 0.85
            },
            'drone_investment_scaling': {
                'commercialdrone': 0.99, 'drones': 0.95, 'entrepreneur': 0.88, 'smallbusiness': 0.85,
                'realestate': 0.90, 'surveying': 0.92, 'agriculture': 0.89
            },
            
            # Universal High-Value Patterns
            'explicit_sourcing': {
                'entrepreneur': 0.9, 'ecommerce': 0.95, 'amazon': 0.85,
                'alibaba': 0.98, 'sourcing': 0.99, 'manufacturing': 0.92
            },
            'quality_issues': {
                'entrepreneur': 0.8, 'ecommerce': 0.9, 'amazon': 0.95,
                'alibaba': 0.9, 'manufacturing': 0.85
            },
            'cost_optimization': {
                'entrepreneur': 0.85, 'smallbusiness': 0.8, 'ecommerce': 0.9,
                'startups': 0.75, 'manufacturing': 0.88
            },
            'scaling_production': {
                'entrepreneur': 0.9, 'ecommerce': 0.85, 'manufacturing': 0.95,
                'startups': 0.8, 'smallbusiness': 0.75
            }
        }
        
        if intent_type in intent_subreddit_map:
            for subreddit, score in intent_subreddit_map[intent_type].items():
                subreddit_scores[subreddit] = score
        
        # Fallback scoring for general business subreddits
        general_subreddits = {
            'entrepreneur': 0.7, 'smallbusiness': 0.65, 'startups': 0.6,
            'business': 0.5, 'freelance': 0.4
        }
        
        for subreddit, score in general_subreddits.items():
            if subreddit not in subreddit_scores:
                subreddit_scores[subreddit] = score
        
        return sorted(subreddit_scores.items(), key=lambda x: x[1], reverse=True)