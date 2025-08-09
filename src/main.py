import streamlit as st
import os
import sys
from dotenv import load_dotenv
from streamlit.components.v1 import html

# Add current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Now import utils (try multiple approaches)
try:
    from utils import (scrape_text, summarize_with_claude, generate_mindmap_with_claude, 
                      generate_flowchart_with_claude, generate_timeline_with_claude, 
                      generate_network_with_claude, create_mermaid_html, normalize_url, 
                      validate_and_fix_mermaid)
except ImportError:
    try:
        from neurommind_mapper.utils import (scrape_text, summarize_with_claude, generate_mindmap_with_claude,
                                           generate_flowchart_with_claude, generate_timeline_with_claude,
                                           generate_network_with_claude, create_mermaid_html, normalize_url,
                                           validate_and_fix_mermaid)
    except ImportError:
        # Last resort - import from full path
        import importlib.util
        utils_path = os.path.join(current_dir, 'utils.py')
        spec = importlib.util.spec_from_file_location("utils", utils_path)
        utils = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(utils)
        scrape_text = utils.scrape_text
        summarize_with_claude = utils.summarize_with_claude
        generate_mindmap_with_claude = utils.generate_mindmap_with_claude
        generate_flowchart_with_claude = utils.generate_flowchart_with_claude
        generate_timeline_with_claude = utils.generate_timeline_with_claude
        generate_network_with_claude = utils.generate_network_with_claude
        create_mermaid_html = utils.create_mermaid_html
        normalize_url = utils.normalize_url
        validate_and_fix_mermaid = utils.validate_and_fix_mermaid

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="NeuroMind Mapper",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better accessibility
st.markdown("""
<style>
    .main-header {
        color: #2E86AB;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #A23B72;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #E8F4FD;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #D4EDDA;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28A745;
        margin: 1rem 0;
    }
    .diagram-card {
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: white;
        transition: all 0.3s ease;
    }
    .diagram-card:hover {
        border-color: #2E86AB;
        box-shadow: 0 2px 8px rgba(46, 134, 171, 0.2);
    }
    .diagram-card.selected {
        border-color: #2E86AB;
        background-color: #f8f9fa;
        box-shadow: 0 2px 8px rgba(46, 134, 171, 0.3);
    }
    .gallery-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def show_diagram_gallery():
    """Display simplified diagram type selection"""
    st.markdown("### 🎨 Choose Your Visualization Style")
    st.markdown("Select how you want to see the information:")
    
    # Initialize session state for diagram choice
    if 'selected_diagram' not in st.session_state:
        st.session_state.selected_diagram = 'mindmap'
    
    # Create columns for clean button layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🧠 **Mind Map**", 
                    key="mindmap_btn", 
                    help="Perfect for organizing concepts and ideas hierarchically",
                    use_container_width=True):
            st.session_state.selected_diagram = 'mindmap'
        
        if st.session_state.selected_diagram == 'mindmap':
            st.success("✅ Selected")
        else:
            st.caption("Great for ADHD learners")
    
    with col2:
        if st.button("🔄 **Flowchart**", 
                    key="flowchart_btn",
                    help="Ideal for processes, steps, and workflows",
                    use_container_width=True):
            st.session_state.selected_diagram = 'flowchart'
        
        if st.session_state.selected_diagram == 'flowchart':
            st.success("✅ Selected")
        else:
            st.caption("Best for processes")
    
    with col3:
        if st.button("📅 **Timeline**", 
                    key="timeline_btn",
                    help="Perfect for historical events and sequences",
                    use_container_width=True):
            st.session_state.selected_diagram = 'timeline'
        
        if st.session_state.selected_diagram == 'timeline':
            st.success("✅ Selected")
        else:
            st.caption("Great for history")
    
    with col4:
        if st.button("🕸️ **Network**", 
                    key="network_btn",
                    help="Shows relationships and connections between ideas",
                    use_container_width=True):
            st.session_state.selected_diagram = 'network'
        
        if st.session_state.selected_diagram == 'network':
            st.success("✅ Selected")
        else:
            st.caption("Shows connections")
    
    return st.session_state.selected_diagram

def create_change_diagram_section(current_type, text, api_key):
    """Allow users to try different diagram types after generation"""
    st.markdown("---")
    st.markdown("### 🔄 Try Different Visualization")
    st.markdown("Not quite what you expected? Try a different diagram type:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if current_type != 'mindmap' and st.button("🧠 Try Mind Map", use_container_width=True):
            st.session_state.selected_diagram = 'mindmap'
            st.session_state.regenerate = True
            st.rerun()
    
    with col2:
        if current_type != 'flowchart' and st.button("🔄 Try Flowchart", use_container_width=True):
            st.session_state.selected_diagram = 'flowchart'
            st.session_state.regenerate = True
            st.rerun()
    
    with col3:
        if current_type != 'timeline' and st.button("📅 Try Timeline", use_container_width=True):
            st.session_state.selected_diagram = 'timeline'
            st.session_state.regenerate = True
            st.rerun()

def main():
    # Header
    st.markdown('<h1 class="main-header">🧠 NeuroMind Mapper</h1>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">An AI-powered tool to create visual diagrams for neurodiverse learners</div>', unsafe_allow_html=True)
    
    # Sidebar with instructions
    with st.sidebar:
        st.header("📝 How to Use")
        st.markdown("""
        **Simple 3-step process:**
        
        1. **📝 Enter URL** - Paste any article link
        2. **🎨 Choose Type** - Pick your visualization style  
        3. **🚀 Generate** - Create your diagram
        4. **🔄 Try Different** - Switch types if desired
        
        **Great sources:**
        - News articles (BBC, CNN, Reuters)
        - Blog posts (Medium, personal blogs)
        - Educational content
        - Wikipedia articles
        """)
        
        st.header("🎯 Why Visual Learning?")
        st.markdown("""
        - **65% are visual learners**
        - **ADHD-friendly** structure
        - **Quick understanding** of complex topics
        - **Better memory** retention
        """)
        
        st.header("📚 Coming Soon")
        st.info("**Diagram Library** - Browse examples and learn about each visualization type")
    
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # STEP 1: URL Input (moved to top)
        st.markdown("### 🔗 Step 1: Enter Article URL")
        
        # URL input outside form to avoid form conflicts
        url = st.text_input(
            "Enter a URL to create your diagram:",
            placeholder="google.com, bbc.com/news, medium.com/@author/article",
            help="Enter any website URL - we'll handle the https:// part!",
            label_visibility="collapsed"
        )
        
        # Show URL preview if user has entered something
        if url and url.strip():
            normalized_url = normalize_url(url.strip())
            st.info(f"📡 Will fetch: **{normalized_url}**")
            
            # STEP 2: Diagram type selection (only show if URL entered)
            st.markdown("### 🎨 Step 2: Choose Visualization Type")
            selected_diagram = show_diagram_gallery()
            
            # STEP 3: Generate button
            st.markdown("### 🚀 Step 3: Generate Diagram")
            with st.form("generate_form", clear_on_submit=False):
                submitted = st.form_submit_button(f"Generate {selected_diagram.title()}", use_container_width=True)
        else:
            submitted = False
            selected_diagram = 'mindmap'  # default
        
        # Check if we need to regenerate with different type
        if 'regenerate' in st.session_state and st.session_state.regenerate:
            submitted = True
            url = st.session_state.get('last_url', '')
            selected_diagram = st.session_state.selected_diagram
            st.session_state.regenerate = False
        
        if submitted and url:
            # Store URL for regeneration
            st.session_state.last_url = url
            
            # Normalize the URL
            normalized_url = normalize_url(url.strip())
            
            # Validate normalized URL
            if not normalized_url or not normalized_url.startswith(('http://', 'https://')):
                st.error("❌ Please enter a valid website URL (e.g., google.com)")
                return
            
            # Get API key
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                st.error("❌ Please set your ANTHROPIC_API_KEY in the .env file")
                return
            
            # Use cached text if regenerating, otherwise scrape
            if 'cached_text' not in st.session_state or st.session_state.get('last_url') != url:
                # Process the URL
                with st.spinner(f"🔍 Scraping content from {normalized_url}..."):
                    text = scrape_text(normalized_url)
                
                if text.startswith("Error") or text.startswith("Failed"):
                    st.error(f"❌ Could not access **{normalized_url}**\n\n**Try:**\n- Check if the website is accessible\n- Use a different article URL\n- Ensure the site allows web scraping")
                    return
                
                st.session_state.cached_text = text
            else:
                text = st.session_state.cached_text
            
            # Show original text in expander (only once)
            if 'cached_text' not in st.session_state or st.session_state.get('last_url') != url:
                with st.expander("📄 View Original Text"):
                    st.text_area("Scraped Content", text, height=200)
            
            # Generate summary (only once)
            if 'cached_summary' not in st.session_state or st.session_state.get('last_url') != url:
                with st.spinner("📝 Creating summary..."):
                    summary = summarize_with_claude(text, api_key)
                st.session_state.cached_summary = summary
            else:
                summary = st.session_state.cached_summary
            
            st.markdown('<div class="success-box"><strong>📋 AI Summary</strong></div>', unsafe_allow_html=True)
            st.write(summary)
            
            # Generate diagram based on selected type
            with st.spinner(f"🎨 Generating {selected_diagram}..."):
                if selected_diagram == 'mindmap':
                    diagram_code = generate_mindmap_with_claude(text, api_key)
                elif selected_diagram == 'flowchart':
                    diagram_code = generate_flowchart_with_claude(text, api_key)
                elif selected_diagram == 'timeline':
                    diagram_code = generate_timeline_with_claude(text, api_key)
                else:  # network
                    diagram_code = generate_network_with_claude(text, api_key)
            
            if diagram_code.startswith("Error"):
                st.error(diagram_code)
                return
            
            # Validate and fix the diagram code
            try:
                if selected_diagram == 'mindmap':
                    validated_code = validate_and_fix_mermaid(diagram_code)
                else:
                    validated_code = diagram_code  # Other types need their own validation
                
                # Show diagram code in expander
                with st.expander("🔧 View Diagram Code"):
                    st.code(validated_code, language="text")
                
                # Display diagram
                st.markdown(f'<div class="success-box"><strong>🗺️ Your {selected_diagram.title()} Visualization</strong></div>', unsafe_allow_html=True)
                html_content = create_mermaid_html(validated_code)
                html(html_content, width=800, height=600)
                
                # Add option to try different diagram types
                create_change_diagram_section(selected_diagram, text, api_key)
                
            except Exception as e:
                st.error(f"⚠️ Diagram generation failed: {str(e)}")
                st.info("💡 **Tip**: Try with a shorter article or different content")
                
                # Show the raw code for debugging
                with st.expander("🔧 Debug: Raw Diagram Code"):
                    st.code(diagram_code, language="text")
    
    with col2:
        st.markdown("### 💡 Quick Tips")
        st.info("""
        **Best articles:**
        - 500-2000 words
        - Clear structure
        - Single main topic
        - Well-organized content
        """)
        
        st.markdown("### 🎨 Diagram Guide")
        
        diagram_info = {
            "🧠 Mind Map": "Perfect for concepts, topics, and hierarchical information. **Recommended for most content.**",
            "🔄 Flowchart": "Ideal for processes, step-by-step guides, and decision trees.",
            "📅 Timeline": "Great for historical events, project phases, and chronological content.", 
            "🕸️ Network": "Shows relationships and connections between different concepts."
        }
        
        for name, description in diagram_info.items():
            with st.expander(name):
                st.write(description)
        
        st.markdown("### ✨ Pro Tips")
        st.success("""
        - **Start with Mind Map** - works for 80% of content
        - **Try different types** for the same article
        - **Use Timeline** for historical content
        - **Flowcharts** shine with how-to guides
        """)

if __name__ == "__main__":
    main()