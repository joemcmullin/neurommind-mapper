import requests
from bs4 import BeautifulSoup
import anthropic
import os
from typing import Optional

def scrape_text(url: str) -> str:
    """
    Scrape text content from a webpage
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        str: Extracted text content or error message
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text and clean it up
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        else:
            return f"Failed to scrape website. Status code: {response.status_code}"
            
    except Exception as e:
        return f"Error scraping website: {str(e)}"

def summarize_with_claude(text: str, api_key: str) -> str:
    """
    Generate a summary using Claude
    
    Args:
        text (str): Text to summarize
        api_key (str): Anthropic API key
        
    Returns:
        str: Summary of the text
    """
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""Please provide a comprehensive summary of the following text. 
    Focus on the main ideas, key concepts, and important details that would help someone 
    understand the content quickly. Make it suitable for neurodiverse learners by using 
    clear, structured language:

    {text[:4000]}  # Limit text to avoid token limits
    """
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def generate_mindmap_with_claude(text: str, api_key: str) -> str:
    """
    Generate Mermaid.js mindmap code using Claude
    
    Args:
        text (str): Text to convert to mindmap
        api_key (str): Anthropic API key
        
    Returns:
        str: Mermaid.js mindmap code
    """
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""Create a Mermaid.js mindmap with PERFECT syntax for neurodiverse learners.

CRITICAL RULES:
1. NO markdown code blocks - do NOT include ```
2. Start with exactly: mindmap
3. Second line must be: root(Topic Name)
4. Use exactly 2 spaces for main branches, 6 spaces for sub-items
5. All labels in parentheses: (Label Name)
6. Icons use ::icon(fa fa-name) and go UNDER branch names
7. Maximum 4 main branches with 2-4 sub-items each

EXACT FORMAT:
mindmap
  root(Main Topic)
    (Branch 1)
      ::icon(fa fa-lightbulb)
      (Sub Item A)
      (Sub Item B)
    (Branch 2)
      ::icon(fa fa-cogs)
      (Sub Item C)
      (Sub Item D)

FORBIDDEN:
- No ``` or markdown
- No extra indentation
- No special characters in labels
- No more than 4 main branches

Text to convert: {text[:2000]}

Return ONLY the mindmap code without any markdown formatting."""
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Error generating mindmap: {str(e)}"

def generate_flowchart_with_claude(text: str, api_key: str) -> str:
    """
    Generate Mermaid.js flowchart code using Claude
    
    Args:
        text (str): Text to convert to flowchart
        api_key (str): Anthropic API key
        
    Returns:
        str: Mermaid.js flowchart code
    """
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""Create a Mermaid.js flowchart for neurodiverse learners.

CRITICAL RULES:
1. Start with: flowchart TD
2. Use simple node IDs: A, B, C, etc.
3. Node labels in brackets: A[Start Here]
4. Arrows: A --> B
5. Decisions: C{{Question?}}
6. Decision paths: C -->|Yes| D
7. Maximum 8-10 nodes total
8. Clear, simple language

EXACT FORMAT:
flowchart TD
    A[Starting Point] --> B[Next Step]
    B --> C{{Decision Point?}}
    C -->|Yes| D[Path A]
    C -->|No| E[Path B]
    D --> F[Final Result]
    E --> F

Text to convert: {text[:2000]}

Return ONLY the flowchart code without markdown formatting."""
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Error generating flowchart: {str(e)}"

def generate_timeline_with_claude(text: str, api_key: str) -> str:
    """
    Generate Mermaid.js timeline code using Claude
    
    Args:
        text (str): Text to convert to timeline
        api_key (str): Anthropic API key
        
    Returns:
        str: Mermaid.js timeline code
    """
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""Create a Mermaid.js timeline for neurodiverse learners.

CRITICAL RULES:
1. Start with: timeline
2. Add title: title Timeline Name
3. Use sections if multiple periods
4. Format: Period : Event description
5. Keep events brief and clear
6. Maximum 6-8 events total
7. Chronological order

EXACT FORMAT:
timeline
    title Article Timeline
    section Early Period
        Event 1 : Brief description
        Event 2 : Another event
    section Later Period
        Event 3 : More recent event
        Event 4 : Latest development

Text to convert: {text[:2000]}

