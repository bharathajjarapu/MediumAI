from groq import Groq
import requests

UNSPLASH_BASE_URL = "https://api.unsplash.com"

def write_blog(query: str, summary: str, groq_api_key: str, unsplash_api_key: str) -> str:
    client = Groq(api_key=groq_api_key)

    prompt = f"""Write a Captivating blog post with no links, use plain text only based on the following query and research summary:

    Query: {query}
    Research Summary: {summary}

    Do not use Summary if it doesn't relate to the query.

    Your blog post should follow this structure:
    1. Attention-grabbing title
    2. Engaging introduction that hooks the reader
    3. Main body with 3-4 key points, each in its own section
    4. Real-world examples or case studies to illustrate points
    5. Discussion of potential implications or future developments
    6. Conclusion that summarizes key takeaways and invites reader engagement

    Use a conversational yet professional tone, and include:
    - Relevant statistics or data points
    - Quotes from experts (you can create these based on the summary)
    - Subheadings for each main section
    - A very short conclusion.

    Make sure to use all the possible formatting styles mentioned in the prompt.

    Format the post using Markdown, including:
    - # for the main title
    - ## for section headings
    - *italic* and **bold** for emphasis
    - > for blockquotes
    - - for bullet points
    - use curly brackets for code snippets

    Aim for a length of about 1000-1500 words.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
        )
        blog_content = chat_completion.choices[0].message.content

        blog_content_with_images = add_images_to_blog(query, blog_content, unsplash_api_key)

        return blog_content_with_images
    except Exception as e:
        raise Exception(f"Error generating blog content: {str(e)}")


def add_images_to_blog(query: str, blog_content: str, unsplash_api_key: str) -> str:

    paragraphs = blog_content.split("\n\n")
    num_paragraphs = len(paragraphs)

    num_images = max(3, min(num_paragraphs // 3, 10))
    image_urls = search_unsplash_images(query, num_images, unsplash_api_key)

    if image_urls:
        new_content = paragraphs[0] + "\n\n"
        if len(image_urls) > 0:
            new_content += f"![Main image related to {query}]({image_urls[0]})\n\n"

        image_index = 1
        for i, paragraph in enumerate(paragraphs[1:]):
            new_content += paragraph + "\n\n"
            if (i + 1) % (num_paragraphs // num_images) == 0 and image_index < len(image_urls):
                new_content += f"![Image related to {query}]({image_urls[image_index]})\n\n"
                image_index += 1

        return new_content
    else:
        return blog_content


def search_unsplash_images(query: str, num_images: int, unsplash_api_key: str) -> list:
    url = f"{UNSPLASH_BASE_URL}/search/photos"
    params = {
        "query": query,
        "per_page": num_images,
        "client_id": unsplash_api_key,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    image_urls = [result["urls"]["regular"] for result in data["results"]]
    return image_urls