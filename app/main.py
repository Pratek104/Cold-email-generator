import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    # Sidebar for navigation and description
    with st.sidebar:
        st.image("logo.jpg", width=150)  
        st.title("Cold Mail Generator 📧")
        st.markdown("""
        **Welcome to the Cold Email Generator!**  
        This tool allows you to quickly generate professional cold emails for job opportunities based on job descriptions from websites.
        \n**How to use it:**
        1. Enter the URL of the job posting.
        2. Click 'Submit' to generate an email draft.
        3. Get the generated email and tailor it further to your needs.
        """)
        st.write("Powered by AI & Streamlit")

    # Main page layout
    st.title("Cold Mail Generator 📧")
    st.markdown("Generate personalized cold emails for job opportunities in just a few clicks!")
    
    # Input field for URL and submission
    url_input = st.text_input("Enter a job posting URL", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Generate Email")

    # Processing input and generating email
    if submit_button:
        with st.spinner("Fetching job details..."):
            try:
                # Load the web data
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)

                # Load portfolio and extract job details
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                st.success("Job details fetched successfully! Generating email...")

                # Display generated emails
                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    
                    # Displaying each email
                    st.subheader(f"Generated Email for {job.get('role', 'the job')}")
                    st.code(email, language='markdown')
                    
            except Exception as e:
                st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    # Initialize the Chain and Portfolio instances
    chain = Chain()
    portfolio = Portfolio()

    # Streamlit page configuration

    st.set_page_config(
        layout="wide", 
        page_title="AI Cold Email Generator", 
        page_icon="📧", 
        initial_sidebar_state="expanded"
    )
    
    # Run the app
    create_streamlit_app(chain, portfolio, clean_text)
