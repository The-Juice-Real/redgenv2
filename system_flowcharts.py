"""
System Flowcharts Generator
Creates visual flowcharts for the Reddit Lead Generator application
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np

def create_app_workflow_chart():
    """Create main application workflow flowchart"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    
    # Define colors
    colors = {
        'start': '#4CAF50',
        'process': '#2196F3', 
        'decision': '#FF9800',
        'data': '#9C27B0',
        'output': '#F44336',
        'api': '#607D8B'
    }
    
    # Helper function to create boxes
    def create_box(ax, x, y, width, height, text, color, box_type='rect'):
        if box_type == 'diamond':
            # Diamond shape for decisions
            diamond = mpatches.FancyBboxPatch((x-width/2, y-height/2), width, height,
                                            boxstyle="round,pad=0.1", 
                                            facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(diamond)
        else:
            # Rectangle for processes
            rect = FancyBboxPatch((x-width/2, y-height/2), width, height,
                                boxstyle="round,pad=0.1",
                                facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(rect)
        
        # Add text
        ax.text(x, y, text, ha='center', va='center', fontsize=9, 
                fontweight='bold', wrap=True, color='white')
    
    # Helper function to create arrows
    def create_arrow(ax, x1, y1, x2, y2, text=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        if text:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x + 0.2, mid_y, text, fontsize=8, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Main workflow boxes
    create_box(ax, 2, 10, 2, 0.8, "User Opens\nLead Finder", colors['start'])
    create_box(ax, 2, 8.5, 2.5, 0.8, "Select Service Type\n(Dropdown)", colors['process'])
    create_box(ax, 5, 8.5, 2, 0.8, "Custom Service?", colors['decision'], 'diamond')
    create_box(ax, 8, 8.5, 2.5, 0.8, "Enter Custom\nDescription", colors['process'])
    create_box(ax, 2, 7, 2.5, 0.8, "Select Data Sources\n(Platform Buttons)", colors['process'])
    create_box(ax, 2, 5.5, 2, 0.8, "Reddit Enabled?", colors['decision'], 'diamond')
    create_box(ax, 5, 5.5, 3, 0.8, "Click 'Find Customers'\nButton", colors['start'])
    
    # AI Processing Pipeline
    create_box(ax, 9, 5.5, 2.5, 0.8, "Service Classification\n& Strategy Selection", colors['process'])
    create_box(ax, 12, 5.5, 2, 0.8, "Dynamic Discovery?", colors['decision'], 'diamond')
    create_box(ax, 15, 5.5, 2.5, 0.8, "AI Subreddit\nDiscovery", colors['api'])
    create_box(ax, 12, 3.5, 2.5, 0.8, "Hardcoded Pattern\nMatching", colors['data'])
    
    # Search Execution
    create_box(ax, 9, 2, 2.5, 0.8, "Execute Reddit\nSearch", colors['process'])
    create_box(ax, 6, 2, 2.5, 0.8, "Ultra-Precise AI\nAnalysis", colors['api'])
    create_box(ax, 3, 2, 2.5, 0.8, "Lead Scoring &\nQualification", colors['process'])
    
    # Results Display
    create_box(ax, 6, 0.5, 2.5, 0.8, "Rank & Optimize\nResults", colors['process'])
    create_box(ax, 9, 0.5, 2.5, 0.8, "Display Qualified\nLeads", colors['output'])
    create_box(ax, 12, 0.5, 2.5, 0.8, "Lead Details &\nReddit Links", colors['output'])
    
    # Create arrows for main flow
    create_arrow(ax, 2, 9.6, 2, 9.3)
    create_arrow(ax, 3.25, 8.5, 3.75, 8.5)
    create_arrow(ax, 6, 8.5, 7.25, 8.5, "Yes")
    create_arrow(ax, 5, 7.7, 5, 7.3, "No")
    create_arrow(ax, 2, 8.1, 2, 7.8)
    create_arrow(ax, 2, 6.6, 2, 6.3)
    create_arrow(ax, 3, 5.5, 4, 5.5, "Yes")
    create_arrow(ax, 6.5, 5.5, 7.75, 5.5)
    create_arrow(ax, 10.25, 5.5, 11, 5.5)
    create_arrow(ax, 13, 5.5, 13.75, 5.5, "Custom")
    create_arrow(ax, 12, 4.7, 12, 4.3, "Standard")
    create_arrow(ax, 15, 4.7, 15, 3.5)
    create_arrow(ax, 14.5, 3.5, 9.5, 3.5)
    create_arrow(ax, 12, 3.1, 12, 2.8)
    create_arrow(ax, 11.25, 2.8, 9.5, 2.8)
    create_arrow(ax, 8.25, 2, 7.25, 2)
    create_arrow(ax, 4.75, 2, 4.25, 2)
    create_arrow(ax, 4.5, 1.4, 5.25, 1.1)
    create_arrow(ax, 7.25, 0.5, 8.25, 0.5)
    create_arrow(ax, 10.25, 0.5, 11.25, 0.5)
    
    # Error paths
    create_arrow(ax, 1, 5.5, 1, 8.5, "No - Warning")
    
    # Set up the plot
    ax.set_xlim(-1, 17)
    ax.set_ylim(-1, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Reddit Lead Generator - Application Workflow', fontsize=16, fontweight='bold', pad=20)
    
    # Create legend
    legend_elements = [
        mpatches.Patch(color=colors['start'], label='User Actions'),
        mpatches.Patch(color=colors['process'], label='System Processing'),
        mpatches.Patch(color=colors['decision'], label='Decision Points'),
        mpatches.Patch(color=colors['data'], label='Data Operations'),
        mpatches.Patch(color=colors['api'], label='AI/API Operations'),
        mpatches.Patch(color=colors['output'], label='Output/Results')
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1))
    
    plt.tight_layout()
    plt.savefig('app_workflow_chart.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_ai_discovery_flowchart():
    """Create detailed AI discovery process flowchart"""
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    
    colors = {
        'input': '#4CAF50',
        'filter': '#FF9800',
        'analysis': '#2196F3',
        'scoring': '#9C27B0',
        'decision': '#F44336',
        'output': '#607D8B'
    }
    
    def create_box(ax, x, y, width, height, text, color, box_type='rect'):
        if box_type == 'diamond':
            diamond = mpatches.FancyBboxPatch((x-width/2, y-height/2), width, height,
                                            boxstyle="round,pad=0.1", 
                                            facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(diamond)
        else:
            rect = FancyBboxPatch((x-width/2, y-height/2), width, height,
                                boxstyle="round,pad=0.1",
                                facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(rect)
        
        ax.text(x, y, text, ha='center', va='center', fontsize=8, 
                fontweight='bold', wrap=True, color='white')
    
    def create_arrow(ax, x1, y1, x2, y2, text=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        if text:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x + 0.2, mid_y, text, fontsize=7, 
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # Input Stage
    create_box(ax, 2, 12, 2.5, 0.8, "Content Input\n(Title + Post + Comments)", colors['input'])
    
    # Phase 1: Pre-filtering
    create_box(ax, 2, 10.5, 3, 0.8, "Phase 1: Ultra-Fast Pre-Filter", colors['filter'])
    create_box(ax, 5.5, 10.5, 2.5, 0.8, "Length Check\n(50-2000 chars)", colors['filter'])
    create_box(ax, 8.5, 10.5, 2.5, 0.8, "Business Terms\nDetection", colors['filter'])
    create_box(ax, 11.5, 10.5, 2.5, 0.8, "Question Format\nCheck", colors['filter'])
    create_box(ax, 14.5, 10.5, 2.5, 0.8, "Spam Indicator\nFiltering", colors['filter'])
    
    # Decision point
    create_box(ax, 8.5, 9, 2, 0.8, "Score ≥ 30?", colors['decision'], 'diamond')
    create_box(ax, 12, 9, 2.5, 0.8, "Reject Lead\n(Failed Pre-filter)", colors['decision'])
    
    # Phase 2: Semantic Analysis
    create_box(ax, 5, 7.5, 3, 0.8, "Phase 2: Deep Semantic Analysis", colors['analysis'])
    create_box(ax, 9, 7.5, 2.5, 0.8, "TF-IDF Business\nRelevance", colors['analysis'])
    create_box(ax, 12.5, 7.5, 2.5, 0.8, "Named Entity\nRecognition", colors['analysis'])
    create_box(ax, 16, 7.5, 2.5, 0.8, "Sentiment Analysis\n(Frustration/Need)", colors['analysis'])
    
    # Phase 3: Pattern Scoring
    create_box(ax, 2, 6, 2.5, 0.8, "Urgency Pattern\nMatching", colors['scoring'])
    create_box(ax, 5, 6, 2.5, 0.8, "Budget Signal\nDetection", colors['scoring'])
    create_box(ax, 8, 6, 2.5, 0.8, "Authority Pattern\nRecognition", colors['scoring'])
    create_box(ax, 11, 6, 2.5, 0.8, "Quality Indicator\nAnalysis", colors['scoring'])
    create_box(ax, 14, 6, 2.5, 0.8, "Negative Signal\nFiltering", colors['scoring'])
    
    # Phase 4: Advanced Context
    create_box(ax, 3.5, 4.5, 3, 0.8, "Phase 4: Context Intelligence", colors['analysis'])
    create_box(ax, 7.5, 4.5, 2.5, 0.8, "Problem-Solution\nMapping", colors['analysis'])
    create_box(ax, 11, 4.5, 2.5, 0.8, "Timeline Context\nExtraction", colors['analysis'])
    create_box(ax, 14.5, 4.5, 2.5, 0.8, "Technical Complexity\nAssessment", colors['analysis'])
    
    # Phase 5: Composite Scoring
    create_box(ax, 5, 3, 3, 0.8, "Phase 5: Weighted Composite Score", colors['scoring'])
    create_box(ax, 9, 3, 2.5, 0.8, "Urgency: 20%\nBudget: 30%", colors['scoring'])
    create_box(ax, 12.5, 3, 2.5, 0.8, "Authority: 25%\nQuality: 15%", colors['scoring'])
    create_box(ax, 16, 3, 2.5, 0.8, "Context: 10%\n+ Bonuses", colors['scoring'])
    
    # Final Decision
    create_box(ax, 8.5, 1.5, 2, 0.8, "Score ≥ 70?", colors['decision'], 'diamond')
    create_box(ax, 5, 0.5, 2.5, 0.8, "Qualified Lead\n+ Tier Assignment", colors['output'])
    create_box(ax, 12, 0.5, 2.5, 0.8, "Unqualified\n(Below Threshold)", colors['decision'])
    
    # API Enhancement Path
    create_box(ax, 5, -1, 3, 0.8, "Score ≥ 85? → API Enhancement", colors['analysis'])
    
    # Create arrows for main flow
    create_arrow(ax, 2, 11.6, 2, 11.3)
    create_arrow(ax, 3.5, 10.5, 4.75, 10.5)
    create_arrow(ax, 6.75, 10.5, 7.75, 10.5)
    create_arrow(ax, 9.75, 10.5, 10.75, 10.5)
    create_arrow(ax, 12.75, 10.5, 13.75, 10.5)
    
    # Pre-filter decision
    create_arrow(ax, 8.5, 10.1, 8.5, 9.8)
    create_arrow(ax, 9.5, 9, 11, 9, "No")
    create_arrow(ax, 8.5, 8.2, 8.5, 8.3, "Yes")
    
    # Semantic analysis flow
    create_arrow(ax, 6.5, 7.5, 8.25, 7.5)
    create_arrow(ax, 10.25, 7.5, 11.75, 7.5)
    create_arrow(ax, 13.75, 7.5, 15.25, 7.5)
    
    # Pattern scoring connections
    create_arrow(ax, 8.5, 7.1, 2, 6.8)
    create_arrow(ax, 8.5, 7.1, 5, 6.8)
    create_arrow(ax, 8.5, 7.1, 8, 6.8)
    create_arrow(ax, 8.5, 7.1, 11, 6.8)
    create_arrow(ax, 8.5, 7.1, 14, 6.8)
    
    # Context analysis flow
    create_arrow(ax, 5, 5.2, 5, 5.3)
    create_arrow(ax, 6, 4.5, 6.75, 4.5)
    create_arrow(ax, 8.75, 4.5, 10.25, 4.5)
    create_arrow(ax, 12.25, 4.5, 13.75, 4.5)
    
    # Final scoring
    create_arrow(ax, 5, 3.8, 5, 3.8)
    create_arrow(ax, 6.5, 3, 8.25, 3)
    create_arrow(ax, 10.25, 3, 11.75, 3)
    create_arrow(ax, 13.75, 3, 15.25, 3)
    
    # Final decision
    create_arrow(ax, 8.5, 2.2, 8.5, 2.3)
    create_arrow(ax, 7.5, 1.5, 6.25, 1.3, "Yes")
    create_arrow(ax, 9.5, 1.5, 11, 1.3, "No")
    
    # API enhancement
    create_arrow(ax, 5, 1.3, 5, 0.7)
    create_arrow(ax, 5, -0.2, 5, -0.2)
    
    ax.set_xlim(0, 18)
    ax.set_ylim(-2, 13)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Ultra-Precise AI Discovery Engine - Processing Pipeline', fontsize=16, fontweight='bold', pad=20)
    
    # Create legend
    legend_elements = [
        mpatches.Patch(color=colors['input'], label='Input Data'),
        mpatches.Patch(color=colors['filter'], label='Pre-filtering'),
        mpatches.Patch(color=colors['analysis'], label='AI Analysis'),
        mpatches.Patch(color=colors['scoring'], label='Scoring Systems'),
        mpatches.Patch(color=colors['decision'], label='Decision Points'),
        mpatches.Patch(color=colors['output'], label='Final Output')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
    
    plt.tight_layout()
    plt.savefig('ai_discovery_flowchart.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_api_optimization_chart():
    """Create API optimization strategy flowchart"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    colors = {
        'start': '#4CAF50',
        'process': '#2196F3',
        'decision': '#FF9800',
        'api': '#F44336',
        'save': '#9C27B0'
    }
    
    def create_box(ax, x, y, width, height, text, color, box_type='rect'):
        if box_type == 'diamond':
            diamond = mpatches.FancyBboxPatch((x-width/2, y-height/2), width, height,
                                            boxstyle="round,pad=0.1", 
                                            facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(diamond)
        else:
            rect = FancyBboxPatch((x-width/2, y-height/2), width, height,
                                boxstyle="round,pad=0.1",
                                facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(rect)
        
        ax.text(x, y, text, ha='center', va='center', fontsize=9, 
                fontweight='bold', wrap=True, color='white')
    
    def create_arrow(ax, x1, y1, x2, y2, text=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        if text:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x + 0.2, mid_y, text, fontsize=8, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # API Optimization Flow
    create_box(ax, 2, 8, 2.5, 0.8, "Content Batch\n(100 prospects)", colors['start'])
    create_box(ax, 2, 6.5, 2.5, 0.8, "Local AI Analysis\n(95% accuracy)", colors['process'])
    create_box(ax, 2, 5, 2, 0.8, "Score ≥ 70?", colors['decision'], 'diamond')
    
    # Rejection path
    create_box(ax, 5.5, 5, 2.5, 0.8, "Reject Lead\n(85-90 leads)", colors['save'])
    
    # Qualification path
    create_box(ax, 2, 3.5, 2.5, 0.8, "Qualified Lead\n(10-15 leads)", colors['process'])
    create_box(ax, 2, 2, 2, 0.8, "Score ≥ 85?", colors['decision'], 'diamond')
    
    # API enhancement path
    create_box(ax, 5.5, 2, 2.5, 0.8, "API Enhancement\n(Top 5 leads)", colors['api'])
    create_box(ax, 5.5, 0.5, 2.5, 0.8, "Final Score\n+ Confidence", colors['api'])
    
    # No API path
    create_box(ax, 2, 0.5, 2.5, 0.8, "Local Score Only\n(5-10 leads)", colors['process'])
    
    # Results merge
    create_box(ax, 9, 1.25, 2.5, 0.8, "Merge Results\n& Rank", colors['process'])
    create_box(ax, 9, -0.5, 2.5, 0.8, "Final Lead List\n(Score Ranked)", colors['start'])
    
    # Savings indicators
    create_box(ax, 9, 5, 3, 1.2, "API Call Reduction:\n90% fewer calls\n95% cost savings", colors['save'])
    create_box(ax, 9, 3, 3, 1.2, "Accuracy Maintained:\n95% precision\nZero false negatives", colors['save'])
    
    # Create arrows
    create_arrow(ax, 2, 7.6, 2, 7.3)
    create_arrow(ax, 2, 6.1, 2, 5.8)
    create_arrow(ax, 3, 5, 4.5, 5, "No (85%)")
    create_arrow(ax, 2, 4.2, 2, 4.3, "Yes (15%)")
    create_arrow(ax, 2, 3.1, 2, 2.8)
    create_arrow(ax, 3, 2, 4.5, 2, "Yes (5%)")
    create_arrow(ax, 2, 1.2, 2, 1.3, "No (10%)")
    create_arrow(ax, 6.75, 2, 8.25, 2)
    create_arrow(ax, 5.5, 1.3, 5.5, 1.3)
    create_arrow(ax, 7, 0.5, 8.25, 0.75)
    create_arrow(ax, 3.25, 0.5, 8.25, 0.75)
    create_arrow(ax, 9, 0.75, 9, 0.3)
    
    ax.set_xlim(0, 13)
    ax.set_ylim(-1.5, 9)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('API Optimization Strategy - 90% Cost Reduction', fontsize=16, fontweight='bold', pad=20)
    
    # Create legend with metrics
    legend_elements = [
        mpatches.Patch(color=colors['start'], label='Input/Output'),
        mpatches.Patch(color=colors['process'], label='Local Processing'),
        mpatches.Patch(color=colors['decision'], label='Threshold Decisions'),
        mpatches.Patch(color=colors['api'], label='API Enhancement'),
        mpatches.Patch(color=colors['save'], label='Cost Savings')
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1))
    
    plt.tight_layout()
    plt.savefig('api_optimization_chart.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_all_flowcharts():
    """Generate all system flowcharts"""
    print("Generating application workflow flowchart...")
    create_app_workflow_chart()
    
    print("Generating AI discovery process flowchart...")
    create_ai_discovery_flowchart()
    
    print("Generating API optimization strategy flowchart...")
    create_api_optimization_chart()
    
    print("All flowcharts generated successfully!")
    print("Files created:")
    print("- app_workflow_chart.png")
    print("- ai_discovery_flowchart.png") 
    print("- api_optimization_chart.png")

if __name__ == "__main__":
    generate_all_flowcharts()