"""
Test the improved scoring system against the logged leads to verify accuracy
"""

from improved_lead_scoring import ImprovedLeadScoring
import json

def test_scoring_accuracy():
    scorer = ImprovedLeadScoring()
    
    # Test cases from the actual logged leads
    test_cases = [
        {
            'title': "I'm an SEO/Digital Marketing Consultant...I just helped take a client's eCommerce company from just 3 total sales, to nearly $100,00/mo revenue",
            'content': "Here's a long-ass post with some takeaways & strategies I used to get there.",
            'author': 'Sim_Strategy',
            'expected': 'Should be filtered out - content creator'
        },
        {
            'title': "3 months ago I posted the exact process on how I sold $150,000 selling T-shirt on Amazon",
            'content': "I will now explain the exact steps you can take to earn your first $1,000,000 selling on Amazon",
            'author': 'W1ZZ4RD',
            'expected': 'Should be filtered out - sharing experience'
        },
        {
            'title': "Need help finding a reliable manufacturer in China for custom electronics",
            'content': "Looking for quotes from multiple suppliers for a new product. Need samples and pricing ASAP for my startup.",
            'author': 'startup_founder',
            'expected': 'Should score high - genuine prospect'
        },
        {
            'title': "Hopefully helpful advice if you're looking for a job in Marketing",
            'content': "Here are some tips I've learned over the years...",
            'author': 'lickitysplitstyle',
            'expected': 'Should be filtered out - giving advice'
        },
        {
            'title': "Where can I find bulk suppliers for private label products?",
            'content': "I'm looking to source products from China or other Asian countries. Need minimum order quantities and pricing information.",
            'author': 'ecommerce_newbie',
            'expected': 'Should score high - genuine sourcing need'
        }
    ]
    
    print("Testing improved scoring system accuracy:\n")
    
    for i, case in enumerate(test_cases, 1):
        result = scorer.score_lead_accurately(
            case['content'], 
            case['title'], 
            case['author'], 
            'Entrepreneur'
        )
        
        print(f"Test Case {i}:")
        print(f"Title: {case['title'][:60]}...")
        print(f"Expected: {case['expected']}")
        print(f"Score: {result['lead_score']}")
        print(f"Qualified: {result['is_qualified']}")
        print(f"Intent: {result['buying_intent']['category']}")
        print(f"Reason: {result['reason']}")
        print(f"China Relevant: {result.get('china_sourcing_relevance', False)}")
        print("-" * 50)

if __name__ == "__main__":
    test_scoring_accuracy()