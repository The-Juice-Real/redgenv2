"""
Service Tournament Analysis
Ranking 30 services based on Reddit lead generation effectiveness
"""

services = [
    "YouTube Video Editing",
    "TikTok Content Creation", 
    "Instagram Reels Editing",
    "Podcast Editing & Production",
    "Wedding Video Editing",
    "Corporate Video Production",
    "Logo Design & Branding",
    "Social Media Graphics Design",
    "Thumbnail Design for YouTubers",
    "Voice-over Services",
    "Social Media Management",
    "Content Writing & Copywriting",
    "Email Marketing Automation",
    "Instagram Growth Services",
    "YouTube Channel Optimization",
    "Facebook Ads Management",
    "Google Ads Management",
    "SEO Services",
    "Influencer Outreach",
    "Lead Generation Services",
    "Virtual Assistant Services",
    "Data Entry & Management",
    "Business Process Automation",
    "Online Course Creation",
    "E-commerce Store Setup",
    "Website Development",
    "Mobile App Development",
    "Bookkeeping & Accounting",
    "Customer Service Outsourcing",
    "Project Management Consulting"
]

def analyze_reddit_effectiveness(service):
    """Analyze how well our Reddit tool serves each service"""
    
    # Scoring factors (1-10 scale):
    # 1. Reddit community activity
    # 2. Lead quality indicators
    # 3. Conversion potential
    # 4. Pain point frequency
    # 5. User engagement patterns
    
    scores = {
        "YouTube Video Editing": {
            "reddit_activity": 9,  # r/YouTubeCreators, r/NewTubers very active
            "lead_quality": 8,     # Clear pain points, budget discussions
            "conversion": 8,       # Direct need, immediate solutions
            "pain_frequency": 9,   # Constant editing struggles
            "engagement": 8,       # High emotional investment
            "total": 42
        },
        "TikTok Content Creation": {
            "reddit_activity": 7,  # r/TikTokCreators active but smaller
            "lead_quality": 6,     # Often younger demographic, lower budgets
            "conversion": 6,       # Quick turnaround expectations
            "pain_frequency": 8,   # Daily content pressure
            "engagement": 7,       # High but transient
            "total": 34
        },
        "Instagram Reels Editing": {
            "reddit_activity": 6,  # Less Reddit discussion than YouTube
            "lead_quality": 5,     # Mixed quality, some low budget
            "conversion": 6,       # Fast-paced environment
            "pain_frequency": 7,   # Regular need but less discussed
            "engagement": 6,       # Moderate engagement
            "total": 30
        },
        "Podcast Editing & Production": {
            "reddit_activity": 8,  # r/podcasting very active
            "lead_quality": 9,     # Professional podcasters with budgets
            "conversion": 9,       # Long-term recurring need
            "pain_frequency": 8,   # Technical complexity discussions
            "engagement": 8,       # Professional investment
            "total": 42
        },
        "Wedding Video Editing": {
            "reddit_activity": 7,  # r/WeddingPhotography, r/WeddingPlanning
            "lead_quality": 9,     # High-value clients, urgent timelines
            "conversion": 8,       # Emotional purchase, premium pricing
            "pain_frequency": 6,   # Seasonal, specific timing
            "engagement": 8,       # High emotional investment
            "total": 38
        },
        "Corporate Video Production": {
            "reddit_activity": 5,  # Limited Reddit presence for corporate
            "lead_quality": 8,     # Professional budgets
            "conversion": 7,       # Longer sales cycles
            "pain_frequency": 5,   # Less frequent Reddit discussion
            "engagement": 6,       # Professional but formal
            "total": 31
        },
        "Logo Design & Branding": {
            "reddit_activity": 7,  # r/entrepreneur, r/smallbusiness
            "lead_quality": 6,     # Wide range of budgets
            "conversion": 7,       # One-time but urgent need
            "pain_frequency": 8,   # Startup discussions frequent
            "engagement": 7,       # Identity-related, emotional
            "total": 35
        },
        "Social Media Graphics Design": {
            "reddit_activity": 6,  # Scattered across communities
            "lead_quality": 5,     # Often low-budget requests
            "conversion": 6,       # Template expectations
            "pain_frequency": 7,   # Regular need
            "engagement": 6,       # Moderate engagement
            "total": 30
        },
        "Thumbnail Design for YouTubers": {
            "reddit_activity": 8,  # Specific YouTuber pain point
            "lead_quality": 7,     # Growing creators with some budget
            "conversion": 8,       # Direct impact on views
            "pain_frequency": 9,   # Every video needs thumbnail
            "engagement": 8,       # Performance-driven
            "total": 40
        },
        "Voice-over Services": {
            "reddit_activity": 6,  # Limited specific communities
            "lead_quality": 7,     # Professional projects
            "conversion": 7,       # Specialized skill appreciation
            "pain_frequency": 5,   # Less frequent need
            "engagement": 6,       # Project-specific
            "total": 31
        },
        "Social Media Management": {
            "reddit_activity": 8,  # r/socialmedia, r/entrepreneur
            "lead_quality": 7,     # Business owners with budgets
            "conversion": 8,       # Ongoing monthly service
            "pain_frequency": 9,   # Constant struggle discussion
            "engagement": 8,       # Business growth focus
            "total": 40
        },
        "Content Writing & Copywriting": {
            "reddit_activity": 7,  # r/entrepreneur, r/marketing
            "lead_quality": 7,     # Professional service recognition
            "conversion": 8,       # Ongoing need
            "pain_frequency": 8,   # Regular content struggles
            "engagement": 7,       # Business necessity
            "total": 37
        },
        "Email Marketing Automation": {
            "reddit_activity": 6,  # More technical, smaller communities
            "lead_quality": 8,     # Professional implementation
            "conversion": 8,       # High-value service
            "pain_frequency": 6,   # Less frequent discussion
            "engagement": 7,       # ROI-focused
            "total": 35
        },
        "Instagram Growth Services": {
            "reddit_activity": 7,  # r/Instagram, r/InstagramMarketing
            "lead_quality": 6,     # Mixed quality, some sketchy
            "conversion": 7,       # Competitive market
            "pain_frequency": 8,   # Growth struggles common
            "engagement": 7,       # Results-focused
            "total": 35
        },
        "YouTube Channel Optimization": {
            "reddit_activity": 9,  # r/YouTubeCreators very active
            "lead_quality": 8,     # Serious creators seeking growth
            "conversion": 8,       # Performance-driven investment
            "pain_frequency": 9,   # Algorithm struggles constant
            "engagement": 9,       # High emotional investment
            "total": 43
        },
        "Facebook Ads Management": {
            "reddit_activity": 6,  # r/FacebookAds, r/PPC
            "lead_quality": 8,     # Business owners with ad budgets
            "conversion": 8,       # ROI-measurable service
            "pain_frequency": 7,   # Platform complexity discussions
            "engagement": 7,       # Performance-focused
            "total": 36
        },
        "Google Ads Management": {
            "reddit_activity": 6,  # r/GoogleAds, r/PPC
            "lead_quality": 8,     # Professional service market
            "conversion": 8,       # High-value clients
            "pain_frequency": 7,   # Technical complexity
            "engagement": 7,       # ROI-driven
            "total": 36
        },
        "SEO Services": {
            "reddit_activity": 7,  # r/SEO, r/entrepreneur
            "lead_quality": 7,     # Long-term focused clients
            "conversion": 7,       # Longer sales cycles
            "pain_frequency": 8,   # Ranking struggles frequent
            "engagement": 7,       # Technical appreciation
            "total": 36
        },
        "Influencer Outreach": {
            "reddit_activity": 5,  # Limited dedicated communities
            "lead_quality": 6,     # Brand-dependent budgets
            "conversion": 6,       # Relationship-building service
            "pain_frequency": 6,   # Specific campaign needs
            "engagement": 6,       # Professional networking
            "total": 29
        },
        "Lead Generation Services": {
            "reddit_activity": 6,  # r/sales, r/entrepreneur
            "lead_quality": 7,     # B2B service recognition
            "conversion": 7,       # Results-dependent
            "pain_frequency": 7,   # Sales struggles common
            "engagement": 7,       # Revenue-focused
            "total": 34
        },
        "Virtual Assistant Services": {
            "reddit_activity": 7,  # r/entrepreneur, r/productivity
            "lead_quality": 6,     # Wide range of needs/budgets
            "conversion": 7,       # Ongoing relationship potential
            "pain_frequency": 8,   # Overwhelm discussions frequent
            "engagement": 7,       # Productivity focus
            "total": 35
        },
        "Data Entry & Management": {
            "reddit_activity": 4,  # Limited Reddit discussion
            "lead_quality": 5,     # Often low-budget work
            "conversion": 5,       # Price-competitive market
            "pain_frequency": 5,   # Less discussed pain point
            "engagement": 4,       # Transactional
            "total": 23
        },
        "Business Process Automation": {
            "reddit_activity": 6,  # r/automation, r/productivity
            "lead_quality": 8,     # Technical appreciation
            "conversion": 8,       # High-value optimization
            "pain_frequency": 7,   # Efficiency discussions
            "engagement": 7,       # ROI-focused
            "total": 36
        },
        "Online Course Creation": {
            "reddit_activity": 7,  # r/OnlineEducation, r/coursecreators
            "lead_quality": 7,     # Knowledge monetization focus
            "conversion": 7,       # Comprehensive service need
            "pain_frequency": 8,   # Course creation struggles
            "engagement": 8,       # Educational mission-driven
            "total": 37
        },
        "E-commerce Store Setup": {
            "reddit_activity": 8,  # r/ecommerce, r/shopify, r/entrepreneur
            "lead_quality": 8,     # Business launch investment
            "conversion": 8,       # Critical business need
            "pain_frequency": 8,   # Technical setup struggles
            "engagement": 8,       # Business success focus
            "total": 40
        },
        "Website Development": {
            "reddit_activity": 7,  # r/webdev, r/entrepreneur
            "lead_quality": 7,     # Professional service market
            "conversion": 7,       # Standard business need
            "pain_frequency": 7,   # Technical discussions
            "engagement": 7,       # Business necessity
            "total": 35
        },
        "Mobile App Development": {
            "reddit_activity": 6,  # r/androiddev, r/iOSProgramming
            "lead_quality": 8,     # High-value projects
            "conversion": 7,       # Longer development cycles
            "pain_frequency": 6,   # Technical complexity
            "engagement": 7,       # Innovation-focused
            "total": 34
        },
        "Bookkeeping & Accounting": {
            "reddit_activity": 5,  # r/bookkeeping, r/accounting
            "lead_quality": 7,     # Professional necessity
            "conversion": 8,       # Ongoing monthly need
            "pain_frequency": 6,   # Less emotionally discussed
            "engagement": 6,       # Compliance-focused
            "total": 32
        },
        "Customer Service Outsourcing": {
            "reddit_activity": 4,  # Limited Reddit presence
            "lead_quality": 7,     # Professional service
            "conversion": 7,       # Operational necessity
            "pain_frequency": 5,   # Less discussed publicly
            "engagement": 5,       # Operational focus
            "total": 28
        },
        "Project Management Consulting": {
            "reddit_activity": 5,  # r/projectmanagement
            "lead_quality": 8,     # Professional expertise
            "conversion": 7,       # Relationship-building
            "pain_frequency": 6,   # Specific problem discussions
            "engagement": 6,       # Process improvement
            "total": 32
        }
    }
    
    return scores.get(service, {"total": 0})