Return ONLY the timeline code without markdown formatting."""
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Error generating timeline: {str(e)}"

def generate_network_with_claude(text: str, api_key: str) -> str:
    """
    Generate Mermaid.js network/graph code using Claude
    
    Args:
        text (str): Text to convert to network
        api_key (str): Anthropic API key
        
    Returns:
        str: Mermaid.js graph code
    """
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""Create a Mermaid.js concept network for neurodiverse learners.

CRITICAL RULES:
1. Start with: graph TD
2. Use simple node IDs: A, B, C, etc.
3. Node labels in brackets: A[Concept Name]
4. Connections: A --- B or A --> B
5. Show relationships between concepts
6. Maximum 8 nodes total
7. Add styling for key nodes

EXACT FORMAT:
graph TD
    A[Main Concept] --- B[Related Idea]
    A --- C[Another Concept]
    B --- D[Supporting Point]
    C --- E[Detail]
    style A fill:#e1f5fe
    style B fill:#f3e5f5

Text to convert: {text[:2000]}

Return ONLY the graph code without markdown formatting."""
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Error generating network: {str(e)}"

def validate_and_fix_mermaid(mermaid_code: str) -> str:
    """
    Validate and fix common Mermaid.js syntax issues
    
    Args:
        mermaid_code (str): Raw Mermaid.js code from AI
        
    Returns:
        str: Cleaned and validated Mermaid.js code
    """
    # Remove markdown code block markers
    mermaid_code = mermaid_code.replace('```mermaid', '').replace('```', '').strip()
    
    lines = mermaid_code.strip().split('\n')
    fixed_lines = ['mindmap']
    root_found = False
    current_branch = None
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and mindmap declaration
        if not line or line == 'mindmap':
            continue
            
        # Remove problematic characters
        if line == '(```)' or '```' in line:
            continue
            
        # Handle root element
        if not root_found and line.startswith('(') and line.endswith(')'):
            # First meaningful line becomes root
            topic = line.strip('()')
            fixed_lines.append(f'  root({topic})')
            root_found = True
            continue
            
        # Handle icons
        if line.startswith('::icon('):
            if current_branch:
                fixed_lines.append(f'      {line}')
            continue
            
        # Handle regular nodes
        if line.startswith('(') and line.endswith(')'):
            content = line.strip('()')
            
            # Determine if this should be a main branch or sub-item
            # Main branches are typically broader topics
            main_branch_keywords = ['marketing', 'strategy', 'content', 'advertising', 'automation', 'analytics', 'creation', 'search', 'social']
            
            is_main_branch = any(keyword in content.lower() for keyword in main_branch_keywords)
            
            if is_main_branch and len([l for l in fixed_lines if l.startswith('    (')]) < 4:
                # This is a main branch
                fixed_lines.append(f'    ({content})')
                current_branch = content
            else:
                # This is a sub-item
                fixed_lines.append(f'      ({content})')
    
    # Ensure we have a valid structure
    if len(fixed_lines) < 3:  # mindmap + root + at least one branch
        return """mindmap
  root(Article Content)
    (Main Topics)
      (Key Point 1)
      (Key Point 2)
    (Details)
      (Important Info)
      (Supporting Facts)"""
    
    return '\n'.join(fixed_lines)

def normalize_url(url: str) -> str:
    """
    Normalize URL input to ensure proper format
    
    Args:
        url (str): User input URL
        
    Returns:
        str: Normalized URL with proper protocol
    """
    # Remove leading/trailing whitespace
    url = url.strip()
    
    # If empty, return as-is
    if not url:
        return url
    
    # If already has protocol, return as-is
    if url.startswith(('http://', 'https://')):
        return url
    
    # If starts with www., add https://
    if url.startswith('www.'):
        return f'https://{url}'
    
    # For everything else, add https://
    return f'https://{url}'

