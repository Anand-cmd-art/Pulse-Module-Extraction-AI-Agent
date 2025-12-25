import streamlit as st
import json
from dotenv import load_dotenv
from src.utils.helpers import validate_url, normalize_url
from src.crawler.spider import DocumentationSpider
from src.agent.extractor import AIInferenceAgent

# Initialize Environment
load_dotenv()
st.set_page_config(page_title="Pulse Module Extractor", page_icon="URL", layout="wide")

# UI Layout
st.title("Pulse - Module Extraction AI Agent")
st.markdown("Enter documentation URLs to automatically extract product hierarchies.")

# Input Section
urls_input = st.text_area("Documentation URLs (one per line):", height=100, 
                         placeholder="https://help.instagram.com/\nhttps://help.zluri.com/")

if st.button("Start Extraction"):
    if not urls_input.strip():
        st.warning("Please enter at least one URL.")
        st.stop()

    # 1. Validation Phase
    raw_list = [u.strip() for u in urls_input.split('\n') if u.strip()]
    valid_urls = [normalize_url(u) for u in raw_list if validate_url(u)]

    if not valid_urls:
        st.error(" No valid HTTP/HTTPS URLs found. Please check your input.")
        st.stop()

    # 2. Execution Phase
    with st.status("AI Agent Running...", expanded=True) as status:
        full_context = ""
        
        # Crawling
        for url in valid_urls:
            st.write(f" Crawling {url} and its internal links...")
            spider = DocumentationSpider(url)
            spider.crawl(url)
            content = spider.get_content()
            full_context += content
            st.write(f"Extracted {len(content)} characters from {len(spider.visited)} pages.")
        
        if not full_context:
            status.update(label="Failed!", state="error")
            st.error("Could not extract any content. The site might be blocking scrapers.")
            st.stop()

        # Inference
        st.write("Analyzing content structure with Gemma-3-27b...")
        try:
            agent = AIInferenceAgent()
            result_obj = agent.extract(full_context)
            status.update(label="Extraction Complete!", state="complete")
            
            # 3. Output Phase
            st.divider()
            st.subheader("Extracted Hierarchy")
            
            # Convert Pydantic object to dict for display/download
            json_data = result_obj.model_dump()
            
            # Display JSON
            st.json(json_data)
            
            # Download Button
            st.download_button(
                label=" Download JSON Report",
                data=json.dumps(json_data, indent=4),
                file_name="pulse_hierarchy.json",
                mime="application/json"
            )
            
        except Exception as e:
            status.update(label="Error during AI Inference", state="error")
            st.error(f"AI Processing Failed: {str(e)}")