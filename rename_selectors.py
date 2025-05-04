#!/usr/bin/env python3
import os
import re
import random
import string
import sys

# Function to generate a random name
def generate_random_name(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Dictionary to store original selector to random name mapping
selector_map = {}

# Function to extract all stui-* selectors from CSS files
def extract_selectors(css_file):
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all .stui-* selectors
    selectors = re.findall(r'\.stui-[a-zA-Z0-9_-]+(?:__[a-zA-Z0-9_-]+)?', content)
    
    # Add to mapping if not already there
    for selector in selectors:
        if selector not in selector_map:
            # Remove the leading dot for the key
            selector_key = selector[1:]
            selector_map[selector_key] = generate_random_name()
    
    return selector_map

# Function to update CSS files with new selectors
def update_css_file(css_file):
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all occurrences of selectors
    for old_selector, new_name in selector_map.items():
        # Replace the selector with dot
        content = content.replace(f'.{old_selector}', f'.{new_name}')
    
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)

# Function to update HTML files with new class names
def update_html_file(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace class attributes
    for old_selector, new_name in selector_map.items():
        # Replace class="stui-*" with class="new_name"
        content = re.sub(r'class=(["\'])(.*?)' + old_selector + r'(.*?)(["\'])', 
                         r'class=\1\2' + new_name + r'\3\4', content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

# Function to update JavaScript files that might reference these classes
def update_js_file(js_file):
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all occurrences of selectors in JS
    for old_selector, new_name in selector_map.items():
        # Replace various JS patterns that might reference the class
        content = content.replace(f'".{old_selector}"', f'".{new_name}"')
        content = content.replace(f"'.{old_selector}'", f"'.{new_name}'")
        content = content.replace(f'"{old_selector}"', f'"{new_name}"')
        content = content.replace(f"'{old_selector}'", f"'{new_name}'")
    
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(content)

# Main function
def main():
    # Directory containing CSS files
    css_dir = './statics/css'
    html_dir = './template/default/html-es'
    js_dir = './statics/js'
    
    # Process all CSS files to build the selector map
    for root, dirs, files in os.walk(css_dir):
        for file in files:
            if file.endswith('.css'):
                css_file = os.path.join(root, file)
                extract_selectors(css_file)
    
    # Print the mapping for reference
    print("Selector mapping:")
    for old, new in selector_map.items():
        print(f"{old} -> {new}")
    
    # Update CSS files
    for root, dirs, files in os.walk(css_dir):
        for file in files:
            if file.endswith('.css'):
                css_file = os.path.join(root, file)
                print(f"Updating CSS file: {css_file}")
                update_css_file(css_file)
    
    # Update HTML files
    for root, dirs, files in os.walk(html_dir):
        for file in files:
            if file.endswith('.html'):
                html_file = os.path.join(root, file)
                print(f"Updating HTML file: {html_file}")
                update_html_file(html_file)
    
    # Update JS files
    for root, dirs, files in os.walk(js_dir):
        for file in files:
            if file.endswith('.js'):
                js_file = os.path.join(root, file)
                print(f"Updating JS file: {js_file}")
                update_js_file(js_file)
    
    print("Selector renaming complete!")

if __name__ == "__main__":
    main()

