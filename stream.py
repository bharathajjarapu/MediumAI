import streamlit as st
from research import research_link
from blogger import write_blog
from medium import upload_medium

def main():
    st.set_page_config(page_title="AI Blog Generator", page_icon="📝")
    st.title("AI Blog Generator")

    # API key inputs
    groq_api_key = st.text_input("Enter your Groq API Key:", type="password")
    medium_api_token = st.text_input("Enter your Medium API Token:", type="password")
    unsplash_api_key = st.text_input("Enter your Unsplash API Key:", type="password")

    if not groq_api_key or not medium_api_token:
        st.warning("Please enter both API keys to proceed.")
        return

    # User input
    query = st.text_input("Enter a topic for research:", "Latest developments in AI language models")

    if st.button("Generate and Publish Blog"):
        try:
            # Research
            with st.spinner("Researching..."):
                research_summary = research_link(query)
            st.success("Research completed!")

            # Write blog
            with st.spinner("Generating blog content..."):
                blog_content = write_blog(query, research_summary, groq_api_key, unsplash_api_key)
            st.success("Blog content generated!")

            # Upload to Medium
            with st.spinner("Uploading to Medium..."):
                medium_url = upload_medium(query, blog_content, medium_api_token)
            st.success("Upload completed!")

            # Display result
            st.success(f"Blog post published successfully!")
            st.markdown(f"[View Blog Post on Medium]({medium_url})")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
