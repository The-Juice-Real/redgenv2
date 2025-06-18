"""
Advanced Lead Scoring System V3.0
Implementing deduplication, engagement quality, and manufacturing complexity analysis
"""

import re
import hashlib
from typing import Dict, List, Any, Set, Tuple
from datetime import datetime
import math

class AdvancedLeadScoringV3:
    def __init__(self):
        # Iteration 2 improvements
        self.seen_content_hashes = set()  # For deduplication
        
        # Service-specific complexity patterns
        self.service_complexity_patterns = {
            # Social Media Posting Service Patterns
            'social_media': {
                'micro_influencer': {
                    'patterns': ['1k.*10k.*followers', 'small.*following', 'starting.*out', 'growing.*audience'],
                    'score': 85, 'priority': 'high', 'budget_estimate': '$500-2K'
                },
                'established_creator': {
                    'patterns': ['100k.*followers', 'monetizing', 'brand.*partnerships', 'sponsored.*content'],
                    'score': 95, 'priority': 'immediate', 'budget_estimate': '$2K-10K'
                },
                'agency_scaling': {
                    'patterns': ['multiple.*clients', 'social.*media.*agency', 'team.*of.*creators', 'scaling.*operations'],
                    'score': 98, 'priority': 'immediate', 'budget_estimate': '$5K-25K'
                },
                'burnout_signals': {
                    'patterns': ['burnt.*out', 'overwhelmed.*posting', 'consistency.*struggle', 'need.*help.*content'],
                    'score': 92, 'priority': 'immediate', 'budget_estimate': '$1K-5K'
                }
            },
            # Video Editing Service Patterns
            'video_editing': {
                'professional_needs': {
                    'patterns': ['4k.*video', 'color.*grading', 'wedding.*videography', 'corporate.*video', 'motion.*graphics'],
                    'score': 94, 'priority': 'high', 'budget_estimate': '$2K-15K'
                },
                'urgent_projects': {
                    'patterns': ['rush.*editing', 'urgent.*deadline', 'same.*day.*turnaround', 'asap.*video'],
                    'score': 98, 'priority': 'immediate', 'budget_estimate': '$500-5K'
                },
                'workflow_optimization': {
                    'patterns': ['editing.*workflow', 'render.*time', 'premiere.*crashing', 'storage.*issues'],
                    'score': 88, 'priority': 'high', 'budget_estimate': '$1K-8K'
                },
                'content_creator_volume': {
                    'patterns': ['youtube.*channel', 'daily.*videos', 'content.*creation', 'multiple.*projects'],
                    'score': 91, 'priority': 'high', 'budget_estimate': '$1K-10K'
                }
            },
            # Drone Service Patterns
            'drone_services': {
                'commercial_operations': {
                    'patterns': ['commercial.*drone', 'part.*107', 'aerial.*photography.*business', 'drone.*services.*company'],
                    'score': 96, 'priority': 'immediate', 'budget_estimate': '$5K-50K'
                },
                'fleet_management': {
                    'patterns': ['multiple.*drones', 'drone.*fleet', 'expanding.*operations', 'scaling.*business'],
                    'score': 98, 'priority': 'immediate', 'budget_estimate': '$10K-100K'
                },
                'repair_urgent': {
                    'patterns': ['drone.*crashed', 'gimbal.*broken', 'urgent.*repair', 'parts.*needed.*asap'],
                    'score': 94, 'priority': 'immediate', 'budget_estimate': '$200-2K'
                },
                'professional_upgrade': {
                    'patterns': ['upgrade.*equipment', 'better.*camera', 'professional.*grade', 'high.*end.*drone'],
                    'score': 89, 'priority': 'high', 'budget_estimate': '$2K-20K'
                }
            },
            # Manufacturing complexity (original)
            'manufacturing': {
                'simple': {
                    'patterns': ['simple', 'basic', 'standard', 'off-shelf', 'existing design'],
                    'score': 80, 'priority': 'medium', 'budget_estimate': '$1K-10K'
                },
                'complex': {
                    'patterns': ['engineering', 'design from scratch', 'prototype', 'r&d', 'innovation'],
                    'score': 92, 'priority': 'high', 'budget_estimate': '$10K-100K'
                }
            }
        }
        
        # Budget estimation signals
        self.budget_signals = {
            'micro': {
                'patterns': ['under.*1000', 'less.*thousand', 'small.*budget', 'tight.*budget'],
                'range': '< $1K',
                'score_modifier': 0.7
            },
            'small': {
                'patterns': ['1000.*5000', '1k.*5k', 'few.*thousand'],
                'range': '$1K-$5K',
                'score_modifier': 0.9
            },
            'medium': {
                'patterns': ['5000.*50000', '5k.*50k', 'moderate.*budget'],
                'range': '$5K-$50K',
                'score_modifier': 1.2
            },
            'large': {
                'patterns': ['50000.*500000', '50k.*500k', 'substantial.*budget'],
                'range': '$50K-$500K',
                'score_modifier': 1.4
            },
            'enterprise': {
                'patterns': ['500000', '500k', 'million', 'large.*scale', 'enterprise.*budget'],
                'range': '$500K+',
                'score_modifier': 1.6
            }
        }
        
        # Decision maker authority indicators
        self.authority_levels = {
            'owner': {
                'indicators': ['owner', 'founder', 'ceo', 'president', 'my company', 'my business'],
                'authority_score': 100,
                'decision_speed': 'fast'
            },
            'executive': {
                'indicators': ['director', 'vp', 'manager', 'head of', 'lead'],
                'authority_score': 80,
                'decision_speed': 'medium'
            },
            'employee': {
                'indicators': ['employee', 'work for', 'my boss', 'supervisor'],
                'authority_score': 40,
                'decision_speed': 'slow'
            },
            'consultant': {
                'indicators': ['consultant', 'advisor', 'helping client', 'on behalf'],
                'authority_score': 60,
                'decision_speed': 'medium'
            }
        }
        
        # Compliance and regulatory requirements
        self.compliance_requirements = {
            'fda_regulated': {
                'keywords': ['fda', 'medical device', 'pharmaceutical', 'food safety'],
                'complexity_multiplier': 2.0,
                'lead_time_impact': 'high'
            },
            'ce_marking': {
                'keywords': ['ce mark', 'european compliance', 'eu regulation'],
                'complexity_multiplier': 1.5,
                'lead_time_impact': 'medium'
            },
            'fcc_certified': {
                'keywords': ['fcc', 'electronic certification', 'radio frequency'],
                'complexity_multiplier': 1.4,
                'lead_time_impact': 'medium'
            },
            'ul_listed': {
                'keywords': ['ul listed', 'safety certification', 'electrical safety'],
                'complexity_multiplier': 1.3,
                'lead_time_impact': 'low'
            }
        }
        
        # Supply chain sophistication levels
        self.supply_chain_maturity = {
            'dropshipping': {
                'indicators': ['dropship', 'no inventory', 'ship direct', 'zero stock'],
                'sophistication_score': 20,
                'business_model': 'low_touch'
            },
            'basic_wholesale': {
                'indicators': ['buy bulk', 'wholesale', 'resell', 'distribute'],
                'sophistication_score': 40,
                'business_model': 'traditional'
            },
            'private_label': {
                'indicators': ['private label', 'white label', 'own brand', 'custom packaging'],
                'sophistication_score': 70,
                'business_model': 'branded'
            },
            'oem_odm': {
                'indicators': ['oem', 'odm', 'custom manufacturing', 'designed for us'],
                'sophistication_score': 90,
                'business_model': 'advanced'
            },
            'integrated_supply': {
                'indicators': ['supply chain', 'logistics partner', 'end-to-end', 'vertical integration'],
                'sophistication_score': 100,
                'business_model': 'sophisticated'
            }
        }
        
        # Quality standards detection
        self.quality_standards = {
            'basic': {
                'keywords': ['cheap', 'budget', 'basic quality', 'good enough'],
                'quality_focus': 'cost_driven',
                'score_modifier': 0.8
            },
            'standard': {
                'keywords': ['decent quality', 'market standard', 'acceptable'],
                'quality_focus': 'market_standard',
                'score_modifier': 1.0
            },
            'premium': {
                'keywords': ['high quality', 'premium', 'superior', 'best quality'],
                'quality_focus': 'quality_driven',
                'score_modifier': 1.3
            },
            'luxury': {
                'keywords': ['luxury', 'top tier', 'exceptional', 'world class'],
                'quality_focus': 'luxury_segment',
                'score_modifier': 1.5
            }
        }
        
        # Engagement authenticity patterns
        self.bot_indicators = [
            'generic response', 'copy paste', 'spam', 'promotional link',
            'buy now', 'click here', 'limited time', 'act fast'
        ]
        
        # Relationship building opportunities
        self.relationship_indicators = {
            'high_potential': ['long term', 'partnership', 'ongoing', 'regular orders'],
            'medium_potential': ['repeat business', 'future needs', 'growing company'],
            'low_potential': ['one time', 'single order', 'test order']
        }
    
    def _detect_service_type(self, content: str, title: str, subreddit: str) -> str:
        """Detect the most relevant service type from content"""
        full_text = f"{title} {content}".lower()
        subreddit_lower = subreddit.lower()
        
        # Social Media indicators
        social_indicators = ['social media', 'instagram', 'tiktok', 'youtube', 'content creator', 
                           'influencer', 'followers', 'engagement', 'posting', 'algorithm']
        social_subreddits = ['socialmedia', 'instagram', 'tiktok', 'youtube', 'influencer', 'contentcreator']
        
        # Video Editing indicators  
        video_indicators = ['video editing', 'premiere', 'after effects', 'color grading', 
                          'videography', 'wedding video', 'corporate video', 'render']
        video_subreddits = ['videoediting', 'videography', 'filmmakers', 'premiere', 'aftereffects']
        
        # Drone indicators
        drone_indicators = ['drone', 'drones', 'aerial', 'dji', 'phantom', 'mavic', 'part 107', 
                          'commercial drone', 'gimbal', 'fpv']
        drone_subreddits = ['drones', 'dji', 'commercialdrone', 'aerial', 'fpv', 'droneracing']
        
        # Manufacturing indicators (original)
        manufacturing_indicators = ['manufacturing', 'sourcing', 'supplier', 'factory', 'alibaba']
        
        # Score each service type
        social_score = sum(1 for indicator in social_indicators if indicator in full_text)
        social_score += sum(3 for sub in social_subreddits if sub in subreddit_lower)
        
        video_score = sum(1 for indicator in video_indicators if indicator in full_text)
        video_score += sum(3 for sub in video_subreddits if sub in subreddit_lower)
        
        drone_score = sum(1 for indicator in drone_indicators if indicator in full_text)
        drone_score += sum(3 for sub in drone_subreddits if sub in subreddit_lower)
        
        manufacturing_score = sum(1 for indicator in manufacturing_indicators if indicator in full_text)
        
        # Return the highest scoring service type
        scores = {
            'social_media': social_score,
            'video_editing': video_score, 
            'drone_services': drone_score,
            'manufacturing': manufacturing_score
        }
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def _analyze_service_specific_patterns(self, text: str, service_type: str) -> Dict[str, Any]:
        """Analyze patterns specific to detected service type using optimized intelligence"""
        if service_type not in self.service_complexity_patterns:
            return {'category': 'unknown', 'score': 50, 'priority': 'medium'}
        
        service_patterns = self.service_complexity_patterns[service_type]
        best_match = {'category': 'basic', 'score': 50, 'priority': 'medium', 'budget_estimate': '$500-2K'}
        
        for category, pattern_data in service_patterns.items():
            for pattern in pattern_data['patterns']:
                if re.search(pattern, text, re.IGNORECASE):
                    if pattern_data['score'] > best_match['score']:
                        best_match = {
                            'category': category,
                            'score': pattern_data['score'],
                            'priority': pattern_data['priority'],
                            'budget_estimate': pattern_data['budget_estimate']
                        }
        
        return best_match
    
    def _assess_urgency_indicators(self, text: str, service_type: str) -> Dict[str, Any]:
        """Assess urgency based on service-specific indicators"""
        urgency_patterns = {
            'immediate': ['urgent', 'asap', 'rush', 'deadline', 'emergency', 'same day', 'tomorrow'],
            'high': ['soon', 'quickly', 'this week', 'time sensitive', 'priority'],
            'medium': ['planning', 'looking ahead', 'future', 'considering'],
            'low': ['eventually', 'someday', 'when ready', 'no rush']
        }
        
        # Service-specific urgency multipliers
        service_multipliers = {
            'social_media': 1.2,  # Algorithm changes create urgency
            'video_editing': 1.5,  # Event deadlines are common
            'drone_services': 1.3,  # Commercial operations need quick turnaround
            'manufacturing': 1.0    # Traditional timeline expectations
        }
        
        multiplier = service_multipliers.get(service_type, 1.0)
        
        for urgency_level, patterns in urgency_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    base_score = {'immediate': 95, 'high': 80, 'medium': 60, 'low': 30}[urgency_level]
                    return {
                        'level': urgency_level,
                        'score': min(100, int(base_score * multiplier)),
                        'service_factor': multiplier
                    }
        
        return {'level': 'medium', 'score': 60, 'service_factor': multiplier}
    
    def _assess_technical_sophistication(self, text: str, service_type: str) -> Dict[str, Any]:
        """Assess technical sophistication based on service type"""
        sophistication_indicators = {
            'social_media': {
                'basic': ['instagram', 'posting', 'social media'],
                'intermediate': ['content strategy', 'analytics', 'scheduling', 'engagement'],
                'advanced': ['multi-platform', 'api integration', 'automation', 'attribution'],
                'expert': ['programmatic', 'machine learning', 'predictive analytics']
            },
            'video_editing': {
                'basic': ['video editing', 'simple cuts', 'basic'],
                'intermediate': ['color grading', 'audio sync', 'transitions'],
                'advanced': ['motion graphics', 'vfx', 'multi-camera', '4k'],
                'expert': ['8k', 'real-time rendering', 'ai enhancement', 'cinema grade']
            },
            'drone_services': {
                'basic': ['drone', 'aerial photos', 'hobby'],
                'intermediate': ['commercial drone', 'real estate', 'photography'],
                'advanced': ['part 107', 'fleet management', 'mapping', 'surveying'],
                'expert': ['autonomous missions', 'ai navigation', 'lidar', 'thermal imaging']
            }
        }
        
        if service_type not in sophistication_indicators:
            return {'level': 'intermediate', 'score': 60}
        
        indicators = sophistication_indicators[service_type]
        sophistication_scores = {'expert': 95, 'advanced': 80, 'intermediate': 60, 'basic': 40}
        
        for level in ['expert', 'advanced', 'intermediate', 'basic']:
            for indicator in indicators[level]:
                if re.search(indicator, text, re.IGNORECASE):
                    return {'level': level, 'score': sophistication_scores[level]}
        
        return {'level': 'intermediate', 'score': 60}

    def analyze_lead_v3(self, content: str, title: str, author: str, 
                       subreddit: str, created_utc: str = None,
                       comments: List[Dict] = None) -> Dict[str, Any]:
        """
        V3 Analysis with deduplication and advanced service-specific intelligence
        """
        full_text = (title + ' ' + content).lower()
        
        # Detect the primary service type for this lead
        detected_service = self._detect_service_type(content, title, subreddit)
        
        # Content deduplication check
        content_hash = self._generate_content_hash(full_text, author)
        if content_hash in self.seen_content_hashes:
            return {
                'lead_score': 0,
                'tier': 'Duplicate',
                'is_qualified': False,
                'reason': 'Duplicate content detected'
            }
        self.seen_content_hashes.add(content_hash)
        
        # Enhanced content creator detection
        if self._detect_content_creator_v3(full_text, title, comments or []):
            return {
                'lead_score': 3,
                'tier': 'Filtered',
                'is_qualified': False,
                'reason': 'Content creator/advisor detected'
            }
        
        # Service-specific advanced analysis
        service_analysis = self._analyze_service_specific_patterns(full_text, detected_service)
        budget_analysis = self._analyze_budget_signals_advanced(full_text)
        authority_analysis = self._assess_decision_authority(full_text, author)
        urgency_analysis = self._assess_urgency_indicators(full_text, detected_service)
        technical_analysis = self._assess_technical_sophistication(full_text, detected_service)
        engagement_quality = self._assess_engagement_authenticity(comments or [])
        relationship_potential = self._assess_relationship_opportunity(full_text)
        
        # Competitive intelligence
        competitor_analysis = self._analyze_competitive_landscape(full_text)
        
        # Calculate composite score with service-specific weightings
        base_score = 0
        
        # Service-specific pattern scoring (primary factor)
        base_score += service_analysis['score'] * 0.30
        
        # Budget readiness scoring
        base_score += budget_analysis['score'] * 0.25
        
        # Decision authority scoring
        base_score += authority_analysis['score'] * 0.20
        
        # Urgency indicators scoring
        base_score += urgency_analysis['score'] * 0.15
        
        # Technical sophistication scoring
        base_score += technical_analysis['score'] * 0.10
        
        # Competitor awareness bonus
        base_score += competitor_analysis * 0.05
        
        # Apply service-specific bonuses
        if detected_service in ['social_media', 'video_editing', 'drone_services']:
            # Modern service types get a relevance boost
            base_score += 5
        
        final_score = min(100, max(0, base_score))
        
        # Advanced tier determination
        tier = self._determine_tier_v3(final_score, authority_analysis, budget_analysis)
        
        # Enhanced qualification criteria for modern services
        is_qualified = (
            final_score >= 40 and
            authority_analysis['level'] != 'employee' and
            urgency_analysis['level'] != 'low'
        )
        
        return {
            'lead_score': final_score,
            'tier': tier,
            'detected_service': detected_service,
            'service_analysis': service_analysis,
            'buying_intent': self._categorize_intent_v3(final_score, authority_analysis),
            'urgency': urgency_analysis,
            'budget_analysis': budget_analysis,
            'authority_analysis': authority_analysis,
            'technical_sophistication': technical_analysis,
            'engagement_quality': engagement_quality,
            'relationship_potential': relationship_potential,
            'competitive_intelligence': competitor_analysis,
            'is_qualified': is_qualified,
            'qualification_reasons': self._generate_qualification_reasons_v3(
                final_score, authority_analysis, service_analysis, urgency_analysis
            ),
            'detailed_analysis': {
                'service_score': service_analysis['score'],
                'budget_score': budget_analysis['score'],
                'authority_score': authority_analysis['score'],
                'urgency_score': urgency_analysis['score'],
                'technical_score': technical_analysis['score'],
                'engagement_score': engagement_quality,
                'relationship_score': relationship_potential
            }
        }
    
    def _generate_content_hash(self, content: str, author: str) -> str:
        """Generate unique hash for content deduplication"""
        # Normalize content for hashing
        normalized = re.sub(r'\s+', ' ', content.strip().lower())
        hash_input = f"{author}:{normalized[:200]}"  # First 200 chars + author
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    def _assess_manufacturing_complexity(self, text: str) -> Dict[str, Any]:
        """Assess manufacturing complexity requirements"""
        max_complexity = 'simple'
        max_score = 0
        
        for complexity, data in self.complexity_indicators.items():
            matches = sum(1 for keyword in data['keywords'] if keyword in text)
            if matches > 0:
                score = matches * 25 * data['score_modifier']
                if score > max_score:
                    max_score = score
                    max_complexity = complexity
        
        return {
            'level': max_complexity,
            'score': min(max_score, 100),
            'modifier': self.complexity_indicators[max_complexity]['score_modifier'],
            'manufacturing_ease': self.complexity_indicators[max_complexity]['manufacturing_ease']
        }
    
    def _analyze_budget_signals_advanced(self, text: str) -> Dict[str, Any]:
        """Advanced budget signal analysis"""
        detected_range = 'unknown'
        max_score = 0
        modifier = 1.0
        
        for budget_level, data in self.budget_signals.items():
            for pattern in data['patterns']:
                if re.search(pattern, text):
                    score = 60 * data['score_modifier']
                    if score > max_score:
                        max_score = score
                        detected_range = data['range']
                        modifier = data['score_modifier']
        
        # Additional budget readiness signals
        budget_readiness = 0
        if 'approved budget' in text:
            budget_readiness += 30
        if 'investment ready' in text:
            budget_readiness += 25
        if 'funding secured' in text:
            budget_readiness += 35
        
        final_score = max_score + budget_readiness
        
        return {
            'range': detected_range,
            'score': min(final_score, 100),
            'modifier': modifier,
            'readiness_indicators': budget_readiness > 0
        }
    
    def _assess_decision_authority(self, text: str, author: str) -> Dict[str, Any]:
        """Assess decision-making authority"""
        detected_level = 'unknown'
        max_score = 0
        
        # Check text content
        for level, data in self.authority_levels.items():
            matches = sum(1 for indicator in data['indicators'] if indicator in text)
            if matches > 0:
                if data['authority_score'] > max_score:
                    max_score = data['authority_score']
                    detected_level = level
        
        # Check username for authority indicators
        author_lower = author.lower()
        for level, data in self.authority_levels.items():
            if any(indicator in author_lower for indicator in data['indicators'][:3]):  # Check first 3 indicators
                if data['authority_score'] > max_score:
                    max_score = data['authority_score']
                    detected_level = level
        
        return {
            'level': detected_level,
            'score': max_score,
            'decision_speed': self.authority_levels.get(detected_level, {}).get('decision_speed', 'unknown')
        }
    
    def _detect_compliance_requirements(self, text: str) -> Dict[str, Any]:
        """Detect regulatory compliance requirements"""
        requirements = []
        complexity_multiplier = 1.0
        
        for requirement, data in self.compliance_requirements.items():
            matches = sum(1 for keyword in data['keywords'] if keyword in text)
            if matches > 0:
                requirements.append({
                    'type': requirement,
                    'complexity_multiplier': data['complexity_multiplier'],
                    'lead_time_impact': data['lead_time_impact']
                })
                complexity_multiplier = max(complexity_multiplier, data['complexity_multiplier'])
        
        return {
            'requirements': requirements,
            'complexity_multiplier': complexity_multiplier,
            'has_regulatory_needs': len(requirements) > 0
        }
    
    def _assess_supply_chain_sophistication(self, text: str) -> Dict[str, Any]:
        """Assess supply chain sophistication level"""
        detected_level = 'basic_wholesale'  # Default
        max_score = 0
        
        for level, data in self.supply_chain_maturity.items():
            matches = sum(1 for indicator in data['indicators'] if indicator in text)
            if matches > 0 and data['sophistication_score'] > max_score:
                max_score = data['sophistication_score']
                detected_level = level
        
        return {
            'level': detected_level,
            'score': max_score,
            'business_model': self.supply_chain_maturity[detected_level]['business_model']
        }
    
    def _analyze_quality_standards(self, text: str) -> Dict[str, Any]:
        """Analyze quality standard requirements"""
        detected_standard = 'standard'  # Default
        max_score = 50
        modifier = 1.0
        
        for standard, data in self.quality_standards.items():
            matches = sum(1 for keyword in data['keywords'] if keyword in text)
            if matches > 0:
                score = matches * 25 * data['score_modifier']
                if score > max_score:
                    max_score = score
                    detected_standard = standard
                    modifier = data['score_modifier']
        
        return {
            'standard': detected_standard,
            'score': min(max_score, 100),
            'modifier': modifier,
            'quality_focus': self.quality_standards[detected_standard]['quality_focus']
        }
    
    def _assess_engagement_authenticity(self, comments: List[Dict]) -> float:
        """Assess quality and authenticity of engagement"""
        if not comments:
            return 50  # Neutral if no comments
        
        authentic_score = 0
        total_comments = len(comments)
        
        for comment in comments:
            content = comment.get('content', '').lower()
            
            # Penalize bot-like responses
            bot_signals = sum(1 for indicator in self.bot_indicators if indicator in content)
            if bot_signals > 0:
                continue
            
            # Reward authentic engagement
            if len(content) > 20:  # Substantial response
                authentic_score += 15
            if '?' in content:  # Questions indicate engagement
                authentic_score += 10
            if any(word in content for word in ['interested', 'help', 'contact', 'discuss']):
                authentic_score += 20
        
        # Calculate authenticity ratio
        if total_comments > 0:
            authenticity_ratio = authentic_score / total_comments
            return min(100, authenticity_ratio * 5)  # Scale to 100
        
        return 50
    
    def _assess_relationship_opportunity(self, text: str) -> float:
        """Assess long-term relationship building potential"""
        for potential, indicators in self.relationship_indicators.items():
            matches = sum(1 for indicator in indicators if indicator in text)
            if matches > 0:
                if potential == 'high_potential':
                    return 90
                elif potential == 'medium_potential':
                    return 60
                else:  # low_potential
                    return 30
        
        return 50  # Default moderate potential
    
    def _analyze_competitive_landscape(self, text: str) -> float:
        """Analyze competitive intelligence within posts"""
        competitor_mentions = 0
        negative_experiences = 0
        
        competitors = ['alibaba', 'global sources', 'made-in-china', 'dhgate']
        negative_terms = ['bad experience', 'avoid', 'terrible', 'scam']
        
        for competitor in competitors:
            if competitor in text:
                competitor_mentions += 1
                # Check if negative sentiment toward competitor
                for negative in negative_terms:
                    if negative in text and competitor in text:
                        negative_experiences += 1
        
        # Score based on competitive awareness and dissatisfaction
        base_score = competitor_mentions * 15
        dissatisfaction_bonus = negative_experiences * 25
        
        return min(100, base_score + dissatisfaction_bonus)
    
    def _detect_content_creator_v3(self, text: str, title: str, comments: List[Dict]) -> bool:
        """Enhanced content creator detection"""
        # Original patterns
        creator_patterns = [
            'i help', 'i helped', 'consultant', 'here\'s how', 'my experience',
            'success story', 'ama', 'ask me anything', 'sharing my', 'tutorial'
        ]
        
        # Enhanced patterns for V3
        enhanced_patterns = [
            'my journey', 'lessons learned', 'what i discovered', 'my approach',
            'strategy that worked', 'how i achieved', 'my method', 'tips from experience'
        ]
        
        all_patterns = creator_patterns + enhanced_patterns
        
        strong_indicators = sum(1 for pattern in all_patterns if pattern in text)
        
        # Check if receiving many questions (indicator of advice-giving)
        if comments:
            question_responses = sum(1 for c in comments if '?' in c.get('content', ''))
            if question_responses > 3:  # Getting lots of questions
                strong_indicators += 2
        
        return strong_indicators >= 2
    
    def _determine_tier_v3(self, score: float, authority: Dict, budget: Dict) -> str:
        """Enhanced tier determination with authority and budget factors"""
        base_tier = self._determine_basic_tier(score)
        
        # Upgrade based on authority
        if authority['level'] == 'owner' and score >= 60:
            return 'Burning'
        elif authority['level'] == 'executive' and score >= 70:
            return 'Hot'
        
        # Upgrade based on budget readiness
        if budget.get('readiness_indicators') and score >= 55:
            if base_tier in ['Warm', 'Cool']:
                return 'Hot'
        
        return base_tier
    
    def _determine_basic_tier(self, score: float) -> str:
        """Basic tier determination"""
        if score >= 85:
            return 'Burning'
        elif score >= 70:
            return 'Hot'
        elif score >= 50:
            return 'Warm'
        elif score >= 30:
            return 'Cool'
        else:
            return 'Cold'
    
    def _categorize_intent_v3(self, score: float, authority: Dict) -> Dict[str, str]:
        """Enhanced intent categorization"""
        base_intent = 'Low'
        if score >= 75:
            base_intent = 'Very High'
        elif score >= 60:
            base_intent = 'High'
        elif score >= 45:
            base_intent = 'Medium'
        
        # Authority modifier
        if authority['level'] == 'owner':
            if base_intent == 'Medium':
                base_intent = 'High'
            elif base_intent == 'High':
                base_intent = 'Very High'
        
        return {'category': base_intent}
    
    def _categorize_urgency_v3(self, score: float) -> Dict[str, str]:
        """Enhanced urgency categorization"""
        if score >= 80:
            return {'level': 'Immediate'}
        elif score >= 65:
            return {'level': 'High'}
        elif score >= 45:
            return {'level': 'Medium'}
        else:
            return {'level': 'Low'}
    
    def _generate_qualification_reasons_v3(self, score: float, authority: Dict, 
                                         service_analysis: Dict, urgency: Dict) -> List[str]:
        """Generate detailed qualification reasoning for service-specific leads"""
        reasons = []
        
        # Service-specific qualification reasons
        if service_analysis['score'] >= 90:
            reasons.append(f"High-value {service_analysis['category']} opportunity detected")
        
        if urgency['level'] == 'immediate':
            reasons.append(f"Urgent timeline with {urgency['service_factor']}x service multiplier")
        
        if authority['level'] in ['owner', 'decision_maker']:
            reasons.append(f"Direct access to {authority['level']} level")
        
        if score >= 80:
            reasons.append("Premium tier prospect with strong intent signals")
        elif score >= 60:
            reasons.append("Qualified lead with moderate conversion potential")
        else:
            reasons.append("Basic qualification with growth potential")
        
        # Budget estimation context
        if 'budget_estimate' in service_analysis:
            reasons.append(f"Estimated budget range: {service_analysis['budget_estimate']}")
        
        return reasons

    def _generate_qualification_reasons(self, score: float, authority: Dict, 
                                      supply_chain: Dict, engagement: float) -> List[str]:
        """Generate detailed qualification reasoning"""
        reasons = []
        
        if score >= 35:
            reasons.append(f"Score threshold met ({score:.1f}/100)")
        else:
            reasons.append(f"Score below threshold ({score:.1f}/100)")
        
        if authority['level'] != 'employee':
            reasons.append(f"Decision authority: {authority['level']}")
        else:
            reasons.append("Limited decision authority (employee)")
        
        if supply_chain['level'] != 'dropshipping':
            reasons.append(f"Serious business model: {supply_chain['business_model']}")
        else:
            reasons.append("Dropshipping model - lower priority")
        
        if engagement >= 30:
            reasons.append("Authentic engagement detected")
        else:
            reasons.append("Low engagement quality")
        
        return reasons