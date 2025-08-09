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
    
    prompt = f"""You are creating a mindmap for someone with ADHD and other neurodiverse learning needs. 
    
    Please convert the following text into a Mermaid.js mindmap format. Follow these guidelines:
    
    1. Use clear, concise node labels
    2. Organize information hierarchically from main topics to subtopics
    3. Limit each branch to 3-5 items to avoid overwhelming
    4. Use descriptive but brief text
    5. Include icons using ::icon(fa fa-icon-name) where appropriate
    6. Structure should be: mindmap root(Main Topic) with branches
    
    Example format:
    ```
    mindmap
      root(Main Topic)
        (Branch 1)
          ::icon(fa fa-lightbulb)
          (Subtopic 1)
          (Subtopic 2)
        (Branch 2)
          ::icon(fa fa-gear)
          (Subtopic 3)
          (Subtopic 4)
    ```
    
    Text to convert:
    {text[:3000]}
    
    Please provide ONLY the Mermaid.js code, starting with 'mindmap' and nothing else.
    """
    
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
    Create HTML to display Mermaid.js diagram
    
    Args:
        mindmap_code (str): Mermaid.js code
        
    Returns:
        str: HTML code for displaying the mindmap
    """
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px;
                background-color: #f8f9fa;
            }}
            .mermaid {{
                display: flex;
                justify-content: center;
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <div class="mermaid">{mindmap_code}</div>
        <script>
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'default',
                mindmap: {{
                    padding: 20
                }}
            }});
        </script>
    </body>
    </html>
    """
    return html_code