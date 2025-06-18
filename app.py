import streamlit as st
import json
from datetime import datetime
from typing import Dict, Any, List

# Import enhanced modules
from enhanced_reddit_scraper import EnhancedRedditScraper
from crm_system import CRMSystem
from optimized_lead_finder import OptimizedLeadFinder

# Configure page
st.set_page_config(
    page_title="Reddit Lead Generator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load translations
TRANSLATIONS = {
    'en': {
        'title': 'Reddit Lead Generator',
        'lead_finder': 'Lead Finder',
        'crm_dashboard': 'CRM Dashboard',
        'analytics': 'Analytics',
        'settings': 'Settings',
        'find_customers': 'Find Customers',
        'service_type': 'Select Service Type',
        'describe_service': 'Describe Your Service',
        'search_results': 'Lead Discovery Results',
        'no_leads': 'No qualified leads found. Try adjusting your service description.',
        'search_error': 'Search error occurred',
        'leads_found': 'qualified leads found for'
    }
}

def get_text(key, lang='en'):
    """Get translated text for the given key and language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

def display_lead_finder():
    """Display lead discovery interface"""
    
    # Simplified header
    st.title("🎯 AI Lead Discovery")
    
    # Compact form in container
    with st.container():
        # Service selection
        service_options = [
            "Social Media Management",
            "Virtual Assistant Services", 
            "YouTube Video Editing",
            "Manufacturing & Sourcing",
            "E-commerce Store Setup",
            "Custom Description"
        ]
        
        selected_service = st.selectbox("Service Type", service_options, index=0)
        
        # Conditional input
        if selected_service == "Custom Description":
            service_description = st.text_area(
                "Describe Your Service",
                placeholder="e.g., podcast editing for real estate agents...",
                height=80,
                label_visibility="collapsed"
            )
        else:
            service_description = selected_service.lower()
        
        # Compact platform selector
        st.markdown("**Data Sources**")
        col1, col2, col3, col4 = st.columns(4)
        
        # Initialize platform state
        if 'platforms' not in st.session_state:
            st.session_state.platforms = {'reddit': True, 'facebook': False, 'twitter': False, 'linkedin': False}
        
        with col1:
            reddit_icon = "🟠" if st.session_state.platforms['reddit'] else "⚫"
            if st.button(f"{reddit_icon} Reddit", key="reddit", use_container_width=True):
                st.session_state.platforms['reddit'] = not st.session_state.platforms['reddit']
                st.rerun()
        
        with col2:
            st.button("⚫ Facebook", disabled=True, use_container_width=True, help="Coming soon")
        
        with col3:
            st.button("⚫ Twitter", disabled=True, use_container_width=True, help="Coming soon")
        
        with col4:
            st.button("⚫ LinkedIn", disabled=True, use_container_width=True, help="Coming soon")
        
        # Status and search
        if st.session_state.platforms['reddit'] and service_description and service_description.strip():
            if st.button("🚀 Find Customers", type="primary", use_container_width=True):
                try:
                    # Initialize CRM system for exclusion tracking
                    crm = CRMSystem()
                    
                    finder = OptimizedLeadFinder()
                    
                    with st.spinner("Discovering prospects with exclusion filtering..."):
                        results = finder.find_leads_for_service(
                            service_description=service_description,
                            max_leads=50,
                            max_subreddits=15,
                            posts_per_subreddit=400,
                            comments_per_post=0
                        )
                        
                        # Apply CRM exclusion filtering to results
                        if results and 'top_leads' in results:
                            excluded_ids = set(crm.get_exclusion_list())
                            original_count = len(results['top_leads'])
                            
                            # Filter out excluded leads
                            filtered_leads = [
                                lead for lead in results['top_leads'] 
                                if lead.get('id') not in excluded_ids
                            ]
                            
                            excluded_count = original_count - len(filtered_leads)
                            
                            # Update results with filtered leads and exclusion stats
                            results['top_leads'] = filtered_leads
                            results['exclusion_summary'] = {
                                'total_excluded': excluded_count,
                                'total_found': original_count,
                                'exclusion_rate_percent': (excluded_count / max(original_count, 1)) * 100,
                                'posts_processed': len(filtered_leads)
                            }
                    
                    st.session_state.lead_results = results
                    st.session_state.selected_service = service_description
                    st.session_state.crm = crm
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Search error: {str(e)}")
        else:
            disabled_reason = "Enable Reddit and describe your service" if not st.session_state.platforms['reddit'] else "Describe your service"
            st.button("🚀 Find Customers", disabled=True, use_container_width=True, help=disabled_reason)
    
    # Results section
    if 'lead_results' in st.session_state and st.session_state.lead_results:
        st.markdown("---")
        display_search_results(st.session_state.lead_results, st.session_state.get('selected_service', 'Service'))

def display_search_results(results, service_description):
    """Display results from lead search with CRM integration"""
    
    st.markdown("---")
    st.markdown("## 🎯 Lead Discovery Results")
    
    if 'top_leads' in results and results['top_leads']:
        leads = results['top_leads']
        
        # Show exclusion summary if available
        if 'exclusion_summary' in results:
            exclusion_info = results['exclusion_summary']
            if exclusion_info.get('total_excluded', 0) > 0:
                st.info(f"Excluded {exclusion_info['total_excluded']} posts already in CRM ({exclusion_info.get('exclusion_rate_percent', 0):.1f}% exclusion rate)")
        
        st.success(f"Found {len(leads)} qualified leads for: **{service_description}**")
        
        # Display leads in cards with CRM functionality
        for i, lead in enumerate(leads):
            with st.expander(f"Lead #{i+1} - Score: {lead.get('lead_score', 0):.1f}", expanded=i < 3):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Subreddit:** r/{lead.get('subreddit', 'unknown')}")
                    st.markdown(f"**Author:** {lead.get('author', 'unknown')}")
                    st.markdown(f"**Title:** {lead.get('title', 'No title')}")
                    st.markdown(f"**Content Preview:**")
                    st.markdown(f"_{lead.get('content', 'No content')[:200]}..._")
                
                with col2:
                    st.metric("Lead Score", f"{lead.get('lead_score', 0):.1f}")
                    st.metric("Priority", lead.get('priority_level', 'Unknown'))
                    
                    if 'reddit_link' in lead or 'url' in lead:
                        reddit_url = lead.get('reddit_link', lead.get('url', ''))
                        st.markdown(f"[View on Reddit]({reddit_url})")
                    
                    # CRM Action Buttons
                    st.markdown("**CRM Actions:**")
                    
                    # Check if lead is already in CRM
                    lead_in_crm = False
                    if 'crm' in st.session_state:
                        crm = st.session_state.crm
                        excluded_ids = set(crm.get_exclusion_list())
                        lead_in_crm = lead.get('id') in excluded_ids
                    
                    if lead_in_crm:
                        st.caption("✅ Lead saved in CRM")
                        st.info("Lead already in CRM database")
                    else:
                        # Add to CRM button for new leads
                        crm_key = f"add_crm_{lead.get('id', i)}"
                        if st.button("📝 Add to CRM", key=crm_key, use_container_width=True):
                            if 'crm' in st.session_state:
                                crm = st.session_state.crm
                                
                                # Normalize lead data for CRM compatibility
                                normalized_lead = {
                                    'id': lead.get('id') or lead.get('post_id') or f"lead_{i}",
                                    'author': lead.get('author') or lead.get('username', 'Unknown'),
                                    'title': lead.get('title', ''),
                                    'content': lead.get('content') or lead.get('text') or lead.get('body', ''),
                                    'subreddit': lead.get('subreddit', ''),
                                    'reddit_link': lead.get('reddit_link') or lead.get('url') or lead.get('link', ''),
                                    'lead_score': lead.get('lead_score', 0),
                                    'priority_level': lead.get('priority_level', 'Unknown')
                                }
                                
                                try:
                                    result = crm.save_lead_to_crm(
                                        post_data=normalized_lead,
                                        lead_score=normalized_lead['lead_score'],
                                        notes=""
                                    )
                                    if result.get('success'):
                                        st.success(f"Saved to CRM: {result['message']}")
                                        st.rerun()
                                    else:
                                        st.error(f"Failed to save: {result.get('error', 'Unknown error')}")
                                except Exception as e:
                                    st.error(f"CRM Save Error: {str(e)}")
                                    with st.expander("Debug Info"):
                                        st.write("Original lead:", lead)
                                        st.write("Normalized lead:", normalized_lead)
                

    
    else:
        st.warning("No qualified leads found. Try adjusting your service description.")

def display_crm_dashboard():
    """Display comprehensive CRM dashboard with saved leads"""
    st.title("📊 CRM Dashboard")
    
    # Initialize CRM if not exists
    if 'crm' not in st.session_state:
        st.session_state.crm = CRMSystem()
    
    crm = st.session_state.crm
    
    # CRM Statistics
    stats = crm.get_crm_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", stats['total_leads'])
    with col2:
        st.metric("Excluded Posts", stats['exclusion_list_size'])
    with col3:
        new_leads = stats['status_breakdown'].get('new', 0)
        st.metric("New Leads", new_leads)
    with col4:
        contacted_leads = stats['status_breakdown'].get('contacted', 0)
        st.metric("Contacted", contacted_leads)
    
    # Status breakdown
    if stats['status_breakdown']:
        st.markdown("### Lead Status Breakdown")
        status_col1, status_col2 = st.columns(2)
        
        with status_col1:
            for status, count in stats['status_breakdown'].items():
                st.write(f"**{status.title()}:** {count}")
        
        with status_col2:
            if stats['top_subreddits']:
                st.markdown("**Top Subreddits:**")
                for sub_data in stats['top_subreddits'][:5]:
                    st.write(f"r/{sub_data['subreddit']}: {sub_data['count']} leads")
    
    # Saved Leads Table
    st.markdown("### Saved Leads")
    
    leads = crm.get_all_leads()
    
    if leads:
        # Filter and search
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            status_filter = st.selectbox("Filter by Status", 
                                       ["All"] + list(stats['status_breakdown'].keys()))
        
        with col_filter2:
            search_term = st.text_input("Search leads", placeholder="Search by username or content")
        
        # Apply filters
        filtered_leads = leads
        if status_filter != "All":
            filtered_leads = [lead for lead in filtered_leads if lead.get('status') == status_filter]
        
        if search_term:
            search_lower = search_term.lower()
            filtered_leads = [
                lead for lead in filtered_leads 
                if search_lower in lead.get('username', '').lower() 
                or search_lower in lead.get('post_description', '').lower()
                or search_lower in lead.get('post_title', '').lower()
            ]
        
        st.write(f"Showing {len(filtered_leads)} of {len(leads)} leads")
        
        # Display leads
        for i, lead in enumerate(filtered_leads):
            with st.expander(f"{lead.get('username', 'Unknown')} - r/{lead.get('subreddit', 'unknown')} - Score: {lead.get('lead_score', 0):.1f}"):
                col_lead1, col_lead2 = st.columns([2, 1])
                
                with col_lead1:
                    st.markdown(f"**Title:** {lead.get('post_title', 'No title')}")
                    st.markdown(f"**Description:** {lead.get('post_description', 'No description')[:200]}...")
                    st.markdown(f"**Saved:** {lead.get('saved_at', 'Unknown')[:19]}")
                    
                    if lead.get('reddit_link'):
                        st.markdown(f"[View on Reddit]({lead['reddit_link']})")
                
                with col_lead2:
                    st.metric("Lead Score", f"{lead.get('lead_score', 0):.1f}")
                    
                    # Status update with mapping for old format
                    status_options = ["new", "contacted", "qualified", "closed", "rejected"]
                    current_status = lead.get('status', 'new').lower()
                    
                    # Map old status values to new ones
                    status_mapping = {
                        'new lead': 'new',
                        'contacted': 'contacted',
                        'qualified': 'qualified', 
                        'closed': 'closed',
                        'rejected': 'rejected'
                    }
                    
                    normalized_status = status_mapping.get(current_status, 'new')
                    
                    try:
                        status_index = status_options.index(normalized_status)
                    except ValueError:
                        status_index = 0  # Default to 'new'
                    
                    new_status = st.selectbox(
                        "Status", 
                        status_options,
                        index=status_index,
                        key=f"status_{lead.get('id', i)}"
                    )
                    
                    # Notes
                    notes = st.text_area(
                        "Notes", 
                        value=lead.get('user_notes', ''),
                        height=80,
                        key=f"notes_{lead.get('id', i)}"
                    )
                    
                    # Update and delete buttons
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        if st.button("Update", key=f"update_{lead.get('id', i)}"):
                            crm.update_lead_status(lead['id'], new_status, notes or "")
                            st.success("Lead updated!")
                            st.rerun()
                    
                    with col_btn2:
                        if st.button("Delete", key=f"delete_{lead.get('id', i)}", type="secondary"):
                            crm.delete_lead(lead['id'])
                            st.success("Lead deleted and removed from exclusion list!")
                            st.rerun()
                    
                    # Research button if not already researched
                    username = lead.get('username', '')
                    if username and username != '[deleted]':
                        if st.button("Research User", key=f"crm_research_{lead.get('id', i)}"):
                            with st.spinner(f"Researching {username}..."):
                                profile = crm.research_user_profile(username)
                                st.session_state[f'crm_profile_{username}'] = profile
                                st.rerun()
                        
                        # Show research if available
                        if f'crm_profile_{username}' in st.session_state:
                            profile = st.session_state[f'crm_profile_{username}']
                            if 'error' not in profile:
                                st.markdown("**User Research:**")
                                st.metric("Lead Potential", f"{profile.get('lead_potential', 0)}/100")
                                
                                pain_points = profile.get('pain_points', [])
                                if pain_points:
                                    st.markdown("**Pain Points:**")
                                    for pain in pain_points[:2]:
                                        st.write(f"• {pain[:80]}...")
    else:
        st.info("No leads saved yet. Find leads using the Lead Finder to populate your CRM.")
        
        if st.button("Go to Lead Finder"):
            st.session_state.page = "Lead Finder"
            st.rerun()

def display_crm_analytics():
    """Display analytics placeholder"""
    st.title("📈 Analytics")
    st.info("Analytics functionality coming soon...")

def main():
    """Main application entry point"""
    
    # Sidebar navigation and guide
    with st.sidebar:
        st.title("🎯 Reddit Lead Generator")
        
        page = st.radio(
            "Navigation",
            ["Lead Finder", "CRM Dashboard", "Analytics"],
            index=0
        )
        
        # Compact guide section
        if page == "Lead Finder":
            st.markdown("---")
            
            # Single compact guide expander
            with st.expander("📖 Quick Guide", expanded=False):
                
                # Tabbed interface for better organization
                tab1, tab2, tab3 = st.tabs(["🎯 Best For", "🚀 How-To", "📊 Services"])
                
                with tab1:
                    st.markdown("""
                    **Ideal Users:**
                    Creative professionals, digital marketers, VAs, consultants serving creators & small businesses
                    
                    **Sweet Spot:** Services with active Reddit discussions about pain points
                    """)
                
                with tab2:
                    st.markdown("""
                    1. Select service type
                    2. Enable Reddit source  
                    3. Click "Find Customers"
                    4. Review scored leads
                    
                    💡 Use "Custom" for niche services
                    """)
                
                with tab3:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        **Creative:**
                        • YouTube Video Editing
                        • Podcast Production
                        • Wedding Video
                        • Logo Design
                        • Thumbnail Design
                        • Voice-over Services
                        • Content Creation
                        • Graphics Design
                        • Video Production
                        • Brand Design
                        """)
                    with col2:
                        st.markdown("""
                        **Business:**
                        • Social Media Mgmt
                        • Virtual Assistant
                        • E-commerce Setup
                        • SEO Services
                        • Web Development
                        • Email Marketing
                        • Content Writing
                        • Facebook Ads
                        • Process Automation
                        • Online Courses
                        """)
            
            # Minimal footer
            st.markdown("*Facebook, Twitter, LinkedIn coming soon*")
    
    # Main content area
    if page == "Lead Finder":
        display_lead_finder()
    elif page == "CRM Dashboard":
        display_crm_dashboard()
    elif page == "Analytics":
        display_crm_analytics()

if __name__ == "__main__":
    main()