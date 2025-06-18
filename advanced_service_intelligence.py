"""
Advanced Service Intelligence System
Implements 10 iterations of optimization for Drone, Manufacturing, and Video Editing services
"""

from typing import Dict, List, Any, Tuple
import re
from datetime import datetime

class AdvancedServiceIntelligence:
    """Advanced intelligence patterns for service-specific lead qualification"""
    
    def __init__(self):
        self.iteration_patterns = self._initialize_iteration_patterns()
        self.urgency_multipliers = self._initialize_urgency_multipliers()
        self.budget_indicators = self._initialize_budget_indicators()
        self.quality_filters = self._initialize_quality_filters()
    
    def _initialize_iteration_patterns(self) -> Dict[str, Dict]:
        """Initialize patterns from 10 iterations of optimization"""
        return {
            'drone_services': {
                'iteration_2': {
                    'certification_tiers': {
                        'part_107_commercial': {'score_boost': 25, 'priority': 'immediate'},
                        'beyond_visual_line': {'score_boost': 30, 'priority': 'immediate'},
                        'night_operations': {'score_boost': 20, 'priority': 'high'},
                        'over_people_waiver': {'score_boost': 35, 'priority': 'immediate'}
                    },
                    'industry_specializations': {
                        'infrastructure_inspection': {'score_boost': 30, 'avg_contract': '$15K-50K'},
                        'precision_agriculture': {'score_boost': 25, 'avg_contract': '$10K-30K'},
                        'emergency_response': {'score_boost': 35, 'avg_contract': '$20K-75K'},
                        'surveying_mapping': {'score_boost': 28, 'avg_contract': '$12K-40K'},
                        'thermal_inspection': {'score_boost': 32, 'avg_contract': '$18K-60K'}
                    }
                },
                'iteration_3': {
                    'equipment_sophistication': {
                        'lidar_equipped': {'score_boost': 40, 'market_tier': 'enterprise'},
                        'thermal_camera': {'score_boost': 35, 'market_tier': 'professional'},
                        'multispectral_sensors': {'score_boost': 30, 'market_tier': 'agricultural'},
                        'rtk_gps': {'score_boost': 25, 'market_tier': 'surveying'}
                    },
                    'compliance_requirements': {
                        'faa_part_107': {'score_boost': 20, 'necessity': 'mandatory'},
                        'airspace_authorization': {'score_boost': 15, 'necessity': 'situational'},
                        'insurance_coverage': {'score_boost': 10, 'necessity': 'business'},
                        'remote_id': {'score_boost': 8, 'necessity': 'upcoming'}
                    }
                },
                'iteration_4': {
                    'market_segments': {
                        'real_estate_luxury': {'score_boost': 22, 'budget_range': '$500-2K'},
                        'construction_progress': {'score_boost': 28, 'budget_range': '$5K-25K'},
                        'solar_inspection': {'score_boost': 30, 'budget_range': '$8K-35K'},
                        'oil_gas_pipeline': {'score_boost': 45, 'budget_range': '$25K-100K'},
                        'insurance_claims': {'score_boost': 35, 'budget_range': '$10K-50K'}
                    },
                    'service_urgency': {
                        'emergency_response': {'multiplier': 3.0, 'timeline': 'immediate'},
                        'insurance_deadline': {'multiplier': 2.5, 'timeline': '24-48h'},
                        'weather_dependent': {'multiplier': 2.0, 'timeline': '1-3 days'},
                        'seasonal_work': {'multiplier': 1.5, 'timeline': '1-2 weeks'}
                    }
                }
            },
            
            'manufacturing_services': {
                'iteration_2': {
                    'manufacturing_complexity': {
                        'high_precision_cnc': {'score_boost': 35, 'avg_order': '$50K-500K'},
                        'medical_device': {'score_boost': 40, 'avg_order': '$100K-1M'},
                        'aerospace_certified': {'score_boost': 45, 'avg_order': '$200K-2M'},
                        'automotive_tier1': {'score_boost': 38, 'avg_order': '$150K-800K'},
                        'electronics_assembly': {'score_boost': 30, 'avg_order': '$25K-300K'}
                    },
                    'global_sourcing': {
                        'nearshoring_mexico': {'score_boost': 25, 'trend': 'growing'},
                        'vietnam_electronics': {'score_boost': 20, 'trend': 'stable'},
                        'india_precision': {'score_boost': 22, 'trend': 'emerging'},
                        'us_reshoring': {'score_boost': 30, 'trend': 'accelerating'}
                    }
                },
                'iteration_3': {
                    'certification_requirements': {
                        'iso_9001': {'score_boost': 15, 'necessity': 'standard'},
                        'iso_13485_medical': {'score_boost': 35, 'necessity': 'medical'},
                        'as9100_aerospace': {'score_boost': 40, 'necessity': 'aerospace'},
                        'iatf_16949_auto': {'score_boost': 30, 'necessity': 'automotive'},
                        'fda_compliant': {'score_boost': 38, 'necessity': 'medical_device'}
                    },
                    'production_scale': {
                        'prototype_development': {'score_boost': 25, 'volume': '1-100'},
                        'small_batch': {'score_boost': 20, 'volume': '100-5K'},
                        'medium_production': {'score_boost': 30, 'volume': '5K-100K'},
                        'high_volume': {'score_boost': 35, 'volume': '100K+'}
                    }
                },
                'iteration_4': {
                    'technology_adoption': {
                        'industry_4_0': {'score_boost': 30, 'maturity': 'advanced'},
                        'additive_manufacturing': {'score_boost': 25, 'maturity': 'growing'},
                        'automation_robotics': {'score_boost': 28, 'maturity': 'mature'},
                        'ai_quality_control': {'score_boost': 35, 'maturity': 'emerging'}
                    },
                    'sustainability_focus': {
                        'carbon_neutral': {'score_boost': 20, 'trend': 'mandatory'},
                        'circular_economy': {'score_boost': 18, 'trend': 'growing'},
                        'renewable_energy': {'score_boost': 15, 'trend': 'standard'},
                        'waste_reduction': {'score_boost': 12, 'trend': 'expected'}
                    }
                }
            },
            
            'video_editing_services': {
                'iteration_2': {
                    'platform_optimization': {
                        'youtube_long_form': {'score_boost': 20, 'rate': '$50-200/hour'},
                        'tiktok_shorts': {'score_boost': 25, 'rate': '$25-100/video'},
                        'instagram_reels': {'score_boost': 22, 'rate': '$30-120/video'},
                        'linkedin_content': {'score_boost': 18, 'rate': '$40-150/video'},
                        'podcast_video': {'score_boost': 28, 'rate': '$60-250/episode'}
                    },
                    'content_categories': {
                        'educational_content': {'score_boost': 25, 'growth': 'high'},
                        'corporate_training': {'score_boost': 30, 'growth': 'stable'},
                        'product_demos': {'score_boost': 28, 'growth': 'medium'},
                        'testimonials': {'score_boost': 20, 'growth': 'steady'},
                        'live_event_recap': {'score_boost': 35, 'growth': 'explosive'}
                    }
                },
                'iteration_3': {
                    'technical_specialization': {
                        'motion_graphics': {'score_boost': 30, 'complexity': 'high'},
                        'color_grading': {'score_boost': 25, 'complexity': 'medium'},
                        'audio_restoration': {'score_boost': 35, 'complexity': 'high'},
                        'multi_camera_sync': {'score_boost': 28, 'complexity': 'medium'},
                        'vfx_compositing': {'score_boost': 40, 'complexity': 'expert'}
                    },
                    'software_expertise': {
                        'premiere_pro': {'score_boost': 15, 'market_share': '60%'},
                        'final_cut_pro': {'score_boost': 12, 'market_share': '25%'},
                        'davinci_resolve': {'score_boost': 20, 'market_share': '10%'},
                        'after_effects': {'score_boost': 25, 'market_share': '70%'},
                        'avid_media': {'score_boost': 30, 'market_share': '5%'}
                    }
                },
                'iteration_4': {
                    'market_segments': {
                        'wedding_videography': {'score_boost': 25, 'avg_project': '$2K-8K'},
                        'corporate_events': {'score_boost': 30, 'avg_project': '$5K-20K'},
                        'documentary_production': {'score_boost': 35, 'avg_project': '$10K-100K'},
                        'commercial_advertising': {'score_boost': 40, 'avg_project': '$15K-150K'},
                        'streaming_content': {'score_boost': 28, 'avg_project': '$3K-25K'}
                    },
                    'urgency_patterns': {
                        'same_day_turnaround': {'multiplier': 3.5, 'premium': '200-400%'},
                        'next_day_delivery': {'multiplier': 2.5, 'premium': '100-200%'},
                        'weekly_deadline': {'multiplier': 1.8, 'premium': '50-100%'},
                        'monthly_project': {'multiplier': 1.2, 'premium': '10-25%'}
                    }
                }
            }
        }
    
    def _initialize_urgency_multipliers(self) -> Dict[str, Dict]:
        """Initialize urgency detection and scoring multipliers"""
        return {
            'immediate': {'multiplier': 3.0, 'keywords': ['urgent', 'asap', 'emergency', 'immediate', 'rush']},
            'high': {'multiplier': 2.0, 'keywords': ['deadline', 'soon', 'quickly', 'priority', 'time-sensitive']},
            'medium': {'multiplier': 1.5, 'keywords': ['prefer', 'hoping', 'looking for', 'planning']},
            'low': {'multiplier': 1.0, 'keywords': ['eventually', 'future', 'considering', 'exploring']}
        }
    
    def _initialize_budget_indicators(self) -> Dict[str, Dict]:
        """Initialize budget detection patterns"""
        return {
            'enterprise': {'multiplier': 2.5, 'indicators': ['budget allocated', 'approved funding', 'corporate budget']},
            'high': {'multiplier': 2.0, 'indicators': ['investment ready', 'serious budget', 'substantial funding']},
            'medium': {'multiplier': 1.5, 'indicators': ['budget planning', 'cost consideration', 'price range']},
            'low': {'multiplier': 1.0, 'indicators': ['tight budget', 'cost-effective', 'affordable']}
        }
    
    def _initialize_quality_filters(self) -> Dict[str, List]:
        """Initialize quality filtering patterns"""
        return {
            'high_intent': [
                'looking for', 'need help with', 'seeking', 'require', 'must have',
                'project starting', 'deadline approaching', 'budget approved', 'ready to hire'
            ],
            'decision_authority': [
                'decision maker', 'authorized to', 'company owner', 'project manager',
                'procurement', 'sourcing manager', 'buying for', 'budget authority'
            ],
            'quality_requirements': [
                'professional quality', 'high standards', 'certified', 'experienced',
                'proven track record', 'references required', 'portfolio review'
            ],
            'exclude_patterns': [
                'just browsing', 'maybe someday', 'thinking about', 'not sure if',
                'free advice', 'volunteer work', 'student project', 'personal hobby'
            ]
        }
    
    def analyze_service_intelligence(self, content: str, title: str, service_type: str) -> Dict[str, Any]:
        """Apply advanced service intelligence analysis"""
        
        text = f"{title} {content}".lower()
        
        # Base analysis
        service_analysis = self._analyze_service_patterns(text, service_type)
        urgency_analysis = self._analyze_urgency_patterns(text)
        budget_analysis = self._analyze_budget_patterns(text)
        quality_analysis = self._analyze_quality_patterns(text)
        
        # Calculate composite intelligence score
        base_score = service_analysis.get('score_boost', 0)
        urgency_multiplier = urgency_analysis.get('multiplier', 1.0)
        budget_multiplier = budget_analysis.get('multiplier', 1.0)
        quality_modifier = quality_analysis.get('quality_score', 1.0)
        
        intelligence_score = (base_score * urgency_multiplier * budget_multiplier * quality_modifier)
        
        return {
            'intelligence_score': min(intelligence_score, 100),  # Cap at 100
            'service_analysis': service_analysis,
            'urgency_analysis': urgency_analysis,
            'budget_analysis': budget_analysis,
            'quality_analysis': quality_analysis,
            'optimization_tier': self._determine_optimization_tier(intelligence_score),
            'recommendations': self._generate_recommendations(service_analysis, urgency_analysis, budget_analysis)
        }
    
    def _analyze_service_patterns(self, text: str, service_type: str) -> Dict[str, Any]:
        """Analyze service-specific patterns from iterations"""
        
        if service_type not in self.iteration_patterns:
            return {'score_boost': 0, 'patterns_found': []}
        
        patterns = self.iteration_patterns[service_type]
        score_boost = 0
        patterns_found = []
        
        # Analyze patterns from all iterations
        for iteration_key, iteration_data in patterns.items():
            for category, category_data in iteration_data.items():
                for pattern_name, pattern_info in category_data.items():
                    # Convert pattern name to search terms
                    search_terms = pattern_name.replace('_', ' ')
                    if search_terms in text:
                        score_boost += pattern_info.get('score_boost', 0)
                        patterns_found.append({
                            'pattern': pattern_name,
                            'category': category,
                            'iteration': iteration_key,
                            'boost': pattern_info.get('score_boost', 0),
                            'metadata': pattern_info
                        })
        
        return {
            'score_boost': min(score_boost, 50),  # Cap individual service boost
            'patterns_found': patterns_found,
            'specialization_level': self._determine_specialization_level(patterns_found)
        }
    
    def _analyze_urgency_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze urgency indicators"""
        
        urgency_score = 0
        urgency_level = 'low'
        urgency_indicators = []
        
        for level, data in self.urgency_multipliers.items():
            for keyword in data['keywords']:
                if keyword in text:
                    urgency_score = max(urgency_score, data['multiplier'])
                    urgency_level = level
                    urgency_indicators.append(keyword)
        
        return {
            'multiplier': urgency_score,
            'level': urgency_level,
            'indicators': urgency_indicators,
            'timeline_pressure': self._assess_timeline_pressure(text)
        }
    
    def _analyze_budget_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze budget indicators"""
        
        budget_score = 1.0
        budget_level = 'unknown'
        budget_indicators = []
        
        for level, data in self.budget_indicators.items():
            for indicator in data['indicators']:
                if indicator in text:
                    budget_score = max(budget_score, data['multiplier'])
                    budget_level = level
                    budget_indicators.append(indicator)
        
        return {
            'multiplier': budget_score,
            'level': budget_level,
            'indicators': budget_indicators,
            'budget_readiness': self._assess_budget_readiness(text)
        }
    
    def _analyze_quality_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze quality indicators"""
        
        quality_score = 1.0
        quality_indicators = {
            'high_intent': 0,
            'decision_authority': 0,
            'quality_requirements': 0,
            'exclusions': 0
        }
        
        # Check for quality patterns
        for category, patterns in self.quality_filters.items():
            for pattern in patterns:
                if pattern in text:
                    if category == 'exclude_patterns':
                        quality_indicators['exclusions'] += 1
                    else:
                        quality_indicators[category] += 1
        
        # Calculate composite quality score
        positive_score = (
            quality_indicators['high_intent'] * 0.4 +
            quality_indicators['decision_authority'] * 0.3 +
            quality_indicators['quality_requirements'] * 0.3
        )
        
        # Apply exclusion penalty
        exclusion_penalty = quality_indicators['exclusions'] * 0.2
        quality_score = max(0.1, positive_score - exclusion_penalty)
        
        return {
            'quality_score': min(quality_score, 2.0),  # Cap at 2x boost
            'indicators': quality_indicators,
            'qualification_level': self._determine_qualification_level(quality_score)
        }
    
    def _determine_specialization_level(self, patterns_found: List) -> str:
        """Determine specialization level based on patterns"""
        if len(patterns_found) >= 3:
            return 'expert'
        elif len(patterns_found) >= 2:
            return 'advanced'
        elif len(patterns_found) >= 1:
            return 'intermediate'
        else:
            return 'basic'
    
    def _assess_timeline_pressure(self, text: str) -> str:
        """Assess timeline pressure from text"""
        immediate_indicators = ['today', 'tomorrow', 'this week', 'asap', 'emergency']
        urgent_indicators = ['next week', 'month end', 'quarter end', 'deadline']
        
        for indicator in immediate_indicators:
            if indicator in text:
                return 'immediate'
        
        for indicator in urgent_indicators:
            if indicator in text:
                return 'urgent'
        
        return 'standard'
    
    def _assess_budget_readiness(self, text: str) -> str:
        """Assess budget readiness level"""
        ready_indicators = ['budget approved', 'funding secured', 'ready to invest']
        planning_indicators = ['budget planning', 'cost evaluation', 'price comparison']
        
        for indicator in ready_indicators:
            if indicator in text:
                return 'ready'
        
        for indicator in planning_indicators:
            if indicator in text:
                return 'planning'
        
        return 'exploratory'
    
    def _determine_qualification_level(self, quality_score: float) -> str:
        """Determine lead qualification level"""
        if quality_score >= 1.5:
            return 'highly_qualified'
        elif quality_score >= 1.2:
            return 'qualified'
        elif quality_score >= 0.8:
            return 'moderately_qualified'
        else:
            return 'low_qualified'
    
    def _determine_optimization_tier(self, intelligence_score: float) -> str:
        """Determine optimization tier based on intelligence score"""
        if intelligence_score >= 80:
            return 'premium'
        elif intelligence_score >= 60:
            return 'high_value'
        elif intelligence_score >= 40:
            return 'standard'
        else:
            return 'basic'
    
    def _generate_recommendations(self, service_analysis: Dict, urgency_analysis: Dict, 
                                budget_analysis: Dict) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        # Service-specific recommendations
        specialization = service_analysis.get('specialization_level', 'basic')
        if specialization == 'expert':
            recommendations.append("High-value specialized lead - prioritize immediate contact")
        elif specialization == 'advanced':
            recommendations.append("Advanced specialization detected - strong conversion potential")
        
        # Urgency recommendations
        urgency_level = urgency_analysis.get('level', 'low')
        if urgency_level == 'immediate':
            recommendations.append("Immediate response required - contact within 1 hour")
        elif urgency_level == 'high':
            recommendations.append("High urgency - respond within 4-6 hours")
        
        # Budget recommendations
        budget_level = budget_analysis.get('level', 'unknown')
        if budget_level == 'enterprise':
            recommendations.append("Enterprise budget - prepare comprehensive proposal")
        elif budget_level == 'high':
            recommendations.append("Strong budget indicators - focus on value proposition")
        
        return recommendations if recommendations else ["Standard follow-up recommended"]

# Global instance for integration
service_intelligence = AdvancedServiceIntelligence()