def run_tournament():
    """Run tournament-style ranking"""
    
    print("🏆 SERVICE TOURNAMENT ANALYSIS")
    print("Ranking services by Reddit lead generation effectiveness\n")
    
    # Get all scores
    service_scores = []
    for service in services:
        score_data = analyze_reddit_effectiveness(service)
        service_scores.append((service, score_data["total"]))
    
    # Sort by total score
    service_scores.sort(key=lambda x: x[1], reverse=True)
    
    print("📊 FINAL RANKINGS (Based on Reddit Lead Generation Effectiveness):\n")
    
    for i, (service, score) in enumerate(service_scores, 1):
        tier = "🥇 TIER 1" if score >= 40 else "🥈 TIER 2" if score >= 35 else "🥉 TIER 3" if score >= 30 else "⚪ TIER 4"
        print(f"{i:2d}. {service:<35} | Score: {score:2d} | {tier}")
    
    print("\n" + "="*80)
    print("🎯 TOP 5 RECOMMENDATIONS FOR MVP LAUNCH:")
    print("="*80)
    
    top_5 = service_scores[:5]
    for i, (service, score) in enumerate(top_5, 1):
        detail = analyze_reddit_effectiveness(service)
        print(f"\n{i}. {service} (Score: {score})")
        print(f"   Reddit Activity: {detail.get('reddit_activity', 0)}/10")
        print(f"   Lead Quality: {detail.get('lead_quality', 0)}/10") 
        print(f"   Conversion Potential: {detail.get('conversion', 0)}/10")
        print(f"   Pain Point Frequency: {detail.get('pain_frequency', 0)}/10")
        print(f"   User Engagement: {detail.get('engagement', 0)}/10")
    
    return service_scores

if __name__ == "__main__":
    rankings = run_tournament()