def analyze_diagram_complexity(diagram_code: str) -> dict:
    """
    Analyze diagram complexity to determine optimal sizing
    
    Args:
        diagram_code (str): Mermaid diagram code
        
    Returns:
        dict: Complexity analysis with scoring and recommendations
    """
    import re
    
    # Initialize analysis
    analysis = {
        'type': 'unknown',
        'node_count': 0,
        'edge_count': 0,
        'text_density': 0,
        'max_depth': 0,
        'branching_factor': 0,
        'complexity_score': 0,
        'recommended_height': 500,
        'recommended_width': '100%'
    }
    
    lines = diagram_code.strip().split('\n')
    
    # Determine diagram type
    if 'mindmap' in diagram_code:
        analysis['type'] = 'mindmap'
    elif 'flowchart' in diagram_code:
        analysis['type'] = 'flowchart'
    elif 'timeline' in diagram_code:
        analysis['type'] = 'timeline'
    elif 'graph' in diagram_code:
        analysis['type'] = 'network'
    
    # Count nodes and analyze structure
    nodes = set()
    edges = 0
    total_text_length = 0
    max_line_length = 0
    current_depth = 0
    max_depth = 0
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('%%'):
            continue
            
        # Count indentation for depth analysis
        indent_level = (len(line) - len(line.lstrip())) // 2
        current_depth = max(current_depth, indent_level)
        max_depth = max(max_depth, current_depth)
        
        # Extract nodes and text content
        if analysis['type'] == 'mindmap':
            # Mindmap nodes: (Node Name) or root(Name)
            node_matches = re.findall(r'\(([^)]+)\)', line)
            for match in node_matches:
                nodes.add(match)
                total_text_length += len(match)
                max_line_length = max(max_line_length, len(match))
                
        elif analysis['type'] == 'flowchart':
            # Flowchart nodes: A[Label], A{Decision}, etc.
            node_matches = re.findall(r'([A-Z]\d*)\[([^\]]+)\]', line)
            decision_matches = re.findall(r'([A-Z]\d*)\{([^}]+)\}', line)
            
            for match in node_matches + decision_matches:
                nodes.add(match[0])
                total_text_length += len(match[1])
                max_line_length = max(max_line_length, len(match[1]))
            
            # Count edges: A --> B, A -->|label| B
            edge_matches = re.findall(r'-->', line)
            edges += len(edge_matches)
            
        elif analysis['type'] == 'timeline':
            # Timeline events
            event_matches = re.findall(r'([^:]+):\s*(.+)', line)
            for match in event_matches:
                nodes.add(match[0])
                total_text_length += len(match[1])
                max_line_length = max(max_line_length, len(match[1]))
                
        elif analysis['type'] == 'network':
            # Network nodes: A[Label] --- B[Label]
            node_matches = re.findall(r'([A-Z])\[([^\]]+)\]', line)
            for match in node_matches:
                nodes.add(match[0])
                total_text_length += len(match[1])
                max_line_length = max(max_line_length, len(match[1]))
            
            # Count connections
            connection_matches = re.findall(r'(---|-->)', line)
            edges += len(connection_matches)
    
    # Update analysis
    analysis['node_count'] = len(nodes)
    analysis['edge_count'] = edges
    analysis['max_depth'] = max_depth
    analysis['text_density'] = total_text_length / max(len(nodes), 1)
    analysis['branching_factor'] = edges / max(len(nodes), 1) if len(nodes) > 0 else 0
    
    # Calculate complexity score (0-100)
    complexity_score = 0
    
    # Node count contribution (0-30 points)
    if analysis['node_count'] <= 5:
        complexity_score += analysis['node_count'] * 3
    elif analysis['node_count'] <= 15:
        complexity_score += 15 + (analysis['node_count'] - 5) * 1.5
    else:
        complexity_score += 30
    
    # Depth contribution (0-25 points)  
    complexity_score += min(analysis['max_depth'] * 5, 25)
    
    # Text density contribution (0-20 points)
    avg_text_length = analysis['text_density']
    if avg_text_length > 50:
        complexity_score += 20
    elif avg_text_length > 25:
        complexity_score += 15
    elif avg_text_length > 15:
        complexity_score += 10
    else:
        complexity_score += avg_text_length / 3
    
    # Branching factor contribution (0-15 points)
    complexity_score += min(analysis['branching_factor'] * 10, 15)
    
    # Type-specific bonus (0-10 points)
    type_complexity = {
        'mindmap': 5,
        'flowchart': 8,
        'timeline': 4,
        'network': 10
    }
    complexity_score += type_complexity.get(analysis['type'], 5)
    
    analysis['complexity_score'] = min(int(complexity_score), 100)
    
    # Calculate recommended dimensions based on complexity - Much larger base sizes
    base_height = 1000  # Increased significantly from 600
    if analysis['complexity_score'] <= 20:
        analysis['recommended_height'] = base_height
    elif analysis['complexity_score'] <= 40:
        analysis['recommended_height'] = base_height + 400  
    elif analysis['complexity_score'] <= 60:
        analysis['recommended_height'] = base_height + 800  
    elif analysis['complexity_score'] <= 80:
        analysis['recommended_height'] = base_height + 1200 
    else:
        analysis['recommended_height'] = base_height + 1600  
    
    # Ensure minimum readability 
    min_height_per_node = 100  # Increased from 90
    min_required_height = analysis['node_count'] * min_height_per_node
    analysis['recommended_height'] = max(analysis['recommended_height'], min_required_height)
    
    # Cap maximum height for initial display 
    analysis['recommended_height'] = min(analysis['recommended_height'], 2500)  # Increased from 1800
    
    return analysis

