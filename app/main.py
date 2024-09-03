import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(
        page_title="ConnectPro - Instant Email generator!!",
        page_icon="📧",
        layout="wide"
    )

    st.title("📧 ConnectPro - Instant Email generator!!")

    st.sidebar.header("Configuration")
    url_input = st.sidebar.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-35436")
    submit_button = st.sidebar.button("Generate Email")

    if submit_button:
        if url_input:
            with st.spinner("Processing..."):
                try:
                    loader = WebBaseLoader([url_input])
                    page_content = loader.load().pop().page_content
                    data = clean_text(page_content)

                    portfolio.load_portfolio()

                    jobs = llm.extract_jobs(data)
                    
                    if jobs:
                        for job in jobs:
                            role = job.get('role', 'Not specified')
                            title = job.get('title', 'No title')
                            skills = job.get('skills', [])
                            description = job.get('description', 'No description')
                            
                            links = portfolio.query_links(skills)
                            
                            email = llm.write_mail(job, links)
                            
                            # Display job details and generated email
                            st.write(f"**Role:** {role}")
                            st.write(f"**Description:** {description}")
                            st.write(f"**Skills:** {', '.join(skills)}")
                            st.write("### Generated Email:")
                            st.code(email, language='markdown')
                    else:
                        st.warning("No job postings found in the provided URL.")
                except Exception as e:
                    st.error(f"An Error Occurred: {e}")
        else:
            st.warning("Please enter a URL before submitting.")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
