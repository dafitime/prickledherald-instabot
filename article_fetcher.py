import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import random

PRICKLED_HERALD_RSS = "https://prickledherald.com/feed/"
IMAGE_SAVE_PATH = "latest_article.jpg"

def fetch_articles():
    """Fetches the latest articles from Prickled Herald's RSS feed."""
    response = requests.get(PRICKLED_HERALD_RSS)
    
    if response.status_code != 200:
        print(f"ERROR: Failed to fetch RSS feed. Status code: {response.status_code}")
        return []

    # Parse the RSS feed
    root = ET.fromstring(response.text)
    articles = []

    # Find all <item> elements (list of articles)
    for item in root.findall(".//item"):
        link_element = item.find("link")
        title_element = item.find("title")

        article_url = link_element.text if link_element is not None else None
        title = title_element.text if title_element is not None else "Untitled"

        if article_url:
            articles.append({"title": title, "url": article_url})

    return articles

def fetch_latest_article():
    """Fetches the latest article (first entry from fetch_articles)."""
    articles = fetch_articles()
    if articles:
        return extract_article_details(articles[0]["url"])
    return None, None

def extract_article_hashtags(soup):
    """Extracts hashtags from the article's metadata or body text."""
    hashtags = []

    # Try extracting from meta tags (common in WordPress)
    meta_tags = soup.find_all("meta", {"property": "article:tag"})
    for tag in meta_tags:
        if tag.get("content"):
            hashtags.append("#" + tag["content"].replace(" ", ""))  # Format as hashtags

    # If no meta tags found, check for manually written hashtags in the article
    body_text = soup.get_text().split()  # Split into words
    for word in body_text:
        if word.startswith("#") and len(word) > 2:
            hashtags.append(word)

    return list(set(hashtags))  # Remove duplicates

def generate_relevant_hashtags(title, existing_hashtags):
    """Generates hashtags based on the title, filling in if there are less than 10."""
    base_hashtags = ["#news", "#satire", "#comedynews", "#trending", "#meme", "#funnynews"]

    # Extract keywords from title
    words = title.lower().split()
    words = [word.strip(",.!?()") for word in words if len(word) > 3]

    # Convert words into hashtags
    generated_hashtags = ["#" + word for word in words if "#" + word not in existing_hashtags]

    # Fill up to 10 hashtags
    final_hashtags = existing_hashtags + generated_hashtags[:10 - len(existing_hashtags)]

    # If still less than 10, add base hashtags
    while len(final_hashtags) < 10:
        final_hashtags.append(random.choice(base_hashtags))

    return " ".join(list(set(final_hashtags[:10])))  # Return unique 10 hashtags

def extract_article_details(article_url):
    """Extracts title, image, and hashtags from the article."""
    response = requests.get(article_url)
    if response.status_code != 200:
        print(f"ERROR: Failed to fetch article page. Status code: {response.status_code}")
        return None, None, None, None

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

    # Extract featured image (WordPress usually puts it inside <meta property="og:image">)
    image_tag = soup.find("meta", property="og:image")
    img_url = image_tag["content"] if image_tag else None

    # Extract or generate hashtags
    existing_hashtags = extract_article_hashtags(soup)
    hashtags = generate_relevant_hashtags(title, existing_hashtags)

    print(f"DEBUG: Title = {title}")
    print(f"DEBUG: Image URL = {img_url}")
    print(f"DEBUG: Hashtags = {hashtags}")

    return title, img_url, hashtags, None

def download_image(image_url, save_path=IMAGE_SAVE_PATH):
    """Downloads an image from a URL and saves it locally."""
    if not image_url:
        print("ERROR: No image URL provided")
        return None

    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"DEBUG: Image saved as {save_path}")
        return save_path
    else:
        print("ERROR: Failed to download image")
        return None
