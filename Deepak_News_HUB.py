import streamlit as st
import requests

# Set page title and icon
st.set_page_config(page_title="Deepak News Hub", page_icon="📰")

st.title("📰 Deepak News Hub")
st.markdown("---")

# User Input in the sidebar
with st.sidebar:
    st.header("Search News")
    query = st.text_input("Topic", placeholder="e.g. Technology, AI, Hitachi")
    api_key = "ea01384660a7413396d05f56dedb569d"

if query:
    # We use 2025-12-01 to ensure we get recent results for today
    url = f"https://newsapi.org/v2/everything?q={query}&from=2025-12-01&sortBy=publishedAt&apiKey={api_key}"
    
    with st.spinner('Loading the latest stories...'):
        response = requests.get(url)
        data = response.json()

    if data.get("articles"):
        articles = data["articles"]
        st.success(f"Showing top results for: {query}")

        for art in articles[:10]: # Show top 10 articles
            with st.container():
                col1, col2 = st.columns([1, 2])
                
                # Column 1: Image
                with col1:
                    img_url = art.get("urlToImage")
                    if img_url:
                        st.image(img_url, use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/400x250.png?text=News+Image", use_container_width=True)
                
                # Column 2: Text and Link
                with col2:
                    st.subheader(art["title"])
                    st.write(art["description"])
                    st.markdown(f"[🔗 Read Full Article]({art['url']})")
                
                st.divider()
    else:
        st.warning("No articles found. Try a different keyword.")
else:
    st.info("👈 Enter a topic in the sidebar to start searching!")