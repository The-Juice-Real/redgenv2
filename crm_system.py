"""
Clean CRM System - Research User Functionality Removed
Lightweight CRM with exclusion logic for lead management
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict


class CRMSystem:
    """Lightweight CRM with exclusion logic for lead management"""
    
    def __init__(self):
        self.crm_file = 'crm_data.json'
        self.crm_data = self.load_crm_data()
        
        # Ensure required keys exist
        if 'saved_leads' not in self.crm_data:
            self.crm_data['saved_leads'] = []
        if 'saved_post_ids' not in self.crm_data:
            self.crm_data['saved_post_ids'] = []
        if 'user_research' not in self.crm_data:
            self.crm_data['user_research'] = {}
        if 'created_at' not in self.crm_data:
            self.crm_data['created_at'] = datetime.now().isoformat()
        if 'last_updated' not in self.crm_data:
            self.crm_data['last_updated'] = datetime.now().isoformat()
    
    def load_crm_data(self) -> Dict[str, Any]:
        """Load CRM data from file"""
        default_data = {
            'saved_leads': [],
            'saved_post_ids': [],
            'user_research': {},
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            with open(self.crm_file, 'r') as f:
                data = json.load(f)
                
                # Handle migration from old format
                if 'leads' in data and 'saved_leads' not in data:
                    # Convert old format to new format
                    old_leads = data.get('leads', {})
                    data['saved_leads'] = []
                    data['saved_post_ids'] = []
                    
                    # Convert old lead format to new simplified format
                    for lead_id, lead_data in old_leads.items():
                        if isinstance(lead_data, dict):
                            simplified_lead = {
                                'id': lead_id,
                                'reddit_username': lead_data.get('contact', {}).get('reddit_username', ''),
                                'post_url': lead_data.get('source_details', {}).get('post_url', ''),
                                'title': lead_data.get('lead_details', {}).get('title', ''),
                                'content': lead_data.get('lead_details', {}).get('content', ''),
                                'lead_score': lead_data.get('lead_details', {}).get('lead_score', 0),
                                'status': lead_data.get('status', 'new'),
                                'user_notes': '',
                                'created_date': lead_data.get('created_date', datetime.now().isoformat()),
                                'last_updated': lead_data.get('last_updated', datetime.now().isoformat())
                            }
                            data['saved_leads'].append(simplified_lead)
                            data['saved_post_ids'].append(lead_id)
                    
                    # Remove old leads structure
                    del data['leads']
                    
                    # Save the migrated data immediately
                    with open(self.crm_file, 'w') as f:
                        json.dump(data, f, indent=2)
                
                # Ensure all required keys exist
                for key in default_data:
                    if key not in data:
                        data[key] = default_data[key]
                        
                return data
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return default_data
    
    def save_crm_data(self):
        """Save CRM data to file"""
        try:
            self.crm_data['last_updated'] = datetime.now().isoformat()
            with open(self.crm_file, 'w') as f:
                json.dump(self.crm_data, f, indent=2)
        except Exception as e:
            print(f"Error saving CRM data: {e}")
    
    def save_lead_to_crm(self, post_data: Dict[str, Any], lead_score: float = 0,
                        notes: str = "") -> Dict[str, Any]:
        """
        Save lead to CRM with lightweight storage
        Stores only: link, username, post description (text only)
        """
        
        # Create lightweight lead entry with multiple field mappings
        lead_entry = {
            'id': post_data.get('id', post_data.get('post_id', f"lead_{datetime.now().strftime('%Y%m%d_%H%M%S')}")),
            'reddit_username': post_data.get('author', post_data.get('username', '')),
            'post_url': post_data.get('reddit_link', post_data.get('url', post_data.get('link', ''))),
            'title': post_data.get('title', ''),
            'content': post_data.get('content', post_data.get('text', post_data.get('body', ''))),
            'subreddit': post_data.get('subreddit', ''),
            'lead_score': lead_score or post_data.get('lead_score', 0),
            'priority_level': post_data.get('priority_level', 'Unknown'),
            'status': 'new',
            'user_notes': notes,
            'created_date': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        # Add to CRM data
        self.crm_data['saved_leads'].append(lead_entry)
        
        # Add to exclusion list
        post_id = post_data.get('id', post_data.get('post_id'))
        if post_id and post_id not in self.crm_data['saved_post_ids']:
            self.crm_data['saved_post_ids'].append(post_id)
        
        try:
            self.save_crm_data()
            return {
                'success': True,
                'message': f"Lead saved - {post_data.get('author', post_data.get('username', 'Unknown user'))}",
                'lead_id': lead_entry['id']
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to save CRM data: {str(e)}",
                'lead_id': lead_entry['id']
            }
    
    def get_exclusion_list(self) -> List[str]:
        """Get list of post IDs to exclude from search results"""
        return self.crm_data.get('saved_post_ids', [])
    
    def get_all_leads(self) -> List[Dict[str, Any]]:
        """Get all saved leads from CRM"""
        return self.crm_data.get('saved_leads', [])
    
    def update_lead_status(self, lead_id: str, status: str, notes: str = "") -> bool:
        """Update lead status and notes"""
        
        for lead in self.crm_data['saved_leads']:
            if lead.get('id') == lead_id:
                lead['status'] = status
                lead['user_notes'] = notes
                lead['last_updated'] = datetime.now().isoformat()
                self.save_crm_data()
                return True
        
        return False
    
    def delete_lead(self, lead_id: str) -> bool:
        """Delete lead from CRM and remove from exclusion list"""
        
        # Remove from leads
        original_count = len(self.crm_data['saved_leads'])
        self.crm_data['saved_leads'] = [
            lead for lead in self.crm_data['saved_leads'] 
            if lead.get('id') != lead_id
        ]
        
        # Remove from exclusion list
        if lead_id in self.crm_data['saved_post_ids']:
            self.crm_data['saved_post_ids'].remove(lead_id)
        
        if len(self.crm_data['saved_leads']) < original_count:
            self.save_crm_data()
            return True
        
        return False
    
    def get_crm_stats(self) -> Dict[str, Any]:
        """Get CRM statistics and metrics"""
        
        leads = self.crm_data.get('saved_leads', [])
        
        status_counts = defaultdict(int)
        for lead in leads:
            status_counts[lead.get('status', 'unknown')] += 1
        
        return {
            'total_leads': len(leads),
            'status_breakdown': dict(status_counts),
            'exclusion_list_size': len(self.crm_data.get('saved_post_ids', [])),
            'last_updated': self.crm_data.get('last_updated', ''),
            'created_at': self.crm_data.get('created_at', '')
        }
    
    def search_leads(self, query: str = "", status: str = "", limit: int = 100) -> List[Dict[str, Any]]:
        """Search leads with optional filters"""
        
        leads = self.crm_data.get('saved_leads', [])
        
        # Apply status filter
        if status and status != "all":
            leads = [lead for lead in leads if lead.get('status', '').lower() == status.lower()]
        
        # Apply text search
        if query:
            query_lower = query.lower()
            filtered_leads = []
            for lead in leads:
                # Search in title, content, username, and notes
                searchable_text = f"{lead.get('title', '')} {lead.get('content', '')} {lead.get('reddit_username', '')} {lead.get('user_notes', '')}".lower()
                if query_lower in searchable_text:
                    filtered_leads.append(lead)
            leads = filtered_leads
        
        # Sort by last updated (most recent first)
        leads.sort(key=lambda x: x.get('last_updated', ''), reverse=True)
        
        return leads[:limit]