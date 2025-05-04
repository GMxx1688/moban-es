#!/usr/bin/env python3
import os
import re
import random
import string

# Function to generate a random class name
def generate_random_name(length=8):
    return 'cx_' + ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

# Function to extract CSS selectors from a CSS file
def extract_css_selectors(css_file):
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all CSS selectors (classes starting with .)
    selectors = re.findall(r'\.([a-zA-Z0-9_-]+)', content)
    return list(set(selectors))

# Function to create a mapping of old selectors to new random names
def create_selector_mapping(selectors):
    mapping = {}
    for selector in selectors:
        # Skip numeric selectors and common utility classes
        if selector.isdigit() or selector in ['active', 'disabled', 'hide', 'show', 'fade', 'in']:
            continue
        
        # Generate a unique random name for this selector
        new_name = generate_random_name()
        while new_name in mapping.values():
            new_name = generate_random_name()
        
        mapping[selector] = new_name
    
    return mapping

# Function to update CSS files with new selector names
def update_css_file(css_file, mapping):
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all occurrences of old selectors with new ones
    for old_selector, new_selector in mapping.items():
        content = re.sub(r'\.{}\b'.format(re.escape(old_selector)), '.{}'.format(new_selector), content)
    
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)

# Function to update HTML files with new selector names
def update_html_file(html_file, mapping):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace class attributes
    for old_selector, new_selector in mapping.items():
        # Replace class="selector" or class="... selector ..."
        content = re.sub(r'class=(["\'])(.*?)\b{}\b(.*?)(["\'])'.format(re.escape(old_selector)), 
                         lambda m: 'class={}{}{}{}{}'\
                         .format(m.group(1), m.group(2), new_selector, m.group(3), m.group(4)), 
                         content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

# Function to update JS files with new selector names
def update_js_file(js_file, mapping):
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace selectors in JS code (various patterns)
    for old_selector, new_selector in mapping.items():
        # Replace ".selector" (as a string)
        content = re.sub(r'[\'"]\.{}\b[\'"]'.format(re.escape(old_selector)), 
                         '".{}"'.format(new_selector), content)
        
        # Replace $(".selector") (jQuery selector)
        content = re.sub(r'\$\([\'"]\.{}\b[\'"]\)'.format(re.escape(old_selector)), 
                         '$(".{}")'.format(new_selector), content)
        
        # Replace querySelector(".selector")
        content = re.sub(r'querySelector\([\'"]\.{}\b[\'"]\)'.format(re.escape(old_selector)), 
                         'querySelector(".{}")'.format(new_selector), content)
        
        # Replace querySelectorAll(".selector")
        content = re.sub(r'querySelectorAll\([\'"]\.{}\b[\'"]\)'.format(re.escape(old_selector)), 
                         'querySelectorAll(".{}")'.format(new_selector), content)
    
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(content)

# Main function
def main():
    # Paths
    css_dir = './statics/css'
    template_dir = './template'
    js_dir = './statics/js'
    
    # Get all CSS files
    css_files = [os.path.join(css_dir, f) for f in os.listdir(css_dir) if f.endswith('.css')]
    
    # Extract all selectors from CSS files
    all_selectors = []
    for css_file in css_files:
        all_selectors.extend(extract_css_selectors(css_file))
    
    # Create mapping of old selectors to new random names
    mapping = create_selector_mapping(all_selectors)
    
    # Save mapping to a file for reference
    with open('selector_mapping.txt', 'w', encoding='utf-8') as f:
        for old, new in mapping.items():
            f.write(f"{old} -> {new}\n")
    
    # Update CSS files
    for css_file in css_files:
        update_css_file(css_file, mapping)
    
    # Update HTML files
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                html_file = os.path.join(root, file)
                update_html_file(html_file, mapping)
    
    # Update JS files
    for root, dirs, files in os.walk(js_dir):
        for file in files:
            if file.endswith('.js'):
                js_file = os.path.join(root, file)
                update_js_file(js_file, mapping)
    
    print("Selector renaming completed successfully!")

if __name__ == "__main__":
    main()

