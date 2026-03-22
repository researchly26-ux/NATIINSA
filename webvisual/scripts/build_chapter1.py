import json
import os
import shutil
import re
import html

# Directories
src_dir = r"C:\Users\mulug\OneDrive\Desktop\insa\lfh_extract"
out_dir = r"C:\Users\mulug\OneDrive\Desktop\insa\linuxforhackers"
img_out_dir = os.path.join(out_dir, "images")

# Clean existing images
if os.path.exists(img_out_dir):
    shutil.rmtree(img_out_dir)
os.makedirs(img_out_dir, exist_ok=True)

html_head = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Linux Basics for Hackers - Chapter 1</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        ::-webkit-scrollbar { width: 8px; background: #0d1117; }
        ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 4px; }
        h1, h2, h3, h4, h5, h6 { color: #58a6ff; font-weight: 600; margin-top: 1.5em; margin-bottom: 0.5em; }
        h1 { font-size: 2.2em; border-bottom: 1px solid #30363d; padding-bottom: 0.3em; margin-top:0; color: #fff;}
        h2 { font-size: 1.8em; color: #fff; }
        h3 { font-size: 1.5em; }
        h4 { font-size: 1.2em; color: #79c0ff; }
        p { line-height: 1.6; font-size: 1.05rem; }
        ul { margin-bottom: 1.2em; }
        .terminal { font-family: 'Fira Code', monospace; background-color: #010409; padding: 1.2em; border-radius: 8px; border: 1px solid #30363d; color: #79c0ff; overflow-x: auto; margin-bottom: 1.5em; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }
        .sidebar { background-color: #161b22; border-right: 1px solid #30363d; }
        .sidebar-link { display: block; padding: 0.5em 1.2em; color: #8b949e; text-decoration: none; font-size: 0.9em; border-left: 2px solid transparent; transition: all 0.2s; }
        .sidebar-link:hover { color: #58a6ff; background-color: #0d1117; border-left-color: #58a6ff; }
        img { display: block; max-width: 100%; height: auto; border-radius: 6px; border: 1px solid #30363d; margin: 2rem auto; }
        .note { background: rgba(88,166,255,0.1); border-left: 4px solid #58a6ff; padding: 1rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0; font-size: 0.95rem; }
        .glitch { position: relative; color: white; }
        .glitch::before, .glitch::after { content: attr(data-text); position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.8; }
        .glitch::before { left: 2px; text-shadow: -1px 0 red; clip: rect(24px, 550px, 90px, 0); animation: glitch-anim-2 3s infinite linear alternate-reverse; }
        .glitch::after { left: -2px; text-shadow: -1px 0 blue; clip: rect(85px, 550px, 140px, 0); animation: glitch-anim 2.5s infinite linear alternate-reverse; }
        @keyframes glitch-anim { 0% { clip: rect(24px, 9999px, 83px, 0); } 100% { clip: rect(104px, 9999px, 149px, 0); } }
        @keyframes glitch-anim-2 { 0% { clip: rect(11px, 9999px, 110px, 0); } 100% { clip: rect(93px, 9999px, 33px, 0); } }
        .hacker-term { color: #58a6ff; font-family: 'Fira Code', monospace; font-size: 0.9em; padding: 0.1em 0.3em; background: rgba(88,166,255,0.1); border-radius: 4px; }
    </style>
</head>
<body class="flex min-h-screen">
"""

sidebar_html = """
    <!-- Sidebar -->
    <aside class="sidebar w-72 fixed h-full overflow-y-auto">
        <div class="p-6">
            <h2 class="text-xl font-bold text-white mb-2 glitch border-b-0 pb-0" style="font-size: 1.4rem" data-text="Linux for Hackers">Linux for Hackers</h2>
            <p class="text-xs text-[#58a6ff] font-mono mb-8">~$ chapter 1 session</p>
            <nav class="space-y-1" id="toc">
"""

with open(os.path.join(src_dir, 'chapter1.json'), 'r', encoding='utf-8') as f:
    lines = json.load(f)

content_html = """
    <!-- Main Content -->
    <main class="flex-1 ml-72 p-10 lg:p-16 max-w-4xl mx-auto">
        <div class="prose prose-invert max-w-none">
            <h5 class="text-[#58a6ff] font-mono tracking-widest uppercase text-xs mb-2 mt-0">Chapter 1</h5>
            <h1>Getting Started with the Basics</h1>
"""

toc_links = ""
current_section_id = 0
img_idx = 17 
copied_images = set()

def process_text(t):
    t = html.escape(t)
    t = re.sub(r'\b(root|kali|Linux|\/bin|\/etc|\/dev|bash|ls|cd|pwd|cat|find|grep|locate|whereis)\b', r'<span class="hacker-term">\1</span>', t)
    return t

for i, line in enumerate(lines):
    style = line['style']
    text = line['text']
    
    if 'GETTING STARTED WITH THE BASICS' in text and i < 20: 
        continue
        
    if text.startswith('Figure '):
        img_name = f"image{img_idx}.png"
        src_img_path = os.path.join(src_dir, 'images', img_name)
        dst_img_path = os.path.join(img_out_dir, img_name)
        
        # Copy image if it exists
        if os.path.exists(src_img_path):
            shutil.copy2(src_img_path, dst_img_path)
            copied_images.add(img_name)
            
        content_html += f'<img src="images/{img_name}" alt="{text}" class="shadow-lg shadow-blue-500/10" />\n'
        content_html += f'<p class="text-center text-sm text-gray-500 italic mb-6 mt-2">{html.escape(text)}</p>\n'
        img_idx += 1
        continue
        
    if 'Heading' in style or text.isupper():
        level = 2
        if '3' in style or '4' in style: level = 3
        elif '5' in style or '6' in style: level = 4
        
        sec_id = f"section-{current_section_id}"
        current_section_id += 1
        
        clean_text = text.title()
        
        if level <= 3:
            indent = "" if level == 2 else "&nbsp;&nbsp;"
            toc_links += f'<a href="#{sec_id}" class="sidebar-link">{indent}{html.escape(clean_text)}</a>\n'
            
        content_html += f'<h{level} id="{sec_id}">{html.escape(clean_text)}</h{level}>\n'
        
    elif style == 'Normal' and (text.startswith('kali >') or text.startswith('/') or text.startswith('bin\t') or 'find /' in text or 'aircrack-ng' in text and not '--' in text):
        clean_term = html.escape(text).replace("kali &gt;", "<span class='text-green-400'>kali &gt;</span>")
        content_html += f'<div class="terminal">{clean_term}</div>\n'
        
    elif style == 'Body Text' or style == 'Normal':
        if text.strip().isdigit() and len(text.strip()) < 3:
            continue
            
        p_text = process_text(text)
        
        if text.startswith('NO T E') or text.startswith('Note:'):
            content_html += f'<div class="note">{p_text}</div>\n'
        else:
            content_html += f'<p>{p_text}</p>\n'
            
    elif 'List' in style:
        content_html += f'<ul class="list-disc pl-5 text-[#c9d1d9]"><li>{process_text(text)}</li></ul>\n'
        
    else:
        content_html += f'<p>{process_text(text)}</p>\n'

sidebar_html += toc_links + """
            </nav>
        </div>
    </aside>
"""

content_html += """
        </div>
        
        <div class="mt-20 pt-8 border-t border-[#30363d] flex justify-between">
            <div></div>
            <a href="#" class="px-6 py-3 bg-[#161b22] text-[#58a6ff] rounded border border-[#30363d] hover:bg-[#30363d] transition-all text-sm font-semibold">Next Chapter: Text Manipulation ➔</a>
        </div>
    </main>
</body>
</html>
"""

full_html = html_head + sidebar_html + content_html
with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Generated index.html and copied {len(copied_images)} images: {', '.join(copied_images)}")
