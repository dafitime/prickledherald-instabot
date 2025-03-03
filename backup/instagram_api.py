import requests
import json
import os

# Load credentials from environment variables
ACCESS_TOKEN = "EAAQZARc4eCukBOy8WdI79WdhVMD3zlbFL4Rv8QWFyqSZAB7WGYZAPcL9gIDg9VkHZAsey1Gqj5XUSZA4yLaZBCmOn4eqiAczBgJPtK0WK9uddZAXBZAZAJx2PZBPFZCPPjZCy08NB8BT5DZBWsFswZAzNLZAzo2vX6P4if5yj0ZBanDvsR9LWEgqO470cCveY4GYGfO79pMPodt4rwZDZD"
INSTAGRAM_ACCOUNT_ID = "17841461793452461"

# Graph API URLs
INSTAGRAM_API_URL = "https://graph.facebook.com/v22.0"
PUBLISH_URL = f"{INSTAGRAM_API_URL}/{INSTAGRAM_ACCOUNT_ID}/media"

def upload_photo(image_path, caption=""):
    """Uploads a photo to Instagram using the Graph API."""
    try:
        with open(image_path, "rb") as image_file:
            files = {"source": image_file}
            data = {
                "caption": caption,
                "access_token": ACCESS_TOKEN,
            }

            print("🚀 Uploading image to Instagram...")
            response = requests.post(PUBLISH_URL, files=files, data=data)
            response_data = response.json()

            if "id" in response_data:
                print(f"✅ Successfully uploaded image. Media ID: {response_data['id']}")
                return response_data["id"]
            else:
                print(f"❌ Error uploading image: {response_data}")
                return None

    except Exception as e:
        print(f"❌ Exception while uploading to Instagram: {e}")
        return None
