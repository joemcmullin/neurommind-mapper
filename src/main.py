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
    from utils import scrape_text, summarize_with_claude, generate_mindmap_with_claude, create_mermaid_html, normalize_url
except ImportError:
    try:
        from neurommind_mapper.utils import scrape_text, summarize_with_claude, generate_mindmap_with_claude, create_mermaid_html, normalize_url
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
        create_mermaid_html = utils.create_mermaid_html
        normalize_url = utils.normalize_url

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
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🧠 NeuroMind Mapper</h1>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">An AI-powered tool to create visual mind maps for neurodiverse learners</div>', unsafe_allow_html=True)
    
    # Sidebar with instructions
    with st.sidebar:
        st.header("📝 How to Use")
        st.markdown("""
        1. **Enter a website URL** (we'll add https:// automatically!)
        2. **Examples**: `google.com`, `bbc.com/news`, `medium.com/@author/article`
        3. **Click Generate** to create your mindmap
        4. **View the summary** and visual mindmap
        5. **Save or share** your results
        
        **Great sources:**
        - News articles (BBC, CNN, Reuters)
        - Blog posts (Medium, personal blogs)
        - Educational content
        - Wikipedia articles
        """)
        
        st.header("🎯 Benefits")
        st.markdown("""
        - **Visual Learning**: 65% of people are visual learners
        - **ADHD-Friendly**: Breaks down complex information
        - **Quick Understanding**: Get main ideas fast
        - **Memory Aid**: Visual structure helps retention
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input form
        with st.form("mindmap_form", clear_on_submit=False):
            url = st.text_input(
                "🔗 Enter a URL to create a mindmap:",
                placeholder="google.com, bbc.com/news, medium.com/@author/article",
                help="Enter any website URL - we'll handle the https:// part!"
            )
            
            # Show URL preview if user has entered something
            if url and url.strip():
                normalized_url = normalize_url(url.strip())
                st.info(f"📡 Will fetch: **{normalized_url}**")
            
            submitted = st.form_submit_button("🚀 Generate Mindmap", use_container_width=True)
        
        if submitted and url:
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
            
            # Process the URL
            with st.spinner(f"🔍 Scraping content from {normalized_url}..."):
                text = scrape_text(normalized_url)
            
            if text.startswith("Error") or text.startswith("Failed"):
                st.error(f"❌ Could not access **{normalized_url}**\n\n**Try:**\n- Check if the website is accessible\n- Use a different article URL\n- Ensure the site allows web scraping")
                return
            
            # Show original text in expander
            with st.expander("📄 View Original Text"):
                st.text_area("Scraped Content", text, height=200)
            
            # Generate summary
            with st.spinner("📝 Creating summary..."):
                summary = summarize_with_claude(text, api_key)
            
            st.markdown('<div class="success-box"><strong>📋 AI Summary</strong></div>', unsafe_allow_html=True)
            st.write(summary)
            
            # Generate mindmap
            with st.spinner("🧠 Generating mindmap..."):
                mindmap_code = generate_mindmap_with_claude(text, api_key)
            
            if mindmap_code.startswith("Error"):
                st.error(mindmap_code)
                return
            
            # Show mindmap code in expander
            with st.expander("🔧 View Mermaid Code"):
                st.code(mindmap_code, language="text")
            
            # Display mindmap
            st.markdown('<div class="success-box"><strong>🗺️ Your Visual Mindmap</strong></div>', unsafe_allow_html=True)
            html_content = create_mermaid_html(mindmap_code)
            html(html_content, width=800, height=600)
    
    with col2:
        st.markdown("### 💡 Tips for Better Results")
        st.info("""
        **Choose articles that are:**
        - Well-structured
        - Have clear headings
        - Focus on one main topic
        - Are 500-2000 words long
        """)
        
        st.markdown("### 🎨 Mindmap Features")
        st.success("""
        ✅ Hierarchical organization
        ✅ Color-coded branches  
        ✅ FontAwesome icons
        ✅ Responsive design
        ✅ Clean, ADHD-friendly layout
        """)

if __name__ == "__main__":
    main()