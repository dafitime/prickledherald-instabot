import requests
import json
from PIL import Image
import os

# Replace with your credentials
ACCESS_TOKEN = "EAAQZARc4eCukBOy8WdI79WdhVMD3zlbFL4Rv8QWFyqSZAB7WGYZAPcL9gIDg9VkHZAsey1Gqj5XUSZA4yLaZBCmOn4eqiAczBgJPtK0WK9uddZAXBZAZAJx2PZBPFZCPPjZCy08NB8BT5DZBWsFswZAzNLZAzo2vX6P4if5yj0ZBanDvsR9LWEgqO470cCveY4GYGfO79pMPodt4rwZDZD"
INSTAGRAM_ACCOUNT_ID = "17841461793452461"
IMGUR_CLIENT_ID = "1af97a9366675ac"  # Get from https://api.imgur.com/oauth2/addclient

def convert_image(image_path):
    """Ensures the image is a valid JPEG or PNG before uploading to Imgur."""
    img = Image.open(image_path)
    converted_path = "converted_instagram_post.jpg"
    
    # Convert image to RGB and save it as a valid JPEG
    img.convert("RGB").save(converted_path, "JPEG")
    
    return converted_path

def upload_to_imgur(image_path):
    """Uploads an image to Imgur and returns a publicly accessible URL."""
    image_path = convert_image(image_path)  # Convert before upload

    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    
    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        response = requests.post(
            "https://api.imgur.com/3/upload",
            headers=headers,
            files=files
        )
    
    data = response.json()
    if response.status_code == 200 and "data" in data:
        imgur_url = data["data"]["link"]
        print(f"✅ Image uploaded to Imgur: {imgur_url}")
        return imgur_url
    else:
        print(f"❌ ERROR: Failed to upload image to Imgur: {data}")
        return None

def upload_to_instagram(image_url, caption=""):
    """Uploads an image to Instagram via Facebook Graph API."""
    
    # Step 1: Send the Image URL to Instagram's Media Container
    upload_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
    params = {
        "image_url": image_url,  # ✅ Use the public URL from Imgur
        "caption": caption,
        "access_token": ACCESS_TOKEN,
    }

    response = requests.post(upload_url, params=params)
    result = response.json()

    if "id" not in result:
        print(f"❌ ERROR: Failed to upload image to Instagram: {result}")
        return None

    media_id = result["id"]
    print(f"✅ Uploaded Image ID: {media_id}")

    # Step 2: Publish the uploaded media to Instagram
    publish_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_params = {
        "creation_id": media_id,
        "access_token": ACCESS_TOKEN,
    }

    publish_response = requests.post(publish_url, data=publish_params)
    publish_result = publish_response.json()

    if "id" in publish_result:
        print("✅ Successfully posted to Instagram!")
        return publish_result["id"]
    else:
        print(f"❌ ERROR: Failed to publish media: {publish_result}")
        return None