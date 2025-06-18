"""
Complete CRM Integration Fix
Addresses all identified issues in the lead-to-CRM flow
"""

import streamlit as st
from typing import Dict, Any

def normalize_lead_data(lead: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize lead data to ensure consistent field mapping
    Handles multiple possible field names from different sources
    """
    normalized = {
        'id': lead.get('id') or lead.get('post_id') or f"lead_{int(time.time())}",
        'author': lead.get('author') or lead.get('username') or 'Unknown',
        'title': lead.get('title', ''),
        'content': lead.get('content') or lead.get('text') or lead.get('body', ''),
        'subreddit': lead.get('subreddit', ''),
        'url': lead.get('reddit_link') or lead.get('url') or lead.get('link', ''),
        'lead_score': lead.get('lead_score', 0),
        'priority_level': lead.get('priority_level', 'Unknown'),
        'created_utc': lead.get('created_utc', ''),
        'score': lead.get('score', 0)
    }
    
    # Ensure required fields are not empty
    if not normalized['id']:
        import time
        normalized['id'] = f"lead_{int(time.time())}"
    
    return normalized

def safe_crm_save(crm, lead_data: Dict[str, Any], notes: str = "") -> Dict[str, Any]:
    """
    Safely save lead to CRM with proper error handling
    """
    try:
        # Normalize the lead data first
        normalized_lead = normalize_lead_data(lead_data)
        
        # Attempt to save
        result = crm.save_lead_to_crm(
            post_data=normalized_lead,
            lead_score=normalized_lead['lead_score'],
            notes=notes
        )
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': f"CRM save failed: {str(e)}",
            'debug_data': lead_data
        }

def handle_crm_result(result: Dict[str, Any], lead_data: Dict[str, Any]):
    """
    Handle CRM save result with appropriate user feedback
    """
    if result.get('success'):
        st.success(f"✅ Saved to CRM: {result.get('message', 'Lead saved successfully')}")
        st.rerun()
    else:
        st.error(f"❌ Failed to save lead: {result.get('error', 'Unknown error')}")
        
        # Show debug information
        with st.expander("Debug Information"):
            st.write("Lead data:", lead_data)
            st.write("CRM result:", result)
            
            if 'debug_data' in result:
                st.write("Normalized data:", result['debug_data'])

def ensure_crm_initialization():
    """
    Ensure CRM system is properly initialized in session state
    """
    if 'crm' not in st.session_state:
        from crm_system import CRMSystem
        st.session_state.crm = CRMSystem()
    
    return st.session_state.crm

def check_lead_in_crm(crm, lead: Dict[str, Any]) -> bool:
    """
    Check if lead is already in CRM with multiple ID formats
    """
    excluded_ids = set(crm.get_exclusion_list())
    
    # Check multiple possible ID formats
    possible_ids = [
        lead.get('id'),
        lead.get('post_id'),
        f"lead_{lead.get('id', '')}"
    ]
    
    return any(pid in excluded_ids for pid in possible_ids if pid)