import streamlit as st
import requests
from fpdf import FPDF
import io
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="Deepak News Hub", page_icon="📰", layout="wide")

st.title("📰 Deepak News Hub")
st.markdown("---")

countries = {"Global": "all", "India": "in", "USA": "us", "UK": "gb"}

with st.sidebar:
    st.header("Search Settings")
    query = st.text_input("Topic", placeholder="e.g. Technology, Tata, Copper")
    selected_country = st.selectbox("Select Country", list(countries.keys()))
    country_code = countries[selected_country]
    # This is your active API Key
    api_key = "ea01384660a7413396d05f56dedb569d"

# 2. PDF Function
def create_pdf(articles, topic):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Deepak News Report: {topic.upper()}", ln=True, align='C')
    pdf.ln(10)
    for art in articles[:10]:
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 10, txt=art['title'].encode('latin-1', 'ignore').decode('latin-1'))
        pdf.set_font("Arial", '', 10)
        pdf.write(5, f"Source: {art['source']['name']} | URL: {art['url']}\n")
        pdf.ln(8)
    return pdf.output(dest='S').encode('latin-1')

# 3. Fetching News
if query:
    # Use "Everything" for specific words like 'copper' as 'top-headlines' is often empty
    if country_code == "all" or query.lower() == "copper":
        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={api_key}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?q={query}&country={country_code}&apiKey={api_key}"
    
    with st.spinner('Checking for news...'):
        r = requests.get(url)
        data = r.json()

    if data.get("articles") and len(data["articles"]) > 0:
        articles = data["articles"]
        
        # Sidebar Download Button
        pdf_bytes = create_pdf(articles, query)
        st.sidebar.download_button(label="📥 Download PDF Report", data=pdf_bytes, file_name="news_report.pdf")

        # Display News
        for art in articles[:10]:
            col1, col2 = st.columns([1, 4])
            with col1:
                if art.get("urlToImage"):
                    st.image(art["urlToImage"])
                else:
                    st.image("https://via.placeholder.com/150")
            with col2:
                st.subheader(art["title"])
                st.write(art["description"])
                st.markdown(f"[Read Article]({art['url']})")
            st.divider()
    else:
        st.error(f"No results found for '{query}' in {selected_country}. Try setting Country to 'Global'.")
else:
    st.info("Please type a topic in the sidebar and press Enter.")
