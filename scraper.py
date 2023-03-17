import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def download_3d_objects(url):
    # Get the HTML content of the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the links in the HTML content
    links = [link.get('href') for link in soup.find_all('a')]

    # Filter the links to include only those that point to 3D objects
    filtered_links = [link for link in links if link.endswith(('.glb', '.obj', '.ply'))]

    # Download the 3D objects
    for link in filtered_links:
        # Check if the URL has a protocol scheme and prepend "http://" if it doesn't
        parsed_url = urlparse(link)
        if not parsed_url.scheme:
            link = "http://" + link

        filename = os.path.basename(link)
        response = requests.get(link)
        with open(filename, 'wb') as f:
            f.write(response.content)

        print(f'Downloaded {filename}')

        # Recursively download 3D objects from linked pages
        if link.startswith('http'):
            download_3d_objects(link)

# Example usage: download 3D objects from a webpage recursively
download_3d_objects('http://example.com/3d-objects/')

