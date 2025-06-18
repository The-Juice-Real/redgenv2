import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import streamlit as st

class FollowUpTracker:
    """Track lead follow-ups and engagement over time"""
    
    def __init__(self, data_file: str = "lead_tracking.json"):
        self.data_file = data_file
        self.leads_db = self._load_tracking_data()
    
    def _load_tracking_data(self) -> Dict[str, Any]:
        """Load existing tracking data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        return {
            'leads': {},
            'campaigns': {},
            'last_updated': None
        }
    
    def _save_tracking_data(self):
        """Save tracking data to file"""
        self.leads_db['last_updated'] = datetime.now().isoformat()
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.leads_db, f, indent=2, default=str)
        except IOError:
            st.warning("Could not save tracking data to file")
    
    def add_or_update_lead(self, lead_data: Dict[str, Any], campaign_name: str = "default") -> str:
        """Add new lead or update existing lead in tracking system"""
        
        # Generate unique lead ID
        lead_id = self._generate_lead_id(lead_data)
        
        # Check if lead already exists
        if lead_id in self.leads_db['leads']:
            return self._update_existing_lead(lead_id, lead_data, campaign_name)
        else:
            return self._add_new_lead(lead_id, lead_data, campaign_name)
    
    def _generate_lead_id(self, lead_data: Dict[str, Any]) -> str:
        """Generate unique ID for lead based on username and content hash"""
        username = lead_data.get('author', 'unknown')
        content_hash = str(hash(str(lead_data.get('title', '') + lead_data.get('content', ''))))[:8]
        return f"{username}_{content_hash}"
    
    def _add_new_lead(self, lead_id: str, lead_data: Dict[str, Any], campaign_name: str) -> str:
        """Add new lead to tracking system"""
        
        current_time = datetime.now().isoformat()
        
        self.leads_db['leads'][lead_id] = {
            'first_seen': current_time,
            'last_updated': current_time,
            'lead_score': lead_data.get('lead_score', 0),
            'lead_quality': lead_data.get('lead_quality', 'Unknown'),
            'author': lead_data.get('author', 'unknown'),
            'title': lead_data.get('title', ''),
            'subreddit': lead_data.get('subreddit', ''),
            'permalink': lead_data.get('permalink', ''),
            'campaign': campaign_name,
            'status': 'new',
            'follow_ups': [],
            'engagement_history': [],
            'contact_attempts': 0,
            'last_contact_date': None,
            'conversion_stage': 'awareness',
            'notes': [],
            'buying_intent_level': lead_data.get('buying_intent', {}).get('level', 'Unknown'),
            'business_size': lead_data.get('business_context', {}).get('business_size', 'Unknown'),
            'budget_level': lead_data.get('budget_analysis', {}).get('budget_level', 'unknown'),
            'competitive_pressure': lead_data.get('competitive_intel', {}).get('competitive_pressure', 'low'),
            'urgency_score': lead_data.get('timeline_analysis', {}).get('urgency_score', 0),
            'contact_info': lead_data.get('contact_hints', {}),
            'tags': self._generate_lead_tags(lead_data)
        }
        
        self._save_tracking_data()
        return f"Added new lead: {lead_id}"
    
    def _update_existing_lead(self, lead_id: str, lead_data: Dict[str, Any], campaign_name: str) -> str:
        """Update existing lead with new information"""
        
        existing_lead = self.leads_db['leads'][lead_id]
        current_time = datetime.now().isoformat()
        
        # Update core metrics
        existing_lead['last_updated'] = current_time
        existing_lead['lead_score'] = max(existing_lead['lead_score'], lead_data.get('lead_score', 0))
        existing_lead['lead_quality'] = lead_data.get('lead_quality', existing_lead['lead_quality'])
        
        # Track engagement history
        engagement_event = {
            'timestamp': current_time,
            'activity': 'reddit_post',
            'campaign': campaign_name,
            'score_change': lead_data.get('lead_score', 0) - existing_lead['lead_score'],
            'content_snippet': lead_data.get('title', '')[:100]
        }
        existing_lead['engagement_history'].append(engagement_event)
        
        # Update intent and urgency if higher
        new_urgency = lead_data.get('timeline_analysis', {}).get('urgency_score', 0)
        if new_urgency > existing_lead['urgency_score']:
            existing_lead['urgency_score'] = new_urgency
        
        # Merge contact information
        new_contact_info = lead_data.get('contact_hints', {})
        if new_contact_info.get('has_contact_info'):
            existing_lead['contact_info'].update(new_contact_info)
        
        # Update tags
        new_tags = self._generate_lead_tags(lead_data)
        existing_lead['tags'] = list(set(existing_lead['tags'] + new_tags))
        
        self._save_tracking_data()
        return f"Updated existing lead: {lead_id}"
    
    def _generate_lead_tags(self, lead_data: Dict[str, Any]) -> List[str]:
        """Generate tags for lead categorization"""
        tags = []
        
        # Quality tags
        quality = lead_data.get('lead_quality', '')
        if quality:
            tags.append(quality.lower().replace(' ', '_'))
        
        # Intent tags
        intent = lead_data.get('buying_intent', {}).get('level', '')
        if intent and intent != 'None':
            tags.append(f"intent_{intent.lower()}")
        
        # Business size tags
        business_size = lead_data.get('business_context', {}).get('business_size', '')
        if business_size and business_size != 'Unknown':
            tags.append(f"size_{business_size.lower()}")
        
        # Industry tags
        industry = lead_data.get('enhanced_industry', {}).get('primary_industry', '')
        if industry and industry != 'unknown':
            tags.append(f"industry_{industry}")
        
        # Budget tags
        budget = lead_data.get('budget_analysis', {}).get('budget_level', '')
        if budget and budget != 'unknown':
            tags.append(f"budget_{budget}")
        
        # Urgency tags
        urgency_score = lead_data.get('timeline_analysis', {}).get('urgency_score', 0)
        if urgency_score >= 0.8:
            tags.append('urgent')
        elif urgency_score >= 0.5:
            tags.append('medium_urgency')
        
        # Competitive tags
        competitive_pressure = lead_data.get('competitive_intel', {}).get('competitive_pressure', '')
        if competitive_pressure == 'high':
            tags.append('competitor_dissatisfied')
        
        return tags
    
    def add_follow_up(self, lead_id: str, follow_up_type: str, notes: str, next_action: str, 
                     next_action_date: Optional[str] = None) -> bool:
        """Add follow-up action to lead"""
        
        if lead_id not in self.leads_db['leads']:
            return False
        
        follow_up = {
            'timestamp': datetime.now().isoformat(),
            'type': follow_up_type,  # email, linkedin, call, meeting
            'notes': notes,
            'next_action': next_action,
            'next_action_date': next_action_date,
            'completed': False
        }
        
        self.leads_db['leads'][lead_id]['follow_ups'].append(follow_up)
        self.leads_db['leads'][lead_id]['last_contact_date'] = datetime.now().isoformat()
        self.leads_db['leads'][lead_id]['contact_attempts'] += 1
        
        self._save_tracking_data()
        return True
    
    def update_lead_status(self, lead_id: str, new_status: str, conversion_stage: str = None) -> bool:
        """Update lead status and conversion stage"""
        
        if lead_id not in self.leads_db['leads']:
            return False
        
        self.leads_db['leads'][lead_id]['status'] = new_status
        if conversion_stage:
            self.leads_db['leads'][lead_id]['conversion_stage'] = conversion_stage
        
        self._save_tracking_data()
        return True
    
    def get_leads_due_for_follow_up(self, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Get leads that need follow-up within specified days"""
        
        due_leads = []
        target_date = (datetime.now() + timedelta(days=days_ahead)).isoformat()
        
        for lead_id, lead_data in self.leads_db['leads'].items():
            # Check for pending follow-ups
            for follow_up in lead_data.get('follow_ups', []):
                if (not follow_up.get('completed') and 
                    follow_up.get('next_action_date') and 
                    follow_up['next_action_date'] <= target_date):
                    
                    due_leads.append({
                        'lead_id': lead_id,
                        'lead_data': lead_data,
                        'follow_up': follow_up
                    })
        
        return due_leads
    
    def get_lead_analytics(self) -> Dict[str, Any]:
        """Generate analytics for lead tracking"""
        
        total_leads = len(self.leads_db['leads'])
        if total_leads == 0:
            return {'total_leads': 0}
        
        # Status distribution
        status_counts = {}
        quality_counts = {}
        conversion_stage_counts = {}
        tag_counts = {}
        
        total_score = 0
        contact_attempts_total = 0
        leads_with_contact_info = 0
        
        for lead_data in self.leads_db['leads'].values():
            # Status
            status = lead_data.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # Quality
            quality = lead_data.get('lead_quality', 'Unknown')
            quality_counts[quality] = quality_counts.get(quality, 0) + 1
            
            # Conversion stage
            stage = lead_data.get('conversion_stage', 'unknown')
            conversion_stage_counts[stage] = conversion_stage_counts.get(stage, 0) + 1
            
            # Tags
            for tag in lead_data.get('tags', []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            # Metrics
            total_score += lead_data.get('lead_score', 0)
            contact_attempts_total += lead_data.get('contact_attempts', 0)
            
            if lead_data.get('contact_info', {}).get('has_contact_info'):
                leads_with_contact_info += 1
        
        return {
            'total_leads': total_leads,
            'average_score': total_score / total_leads,
            'status_distribution': status_counts,
            'quality_distribution': quality_counts,
            'conversion_stage_distribution': conversion_stage_counts,
            'top_tags': sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            'contact_coverage': (leads_with_contact_info / total_leads) * 100,
            'average_contact_attempts': contact_attempts_total / total_leads,
            'leads_due_follow_up': len(self.get_leads_due_for_follow_up()),
            'last_updated': self.leads_db.get('last_updated')
        }
    
    def search_leads(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search leads based on filters"""
        
        matching_leads = []
        
        for lead_id, lead_data in self.leads_db['leads'].items():
            match = True
            
            # Apply filters
            if 'status' in filters and lead_data.get('status') != filters['status']:
                match = False
            
            if 'quality' in filters and lead_data.get('lead_quality') != filters['quality']:
                match = False
            
            if 'min_score' in filters and lead_data.get('lead_score', 0) < filters['min_score']:
                match = False
            
            if 'tags' in filters:
                lead_tags = set(lead_data.get('tags', []))
                required_tags = set(filters['tags'])
                if not required_tags.issubset(lead_tags):
                    match = False
            
            if 'business_size' in filters and lead_data.get('business_size') != filters['business_size']:
                match = False
            
            if match:
                matching_leads.append({
                    'lead_id': lead_id,
                    'lead_data': lead_data
                })
        
        return matching_leads
    
    def export_leads_for_crm(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Export leads in CRM-friendly format"""
        
        crm_leads = []
        
        for lead_id, lead_data in self.leads_db['leads'].items():
            if status_filter and lead_data.get('status') != status_filter:
                continue
            
            contact_info = lead_data.get('contact_info', {})
            
            crm_lead = {
                'Lead ID': lead_id,
                'Name': lead_data.get('author', 'Unknown'),
                'Company': ', '.join(contact_info.get('companies_mentioned', [])),
                'Email': ', '.join(contact_info.get('emails_found', [])),
                'LinkedIn': ', '.join(contact_info.get('linkedin_profiles', [])),
                'Phone': ', '.join(contact_info.get('phones_found', [])),
                'Lead Score': lead_data.get('lead_score', 0),
                'Quality': lead_data.get('lead_quality', 'Unknown'),
                'Status': lead_data.get('status', 'new'),
                'Business Size': lead_data.get('business_size', 'Unknown'),
                'Budget Level': lead_data.get('budget_level', 'unknown'),
                'Buying Intent': lead_data.get('buying_intent_level', 'Unknown'),
                'Urgency Score': lead_data.get('urgency_score', 0),
                'Competitive Pressure': lead_data.get('competitive_pressure', 'low'),
                'Source URL': f"https://reddit.com{lead_data.get('permalink', '')}",
                'First Seen': lead_data.get('first_seen', ''),
                'Last Contact': lead_data.get('last_contact_date', ''),
                'Contact Attempts': lead_data.get('contact_attempts', 0),
                'Tags': ', '.join(lead_data.get('tags', [])),
                'Notes': '; '.join([note.get('content', '') for note in lead_data.get('notes', [])])
            }
            
            crm_leads.append(crm_lead)
        
        return crm_leads