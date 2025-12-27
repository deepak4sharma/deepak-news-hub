import streamlit as st
import requests

# Set page title and icon
st.set_page_config(page_title="Deepak News Hub", page_icon="📰", layout="wide")

st.title("📰 Deepak News Hub")
st.markdown("---")

# Dictionary of country names and their codes for the API
countries = {
    "India": "ind",
    "USA": "us",
    "United Kingdom": "UK",
    "Australia": "au",
    "Canada": "ca",
    "Global (Everything)": "all"
}

# User Input in the sidebar
with st.sidebar:
    st.header("Search Settings")
    query = st.text_input("Topic", placeholder="e.g. Technology, AI, Hitachi")
    
    # New Country Selection Feature
    selected_country = st.selectbox("Select Country", list(countries.keys()))
    country_code = countries[selected_country]
    
    api_key = "ea01384660a7413396d05f56dedb569d"

if query:
    # Logic to change the URL based on country selection
    if country_code == "all":
        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={api_key}"
    else:
        # 'top-headlines' works best for specific country filters
        url = f"https://newsapi.org/v2/top-headlines?q={query}&country={country_code}&apiKey={api_key}"
    
    with st.spinner(f'Searching {selected_country} for "{query}"...'):
        response = requests.get(url)
        data = response.json()

    if data.get("articles"):
        articles = data["articles"]
        st.success(f"Found {len(articles)} articles!")

        for art in articles[:12]: 
            with st.container():
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    img_url = art.get("urlToImage")
                    if img_url:
                        st.image(img_url, use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/400x250.png?text=No+Image", use_container_width=True)
                
                with col2:
                    st.subheader(art["title"])
                    st.caption(f"Source: {art['source']['name']} | Published: {art['publishedAt'][:10]}")
                    st.write(art["description"])
                    st.markdown(f"[🔗 Read Full Article]({art['url']})")
                
                st.divider()
    else:
        st.warning("No articles found. Try removing the country filter or changing keywords.")
else:
    st.info("👈 Type a topic (like 'Economy') in the sidebar to fetch the latest news!")

