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

def create_mermaid_html(mindmap_code: str) -> str:
    """
    Create HTML to display Mermaid.js diagram with modal functionality
    
    Args:
        mindmap_code (str): Mermaid.js code
        
    Returns:
        str: HTML code for displaying the mindmap with modal and copy features
    """
    # Escape the code for JavaScript
    escaped_code = mindmap_code.replace('`', '\\`').replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    
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
                overflow: hidden;
            }}
            .mermaid-container {{
                position: relative;
                cursor: pointer;
                transition: all 0.3s ease;
                border-radius: 10px;
                overflow: hidden;
            }}
            .mermaid-container:hover {{
                transform: scale(1.02);
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }}
            .mermaid {{
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: white;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                width: 100%;
                height: 100%;
                box-sizing: border-box;
                overflow: hidden;
                position: relative;
                min-height: 400px;
            }}
            .mermaid svg {{
                max-width: 100% !important;
                max-height: 100% !important;
                width: auto !important;
                height: auto !important;
            }}
            .click-hint {{
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(46, 134, 171, 0.9);
                color: white;
                padding: 8px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                opacity: 0;
                transition: all 0.3s ease;
                z-index: 10;
            }}
            .mermaid-container:hover .click-hint {{
                opacity: 1;
                transform: translateY(-2px);
            }}
            
            /* Modal Styles */
            .modal {{
                display: none;
                position: fixed;
                z-index: 9999;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.8);
                animation: fadeIn 0.3s ease;
            }}
            .modal-content {{
                position: relative;
                background-color: white;
                margin: 2% auto;
                padding: 0;
                border-radius: 15px;
                width: 95%;
                max-width: 1400px;
                height: 90%;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }}
            .modal-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 25px;
                background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
                color: white;
            }}
            .modal-title {{
                font-size: 24px;
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
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
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
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
            }}
            .close-btn {{
                background: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.3);
            }}
            .close-btn:hover {{
                background: rgba(255,255,255,0.3);
                transform: translateY(-2px);
            }}
            .modal-diagram {{
                flex: 1;
                display: flex;
                justify-content: center;
                align-items: center;
                background: linear-gradient(45deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 30px;
                overflow: auto;
            }}
            .modal-mermaid {{
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                max-width: 100%;
                max-height: 100%;
                overflow: auto;
                min-width: 600px;
                min-height: 400px;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .modal-mermaid svg {{
                max-width: none !important;
                max-height: none !important;
                width: auto !important;
                height: auto !important;
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
        <div class="mermaid-container" onclick="openModal()">
            <div class="mermaid" id="diagram">{mindmap_code}</div>
            <div class="click-hint">
                <i class="fas fa-expand-alt"></i> Click to enlarge
            </div>
        </div>

        <!-- Modal -->
        <div id="diagramModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title">
                        <i class="fas fa-diagram-project"></i> 
                        <span>Full Size Diagram</span>
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
                </div>
            </div>
        </div>

        <script>
            // Store the diagram code
            const diagramCode = `{escaped_code}`;
            let modalRendered = false;
            
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
                    container.innerHTML = `<div class="mermaid" id="${{modalDiagramId}}">${{diagramCode}}</div>`;
                    
                    // Re-initialize mermaid for the modal content
                    try {{
                        await mermaid.run({{ nodes: [document.getElementById(modalDiagramId)] }});
                        modalRendered = true;
                    }} catch (error) {{
                        console.log('Mermaid render error:', error);
                        // Fallback: try with mermaid.init
                        mermaid.init(undefined, document.getElementById(modalDiagramId));
                        modalRendered = true;
                    }}
                }}
            }}

            function closeModal() {{
                document.getElementById('diagramModal').style.display = 'none';
                document.body.style.overflow = 'auto';
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