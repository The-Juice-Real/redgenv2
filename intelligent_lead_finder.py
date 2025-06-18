import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import streamlit as st
from reddit_scraper import RedditScraper
from lead_analyzer import LeadAnalyzer
from follow_up_tracker import FollowUpTracker


from lead_scoring_engine import AdvancedLeadScoringEngine
from intelligent_search_patterns import IntelligentSearchPatterns

class IntelligentLeadFinder:
    """AI-powered lead discovery that automatically finds the best subreddits and prospects"""
    
    def __init__(self):
        self.reddit_scraper = RedditScraper()
        self.lead_analyzer = LeadAnalyzer()


        self.scoring_engine = AdvancedLeadScoringEngine()
        self.search_patterns = IntelligentSearchPatterns()
        
        # Service-to-subreddit mapping with search strategies
        self.service_subreddit_map = {
            'web design': {
                'subreddits': ['webdev', 'web_design', 'entrepreneur', 'smallbusiness', 'startups', 'freelance', 'web_development'],
                'search_terms': ['need website', 'website design', 'web designer', 'site redesign', 'landing page', 'portfolio site']
            },
            'marketing': {
                'subreddits': ['marketing', 'entrepreneur', 'smallbusiness', 'startups', 'digitalmarketing', 'SEO', 'socialmedia'],
                'search_terms': ['marketing help', 'promote business', 'get customers', 'marketing strategy', 'advertising', 'brand awareness']
            },
            'app development': {
                'subreddits': ['startups', 'entrepreneur', 'androiddev', 'iOSProgramming', 'reactnative', 'flutter', 'AppBusiness'],
                'search_terms': ['mobile app', 'app developer', 'build app', 'app development', 'iOS app', 'android app']
            },
            'consulting': {
                'subreddits': ['consulting', 'entrepreneur', 'businessanalysis', 'startups', 'smallbusiness', 'freelance'],
                'search_terms': ['business consultant', 'need advice', 'strategy help', 'business problem', 'consulting services']
            },
            'graphic design': {
                'subreddits': ['graphic_design', 'entrepreneur', 'smallbusiness', 'startups', 'freelance', 'logodesign'],
                'search_terms': ['logo design', 'graphic designer', 'branding', 'design help', 'visual identity', 'marketing materials']
            },
            'content writing': {
                'subreddits': ['entrepreneur', 'smallbusiness', 'startups', 'freelancewriters', 'copywriting', 'marketing'],
                'search_terms': ['content writer', 'copywriter', 'blog writing', 'website content', 'content marketing', 'need writer']
            },
            'seo services': {
                'subreddits': ['SEO', 'entrepreneur', 'smallbusiness', 'startups', 'marketing', 'webdev'],
                'search_terms': ['SEO help', 'search rankings', 'google rankings', 'website traffic', 'SEO expert', 'organic traffic']
            },
            'social media': {
                'subreddits': ['socialmedia', 'entrepreneur', 'smallbusiness', 'startups', 'marketing', 'Instagram', 'facebook'],
                'search_terms': ['social media manager', 'social media help', 'Instagram growth', 'facebook marketing', 'social strategy']
            },
            'software development': {
                'subreddits': ['programming', 'webdev', 'entrepreneur', 'startups', 'freelance', 'softwaredevelopment'],
                'search_terms': ['software developer', 'custom software', 'web application', 'software solution', 'development team']
            },
            'e-commerce': {
                'subreddits': ['ecommerce', 'entrepreneur', 'smallbusiness', 'startups', 'shopify', 'amazonFBA'],
                'search_terms': ['online store', 'ecommerce help', 'shopify expert', 'amazon seller', 'online business', 'product launch']
            },
            'china sourcing': {
                'subreddits': ['ecommerce', 'entrepreneur', 'smallbusiness', 'startups', 'amazonFBA', 'dropship', 'FulfillmentByAmazon', 'ImportExport', 'manufacturing', 'alibaba', 'AliExpressDropShip', 'shopify', 'business', 'Aliexpress', 'dropshipping', 'Flipping', 'reseller', 'logistics', 'shipping', 'ProductDesign', 'industrialdesign', 'MechanicalEngineering', 'ElectricalEngineering', 'ProductDevelopment', 'Innovation', 'TechStartups', 'hardwarestartups', 'InventorHelp', 'investing', 'personalfinance', 'financialindependence', 'WorkOnline', 'remotework', 'digitalnomad', 'sidehustle', 'passive_income', 'sweatystartup', 'EntrepreneurRideAlong', 'growmybusiness', 'BusinessIntelligence', 'sales', 'marketing', 'advertising', 'SocialMediaMarketing', 'SEO', 'growthHacking', 'LeanStartups', 'ProductManagement', 'userexperience', 'webdev', 'programming'],
                'search_terms': [
                    'china sourcing', 'alibaba supplier', 'product sourcing', 'manufacturing china', 
                    'private label', 'find supplier', 'china manufacturer', 'product development',
                    'sourcing agent', 'quality control', 'factory audit', 'product inspection',
                    'minimum order quantity', 'MOQ', 'OEM manufacturing', 'ODM manufacturing',
                    'bulk order', 'wholesale china', 'trade assurance', 'supplier verification',
                    'production oversight', 'logistics china', 'shipping from china', 'customs clearance',
                    'product samples', 'prototype development', 'tooling cost', 'mold development',
                    'cost reduction', 'margin improvement', 'supply chain', 'vendor management',
                    'import from china', 'china trade', 'guangzhou', 'shenzhen', 'yiwu'
                ]
            },
            'sourcing services': {
                'subreddits': ['ecommerce', 'entrepreneur', 'smallbusiness', 'startups', 'amazonFBA', 'dropship', 'FulfillmentByAmazon', 'ImportExport', 'manufacturing', 'alibaba', 'AliExpressDropShip', 'shopify', 'business', 'Aliexpress', 'dropshipping', 'Flipping', 'reseller', 'logistics', 'shipping', 'ProductDesign', 'industrialdesign', 'MechanicalEngineering', 'ElectricalEngineering', 'ProductDevelopment', 'Innovation', 'TechStartups', 'hardwarestartups', 'InventorHelp', 'investing', 'personalfinance', 'financialindependence', 'WorkOnline', 'remotework', 'digitalnomad', 'sidehustle', 'passive_income', 'sweatystartup', 'EntrepreneurRideAlong', 'growmybusiness', 'BusinessIntelligence', 'sales', 'marketing', 'advertising', 'SocialMediaMarketing', 'SEO', 'growthHacking', 'LeanStartups', 'ProductManagement', 'userexperience', 'webdev', 'programming', 'freelance'],
                'search_terms': [
                    'sourcing help', 'find manufacturers', 'supplier search', 'product sourcing service',
                    'sourcing consultant', 'china sourcing agent', 'procurement services', 'vendor sourcing',
                    'factory finder', 'manufacturer verification', 'supplier due diligence', 'sourcing strategy',
                    'cost optimization', 'supply chain management', 'international sourcing', 'asia sourcing',
                    'product development china', 'manufacturing partner', 'reliable supplier', 'trusted manufacturer'
                ]
            },
            'social media posting': {
                'subreddits': ['socialmedia', 'instagram', 'tiktok', 'youtube', 'influencer', 'contentcreator', 'smallyoutuber', 'marketing', 'entrepreneur', 'freelance', 'onlinebusiness', 'affiliate', 'SocialMediaMarketing', 'FacebookAds', 'InstagramMarketing', 'TikTokCreators', 'YouTubeCreators', 'LinkedInLunatics', 'TwitterMarketing', 'InfluencerMarketing', 'ContentMarketing', 'DigitalMarketing', 'OnlineMarketing', 'SocialMediaGrowth', 'InstagramGrowth', 'TikTokGrowth', 'YoutubeGrowthTips', 'InfluencerTips', 'CreatorEconomy', 'SocialMediaTips', 'ContentCreation', 'VideoMarketing', 'SocialMediaStrategy', 'BrandBuilding', 'PersonalBranding', 'InfluencerLife', 'ContentCreators', 'SocialInfluencer', 'InstagramInfluencer', 'TikTokInfluencer', 'YouTubeInfluencer', 'SocialMediaHelp', 'InstagramHelp', 'TikTokHelp', 'YouTubeHelp', 'SocialMediaAdvice', 'MarketingAdvice', 'SocialMediaBusiness', 'InfluencerBusiness', 'ContentBusiness'],
                'search_terms': [
                    'social media help', 'content strategy', 'posting schedule', 'engagement boost',
                    'algorithm changes', 'content ideas', 'social media manager', 'brand partnerships',
                    'influencer growth', 'monetize content', 'follower growth', 'content calendar',
                    'burnt out posting', 'need content help', 'social media burnout', 'posting consistency'
                ]
            },
            'video editing': {
                'subreddits': ['videoediting', 'videography', 'filmmakers', 'premiere', 'aftereffects', 'youtube', 'contentcreator', 'weddingvideography', 'corporatevideo', 'cinematography', 'events', 'realestate', 'freelance'],
                'search_terms': [
                    'video editor', 'editing help', 'premiere pro', 'after effects', 'color grading',
                    'video production', 'wedding video', 'youtube editing', 'corporate video',
                    'motion graphics', 'render time', 'video turnaround', 'editing workflow',
                    'video editing overwhelm', 'urgent video editing', 'rush editing', 'quick turnaround'
                ]
            },
            'selling/trading drones': {
                'subreddits': ['drones', 'dji', 'commercialdrone', 'uav', 'aerial', 'fpv', 'droneracing', 'phantom', 'mavic', 'realestate', 'photography', 'surveying', 'agriculture', 'entrepreneur', 'smallbusiness', 'repair'],
                'search_terms': [
                    'drone services', 'aerial photography', 'commercial drone', 'drone repair',
                    'dji drone', 'drone parts', 'part 107', 'drone business', 'aerial videography',
                    'drone fleet', 'drone training', 'gimbal repair', 'fpv drone', 'drone upgrade',
                    'drone crashed', 'gimbal broken', 'drone parts needed', 'commercial operations',
                    'fleet management', 'drone investment', 'scaling drone business'
                ]
            }
        }
        
        # Service classification patterns
        self.service_patterns = {
            'web design': ['web design', 'website design', 'web designer', 'ui/ux', 'frontend', 'wordpress', 'landing page'],
            'marketing': ['marketing', 'digital marketing', 'growth', 'promotion', 'advertising', 'brand', 'lead generation'],
            'app development': ['app development', 'mobile app', 'ios', 'android', 'react native', 'flutter', 'mobile development'],
            'consulting': ['consulting', 'consultant', 'business advice', 'strategy', 'analysis', 'optimization'],
            'graphic design': ['graphic design', 'logo design', 'branding', 'visual design', 'creative design', 'illustrations'],
            'content writing': ['content writing', 'copywriting', 'blog writing', 'content creation', 'technical writing'],
            'seo services': ['seo', 'search optimization', 'search rankings', 'google rankings', 'organic traffic'],
            'social media': ['social media', 'instagram', 'facebook', 'twitter', 'linkedin', 'social marketing'],
            'software development': ['software development', 'programming', 'custom software', 'web application', 'api'],
            'e-commerce': ['ecommerce', 'online store', 'shopify', 'amazon', 'online selling', 'product sales'],
            'china sourcing': [
                'china sourcing', 'sourcing china', 'chinese supplier', 'chinese manufacturer', 'china manufacturing',
                'alibaba', 'guangzhou', 'shenzhen', 'yiwu', 'product sourcing', 'supplier sourcing', 'factory sourcing',
                'private label china', 'oem china', 'odm china', 'china trade', 'import china', 'china import',
                'manufacturing china', 'china factory', 'quality control china', 'inspection china'
            ],
            'sourcing services': [
                'sourcing service', 'sourcing agent', 'sourcing consultant', 'procurement service', 'supplier search',
                'manufacturer search', 'vendor search', 'factory search', 'product development', 'supply chain',
                'manufacturing & sourcing', 'import/export business', 'private label products', 'dropshipping services'
            ],
            'social media posting': [
                'social media posting', 'social media management', 'content creation', 'instagram management',
                'tiktok content', 'youtube content', 'social media strategy', 'content calendar', 'posting schedule',
                'influencer marketing', 'brand partnerships', 'social media burnout', 'content help'
            ],
            'video editing': [
                'video editing', 'video editor', 'post production', 'premiere pro', 'after effects',
                'color grading', 'motion graphics', 'wedding videography', 'corporate video',
                'youtube editing', 'video production', 'editing workflow', 'render time'
            ],
            'selling/trading drones': [
                'drone', 'drones', 'aerial photography', 'commercial drone', 'dji', 'phantom', 'mavic',
                'drone repair', 'drone parts', 'part 107', 'drone business', 'aerial videography',
                'drone fleet', 'gimbal', 'fpv', 'drone racing', 'uav', 'aerial services'
            ]
        }

    def find_leads_for_service(self, service_description: str, max_leads: int = 50, max_subreddits: int = 5, 
                             posts_per_subreddit: int = 50, comments_per_post: int = 20) -> Dict[str, Any]:
        """Main function to find leads based on service description"""
        
        print(f"🎯 STARTING LEAD SEARCH")
        print(f"   Service: {service_description}")
        print(f"   Target leads: {max_leads}, Subreddits: {max_subreddits}")
        print(f"   Posts per subreddit: {posts_per_subreddit}, Comments per post: {comments_per_post}")
        
        # Step 1: Classify the service
        print(f"\n📊 STEP 1: CLASSIFYING SERVICE")
        classified_service = self._classify_service(service_description)
        print(f"   Classified as: {classified_service}")
        
        # Step 2: Get optimal subreddits and search terms
        print(f"\n🔍 STEP 2: BUILDING SEARCH STRATEGY")
        search_strategy = self._get_search_strategy(classified_service, service_description, max_subreddits)
        print(f"   Target subreddits: {search_strategy.get('subreddits', [])[:5]}")
        print(f"   Search terms: {len(search_strategy.get('search_terms', []))} terms")
        
        # Step 3: Execute multi-subreddit search
        print(f"\n🌐 STEP 3: EXECUTING REDDIT SEARCH")
        all_leads = self._execute_multi_subreddit_search(search_strategy, max_leads, posts_per_subreddit, comments_per_post, max_subreddits)
        print(f"   Total prospects found: {len(all_leads)}")
        
        # Step 4: Analyze and score leads
        print(f"\n🧠 STEP 4: ANALYZING AND SCORING LEADS")
        qualified_leads = self._analyze_and_score_leads(all_leads, service_description)
        print(f"   Qualified leads: {len(qualified_leads)}")
        
        # Step 5: Rank and return ALL qualified leads (no arbitrary limit)
        print(f"\n📈 STEP 5: RANKING LEADS")
        top_leads = self._rank_and_filter_leads(qualified_leads, len(qualified_leads))
        print(f"   Final ranked leads: {len(top_leads)}")
        
        # Add Reddit post links to lead data
        for lead in top_leads:
            subreddit = lead.get('subreddit', '')
            post_id = lead.get('post_id', '')
            if subreddit and post_id:
                lead['reddit_link'] = f"https://reddit.com/r/{subreddit}/comments/{post_id}/"
        
        return {
            'service_type': classified_service,
            'search_strategy': search_strategy,
            'total_prospects_found': len(all_leads),
            'qualified_leads': qualified_leads,
            'qualified_leads_count': len(qualified_leads),
            'top_leads': top_leads,
            'search_summary': self._generate_search_summary(search_strategy, qualified_leads),
            'search_metadata': {
                'timestamp': 'recent_search',
                'search_version': '3.0'
            }
        }

    def _classify_service(self, service_description: str) -> str:
        """Advanced semantic service classification with multi-dimensional analysis"""
        
        desc_lower = service_description.lower()
        desc_words = set(desc_lower.split())
        
        # Direct mapping for dropdown service names
        direct_mappings = {
            'social media posting': 'social media posting',
            'video editing': 'video editing', 
            'selling/trading drones': 'selling/trading drones',
            'manufacturing & sourcing': 'sourcing services',
            'e-commerce products': 'e-commerce',
            'digital marketing services': 'marketing',
            'web development': 'web design',
            'consulting services': 'consulting',
            'software solutions': 'software development',
            'import/export business': 'sourcing services',
            'private label products': 'sourcing services',
            'dropshipping services': 'e-commerce',
            'business automation': 'software development'
        }
        
        # Check for direct mapping first
        if desc_lower in direct_mappings:
            return direct_mappings[desc_lower]
        
        # Enhanced scoring with semantic understanding
        service_scores = {}
        
        for service_type, keywords in self.service_patterns.items():
            score = 0
            exact_matches = 0
            context_matches = 0
            
            for keyword in keywords:
                keyword_words = set(keyword.lower().split())
                
                # Exact phrase match (highest weight)
                if keyword.lower() in desc_lower:
                    score += len(keyword_words) * 5
                    exact_matches += 1
                
                # Word overlap scoring
                overlap = len(desc_words.intersection(keyword_words))
                if overlap > 0:
                    score += overlap * 3
                    
                # Contextual proximity scoring
                if len(keyword_words) > 1:
                    for word in keyword_words:
                        if word in desc_lower:
                            context_matches += 1
                            score += 2
                            
            # Boost score for high-confidence classifications
            if exact_matches > 0:
                score *= 1.5
            if context_matches >= len(keywords) * 0.3:
                score *= 1.2
                
            service_scores[service_type] = score
        
        # Advanced classification logic
        if not service_scores or max(service_scores.values()) == 0:
            return 'general'
            
        max_score = max(service_scores.values())
        top_services = [k for k, v in service_scores.items() if v == max_score]
        
        # Handle ties by selecting most specific service
        if len(top_services) == 1:
            return top_services[0]
        else:
            # Prefer more specific categories over general ones
            priority_order = ['product_sourcing', 'manufacturing', 'private_label', 'wholesale', 'general']
            for service in priority_order:
                if service in top_services:
                    return service
            return top_services[0]

    def _get_search_strategy(self, service_type: str, description: str, max_subreddits: int = 5) -> Dict[str, Any]:
        """Advanced search strategy with dynamic subreddit scoring and trend analysis"""
        
        if service_type in self.service_subreddit_map:
            base_strategy = self.service_subreddit_map[service_type]
        else:
            base_strategy = {
                'subreddits': ['entrepreneur', 'smallbusiness', 'startups', 'freelance'],
                'search_terms': ['need help', 'looking for', 'recommendations']
            }
        
        # Advanced intent analysis for dynamic strategy optimization
        intent_analysis = self.search_patterns.analyze_search_intent(description)
        primary_intent = intent_analysis.get('primary_intent')
        
        # Dynamic subreddit ranking based on detected intent
        if primary_intent:
            intent_subreddits = self.search_patterns.rank_subreddits_by_intent(primary_intent)
            # Merge with base strategy, prioritizing intent-based subreddits
            all_subreddits = [sub[0] for sub in intent_subreddits] + base_strategy['subreddits']
            unique_subreddits = list(dict.fromkeys(all_subreddits))  # Remove duplicates while preserving order
        else:
            unique_subreddits = base_strategy['subreddits']
        
        # Score and rank final subreddit list
        scored_subreddits = self._score_subreddits_for_service(unique_subreddits, description)
        
        # If user requests more subreddits than available, add verified active subreddits
        if max_subreddits > len(scored_subreddits):
            additional_subreddits = [
                'AskReddit', 'IAmA', 'todayilearned', 'LifeProTips', 'YouShouldKnow',
                'NoStupidQuestions', 'personalfinance', 'investing', 'financialindependence',
                'WorkOnline', 'remotework', 'digitalnomad', 'sidehustle', 'passive_income',
                'sweatystartup', 'EntrepreneurRideAlong', 'growmybusiness', 'advancedentrepreneur',
                'sales', 'marketing', 'advertising', 'SEO', 'growthHacking', 'LeanStartups',
                'ProductManagement', 'userexperience', 'design', 'webdev', 'programming',
                'forhire', 'slavelabour', 'HireAnEditor', 'freelanceWriters', 'copywriting',
                'graphic_design', 'logodesign', 'web_design', 'learnprogramming', 'cscareerquestions',
                'startups_funding', 'venturecapital', 'smallbiz', 'businessops', 'supply_chain',
                'ecom', 'FBA', 'AmazonSeller', 'ebay', 'etsy', 'shopifystore'
            ]
            
            # Remove duplicates and add new ones
            existing_names = {sub['name'].lower() for sub in scored_subreddits}
            for subreddit in additional_subreddits:
                if subreddit.lower() not in existing_names and len(scored_subreddits) < max_subreddits:
                    scored_subreddits.append({
                        'name': subreddit,
                        'score': 40,  # Lower score for general subreddits
                        'relevance': 'general_business'
                    })
        
        # Generate optimized search terms based on intent
        if primary_intent:
            optimized_terms = self.search_patterns.generate_optimized_search_terms(description, primary_intent)
        else:
            optimized_terms = self.search_patterns.generate_optimized_search_terms(description)
        
        # Combine with base terms and prioritize
        all_terms = base_strategy['search_terms'] + optimized_terms
        prioritized_terms = self._prioritize_search_terms(all_terms, description)
        
        return {
            'subreddits': [sub['name'] for sub in scored_subreddits[:max_subreddits]],
            'subreddit_scores': {sub['name']: sub['score'] for sub in scored_subreddits[:max_subreddits]},
            'search_terms': prioritized_terms[:8],
            'term_priorities': {term: i for i, term in enumerate(prioritized_terms[:8])},
            'service_type': service_type,
            'search_confidence': self._calculate_search_confidence(scored_subreddits, prioritized_terms),
            'intent_analysis': intent_analysis,
            'optimization_level': 'advanced_ai_powered',
            'expected_lead_quality': self._predict_search_quality(intent_analysis, scored_subreddits)
        }

    def _extract_custom_search_terms(self, description: str) -> List[str]:
        """Extract additional search terms from service description"""
        
        # Look for specific technologies, industries, or service aspects
        tech_patterns = [
            r'\b(wordpress|shopify|react|vue|angular|python|php|javascript)\b',
            r'\b(e-commerce|ecommerce|saas|b2b|b2c)\b',
            r'\b(startup|small business|enterprise|freelance)\b'
        ]
        
        extracted_terms = []
        desc_lower = description.lower()
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, desc_lower)
            extracted_terms.extend(matches)
        
        return extracted_terms[:3]  # Limit to 3 additional terms
    
    def _score_subreddits_for_service(self, subreddits: List[str], description: str) -> List[Dict[str, Any]]:
        """Score subreddits based on relevance to service description"""
        scored_subs = []
        desc_words = set(description.lower().split())
        
        for subreddit in subreddits:
            base_score = 50  # Base relevance score
            
            # Boost score based on subreddit name relevance
            sub_words = set(subreddit.lower().replace('_', ' ').split())
            word_overlap = len(desc_words.intersection(sub_words))
            relevance_boost = word_overlap * 15
            
            # Activity score (estimated based on subreddit type)
            activity_scores = {
                'entrepreneur': 85, 'smallbusiness': 75, 'ecommerce': 80,
                'amazon': 90, 'alibaba': 70, 'sourcing': 85,
                'manufacturing': 75, 'startups': 80, 'freelance': 70
            }
            activity_score = activity_scores.get(subreddit.lower(), 60)
            
            final_score = base_score + relevance_boost + (activity_score * 0.3)
            
            scored_subs.append({
                'name': subreddit,
                'score': final_score,
                'relevance_boost': relevance_boost,
                'activity_score': activity_score
            })
        
        return sorted(scored_subs, key=lambda x: x['score'], reverse=True)
    
    def _extract_intelligent_search_terms(self, description: str) -> List[str]:
        """Extract contextual search terms with intent analysis"""
        
        # Intent-based patterns for China sourcing
        intent_patterns = {
            'need_supplier': ['need supplier', 'looking for supplier', 'find manufacturer'],
            'quality_issues': ['quality problems', 'defective products', 'poor quality'],
            'cost_optimization': ['reduce costs', 'cheaper alternative', 'better pricing'],
            'new_product': ['new product', 'product development', 'prototype'],
            'scaling': ['scale production', 'increase volume', 'bulk orders']
        }
        
        extracted_terms = []
        desc_lower = description.lower()
        
        # Extract based on intent patterns
        for intent, patterns in intent_patterns.items():
            for pattern in patterns:
                if pattern in desc_lower:
                    extracted_terms.append(pattern)
                    break
        
        # Extract industry-specific terms
        industry_terms = re.findall(r'\b(?:electronics|textiles|automotive|food|cosmetics|toys|furniture|jewelry|clothing|accessories)\b', desc_lower)
        extracted_terms.extend(industry_terms[:2])
        
        return extracted_terms[:5]
    
    def _generate_time_sensitive_terms(self, description: str) -> List[str]:
        """Generate time-sensitive search terms based on urgency indicators"""
        
        urgency_indicators = ['urgent', 'asap', 'quickly', 'rush', 'deadline', 'immediate']
        seasonal_terms = ['holiday', 'christmas', 'black friday', 'valentine', 'summer']
        
        time_terms = []
        desc_lower = description.lower()
        
        # Check for urgency
        if any(indicator in desc_lower for indicator in urgency_indicators):
            time_terms.extend(['urgent need', 'quick turnaround', 'immediate'])
        
        # Check for seasonal context
        for term in seasonal_terms:
            if term in desc_lower:
                time_terms.append(f'{term} sourcing')
                break
        
        return time_terms[:2]
    
    def _prioritize_search_terms(self, terms: List[str], description: str) -> List[str]:
        """Prioritize search terms based on relevance and effectiveness"""
        
        term_scores = {}
        desc_lower = description.lower()
        
        for term in set(terms):  # Remove duplicates
            score = 0
            
            # Exact match in description (highest priority)
            if term.lower() in desc_lower:
                score += 50
            
            # Word overlap scoring
            term_words = set(term.lower().split())
            desc_words = set(desc_lower.split())
            overlap = len(term_words.intersection(desc_words))
            score += overlap * 10
            
            # Length penalty for very long terms
            if len(term.split()) > 4:
                score -= 5
            
            # Boost for high-value terms
            high_value_terms = ['supplier', 'manufacturer', 'sourcing', 'quality', 'cost']
            if any(hv_term in term.lower() for hv_term in high_value_terms):
                score += 20
            
            term_scores[term] = score
        
        return sorted(term_scores.keys(), key=lambda x: term_scores[x], reverse=True)
    
    def _calculate_search_confidence(self, scored_subreddits: List[Dict], prioritized_terms: List[str]) -> float:
        """Calculate confidence score for search strategy"""
        
        if not scored_subreddits or not prioritized_terms:
            return 0.0
        
        # Average subreddit score (normalized)
        avg_sub_score = sum(sub['score'] for sub in scored_subreddits) / len(scored_subreddits)
        sub_confidence = min(avg_sub_score / 100, 1.0)
        
        # Term relevance score
        term_confidence = min(len(prioritized_terms) / 8, 1.0)
        
        # Combined confidence
        overall_confidence = (sub_confidence * 0.6) + (term_confidence * 0.4)
        
        return round(overall_confidence * 100, 1)
    
    def _predict_search_quality(self, intent_analysis: Dict[str, Any], scored_subreddits: List[Dict]) -> str:
        """Predict expected lead quality based on search strategy"""
        
        intent_confidence = intent_analysis.get('intent_confidence', 0)
        qualification_score = intent_analysis.get('qualification_score', 0)
        avg_subreddit_score = sum(sub['score'] for sub in scored_subreddits) / len(scored_subreddits) if scored_subreddits else 0
        
        # Calculate composite quality prediction
        quality_score = (intent_confidence * 0.4) + (qualification_score * 0.35) + (avg_subreddit_score * 0.25)
        
        if quality_score >= 80:
            return 'Premium Quality Expected'
        elif quality_score >= 60:
            return 'High Quality Expected'
        elif quality_score >= 40:
            return 'Medium Quality Expected'
        else:
            return 'Variable Quality Expected'

    def _execute_multi_subreddit_search(self, strategy: Dict[str, Any], max_leads: int, 
                                        posts_per_subreddit: int = 50, comments_per_post: int = 20,
                                        max_subreddits: int = 5) -> List[Dict[str, Any]]:
        """Search multiple subreddits for prospects"""
        
        all_prospects = []
        
        import concurrent.futures
        import threading
        
        print(f"   Starting parallel search across {len(strategy.get('subreddits', []))} subreddits...")
        
        # Use parallel processing for subreddit searches
        def search_subreddit_parallel(subreddit_term_pair):
            subreddit, search_term = subreddit_term_pair
            try:
                print(f"   🔍 Searching r/{subreddit} for '{search_term}'...")
                results = self.reddit_scraper.search_subreddit(
                    subreddit, 
                    search_term, 
                    limit=min(20, posts_per_subreddit),  # Optimize limit for speed
                    max_comments_per_post=min(10, comments_per_post)  # Reduce comments for speed
                )
                
                prospects = []
                # Add posts
                post_count = 0
                for post in results.get('posts', []):
                    post['source_subreddit'] = subreddit
                    post['search_term'] = search_term
                    post['content_type'] = 'post'
                    prospects.append(post)
                    post_count += 1
                
                # Add comments
                comment_count = 0
                for comment in results.get('comments', []):
                    comment['source_subreddit'] = subreddit
                    comment['search_term'] = search_term
                    comment['content_type'] = 'comment'
                    prospects.append(comment)
                    comment_count += 1
                
                print(f"   ✅ r/{subreddit}: Found {post_count} posts, {comment_count} comments")
                return prospects
            except Exception as e:
                print(f"   ❌ r/{subreddit}: Search failed - {str(e)}")
                return []
        
        # Create subreddit-term pairs for parallel processing
        search_pairs = []
        max_subs_to_search = min(max_subreddits, len(strategy['subreddits']))  # Use the user's setting
        for subreddit in strategy['subreddits'][:max_subs_to_search]:
            for search_term in strategy['search_terms'][:3]:  # Use top 3 terms for efficiency
                search_pairs.append((subreddit, search_term))
        
        # Parallel execution with ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_pair = {executor.submit(search_subreddit_parallel, pair): pair for pair in search_pairs}
            
            for future in concurrent.futures.as_completed(future_to_pair):
                try:
                    prospects = future.result(timeout=30)  # 30 second timeout per search
                    all_prospects.extend(prospects)
                except Exception as e:
                    continue
        
        return all_prospects  # Return all prospects found, don't limit at this stage

    def _analyze_and_score_leads(self, prospects: List[Dict[str, Any]], service_description: str) -> List[Dict[str, Any]]:
        """Optimized parallel lead scoring with fast filtering"""
        
        import concurrent.futures
        
        # Fast pre-filtering to eliminate obvious non-leads
        def fast_prefilter(prospect):
            if not isinstance(prospect, dict):
                return False
            
            # CRITICAL: Filter out old posts first
            created_utc = prospect.get('created_utc')
            if created_utc:
                try:
                    from datetime import datetime, timedelta
                    if isinstance(created_utc, datetime):
                        post_time = created_utc
                    elif isinstance(created_utc, (int, float)):
                        post_time = datetime.fromtimestamp(created_utc)
                    else:
                        post_time = datetime.fromisoformat(str(created_utc).replace('Z', '+00:00'))
                    
                    # Reject posts older than 30 days at the pre-filter stage
                    days_ago = (datetime.now() - post_time).days
                    if days_ago > 30:
                        return False
                except:
                    pass  # Continue with other filters if date parsing fails
            
            content = (prospect.get('content', '') + ' ' + prospect.get('title', '')).lower()
            
            # Skip very short content
            if len(content) < 20:
                return False
                
            # Skip deleted/removed content
            if content in ['[deleted]', '[removed]', '']:
                return False
                
            # Quick relevance check using service keywords
            service_words = set(service_description.lower().split())
            content_words = set(content.split())
            
            # Must have some overlap with service description or common business terms
            business_terms = {'need', 'looking', 'help', 'service', 'business', 'company', 'cost', 'price', 'budget'}
            if len(service_words.intersection(content_words)) > 0 or len(business_terms.intersection(content_words)) > 0:
                return True
            
            return False
        
        # Pre-filter prospects for efficiency
        print(f"   Pre-filtering {len(prospects)} prospects...")
        filtered_prospects = [p for p in prospects if fast_prefilter(p)]
        print(f"   After pre-filter: {len(filtered_prospects)} prospects remain")
        
        # Import ultra-advanced scoring system
        from rapid_iteration_engine import UltraAdvancedScoringV100
        ultra_scorer = UltraAdvancedScoringV100()
        
        def analyze_single_prospect(prospect):
            try:
                content = prospect.get('content', '')
                title = prospect.get('title', '')
                author = prospect.get('author', '')
                subreddit = prospect.get('source_subreddit', '')
                
                print(f"   📊 Analyzing: {title[:50]}... from r/{subreddit}")
                
                # Prepare metadata for ultra-advanced analysis
                metadata = {
                    'platform': 'reddit',
                    'subreddit': subreddit,
                    'created_utc': prospect.get('created_utc', ''),
                    'score': prospect.get('score', 0),
                    'num_comments': prospect.get('num_comments', 0),
                    'content_type': prospect.get('content_type', 'post')
                }
                
                # Use ultra-advanced scoring system
                scoring_result = ultra_scorer.ultra_score_lead(content, title, author, metadata)
                
                # Enhanced qualification criteria
                ultra_score = scoring_result['ultra_score']
                classification = scoring_result['classification']
                
                print(f"      Score: {ultra_score}, Tier: {classification['tier']}, Priority: {classification['priority']}")
                
                # Adaptive qualification criteria based on service type
                # Social media services have lower thresholds due to different market dynamics
                service_type = service_description.lower()
                if 'social media' in service_type or 'video editing' in service_type or 'drone' in service_type:
                    min_score = 30  # Lower threshold for creative/digital services
                    acceptable_tiers = ['Platinum', 'Gold', 'Silver', 'Bronze']
                else:
                    min_score = 60  # Higher threshold for manufacturing/sourcing
                    acceptable_tiers = ['Platinum', 'Gold', 'Silver']
                
                if (ultra_score >= min_score and 
                    classification['tier'] in acceptable_tiers and
                    classification['priority'] != 'None'):
                    
                    print(f"      ✅ QUALIFIED LEAD")
                    return {
                        **prospect,
                        'lead_score': ultra_score,
                        'classification_tier': classification['tier'],
                        'priority_level': classification['priority'],
                        'buying_intent': {'category': self._map_classification_to_intent(classification)},
                        'urgency': {'level': self._map_priority_to_urgency(classification['priority'])},
                        'budget_indicators': {'category': 'Advanced-Analysis'},
                        'ultra_analysis': {
                            'confidence_interval': scoring_result['confidence_interval'],
                            'recommendation': scoring_result['recommendation'],
                            'next_best_action': scoring_result['next_best_action'],
                            'risk_assessment': scoring_result['risk_assessment']
                        },
                        'component_scores': scoring_result['component_scores'],
                        'author': author,
                        'subreddit': subreddit,
                        'created_utc': prospect.get('created_utc', ''),
                        'content': content[:500]
                    }
                return None
            except Exception as e:
                # Fallback to basic scoring if ultra-system fails
                content = prospect.get('content', '')
                author = prospect.get('author', '')
                subreddit = prospect.get('source_subreddit', '')
                
                if any(word in content.lower() for word in ['urgent', 'quote', 'manufacturer', 'supplier']):
                    return {
                        **prospect,
                        'lead_score': 70,
                        'classification_tier': 'Bronze',
                        'priority_level': 'Medium',
                        'buying_intent': {'category': 'Medium'},
                        'urgency': {'level': 'Medium'},
                        'budget_indicators': {'category': 'Basic-Analysis'},
                        'fallback_reason': f'Ultra-system error: {str(e)[:100]}',
                        'author': author,
                        'subreddit': subreddit,
                        'content': content[:500]
                    }
                return None
        
        # Parallel analysis with smaller batches
        print(f"   Starting parallel analysis of {len(filtered_prospects)} prospects...")
        qualified_leads = []
        batch_size = 50
        
        for i in range(0, len(filtered_prospects), batch_size):
            batch = filtered_prospects[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(filtered_prospects) + batch_size - 1) // batch_size
            
            print(f"   🔄 Processing batch {batch_num}/{total_batches} ({len(batch)} prospects)")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(analyze_single_prospect, prospect) for prospect in batch]
                
                batch_qualified = 0
                for future in concurrent.futures.as_completed(futures, timeout=60):
                    try:
                        result = future.result()
                        if result:
                            qualified_leads.append(result)
                            batch_qualified += 1
                    except:
                        continue
                
                print(f"   ✅ Batch {batch_num} complete: {batch_qualified} qualified leads found")
        
        print(f"\n🎯 ANALYSIS COMPLETE: {len(qualified_leads)} total qualified leads")
        return qualified_leads
    
    def _map_classification_to_intent(self, classification: Dict[str, str]) -> str:
        """Map classification tier to buying intent"""
        tier_mapping = {
            'Platinum': 'Very High',
            'Gold': 'High', 
            'Silver': 'Medium',
            'Bronze': 'Low'
        }
        return tier_mapping.get(classification['tier'], 'Medium')
    
    def _map_priority_to_urgency(self, priority: str) -> str:
        """Map priority level to urgency"""
        priority_mapping = {
            'Immediate': 'Immediate',
            'High': 'High',
            'Medium': 'Medium', 
            'Low': 'Low',
            'None': 'Low'
        }
        return priority_mapping.get(priority, 'Medium')
    
    def _comprehensive_lead_analysis(self, prospect: Dict[str, Any], service_description: str) -> Dict[str, Any]:
        """Comprehensive analysis combining multiple scoring dimensions"""
        
        # Base analysis from existing analyzer
        base_analysis = self.lead_analyzer.analyze_lead_potential(prospect, 'post')
        
        # Intent detection analysis
        intent_analysis = self._analyze_purchase_intent(prospect, service_description)
        
        # Behavioral pattern analysis
        behavioral_analysis = self._analyze_behavioral_patterns(prospect)
        
        # Timing and urgency analysis
        timing_analysis = self._analyze_timing_indicators(prospect)
        
        # Authority and decision-making analysis
        authority_analysis = self._analyze_decision_authority(prospect)
        
        # Combine all analyses
        comprehensive_analysis = {
            **base_analysis,
            'intent_score': intent_analysis['score'],
            'intent_indicators': intent_analysis['indicators'],
            'behavioral_score': behavioral_analysis['score'],
            'behavioral_patterns': behavioral_analysis['patterns'],
            'timing_score': timing_analysis['score'],
            'urgency_level': timing_analysis['urgency'],
            'authority_score': authority_analysis['score'],
            'decision_indicators': authority_analysis['indicators']
        }
        
        return comprehensive_analysis
    
    def _analyze_purchase_intent(self, prospect: Dict[str, Any], service_description: str) -> Dict[str, Any]:
        """Analyze purchase intent with context awareness"""
        
        content = prospect.get('content', '') + ' ' + prospect.get('title', '')
        content_lower = content.lower()
        
        # High-intent indicators
        high_intent_patterns = [
            'need supplier', 'looking for manufacturer', 'sourcing', 'find supplier',
            'quotation', 'quote', 'pricing', 'cost', 'budget', 'purchase',
            'order', 'buy', 'vendor', 'partner', 'urgent', 'asap'
        ]
        
        # Medium-intent indicators
        medium_intent_patterns = [
            'recommend', 'suggestion', 'advice', 'experience with', 'quality',
            'reliable', 'trustworthy', 'anyone know', 'help needed'
        ]
        
        # Low-intent indicators (informational)
        low_intent_patterns = [
            'how to', 'what is', 'explain', 'understand', 'learn',
            'curious', 'wondering', 'general question'
        ]
        
        intent_score = 0
        found_indicators = []
        
        # Score based on intent patterns
        for pattern in high_intent_patterns:
            if pattern in content_lower:
                intent_score += 15
                found_indicators.append(f"High: {pattern}")
        
        for pattern in medium_intent_patterns:
            if pattern in content_lower:
                intent_score += 8
                found_indicators.append(f"Medium: {pattern}")
        
        for pattern in low_intent_patterns:
            if pattern in content_lower:
                intent_score += 3
                found_indicators.append(f"Low: {pattern}")
        
        # Context relevance boost
        service_words = set(service_description.lower().split())
        content_words = set(content_lower.split())
        relevance_overlap = len(service_words.intersection(content_words))
        intent_score += relevance_overlap * 5
        
        return {
            'score': min(intent_score, 100),
            'indicators': found_indicators[:5]
        }
    
    def _analyze_behavioral_patterns(self, prospect: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze behavioral patterns for lead quality assessment"""
        
        content = prospect.get('content', '') + ' ' + prospect.get('title', '')
        
        behavioral_score = 0
        patterns = []
        
        # Professional communication patterns
        professional_indicators = [
            'business', 'company', 'startup', 'entrepreneur', 'ceo', 'founder',
            'manager', 'director', 'operations', 'procurement', 'purchasing'
        ]
        
        for indicator in professional_indicators:
            if indicator in content.lower():
                behavioral_score += 10
                patterns.append(f"Professional: {indicator}")
        
        # Specificity patterns (detailed requirements)
        if len(content.split()) > 50:  # Detailed post
            behavioral_score += 15
            patterns.append("Detailed inquiry")
        
        # Engagement patterns
        engagement_score = prospect.get('score', 0)  # Reddit score
        if engagement_score > 10:
            behavioral_score += 10
            patterns.append("High engagement")
        elif engagement_score > 5:
            behavioral_score += 5
            patterns.append("Medium engagement")
        
        # Response patterns (if available)
        num_comments = prospect.get('num_comments', 0)
        if num_comments > 5:
            behavioral_score += 8
            patterns.append("Active discussion")
        
        return {
            'score': min(behavioral_score, 100),
            'patterns': patterns[:5]
        }
    
    def _analyze_timing_indicators(self, prospect: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze timing and urgency indicators"""
        
        content = prospect.get('content', '') + ' ' + prospect.get('title', '')
        content_lower = content.lower()
        
        timing_score = 0
        urgency_level = 'low'
        
        # Urgency indicators
        urgent_patterns = ['urgent', 'asap', 'immediately', 'rush', 'deadline', 'time sensitive']
        medium_urgency = ['soon', 'quickly', 'fast', 'quick turnaround']
        
        for pattern in urgent_patterns:
            if pattern in content_lower:
                timing_score += 20
                urgency_level = 'high'
                break
        
        if urgency_level != 'high':
            for pattern in medium_urgency:
                if pattern in content_lower:
                    timing_score += 10
                    urgency_level = 'medium'
                    break
        
        # Recency boost (recent posts are more valuable)
        try:
            created_utc = prospect.get('created_utc', 0)
            import time
            hours_ago = (time.time() - created_utc) / 3600
            
            if hours_ago <= 24:
                timing_score += 15
            elif hours_ago <= 72:
                timing_score += 10
            elif hours_ago <= 168:  # 1 week
                timing_score += 5
        except:
            pass
        
        return {
            'score': min(timing_score, 100),
            'urgency': urgency_level
        }
    
    def _analyze_decision_authority(self, prospect: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze decision-making authority and influence"""
        
        content = prospect.get('content', '') + ' ' + prospect.get('title', '')
        content_lower = content.lower()
        
        authority_score = 0
        indicators = []
        
        # Authority indicators
        high_authority = ['ceo', 'founder', 'owner', 'president', 'director', 'vp', 'head of']
        medium_authority = ['manager', 'lead', 'senior', 'coordinator', 'supervisor']
        decision_indicators = ['budget', 'decision', 'approve', 'authorize', 'purchase']
        
        for indicator in high_authority:
            if indicator in content_lower:
                authority_score += 25
                indicators.append(f"High authority: {indicator}")
        
        for indicator in medium_authority:
            if indicator in content_lower:
                authority_score += 15
                indicators.append(f"Medium authority: {indicator}")
        
        for indicator in decision_indicators:
            if indicator in content_lower:
                authority_score += 10
                indicators.append(f"Decision power: {indicator}")
        
        # Business context indicators
        business_context = ['company', 'business', 'startup', 'organization', 'firm']
        for context in business_context:
            if context in content_lower:
                authority_score += 5
                indicators.append(f"Business context: {context}")
                break
        
        return {
            'score': min(authority_score, 100),
            'indicators': indicators[:5]
        }
    
    def _calculate_enhanced_lead_score(self, prospect: Dict[str, Any], analysis: Dict[str, Any], service_description: str) -> float:
        """Calculate enhanced lead score using weighted multi-dimensional analysis"""
        
        # Base score from original analysis
        base_score = analysis.get('lead_score', 0)
        
        # Weighted scoring components
        weights = {
            'base': 0.25,
            'intent': 0.30,
            'behavioral': 0.20,
            'timing': 0.15,
            'authority': 0.10
        }
        
        component_scores = {
            'base': base_score,
            'intent': analysis.get('intent_score', 0),
            'behavioral': analysis.get('behavioral_score', 0),
            'timing': analysis.get('timing_score', 0),
            'authority': analysis.get('authority_score', 0)
        }
        
        # Calculate weighted score
        enhanced_score = sum(weights[component] * score for component, score in component_scores.items())
        
        # Apply service relevance multiplier
        service_relevance = self._calculate_service_relevance(prospect, service_description)
        final_score = enhanced_score * service_relevance
        
        return round(min(final_score, 100), 2)
    
    def _calculate_service_relevance(self, prospect: Dict[str, Any], service_description: str) -> float:
        """Calculate how relevant the prospect is to the specific service"""
        
        content = prospect.get('content', '') + ' ' + prospect.get('title', '')
        content_words = set(content.lower().split())
        service_words = set(service_description.lower().split())
        
        # Calculate word overlap
        overlap = len(content_words.intersection(service_words))
        total_service_words = len(service_words)
        
        if total_service_words == 0:
            return 1.0
        
        relevance_ratio = overlap / total_service_words
        
        # Apply sigmoid function for smooth scaling
        import math
        relevance_score = 1 / (1 + math.exp(-5 * (relevance_ratio - 0.3)))
        
        return max(0.5, min(1.5, relevance_score))  # Keep within reasonable bounds
    
    def _meets_qualification_criteria(self, analysis: Dict[str, Any], score: float) -> bool:
        """Advanced qualification criteria beyond just score"""
        
        # Minimum score threshold
        if score < 25:
            return False
        
        # Must have some intent indication
        if analysis.get('intent_score', 0) < 10:
            return False
        
        # Quality content requirement
        if analysis.get('behavioral_score', 0) < 5:
            return False
        
        return True

    def _rank_and_filter_leads(self, leads: List[Dict[str, Any]], max_results: int) -> List[Dict[str, Any]]:
        """Advanced multi-criteria ranking with machine learning-inspired scoring"""
        
        print(f"   Ranking {len(leads)} qualified leads...")
        
        # Enhanced ranking with multiple criteria
        for i, lead in enumerate(leads):
            # Calculate composite score using advanced scoring
            behavioral_score = lead.get('behavioral_scoring', {})
            composite_score = behavioral_score.get('final_score', lead.get('lead_score', 0))
            
            # Add ranking factors for transparency
            lead['composite_score'] = composite_score
            lead['ranking_factors'] = {
                'score': composite_score,
                'quality_tier': behavioral_score.get('lead_quality_tier', 'Unknown'),
                'action_priority': behavioral_score.get('next_action_priority', 'Low Priority'),
                'intent_level': lead.get('advanced_intent', {}).get('intent_confidence', 0)
            }
            
            if i < 5:  # Log top 5 during ranking
                print(f"   📊 Lead {i+1}: Score {composite_score}, Tier: {lead.get('classification_tier', 'Unknown')}")
        
        # Multi-dimensional sorting
        print(f"   Sorting leads by composite scoring algorithm...")
        leads.sort(key=lambda x: (
            x.get('composite_score', 0),
            x.get('behavioral_scoring', {}).get('intent_score', 0),
            x.get('behavioral_scoring', {}).get('urgency_score', 0),
            x.get('behavioral_scoring', {}).get('authority_score', 0)
        ), reverse=True)
        
        print(f"   🏆 Top lead score: {leads[0].get('composite_score', 0) if leads else 'None'}")
        
        # Remove duplicates and apply quality filters
        final_leads = []
        seen_authors = set()
        
        for lead in leads:
            author = lead.get('author', 'unknown')
            
            # Skip duplicates and low-quality content
            if (author in seen_authors or 
                author in ['[deleted]', '[removed]'] or 
                not lead.get('title') or
                lead.get('composite_score', 0) < 25):
                continue
            
            seen_authors.add(author)
            final_leads.append(lead)
            
            if len(final_leads) >= max_results:
                break
        
        return final_leads

    def _generate_search_summary(self, strategy: Dict[str, Any], leads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of search results"""
        
        if not leads:
            return {
                'total_leads': 0,
                'avg_score': 0,
                'top_subreddits': [],
                'lead_quality_breakdown': {}
            }
        
        # Calculate summary statistics
        total_leads = len(leads)
        avg_score = sum(lead.get('lead_score', 0) for lead in leads) / total_leads
        
        # Top performing subreddits
        subreddit_counts = {}
        for lead in leads:
            subreddit = lead.get('source_subreddit', 'unknown')
            subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1
        
        top_subreddits = sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Lead quality breakdown
        quality_breakdown = {}
        for lead in leads:
            quality = lead.get('lead_quality', 'Unknown')
            quality_breakdown[quality] = quality_breakdown.get(quality, 0) + 1
        
        return {
            'total_leads': total_leads,
            'avg_score': round(avg_score, 1),
            'top_subreddits': top_subreddits,
            'lead_quality_breakdown': quality_breakdown,
            'service_type': strategy.get('service_type', 'general'),
            'subreddits_searched': strategy.get('subreddits', [])
        }

    def get_supported_services(self) -> List[str]:
        """Get list of supported service types"""
        return list(self.service_patterns.keys())

    def suggest_search_improvements(self, results: Dict[str, Any]) -> List[str]:
        """Suggest improvements if search results are poor"""
        
        suggestions = []
        
        if results['qualified_leads'] == 0:
            suggestions.append("Try describing your service with more specific keywords")
            suggestions.append("Consider broadening your service description")
            suggestions.append("Add industry-specific terms (e.g., 'B2B', 'SaaS', 'startup')")
        
        elif results['qualified_leads'] < 10:
            suggestions.append("Consider expanding to related service areas")
            suggestions.append("Try different keywords in your description")
        
        if results.get('search_summary', {}).get('avg_score', 0) < 40:
            suggestions.append("Results show low lead quality - try more specific targeting")
            suggestions.append("Consider adding urgency keywords like 'need', 'urgent', 'ASAP'")
        
        return suggestions[:3]  # Return top 3 suggestions