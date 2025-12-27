import streamlit as st
import requests
from fpdf import FPDF
from datetime import datetime, timedelta

# 1. Page Config
st.set_page_config(page_title="Deepak News Hub", page_icon="📰", layout="wide")

st.title("📰 Deepak News Hub")
st.write(f"Today's Date: {datetime.now().strftime('%Y-%m-%d')}")
st.markdown("---")

# 2. Date Calculation (Current Date - 30 Days)
today = datetime.now()
thirty_days_ago = today - timedelta(days=30)
from_date = thirty_days_ago.strftime('%Y-%m-%d')

countries = {"Global": "all", "India": "in", "USA": "us", "UK": "gb"}

with st.sidebar:
    st.header("Search Settings")
    query = st.text_input("Topic", placeholder="e.g. Hitachi, Copper Prices")
    selected_country = st.selectbox("Select Country", list(countries.keys()))
    country_code = countries[selected_country]
    api_key = "ea01384660a7413396d05f56dedb569d"
    
    st.info(f"Searching news from: {from_date}")

# 3. PDF Function
def create_pdf(articles, topic):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"News Report: {topic.upper()}", ln=True, align='C')
    pdf.ln(10)
    for art in articles[:10]:
        pdf.set_font("Arial", 'B', 11)
        # Handle special characters for PDF
        title = art['title'].encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 10, txt=title)
        pdf.set_font("Arial", '', 9)
        pdf.write(5, f"Source: {art['source']['name']} | Date: {art['publishedAt'][:10]}\n")
        pdf.write(5, f"Link: {art['url']}\n")
        pdf.ln(8)
    return pdf.output(dest='S').encode('latin-1')

# 4. Fetching News
if query:
    # Use 'everything' for general topics to allow the 30-day date filter
    if country_code == "all" or len(query) > 0:
        url = f"https://newsapi.org/v2/everything?q={query}&from={from_date}&sortBy=publishedAt&apiKey={api_key}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?q={query}&country={country_code}&apiKey={api_key}"
    
    with st.spinner('Scanning global news...'):
        r = requests.get(url)
        data = r.json()

    if data.get("articles"):
        articles = data["articles"]
        
        # Download Button in Sidebar
        pdf_bytes = create_pdf(articles, query)
        st.sidebar.download_button(
            label="📥 Download 30-Day Report",
            data=pdf_bytes,
            file_name=f"{query}_report.pdf",
            mime="application/pdf"
        )

        # Main Display
        for art in articles[:10]:
            col1, col2 = st.columns([1, 4])
            with col1:
                img = art.get("urlToImage") if art.get("urlToImage") else "https://via.placeholder.com/150"
                st.image(img, use_container_width=True)
            with col2:
                st.subheader(art["title"])
                st.caption(f"{art['source']['name']} | {art['publishedAt'][:10]}")
                st.write(art["description"])
                st.markdown(f"[🔗 Read Full Article]({art['url']})")
            st.divider()
    else:
        st.error("No articles found for this period. Try a different topic.")
else:
    st.info("👈 Enter a topic in the sidebar and press Enter to see results.")
