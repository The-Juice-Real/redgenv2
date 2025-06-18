"""
Optimized Intelligent Lead Finder V4.0
Eliminates service duplications, implements specialized targeting, and adds adaptive scoring
"""

import json
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
from reddit_scraper import RedditScraper
from intelligent_search_patterns import IntelligentSearchPatterns
from advanced_service_intelligence import service_intelligence
from dynamic_subreddit_discovery import DynamicSubredditDiscovery
from ultra_precise_ai import UltraPreciseAI


class OptimizedLeadFinder:
    """AI-powered lead discovery with specialized service targeting and adaptive scoring"""
    
    def __init__(self):
        self.reddit_scraper = RedditScraper()
        self.search_patterns = IntelligentSearchPatterns()
        self.dynamic_discovery = DynamicSubredditDiscovery()
        self.ultra_ai = UltraPreciseAI()
        
        # Consolidated, specialized service targeting with urgency and budget detection
        self.service_map = {
            # MANUFACTURING & PRODUCTION SERVICES - ITERATION 1 OPTIMIZED
            'manufacturing & sourcing': {
                'subreddits': [
                    # Global Manufacturing Hubs
                    'manufacturing', 'mexicomanufacturing', 'vietnammanufacturing', 'indiamanufacturing',
                    'USmanufacturing', 'nearshoring', 'reshoring', 'globalsupplychain',
                    # Industry-Specific Manufacturing
                    'automotivemanufacturing', 'electronicsmanufacturing', 'medicaldevices', 'aerospace',
                    'textilemanufacturing', 'foodmanufacturing', 'pharmaceuticalmanufacturing',
                    # Prototype & Small-Batch
                    'prototyping', 'rapidprototyping', 'smallbatchmanufacturing', 'custommanufacturing',
                    'contractmanufacturing', 'productdevelopment', 'designformanufacturing',
                    # Quality & Compliance
                    'qualityassurance', 'iso9001', 'regulatorycompliance', 'fda', 'ce', 'rohs',
                    'qualitycontrol', 'testing', 'inspection', 'certification',
                    # Supply Chain & Logistics
                    'supplychain', 'procurement', 'vendor', 'logistics', 'sourcing',
                    'supplychainmanagement', 'lean', 'sixsigma', 'continuousimprovement',
                    # Sustainable Manufacturing
                    'sustainablemanufacturing', 'greenmanufacturing', 'circulareconomy', 'ecofriendly',
                    'carbonneutral', 'zerowaste', 'renewableenergy',
                    # Advanced Manufacturing
                    'additivemanufacturing', '3dprinting', 'cnc', 'automation', 'robotics',
                    'industry40', 'smartmanufacturing', 'iot', 'digitaltwin',
                    # Materials & Engineering
                    'materials', 'metals', 'plastics', 'composites', 'ceramics',
                    'materialscience', 'metallurgy', 'polymers', 'nanotechnology',
                    # Trade Shows & Networking
                    'tradeshows', 'manufacturingexpo', 'industrialexpo', 'b2bnetworking'
                ],
                'search_terms': [
                    # Global Manufacturing Opportunities
                    'mexico manufacturing partner', 'vietnam production facility', 'india manufacturing quote',
                    'nearshoring manufacturing', 'us manufacturing partnership', 'global supply chain',
                    # Industry-Specific Manufacturing
                    'automotive parts manufacturing', 'electronics contract manufacturing', 'medical device production',
                    'aerospace manufacturing certification', 'pharmaceutical manufacturing partnership',
                    # Prototype & Development
                    'rapid prototype manufacturing', 'small batch production run', 'custom part manufacturing',
                    'product development partner', 'prototype to production', 'design for manufacturing',
                    # Quality & Compliance
                    'iso certified manufacturer', 'fda compliant manufacturing', 'quality assurance partner',
                    'regulatory compliance manufacturing', 'testing and certification', 'quality control system',
                    # Supply Chain Solutions
                    'supply chain optimization', 'vendor qualification', 'procurement partnership',
                    'lean manufacturing implementation', 'continuous improvement program',
                    # Sustainable Solutions
                    'sustainable manufacturing partner', 'carbon neutral production', 'eco-friendly manufacturing',
                    'green supply chain', 'circular economy manufacturing', 'zero waste production',
                    # Advanced Technology
                    'additive manufacturing services', '3d printing production', 'automated manufacturing',
                    'smart factory implementation', 'industry 4.0 manufacturing', 'digital manufacturing'
                ],
                'urgency_patterns': [
                    'urgent manufacturing needed', 'production crisis', 'supplier failure emergency',
                    'rush manufacturing order', 'immediate production capacity', 'time-critical manufacturing',
                    'supply chain disruption', 'manufacturing deadline pressure', 'urgent supplier qualification'
                ],
                'budget_patterns': [
                    'manufacturing investment budget', 'production cost optimization', 'tooling budget allocation',
                    'contract manufacturing pricing', 'supply chain budget', 'quality system investment',
                    'automation investment', 'manufacturing capex', 'production volume pricing'
                ],
                'min_score': 30,
                'target_tiers': ['Platinum', 'Gold']
            },
            
            # IMPORT/EXPORT & SOURCING
            'import/export business': {
                'subreddits': [
                    'ImportExport', 'alibaba', 'AliExpressDropShip', 'Aliexpress', 'ecommerce', 
                    'amazonFBA', 'dropshipping', 'entrepreneur', 'logistics', 'shipping', 'trade',
                    'FulfillmentByAmazon', 'dropship', 'reseller', 'wholesale'
                ],
                'search_terms': [
                    'china sourcing', 'alibaba supplier', 'import from china', 'chinese manufacturer',
                    'sourcing agent china', 'guangzhou supplier', 'shenzhen factory', 'yiwu market',
                    'MOQ china', 'trade assurance', 'shipping from china', 'customs clearance'
                ],
                'urgency_patterns': ['urgent sourcing', 'need supplier asap', 'rush sample', 'shipping deadline'],
                'budget_patterns': ['sourcing budget', 'import cost', 'shipping cost', 'MOQ pricing'],
                'min_score': 55,
                'target_tiers': ['Platinum', 'Gold', 'Silver']
            },
            
            # WEBSITE DEVELOPMENT & DIGITAL SERVICES
            'website development': {
                'subreddits': [
                    'smallbusiness', 'entrepreneur', 'startups', 'business', 'LocalBusiness',
                    'webdev', 'web_design', 'webdevelopment', 'WordPress', 'woocommerce',
                    'shopify', 'squarespace', 'freelance', 'SEO', 'digitalmarketing',
                    'restaurantowners', 'realestate', 'fitness', 'healthcare', 'legal'
                ],
                'search_terms': [
                    'need a website', 'website development', 'build a website', 'website designer',
                    'local business website', 'small business website', 'professional website',
                    'online store development', 'wordpress development', 'website redesign',
                    'mobile responsive website', 'business website', 'website launch'
                ],
                'urgency_patterns': [
                    'need website asap', 'website launch next week', 'business opening soon',
                    'website down', 'urgent website help', 'deadline approaching'
                ],
                'budget_patterns': [
                    'website budget', 'affordable website', 'website cost', 'web development budget',
                    'professional website investment', 'website pricing'
                ],
                'min_score': 15,
                'target_tiers': ['Platinum', 'Gold', 'Silver']
            },
            
            # E-COMMERCE & ONLINE BUSINESS
            'e-commerce products': {
                'subreddits': [
                    'ecommerce', 'shopify', 'amazonFBA', 'FulfillmentByAmazon', 'dropship', 
                    'dropshipping', 'AmazonSeller', 'shopifystore', 'etsy', 'entrepreneur', 
                    'onlinebusiness', 'passive_income', 'ecom', 'FBA'
                ],
                'search_terms': [
                    'product launch', 'online store help', 'shopify expert', 'amazon optimization',
                    'product sourcing', 'dropshipping products', 'private label', 'product research',
                    'ecommerce marketing', 'conversion optimization', 'product photography'
                ],
                'urgency_patterns': ['launch deadline', 'urgent optimization', 'sales dropping', 'competition pressure'],
                'budget_patterns': ['marketing budget', 'advertising spend', 'inventory investment', 'store setup cost'],
                'min_score': 45,
                'target_tiers': ['Platinum', 'Gold', 'Silver', 'Bronze']
            },
            
            # DIGITAL MARKETING SERVICES
            'digital marketing services': {
                'subreddits': [
                    'marketing', 'DigitalMarketing', 'PPC', 'FacebookAds', 'GoogleAds', 'SEO', 
                    'growthHacking', 'MarketingAdvice', 'entrepreneur', 'smallbusiness', 'startups',
                    'SocialMediaMarketing', 'contentmarketing', 'advertising'
                ],
                'search_terms': [
                    'digital marketing help', 'marketing strategy', 'lead generation', 'conversion optimization',
                    'facebook ads expert', 'google ads help', 'marketing funnel', 'brand awareness',
                    'customer acquisition', 'marketing ROI', 'growth hacking', 'viral marketing'
                ],
                'urgency_patterns': ['marketing crisis', 'launch campaign', 'urgent optimization', 'competitor threat'],
                'budget_patterns': ['marketing budget', 'ad spend', 'customer acquisition cost', 'ROI target'],
                'min_score': 40,
                'target_tiers': ['Platinum', 'Gold', 'Silver', 'Bronze']
            },
            
            # WEB & SOFTWARE DEVELOPMENT
            'web development': {
                'subreddits': [
                    'webdev', 'programming', 'reactjs', 'node', 'javascript', 'softwaredevelopment', 
                    'web_design', 'entrepreneur', 'startups', 'freelance', 'python', 'django',
                    'flask', 'nextjs', 'vue'
                ],
                'search_terms': [
                    'web developer needed', 'website development', 'custom web app', 'full stack developer',
                    'react developer', 'node.js expert', 'responsive website', 'web application',
                    'database development', 'API integration', 'website optimization'
                ],
                'urgency_patterns': ['urgent development', 'website down', 'launch deadline', 'critical bug'],
                'budget_patterns': ['development budget', 'project cost', 'hourly rate', 'fixed price'],
                'min_score': 50,
                'target_tiers': ['Platinum', 'Gold', 'Silver']
            },
            
            # BUSINESS CONSULTING
            'consulting services': {
                'subreddits': [
                    'consulting', 'entrepreneur', 'smallbusiness', 'startups', 'business', 
                    'BusinessIntelligence', 'strategy', 'management', 'financialplanning',
                    'businessanalysis', 'advancedentrepreneur'
                ],
                'search_terms': [
                    'business consultant', 'strategy consulting', 'business advice', 'growth strategy',
                    'business optimization', 'operational efficiency', 'market analysis', 'business planning',
                    'financial consulting', 'management consulting', 'startup advisor'
                ],
                'urgency_patterns': ['urgent consultation', 'crisis management', 'immediate advice', 'emergency planning'],
                'budget_patterns': ['consulting budget', 'advisor fee', 'retainer cost', 'project investment'],
                'min_score': 55,
                'target_tiers': ['Platinum', 'Gold', 'Silver']
            },
            
            # SOFTWARE SOLUTIONS
            'software solutions': {
                'subreddits': [
                    'programming', 'softwaredevelopment', 'SaaS', 'startups', 'entrepreneur', 
                    'technology', 'automation', 'productivity', 'MachineLearning', 'artificial',
                    'datascience', 'cybersecurity'
                ],
                'search_terms': [
                    'custom software', 'software solution', 'automation tool', 'business software',
                    'enterprise software', 'workflow automation', 'data management', 'software integration',
                    'mobile app development', 'desktop application', 'cloud solution'
                ],
                'urgency_patterns': ['urgent software', 'system failure', 'automation needed', 'efficiency crisis'],
                'budget_patterns': ['software budget', 'development cost', 'licensing fee', 'implementation cost'],
                'min_score': 50,
                'target_tiers': ['Platinum', 'Gold', 'Silver']
            },
            
            # BUSINESS AUTOMATION
            'business automation': {
                'subreddits': [
                    'automation', 'productivity', 'entrepreneur', 'smallbusiness', 'workflow', 
                    'efficiency', 'operations', 'zapier', 'nocode', 'business', 'RPA'
                ],
                'search_terms': [
                    'business automation', 'process automation', 'workflow optimization', 'efficiency improvement',
                    'manual process', 'repetitive tasks', 'time-saving solution', 'operational efficiency',
                    'system integration', 'data automation', 'reporting automation'
                ],
                'urgency_patterns': ['efficiency crisis', 'urgent automation', 'process breakdown', 'scaling pressure'],
                'budget_patterns': ['automation budget', 'efficiency investment', 'time savings value', 'ROI calculation'],
                'min_score': 45,
                'target_tiers': ['Platinum', 'Gold', 'Silver', 'Bronze']
            },
            
            # SOCIAL MEDIA & CONTENT CREATION
            'social media posting': {
                'subreddits': [
                    'socialmedia', 'SocialMediaMarketing', 'ContentCreation', 'instagram', 'tiktok', 
                    'youtube', 'influencer', 'contentcreator', 'CreatorEconomy', 'SocialMediaTips',
                    'InstagramGrowth', 'TikTokGrowth', 'YouTubeCreators', 'PersonalBranding', 
                    'InfluencerMarketing', 'InstagramMarketing', 'TikTokCreators'
                ],
                'search_terms': [
                    'content creation help', 'social media burnout', 'posting consistency', 'content strategy',
                    'engagement boost', 'follower growth', 'content calendar', 'social media manager',
                    'algorithm changes', 'content ideas', 'brand partnerships', 'monetize content'
                ],
                'urgency_patterns': ['content emergency', 'posting deadline', 'engagement dropping', 'algorithm penalty'],
                'budget_patterns': ['content budget', 'creator fee', 'promotion budget', 'collaboration cost'],
                'min_score': 15,
                'target_tiers': ['Platinum', 'Gold', 'Silver', 'Bronze']
            },
            
            # VIDEO EDITING & PRODUCTION - ITERATION 1 OPTIMIZED
            'video editing': {
                'subreddits': [
                    # Platform-Specific Creator Communities
                    'YouTubeCreators', 'TikTokCreators', 'InstagramReels', 'YouTubeHelp', 'NewTubers',
                    'PartneredYouTube', 'smallytchannel', 'CreatorServices', 'ContentCreation',
                    # Professional Video Production
                    'videoediting', 'videography', 'filmmakers', 'cinematography', 'FilmIndustryLA',
                    'VideoEngineering', 'PostProduction', 'ColorGrading', 'MotionDesign',
                    # Software-Specific Communities
                    'premiere', 'aftereffects', 'finalcut', 'davinciresolve', 'avid', 'resolve',
                    'AfterEffectsTemplates', 'VideoEditingTutorials', 'MotionGraphics',
                    # Live Streaming & Events
                    'streaming', 'obs', 'LivestreamFail', 'Twitch', 'streamers', 'BroadcastEngineering',
                    'EventProduction', 'LiveEvents', 'CorporateAV',
                    # Wedding & Event Videography
                    'weddingvideography', 'WeddingPhotography', 'EventPhotography', 'WeddingPlanning',
                    'BridalExchange', 'WeddingIndustry', 'EventPlanning',
                    # Corporate & Business Video
                    'corporatevideo', 'marketing', 'DigitalMarketing', 'VideoMarketing', 'B2BMarketing',
                    'CorporateTraining', 'eLearning', 'EdTech',
                    # Documentary & Film
                    'Documentaries', 'indiefilm', 'Filmmakers', 'screenwriting', 'filmmaking',
                    'DocumentaryFilmmaking', 'FilmFestival', 'IndependentFilm',
                    # Audio Post-Production
                    'AudioPost', 'WeAreTheMusicMakers', 'audioengineering', 'podcasting',
                    'VoiceActing', 'recordingstudio', 'AudioProduction',
                    # Educational Content Creation
                    'Teachers', 'OnlineEducation', 'coursecreators', 'udemy', 'skillshare',
                    'EducationalTechnology', 'LearningDesign',
                    # Gaming & Esports Video
                    'Twitch', 'gaming', 'esports', 'GameDev', 'youtubegaming',
                    'StreamerSupport', 'GamingVideos', 'esportsproduction'
                ],
                'search_terms': [
                    # Platform-Specific Editing Needs
                    'youtube video editor needed', 'tiktok video editing help', 'instagram reels editor',
                    'shorts video editing', 'long-form content editing', 'youtube channel growth editing',
                    # Professional Production Services
                    'professional video editor', 'commercial video production', 'corporate video editing',
                    'documentary post-production', 'film editing services', 'broadcast quality editing',
                    # Software-Specific Expertise
                    'premiere pro video editor', 'after effects motion graphics', 'davinci resolve colorist',
                    'final cut pro editor', 'avid media composer', 'color grading services',
                    # Live Streaming & Event Production
                    'live stream production', 'multi-camera editing', 'event video editing',
                    'webinar post-production', 'conference video editing', 'livestream highlights',
                    # Wedding & Event Videography
                    'wedding video editor', 'same-day edit wedding', 'event videography editing',
                    'wedding highlight reel', 'ceremony video editing', 'reception video production',
                    # Corporate & Training Content
                    'corporate training videos', 'explainer video editing', 'product demo videos',
                    'testimonial video editing', 'company culture videos', 'internal communications video',
                    # Audio Post-Production
                    'video audio cleanup', 'podcast video editing', 'voiceover sync editing',
                    'audio restoration video', 'dialogue editing', 'sound design video',
                    # Educational & Course Content
                    'online course video editing', 'educational content editing', 'tutorial video production',
                    'lecture video editing', 'instructional design video', 'e-learning video production',
                    # Gaming & Entertainment
                    'gaming video editing', 'twitch highlight editing', 'esports video production',
                    'gameplay video editing', 'streaming content editing', 'tournament video editing'
                ],
                'urgency_patterns': [
                    'urgent video editing needed', 'same-day video turnaround', 'deadline tomorrow editing',
                    'wedding this weekend editing', 'live event editing rush', 'client presentation deadline',
                    'youtube upload schedule pressure', 'campaign launch video deadline', 'festival submission deadline',
                    'broadcast deadline editing', 'social media posting urgency', 'product launch video rush'
                ],
                'budget_patterns': [
                    'video editing budget allocated', 'per-minute editing rate', 'rush editing premium',
                    'ongoing editing retainer', 'bulk video editing discount', 'corporate video budget',
                    'wedding videography investment', 'content creation budget', 'marketing video spend',
                    'production company rates', 'freelance editor budget', 'editing service pricing'
                ],
                'min_score': 20,  # Lowered for better lead volume
                'target_tiers': ['Platinum', 'Gold', 'Silver']
            },
            
            # DRONE SERVICES & AERIAL SOLUTIONS - ITERATION 1 OPTIMIZED
            'selling/trading drones': {
                'subreddits': [
                    # Commercial Certification & Professional
                    'part107', 'commercialdrones', 'uavs', 'dronesforwork', 'aerialservices',
                    # Industry-Specific Applications
                    'constructiondrones', 'agriculturedrones', 'realestatephotography', 'surveying', 'mapping',
                    'emergencyservices', 'searchandrescue', 'fireandsafety', 'lawenforcement',
                    # Thermal & Inspection Specialization
                    'thermalimaging', 'industrialinspection', 'powerlineinspection', 'roofinspection',
                    'bridgeinspection', 'pipelineinspection', 'solarinspection',
                    # Cinematography & Creative
                    'aerialcinematography', 'weddingvideography', 'filmmaking', 'cinematography',
                    'dronecinema', 'aerialfilming',
                    # Delivery & Logistics
                    'dronedelivery', 'logistics', 'supplychain', 'lastmiledelivery',
                    # Manufacturer & Technical
                    'dji', 'autel', 'yuneec', 'skydio', 'parrot', 'dronerepair', 'dronemaintenance',
                    'fpv', 'multirotor', 'fixedwing'
                ],
                'search_terms': [
                    # High-Value Commercial Services
                    'part 107 certified pilot', 'commercial drone operator', 'aerial inspection services',
                    'thermal drone inspection', 'construction site surveying', 'agricultural monitoring',
                    'emergency response drone', 'search and rescue drone', 'powerline inspection',
                    'pipeline monitoring', 'roof inspection drone', 'solar panel inspection',
                    # Creative & Media Services
                    'aerial cinematography services', 'wedding drone filming', 'real estate aerial',
                    'commercial video production', 'documentary drone footage', 'event aerial coverage',
                    # Business & Investment
                    'drone service business', 'commercial drone investment', 'drone fleet management',
                    'drone insurance consultation', 'part 107 training business', 'drone pilot certification'
                ],
                'urgency_patterns': [
                    'urgent inspection needed', 'emergency drone services', 'time-sensitive surveying',
                    'weather window closing', 'project deadline drone', 'immediate aerial coverage',
                    'equipment failure inspection', 'safety compliance deadline', 'insurance claim inspection'
                ],
                'budget_patterns': [
                    'commercial drone budget', 'inspection service pricing', 'aerial survey cost',
                    'drone service investment', 'part 107 certification cost', 'equipment insurance budget',
                    'fleet management pricing', 'thermal camera rental', 'inspection contract value'
                ],
                'min_score': 25,  # Lowered for better lead volume
                'target_tiers': ['Platinum', 'Gold', 'Silver']
            }
        }
        
        # Service classification patterns for direct mapping
        self.direct_mappings = {
            'social media posting': 'social media posting',
            'video editing': 'video editing', 
            'selling/trading drones': 'selling/trading drones',
            'manufacturing & sourcing': 'manufacturing & sourcing',
            'e-commerce products': 'e-commerce products',
            'digital marketing services': 'digital marketing services',
            'web development': 'web development',
            'consulting services': 'consulting services',
            'software solutions': 'software solutions',
            'import/export business': 'import/export business',
            'business automation': 'business automation'
        }

    def find_leads_for_service(self, service_description: str, max_leads: int = 50, max_subreddits: int = 5, 
                             posts_per_subreddit: int = 400, comments_per_post: int = 0) -> Dict[str, Any]:
        """Optimized lead finding with specialized service targeting"""
        
        print(f"🎯 STARTING OPTIMIZED LEAD SEARCH")
        print(f"   Service: {service_description}")
        print(f"   Target leads: {max_leads}, Subreddits: {max_subreddits}")
        
        # Step 1: Classify service using direct mapping
        print(f"\n📊 STEP 1: SERVICE CLASSIFICATION")
        classified_service = self._classify_service_optimized(service_description)
        print(f"   Classified as: {classified_service}")
        
        # Step 2: Get targeting strategy (dynamic or specialized)
        print(f"\n🔍 STEP 2: BUILDING TARGETING STRATEGY")
        
        # Use dynamic discovery for custom services, hardcoded for known patterns
        if self._should_use_dynamic_discovery(service_description, classified_service):
            print("   Using AI-powered subreddit discovery...")
            strategy = self.dynamic_discovery.discover_optimal_subreddits(service_description, max_subreddits)
            
            # Fallback to hardcoded patterns if dynamic discovery fails
            if not strategy.get('subreddits') or len(strategy.get('subreddits', [])) == 0:
                print("   Dynamic discovery returned 0 subreddits, using hardcoded fallback...")
                strategy = self._get_optimized_strategy(classified_service, max_subreddits)
                print(f"   Fallback patterns: {len(strategy['subreddits'])} specialized communities")
            else:
                print(f"   Dynamic discovery: {len(strategy['subreddits'])} communities found")
        else:
            print("   Using optimized patterns...")
            strategy = self._get_optimized_strategy(classified_service, max_subreddits)
            print(f"   Hardcoded patterns: {len(strategy['subreddits'])} specialized communities")
            
        print(f"   Search terms: {len(strategy['search_terms'])} targeting keywords")
        
        # Step 3: Execute dynamic search until we get 3 high-quality leads
        print(f"\n🌐 STEP 3: EXECUTING DYNAMIC SEARCH (Target: 3 leads scoring 80+)")
        high_quality_leads = []
        all_prospects = []
        current_subreddits = strategy['subreddits'][:max_subreddits]
        search_round = 1
        
        while len(high_quality_leads) < 3 and search_round <= 3:
            print(f"\n   🔄 Search Round {search_round}")
            
            # Search current batch of subreddits
            prospects = self._execute_optimized_search(
                {**strategy, 'subreddits': current_subreddits}, 
                max_leads, posts_per_subreddit, comments_per_post
            )
            print(f"   Found {len(prospects)} prospects in {len(current_subreddits)} subreddits")
            all_prospects.extend(prospects)
            
            # Score and filter for high-quality leads
            qualified_leads = self._score_leads_adaptively(prospects, classified_service, service_description)
            round_high_quality = [lead for lead in qualified_leads if lead.get('lead_score', 0) >= 80]
            high_quality_leads.extend(round_high_quality)
            
            print(f"   High-quality leads this round: {len(round_high_quality)}")
            print(f"   Total high-quality leads: {len(high_quality_leads)}")
            
            if len(high_quality_leads) >= 3:
                break
                
            # Expand to more subreddits for next round
            if search_round < 3:
                next_batch_size = min(max_subreddits * (search_round + 1), len(strategy['subreddits']))
                current_subreddits = strategy['subreddits'][:next_batch_size]
                print(f"   Expanding to {len(current_subreddits)} subreddits for next round")
            
            search_round += 1
        
        # Step 4: Final processing of all leads
        print(f"\n🧠 STEP 4: FINAL LEAD PROCESSING")
        all_qualified_leads = self._score_leads_adaptively(all_prospects, classified_service, service_description)
        print(f"   Total qualified leads: {len(all_qualified_leads)}")
        print(f"   High-quality leads (80+): {len([l for l in all_qualified_leads if l.get('lead_score', 0) >= 80])}")
        
        # Step 5: Final ranking and optimization
        print(f"\n📈 STEP 5: FINAL OPTIMIZATION")
        top_leads = self._rank_and_optimize(all_qualified_leads, max_leads)
        print(f"   Optimized leads: {len(top_leads)}")
        
        # Add Reddit post links
        for lead in top_leads:
            subreddit = lead.get('subreddit', '')
            post_id = lead.get('post_id', '')
            if subreddit and post_id:
                lead['reddit_link'] = f"https://reddit.com/r/{subreddit}/comments/{post_id}/"
        
        return {
            'service_type': classified_service,
            'search_strategy': strategy,
            'total_prospects_found': len(all_prospects),
            'qualified_leads': all_qualified_leads,
            'qualified_leads_count': len(all_qualified_leads),
            'top_leads': top_leads,
            'optimization_summary': self._generate_optimization_summary(strategy, all_qualified_leads, classified_service)
        }

    def _classify_service_optimized(self, service_description: str) -> str:
        """Optimized service classification with direct mapping"""
        
        desc_lower = service_description.lower()
        
        # Check direct mappings first
        if desc_lower in self.direct_mappings:
            return self.direct_mappings[desc_lower]
        
        # Enhanced classification with better keyword matching
        service_keywords = {
            'video editing & post-production': ['video', 'editing', 'post-production', 'youtube', 'content', 'film'],
            'selling/trading drones': ['drone', 'uav', 'aerial', 'flying', 'quadcopter'],
            'manufacturing & sourcing': ['manufacturing', 'sourcing', 'production', 'factory', 'supplier'],
            'website development': ['website', 'web', 'development', 'site', 'online', 'digital', 'local business']
        }
        
        best_match = 'website development'  # Better default for web-related services
        best_score = 0
        
        # Check against keyword groups
        for service_type, keywords in service_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in desc_lower:
                    score += 10
            
            if score > best_score:
                best_score = score
                best_match = service_type
        
        # If no keyword matches, try service map overlap
        if best_score == 0:
            for service_type in self.service_map.keys():
                score = 0
                service_words = set(service_type.lower().split())
                desc_words = set(desc_lower.split())
                
                overlap = len(service_words.intersection(desc_words))
                if overlap > 0:
                    score = overlap * 10
                    
                if score > best_score:
                    best_score = score
                    best_match = service_type
        
        return best_match
    
    def _should_use_dynamic_discovery(self, service_description: str, classified_service: str) -> bool:
        """Determine whether to use dynamic discovery or hardcoded patterns"""
        
        # Always use dynamic discovery for custom/complex service descriptions
        if len(service_description.split()) > 5:  # Complex descriptions
            return True
            
        # Use dynamic for services that don't fit standard categories well
        desc_lower = service_description.lower()
        
        # If description contains specific industry/niche terms not in our patterns
        niche_indicators = [
            'podcast', 'real estate', 'medical', 'legal', 'automotive', 'fashion',
            'fitness', 'education', 'finance', 'crypto', 'blockchain', 'ai',
            'saas', 'app', 'mobile', 'website', 'ecommerce', 'dropshipping'
        ]
        
        for indicator in niche_indicators:
            if indicator in desc_lower:
                return True
        
        # Use dynamic if confidence in classification is low
        if classified_service == 'manufacturing & sourcing' and 'manufacturing' not in desc_lower:
            return True
            
        return False

    def _get_optimized_strategy(self, service_type: str, max_subreddits: int) -> Dict[str, Any]:
        """Get optimized targeting strategy for service type"""
        
        if service_type not in self.service_map:
            service_type = 'website development'  # Better fallback for custom services
            
        service_config = self.service_map[service_type]
        
        # Use all available subreddits, not just the limit
        all_subreddits = service_config['subreddits']
        selected_subreddits = all_subreddits[:min(len(all_subreddits), max_subreddits * 3)]  # Use 3x more subreddits
        
        return {
            'subreddits': selected_subreddits,
            'search_terms': service_config['search_terms'],
            'urgency_patterns': service_config.get('urgency_patterns', []),
            'budget_patterns': service_config.get('budget_patterns', []),
            'min_score': service_config.get('min_score', 40),
            'target_tiers': service_config.get('target_tiers', ['Platinum', 'Gold', 'Silver', 'Bronze'])
        }

    def _execute_optimized_search(self, strategy: Dict[str, Any], max_leads: int, 
                                posts_per_subreddit: int, comments_per_post: int) -> List[Dict[str, Any]]:
        """Execute optimized parallel search"""
        
        import concurrent.futures
        
        all_prospects = []
        
        def search_subreddit_optimized(subreddit_term_pair):
            subreddit, search_term = subreddit_term_pair
            try:
                print(f"   🔍 Searching r/{subreddit} for '{search_term}'...")
                results = self.reddit_scraper.search_subreddit(
                    subreddit, 
                    search_term, 
                    limit=posts_per_subreddit,
                    max_comments_per_post=0  # No comments processing
                )
                
                prospects = []
                for post in results.get('posts', []):
                    post['source_subreddit'] = subreddit
                    post['search_term'] = search_term
                    post['content_type'] = 'post'
                    prospects.append(post)
                
                print(f"   ✅ r/{subreddit}: Found {len(results.get('posts', []))} posts")
                return prospects
            except Exception as e:
                print(f"   ❌ r/{subreddit}: Search failed - {str(e)}")
                return []
        
        # Create search pairs
        search_pairs = []
        for subreddit in strategy['subreddits']:
            for search_term in strategy['search_terms'][:3]:  # Top 3 terms
                search_pairs.append((subreddit, search_term))
        
        # Execute parallel searches
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_pair = {executor.submit(search_subreddit_optimized, pair): pair for pair in search_pairs}
            
            for future in concurrent.futures.as_completed(future_to_pair):
                try:
                    prospects = future.result(timeout=30)
                    all_prospects.extend(prospects)
                except Exception:
                    continue
        
        return all_prospects

    def _score_leads_adaptively(self, prospects: List[Dict[str, Any]], service_type: str, 
                              service_description: str) -> List[Dict[str, Any]]:
        """Apply adaptive scoring based on service type"""
        
        print(f"   Starting adaptive scoring for {len(prospects)} prospects...")
        
        if service_type not in self.service_map:
            service_type = 'manufacturing & sourcing'
            
        service_config = self.service_map[service_type]
        min_score = service_config['min_score']
        target_tiers = service_config['target_tiers']
        
        # Fast pre-filtering
        filtered_prospects = self._fast_prefilter(prospects, service_description)
        print(f"   After pre-filter: {len(filtered_prospects)} prospects remain")
        
        qualified_leads = []
        
        # Import scoring system
        from rapid_iteration_engine import UltraAdvancedScoringV100
        ultra_scorer = UltraAdvancedScoringV100()
        
        for i, prospect in enumerate(filtered_prospects):
            if i % 20 == 0:
                print(f"   Processing batch {i//20 + 1}...")
                
            try:
                content = prospect.get('content', '')
                title = prospect.get('title', '')
                author = prospect.get('author', '')
                subreddit = prospect.get('source_subreddit', '')
                
                # Apply advanced service intelligence (Iterations 2-10)
                intelligence_analysis = service_intelligence.analyze_service_intelligence(
                    content, title, service_type
                )
                
                # Enhanced urgency and budget detection
                urgency_boost = self._detect_urgency(content, title, service_config)
                budget_boost = self._detect_budget_signals(content, title, service_config)
                
                # Add intelligence boost from 10 iterations
                intelligence_boost = intelligence_analysis.get('intelligence_score', 0) * 0.5
                
                metadata = {
                    'platform': 'reddit',
                    'subreddit': subreddit,
                    'created_utc': prospect.get('created_utc', ''),
                    'score': prospect.get('score', 0),
                    'num_comments': prospect.get('num_comments', 0),
                    'content_type': prospect.get('content_type', 'post'),
                    'urgency_boost': urgency_boost,
                    'budget_boost': budget_boost
                }
                
                scoring_result = ultra_scorer.ultra_score_lead(content, title, author, metadata)
                ultra_score = scoring_result['ultra_score']
                classification = scoring_result['classification']
                
                # Apply service-specific boosts with intelligence enhancement
                final_score = ultra_score + urgency_boost + budget_boost + intelligence_boost
                
                # More permissive qualification logic
                score_threshold = max(20, min_score * 0.6)  # Lower threshold
                tier_qualified = classification['tier'] in target_tiers or classification['tier'] != 'None'
                
                if (final_score >= score_threshold and tier_qualified):
                    
                    qualified_leads.append({
                        **prospect,
                        'lead_score': final_score,
                        'base_score': ultra_score,
                        'urgency_boost': urgency_boost,
                        'budget_boost': budget_boost,
                        'intelligence_boost': intelligence_boost,
                        'intelligence_analysis': intelligence_analysis,
                        'classification_tier': classification['tier'],
                        'priority_level': classification['priority'],
                        'service_optimized': True,
                        'optimization_tier': intelligence_analysis.get('optimization_tier', 'standard'),
                        'specialization_level': intelligence_analysis.get('service_analysis', {}).get('specialization_level', 'basic'),
                        'recommendations': intelligence_analysis.get('recommendations', []),
                        'author': author,
                        'subreddit': subreddit,
                        'content': content[:500]
                    })
            except Exception:
                continue
        
        print(f"   ✅ Adaptive scoring complete: {len(qualified_leads)} qualified leads")
        return qualified_leads

    def _fast_prefilter(self, prospects: List[Dict[str, Any]], service_description: str) -> List[Dict[str, Any]]:
        """Fast pre-filtering for efficiency"""
        
        filtered = []
        service_words = set(service_description.lower().split())
        
        for prospect in prospects:
            content = (prospect.get('content', '') + ' ' + prospect.get('title', '')).lower()
            
            # Skip very short or deleted content
            if len(content) < 15 or content in ['[deleted]', '[removed]', '']:
                continue
                
            # Must have some relevance
            content_words = set(content.split())
            business_terms = {'need', 'looking', 'help', 'service', 'business', 'urgent', 'budget', 'cost'}
            
            if (len(service_words.intersection(content_words)) > 0 or 
                len(business_terms.intersection(content_words)) > 0):
                filtered.append(prospect)
        
        return filtered

    def _detect_urgency(self, content: str, title: str, service_config: Dict) -> float:
        """Detect urgency indicators for scoring boost"""
        
        text = (content + ' ' + title).lower()
        urgency_boost = 0
        
        for pattern in service_config.get('urgency_patterns', []):
            if pattern.lower() in text:
                urgency_boost += 5
                
        # General urgency terms
        general_urgent = ['urgent', 'asap', 'immediately', 'rush', 'deadline', 'emergency']
        for term in general_urgent:
            if term in text:
                urgency_boost += 3
                
        return min(urgency_boost, 15)  # Cap at 15 points

    def _detect_budget_signals(self, content: str, title: str, service_config: Dict) -> float:
        """Detect budget indicators for scoring boost"""
        
        text = (content + ' ' + title).lower()
        budget_boost = 0
        
        for pattern in service_config.get('budget_patterns', []):
            if pattern.lower() in text:
                budget_boost += 4
                
        # General budget terms
        budget_terms = ['budget', 'cost', 'price', 'investment', 'spend', 'fee', 'rate']
        for term in budget_terms:
            if term in text:
                budget_boost += 2
                
        return min(budget_boost, 12)  # Cap at 12 points

    def _rank_and_optimize(self, leads: List[Dict[str, Any]], max_results: int) -> List[Dict[str, Any]]:
        """Final ranking and optimization"""
        
        print(f"   Ranking {len(leads)} qualified leads...")
        
        # Multi-dimensional sorting
        leads.sort(key=lambda x: (
            x.get('lead_score', 0),
            x.get('urgency_boost', 0),
            x.get('budget_boost', 0),
            x.get('score', 0)  # Reddit engagement score
        ), reverse=True)
        
        # Remove duplicates by author
        seen_authors = set()
        final_leads = []
        
        for lead in leads:
            author = lead.get('author', '')
            if author not in seen_authors and len(final_leads) < max_results:
                seen_authors.add(author)
                final_leads.append(lead)
        
        print(f"   🏆 Final optimization: {len(final_leads)} unique leads")
        return final_leads

    def _generate_optimization_summary(self, strategy: Dict, leads: List[Dict], service_type: str) -> Dict[str, Any]:
        """Generate optimization summary"""
        
        if not leads:
            return {
                'optimization_level': 'Low',
                'recommendations': ['Expand search terms', 'Try different subreddits', 'Adjust timing'],
                'service_match': 'Needs improvement'
            }
        
        avg_score = sum(lead.get('lead_score', 0) for lead in leads) / len(leads)
        high_quality_count = sum(1 for lead in leads if lead.get('lead_score', 0) >= 70)
        
        return {
            'optimization_level': 'High' if avg_score >= 60 else 'Medium' if avg_score >= 40 else 'Low',
            'average_score': round(avg_score, 1),
            'high_quality_leads': high_quality_count,
            'service_match': 'Excellent',
            'subreddits_searched': len(strategy['subreddits']),
            'search_terms_used': len(strategy['search_terms'])
        }

    def get_supported_services(self) -> List[str]:
        """Get list of optimized service types"""
        return list(self.service_map.keys())