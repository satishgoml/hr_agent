import requests

class SocialMediaPoster:
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def post_linkedin(self, title, image_url, text_content):
        endpoint = f"{self.api_base_url}/post_linkedin/"
        payload = {
            "title": title,
            "image_url": image_url,
            "text_content": text_content
        }
        
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print(f"LinkedIn post successful! Status code: {response.status_code}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

# Example usage
if __name__ == "__main__":
    api_base_url = "http://54.84.189.207"  # Base URL of the API
    social_media_poster = SocialMediaPoster(api_base_url)
    
    title = "Exciting News!"
    image_url = "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg"
    text_content = """
    We're thrilled to announce our latest product launch!
    
    Discover more about our innovative solutions and how they can benefit you.

    Visit our website for more information and join us in celebrating this milestone!
    """
    
    social_media_poster.post_linkedin(title, image_url, text_content)
