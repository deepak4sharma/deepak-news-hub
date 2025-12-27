import streamlit as st
import requests
from fpdf import FPDF
import io

# Set page title and icon
st.set_page_config(page_title="Deepak News Hub", page_icon="📰", layout="wide")

st.title("📰 Deepak News Hub")
st.markdown("---")

countries = {"India": "in", "USA": "us", "UK": "gb", "Australia": "au", "Global": "all"}

with st.sidebar:
    st.header("Search Settings")
    query = st.text_input("Topic", placeholder="e.g. Hitachi, Supply Chain")
    selected_country = st.selectbox("Select Country", list(countries.keys()))
    country_code = countries[selected_country]
    api_key = "ea01384660a7413396d05f56dedb569d"

def create_pdf(articles, topic):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"News Report: {topic}", ln=True, align='C')
    pdf.ln(10)
    
    for art in articles[:10]:
        pdf.set_font("Arial", 'B', 12)
        # We encode to avoid errors with special characters
        title = art['title'].encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 10, txt=title)
        
        pdf.set_font("Arial", '', 10)
        pdf.write(5, f"Source: {art['source']['name']}\n")
        pdf.write(5, f"Link: {art['url']}\n")
        pdf.ln(10)
    
    return pdf.output(dest='S').encode('latin-1')

if query:
    if country_code == "all":
        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={api_key}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?q={query}&country={country_code}&apiKey={api_key}"
    
    response = requests.get(url)
    data = response.json()

    if data.get("articles"):
        articles = data["articles"]
        
        # Add Download Button to Sidebar
        pdf_data = create_pdf(articles, query)
        st.sidebar.download_button(
            label="📥 Download News Report (PDF)",
            data=pdf_data,
            file_name=f"{query}_news_report.pdf",
            mime="application/pdf"
        )

        for art in articles[:10]:
            col1, col2 = st.columns([1, 3])
            with col1:
                img = art.get("urlToImage")