def create_mermaid_html(mindmap_code: str) -> str:
    """
    Create HTML to display Mermaid.js diagram with adaptive sizing and modal functionality
    
    Args:
        mindmap_code (str): Mermaid.js code
        
    Returns:
        str: HTML code for displaying the mindmap with smart sizing and modal features
    """
    import json
    
    # Analyze diagram complexity for optimal sizing
    complexity_analysis = analyze_diagram_complexity(mindmap_code)
    
    # Escape the code for JavaScript
    escaped_code = mindmap_code.replace('`', '\\`').replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    
    # Create complexity info for display
    complexity_info = f"""
    Complexity Score: {complexity_analysis['complexity_score']}/100
    Nodes: {complexity_analysis['node_count']} | Type: {complexity_analysis['type'].title()}
    Auto-sized: {complexity_analysis['recommended_height']}px height
    """.strip()
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 10px;
                background-color: #f8f9fa;
                overflow-x: hidden;
            }}
            
            /* Adaptive Container Styles */
            .diagram-wrapper {{
                position: relative;
                width: 100%;
                min-height: 900px;
                background: white;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            
            .diagram-controls {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border-bottom: 2px solid #dee2e6;
            }}
            
            .size-controls {{
                display: flex;
                gap: 8px;
                align-items: center;
            }}
            
            .size-label {{
                font-size: 12px;
                font-weight: bold;
                color: #6c757d;
                margin-right: 8px;
            }}
            
            .size-btn {{
                padding: 6px 12px;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background: white;
                color: #495057;
                cursor: pointer;
                font-size: 11px;
                font-weight: bold;
                transition: all 0.3s ease;
            }}
            
            .size-btn:hover {{
                background: #f8f9fa;
                border-color: #2E86AB;
                color: #2E86AB;
            }}
            
            .size-btn.active {{
                background: #2E86AB;
                color: white;
                border-color: #2E86AB;
            }}
            
            .complexity-info {{
                font-size: 10px;
                color: #6c757d;
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            
            .expand-hint {{
                display: flex;
                align-items: center;
                gap: 5px;
                font-size: 11px;
                color: #6c757d;
                cursor: pointer;
                transition: color 0.3s ease;
            }}
            
            .expand-hint:hover {{
                color: #2E86AB;
            }}
            
            .mermaid-container {{
                position: relative;
                cursor: pointer;
                transition: all 0.3s ease;
                background: white;
                height: {complexity_analysis['recommended_height']}px;
                min-height: 800px;
                min-width: 1500px;
                overflow: auto;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            
            .mermaid-container:hover {{
                background: #fafbfc;
            }}
            
            .mermaid {{
                padding: 40px;
                width: 100%;
                height: 100%;
                min-height: 800px;
                display: flex;
                justify-content: center;
                align-items: center;
                position: relative;
            }}
            
            .mermaid svg {{
                max-width: 95% !important;
                max-height: 95% !important;
                width: auto !important;
                height: auto !important;
            }}
            
            .click-overlay {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(46, 134, 171, 0.05);
                opacity: 0;
                transition: opacity 0.3s ease;
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 10;
            }}
            
            .mermaid-container:hover .click-overlay {{
                opacity: 1;
            }}
            
            .click-hint {{
                background: rgba(46, 134, 171, 0.9);
                color: white;
                padding: 12px 20px;
                border-radius: 25px;
                font-size: 14px;
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            }}
            
            /* Modal Styles - Full Screen Experience */
            .modal {{
                display: none;
                position: fixed;
                z-index: 9999;
                left: 0;
                top: 0;
                width: 100vw;
                height: 100vh;
                background-color: rgba(0,0,0,0.95);
                animation: fadeIn 0.4s ease;
            }}
            .modal-content {{
                position: relative;
                background-color: white;
                margin: 0;
                padding: 0;
                border-radius: 0;
                width: 100%;
                height: 100%;
                box-shadow: none;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }}
            .modal-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 25px;
                background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
                color: white;
                flex-shrink: 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }}
            .modal-title {{
                font-size: 20px;
                font-weight: bold;
                margin: 0;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .modal-actions {{
                display: flex;
                gap: 12px;
            }}
            .modal-btn {{
                padding: 10px 18px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 13px;
                font-weight: bold;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .copy-btn {{
                background: #28a745;
                color: white;
            }}
            .copy-btn:hover {{
                background: #218838;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
            }}
            .close-btn {{
                background: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.3);
            }}
            .close-btn:hover {{
                background: rgba(255,255,255,0.3);
                transform: translateY(-1px);
            }}
            .modal-diagram {{
                flex: 1;
                display: flex;
                justify-content: center;
                align-items: center;
                background: linear-gradient(45deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 40px;
                overflow: auto;
                position: relative;
            }}
            .modal-mermaid {{
                background: white;
                padding: 60px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                max-width: none;
                max-height: none;
                overflow: visible;
                min-width: 80vw;
                min-height: 70vh;
                display: flex;
                justify-content: center;
                align-items: center;
                position: relative;
            }}
            .modal-mermaid svg {{
                max-width: none !important;
                max-height: none !important;
                width: auto !important;
                height: auto !important;
                min-width: 600px !important;
                min-height: 400px !important;
            }}
            .zoom-controls {{
                position: absolute;
                top: 20px;
                right: 20px;
                display: flex;
                gap: 8px;
                z-index: 100;
            }}
            .zoom-btn {{
                width: 40px;
                height: 40px;
                border: none;
                border-radius: 50%;
                background: rgba(46, 134, 171, 0.9);
                color: white;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            }}
            .zoom-btn:hover {{
                background: rgba(46, 134, 171, 1);
                transform: scale(1.1);
            }}
            .fullscreen-hint {{
                position: absolute;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0,0,0,0.7);
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 12px;
                opacity: 0.8;
            }}
            .copy-success {{
                background: #d4edda !important;
                color: #155724 !important;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: scale(0.9); }}
                to {{ opacity: 1; transform: scale(1); }}
            }}
            @keyframes copySuccess {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1); }}
            }}
            .copy-animation {{
                animation: copySuccess 0.4s ease;
            }}
        </style>
    </head>
    <body>
        <div class="diagram-wrapper">
            <div class="diagram-controls">
                <div class="size-controls">
                    <span class="size-label">Size:</span>
                    <button class="size-btn" onclick="setSize('compact')" id="compactBtn">Compact</button>
                    <button class="size-btn active" onclick="setSize('optimal')" id="optimalBtn">Auto</button>
                    <button class="size-btn" onclick="setSize('large')" id="largeBtn">Large</button>
                </div>
                <div class="complexity-info">
                    <i class="fas fa-brain"></i>
                    <span>{complexity_info}</span>
                </div>
                <div class="expand-hint" onclick="openModal()">
                    <i class="fas fa-expand-alt"></i>
                    <span>Full Screen</span>
                </div>
            </div>
            
            <div class="mermaid-container" onclick="openModal()" id="diagramContainer">
                <div class="mermaid" id="diagram">{mindmap_code}</div>
                <div class="click-overlay">
                    <div class="click-hint">
                        <i class="fas fa-expand-arrows-alt"></i>
                        Click for full screen view
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div id="diagramModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title">
                        <i class="fas fa-expand-arrows-alt"></i> 
                        <span>Full Screen View</span>
                    </h2>
                    <div class="modal-actions">
                        <button class="modal-btn copy-btn" onclick="copyDiagramCode()" id="copyBtn">
                            <i class="fas fa-copy"></i> Copy Code
                        </button>
                        <button class="modal-btn close-btn" onclick="closeModal()">
                            <i class="fas fa-times"></i> Close
                        </button>
                    </div>
                </div>
                <div class="modal-diagram">
                    <div class="modal-mermaid" id="modalMermaidContainer">
                        <!-- Diagram will be rendered here -->
                    </div>
                    <div class="zoom-controls">
                        <button class="zoom-btn" onclick="zoomIn()" title="Zoom In">
                            <i class="fas fa-plus"></i>
                        </button>
                        <button class="zoom-btn" onclick="zoomOut()" title="Zoom Out">
                            <i class="fas fa-minus"></i>
                        </button>
                        <button class="zoom-btn" onclick="resetZoom()" title="Reset Zoom">
                            <i class="fas fa-expand"></i>
                        </button>
                    </div>
                    <div class="fullscreen-hint">
                        <i class="fas fa-mouse"></i> Scroll to zoom • Click & drag to pan
                    </div>
                </div>
            </div>
        </div>

        <script>
            // Store the diagram code and complexity analysis
            const diagramCode = `{escaped_code}`;
            const complexityAnalysis = {json.dumps(complexity_analysis)};
            let modalRendered = false;
            let currentZoom = 1;
            let modalDiagramElement = null;
            let currentSize = 'optimal';  // Changed from 'compact' to start with Auto
            
            // Size configurations - Much more dramatic differences
            const sizeConfigs = {{
                compact: {{ height: 800, label: 'Compact' }},  // Increased significantly
                optimal: {{ height: Math.max(complexityAnalysis.recommended_height, 1000), label: 'Auto' }},  // Ensure minimum 1000px
                large: {{ height: Math.min(complexityAnalysis.recommended_height * 1.8, 2500), label: 'Large' }}  // Even larger
            }};
            
            // Initialize Mermaid
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'default',
                flowchart: {{
                    useMaxWidth: false,
                    htmlLabels: true
                }},
                mindmap: {{
                    padding: 10,
                    useMaxWidth: false
                }},
                timeline: {{
                    useMaxWidth: false
                }},
                gitGraph: {{
                    useMaxWidth: false
                }}
            }});

            // Size control functions
            function setSize(size) {{
                currentSize = size;
                const container = document.getElementById('diagramContainer');
                const config = sizeConfigs[size];
                
                container.style.height = config.height + 'px';
                
                // Update button states
                document.querySelectorAll('.size-btn').forEach(btn => btn.classList.remove('active'));
                document.getElementById(size + 'Btn').classList.add('active');
                
                // Update complexity info to show current size
                const complexityInfo = document.querySelector('.complexity-info span');
                complexityInfo.textContent = `${{complexityAnalysis.complexity_score}}/100 | ${{complexityAnalysis.node_count}} nodes | ${{config.label}}: ${{config.height}}px`;
            }}

            // Modal functions
            async function openModal() {{
                const modal = document.getElementById('diagramModal');
                modal.style.display = 'block';
                document.body.style.overflow = 'hidden';
                
                // Render diagram in modal if not already rendered
                if (!modalRendered) {{
                    const container = document.getElementById('modalMermaidContainer');
                    
                    // Create a unique ID for the modal diagram
                    const modalDiagramId = 'modalDiagram_' + Date.now();
                    container.innerHTML = `<div class="mermaid" id="${{modalDiagramId}}" style="transform-origin: center center;">${{diagramCode}}</div>`;
                    
                    // Re-initialize mermaid for the modal content
                    try {{
                        await mermaid.run({{ nodes: [document.getElementById(modalDiagramId)] }});
                        modalDiagramElement = document.getElementById(modalDiagramId);
                        modalRendered = true;
                        
                        // Add mouse wheel zoom
                        container.addEventListener('wheel', handleZoom, {{ passive: false }});
                        
                        // Add click and drag panning
                        let isPanning = false;
                        let startX, startY, scrollLeft, scrollTop;
                        
                        container.addEventListener('mousedown', (e) => {{
                            if (e.target.closest('svg')) {{
                                isPanning = true;
                                startX = e.pageX - container.offsetLeft;
                                startY = e.pageY - container.offsetTop;
                                scrollLeft = container.scrollLeft;
                                scrollTop = container.scrollTop;
                                container.style.cursor = 'grabbing';
                            }}
                        }});
                        
                        container.addEventListener('mouseleave', () => {{
                            isPanning = false;
                            container.style.cursor = 'grab';
                        }});
                        
                        container.addEventListener('mouseup', () => {{
                            isPanning = false;
                            container.style.cursor = 'grab';
                        }});
                        
                        container.addEventListener('mousemove', (e) => {{
                            if (!isPanning) return;
                            e.preventDefault();
                            const x = e.pageX - container.offsetLeft;
                            const y = e.pageY - container.offsetTop;
                            const walkX = (x - startX) * 2;
                            const walkY = (y - startY) * 2;
                            container.scrollLeft = scrollLeft - walkX;
                            container.scrollTop = scrollTop - walkY;
                        }});
                        
                        container.style.cursor = 'grab';
                        
                    }} catch (error) {{
                        console.log('Mermaid render error:', error);
                        // Fallback: try with mermaid.init
                        mermaid.init(undefined, document.getElementById(modalDiagramId));
                        modalDiagramElement = document.getElementById(modalDiagramId);
                        modalRendered = true;
                    }}
                }}
                
                // Reset zoom when opening
                resetZoom();
            }}

            function closeModal() {{
                document.getElementById('diagramModal').style.display = 'none';
                document.body.style.overflow = 'auto';
            }}

            // Zoom functions
            function handleZoom(event) {{
                event.preventDefault();
                const delta = event.deltaY > 0 ? -0.1 : 0.1;
                currentZoom = Math.max(0.3, Math.min(3, currentZoom + delta));
                applyZoom();
            }}

            function zoomIn() {{
                currentZoom = Math.min(3, currentZoom + 0.2);
                applyZoom();
            }}

            function zoomOut() {{
                currentZoom = Math.max(0.3, currentZoom - 0.2);
                applyZoom();
            }}

            function resetZoom() {{
                currentZoom = 1;
                applyZoom();
                
                // Center the diagram
                const container = document.getElementById('modalMermaidContainer');
                container.scrollLeft = (container.scrollWidth - container.clientWidth) / 2;
                container.scrollTop = (container.scrollHeight - container.clientHeight) / 2;
            }}

            function applyZoom() {{
                if (modalDiagramElement) {{
                    modalDiagramElement.style.transform = `scale(${{currentZoom}})`;
                    modalDiagramElement.style.transition = 'transform 0.2s ease';
                }}
            }}

            // Copy functionality
            async function copyDiagramCode() {{
                try {{
                    await navigator.clipboard.writeText(diagramCode);
                    showCopySuccess();
                }} catch (err) {{
                    // Fallback for older browsers
                    const textArea = document.createElement('textarea');
                    textArea.value = diagramCode;
                    textArea.style.position = 'fixed';
                    textArea.style.opacity = '0';
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    showCopySuccess();
                }}
            }}

            function showCopySuccess() {{
                const copyBtn = document.getElementById('copyBtn');
                const originalText = copyBtn.innerHTML;
                
                copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                copyBtn.classList.add('copy-success', 'copy-animation');
                
                setTimeout(() => {{
                    copyBtn.innerHTML = originalText;
                    copyBtn.classList.remove('copy-success', 'copy-animation');
                }}, 2500);
            }}

            // Close modal when clicking outside
            window.onclick = function(event) {{
                const modal = document.getElementById('diagramModal');
                if (event.target === modal) {{
                    closeModal();
                }}
            }}

            // Close modal with Escape key
            document.addEventListener('keydown', function(event) {{
                if (event.key === 'Escape') {{
                    closeModal();
                }}
            }});

            // Ensure main diagram renders properly
            document.addEventListener('DOMContentLoaded', function() {{
                // Force re-render of main diagram if needed
                setTimeout(() => {{
                    const mainDiagram = document.getElementById('diagram');
                    if (mainDiagram && !mainDiagram.querySelector('svg')) {{
                        mermaid.init(undefined, mainDiagram);
                    }}
                }}, 100);
            }});
        </script>
    </body>
    </html>
    """
    return html_code