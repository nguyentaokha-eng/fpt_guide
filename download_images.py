#!/usr/bin/env python3
"""
Script to download sample images for FPT Guide static lists.
Run: python download_images.py
"""
import os
import urllib.request
import ssl

# Create SSL context to avoid certificate issues
ssl._create_default_https_context = ssl._create_unverified_context

# Image URLs from Unsplash (free to use)
FOOD_IMAGES = {
    1: "https://images.unsplash.com/photo-1529042410759-befb1204b468?w=640",
    2: "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=640",
    3: "https://images.unsplash.com/photo-1562967968-56c2805f9793?w=640",
    4: "https://images.unsplash.com/photo-1565895405138-6c3a1555da6a?w=640",
    5: "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=640",
    6: "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=640",
    7: "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=640",
    8: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=640",
    9: "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=640",
    10: "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=640",
}

LIVING_IMAGES = {
    1: "https://images.unsplash.com/photo-1554412933-514a83d2f3c8?w=640",
    2: "https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=640",
    3: "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=640",
    4: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=640",
    5: "https://images.unsplash.com/photo-1560185893-a55cbc8c57e8?w=640",
    6: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=640",
    7: "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=640",
    8: "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=640",
    9: "https://images.unsplash.com/photo-1560185007-cde436f6a4d0?w=640",
    10: "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=640",
}

COMMENT_IMAGES = {
    1: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=200",
    2: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200",
    3: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200",
    4: "https://images.unsplash.com/photo-1527980965255-d3b416303d12?w=200",
    5: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200",
}

def download_image(url, filepath):
    """Download an image from URL to filepath."""
    try:
        print(f"Downloading: {url}")
        urllib.request.urlretrieve(url, filepath)
        print(f"Saved: {filepath}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Food images
    food_dir = os.path.join(base_dir, "static", "image", "food")
    print(f"\n=== Downloading Food Images to {food_dir} ===")
    for idx, url in FOOD_IMAGES.items():
        filepath = os.path.join(food_dir, f"{idx}.jpg")
        download_image(url, filepath)
    
    # Living images
    living_dir = os.path.join(base_dir, "static", "image", "living")
    print(f"\n=== Downloading Living Images to {living_dir} ===")
    for idx, url in LIVING_IMAGES.items():
        filepath = os.path.join(living_dir, f"{idx}.jpg")
        download_image(url, filepath)
    
    # Comment images
    comments_dir = os.path.join(base_dir, "static", "image", "comments")
    print(f"\n=== Downloading Comment Images to {comments_dir} ===")
    for idx, url in COMMENT_IMAGES.items():
        filepath = os.path.join(comments_dir, f"{idx}.jpg")
        download_image(url, filepath)
    
    print("\n=== Done! ===")

if __name__ == "__main__":
    main()
