#!/usr/bin/env python3
import os
import re

# Breadcrumb HTML template
BREADCRUMB_HTML = '''
<div class="cx_breadcrumb">
    <div class="container">
        <ul class="cx_breadcrumb__list">
            <li class="cx_breadcrumb__item"><a href="{$maccms.path}">首页</a></li>
            {$breadcrumb_items}
        </ul>
    </div>
</div>
'''

# Breadcrumb CSS
BREADCRUMB_CSS = '''
/* Breadcrumb Navigation */
.cx_breadcrumb {
    padding: 10px 0;
    background-color: #f8f8f8;
    margin-bottom: 15px;
    border-radius: 4px;
}
.cx_breadcrumb__list {
    margin: 0;
    padding: 0;
    list-style: none;
    display: flex;
    flex-wrap: wrap;
}
.cx_breadcrumb__item {
    display: inline-flex;
    align-items: center;
    font-size: 14px;
    color: #666;
}
.cx_breadcrumb__item:not(:last-child)::after {
    content: ">";
    margin: 0 8px;
    color: #ccc;
}
.cx_breadcrumb__item a {
    color: #666;
    text-decoration: none;
}
.cx_breadcrumb__item a:hover {
    color: #ff5f00;
}
.cx_breadcrumb__item:last-child {
    color: #ff5f00;
}
'''

# Function to add breadcrumb CSS to the main CSS file
def add_breadcrumb_css():
    css_file = './statics/css/stui_default.css'
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add breadcrumb CSS at the end of the file
    if 'cx_breadcrumb' not in content:
        content += '\n' + BREADCRUMB_CSS
    
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)

# Function to add breadcrumb HTML to template files
def add_breadcrumb_to_templates():
    # Define the files and their breadcrumb items
    template_breadcrumbs = {
        './template/default/html-es/vod/type.html': '<li class="cx_breadcrumb__item">{$obj.type_name}</li>',
        './template/default/html-es/vod/detail.html': '<li class="cx_breadcrumb__item"><a href="{:mac_url_type($obj.type_id)}">{$obj.type.type_name}</a></li><li class="cx_breadcrumb__item">{$obj.vod_name}</li>',
        './template/default/html-es/vod/play.html': '<li class="cx_breadcrumb__item"><a href="{:mac_url_type($obj.type_id)}">{$obj.type.type_name}</a></li><li class="cx_breadcrumb__item"><a href="{:mac_url_detail($obj)}">{$obj.vod_name}</a></li><li class="cx_breadcrumb__item">{$obj.player_info.show}</li>',
        './template/default/html-es/vod/search.html': '<li class="cx_breadcrumb__item">搜索 "{$param.wd}"</li>',
        './template/default/html-es/topic/index.html': '<li class="cx_breadcrumb__item">专题</li>',
        './template/default/html-es/topic/detail.html': '<li class="cx_breadcrumb__item"><a href="{:mac_url(\'topic/index\')}">专题</a></li><li class="cx_breadcrumb__item">{$obj.topic_name}</li>',
        './template/default/html-es/gbook/index.html': '<li class="cx_breadcrumb__item">留言反馈</li>',
    }
    
    # Add breadcrumb to each template file
    for template_file, breadcrumb_items in template_breadcrumbs.items():
        if os.path.exists(template_file):
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace breadcrumb items placeholder
            breadcrumb_html = BREADCRUMB_HTML.replace('{$breadcrumb_items}', breadcrumb_items)
            
            # Find the position to insert the breadcrumb (after the head include)
            head_pattern = r'{include file="block/head"}'
            match = re.search(head_pattern, content)
            
            if match:
                insert_pos = match.end()
                content = content[:insert_pos] + '\n' + breadcrumb_html + content[insert_pos:]
                
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Added breadcrumb to {template_file}")
            else:
                print(f"Could not find insertion point in {template_file}")

# Main function
def main():
    # Add breadcrumb CSS
    add_breadcrumb_css()
    
    # Add breadcrumb HTML to templates
    add_breadcrumb_to_templates()
    
    print("Breadcrumb navigation added successfully!")

if __name__ == "__main__":
    main()

