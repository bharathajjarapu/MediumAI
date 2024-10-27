import sys
from research import research_link
from blogger import write_blog
from medium import upload_medium

def main():
    print("AI Blog Generator")
    print("-----------------")

    # API key inputs
    groq_api_key = input("Enter your Groq API Key: ")
    medium_api_token = input("Enter your Medium API Token: ")

    if not groq_api_key or not medium_api_token:
        print("Error: Please enter both API keys to proceed.")
        return

    # User input
    query = input("Enter a topic for research: ") or "Latest developments in AI language models"

    try:
        # Research
        print("Researching...")
        research_summary = research_link(query)
        print("Research completed!")

        # Write blog
        print("Generating blog content...")
        blog_content = write_blog(query, research_summary, groq_api_key)
        print("Blog content generated!")

        print("\nGenerated Blog Content:")
        print(blog_content)

        # Upload to Medium
        print("\nUploading to Medium...")
        medium_url = upload_medium(query, blog_content, medium_api_token)
        print("Upload completed!")

        # Display result
        print(f"\nBlog post published successfully!")
        print(f"View Blog Post on Medium: {medium_url}")

    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()