#!/usr/bin/env/python3
import os
import json
from pathlib import Path
import re
import html

class Pager:
    def __init__(self, config_file="config.json"):
        # Load config
        self.config = self.load_config(config_file)
        self.input_dir = Path(self.config.get("input_dir", "content"))
        self.output_dir = Path(self.config.get("output_dir", "public"))
        self.theme = self.config.get("theme", "default")
        self.output_dir.mkdir(exist_ok=True)
        self.pages = []

    def load_config(self, config_file):
        default_config = {
            "input_dir": "content",
            "output_dir": "public",
            "theme": "default",
            "title": "Pager Site",
            "javascript_libs": []
        }
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return {**default_config, **json.load(f)}
        return default_config

    # Enhanced Markdown with custom codes
    def md_to_html(self, content):
        # Custom codes
        content = re.sub(r':::animate:(fade|bounce|pulse) (.*?):::', 
                        r'<div class="animate-\1">\2</div>', content, flags=re.S)
        content = re.sub(r':::js:(alert|prompt) (.*?):::', 
                        r'<button onclick="\1(\'\2\')">Click Me</button>', content, flags=re.S)
        
        # Standard Markdown
        content = re.sub(r'^# (.*)$', r'<h1>\1</h1>', content, flags=re.M)
        content = re.sub(r'^## (.*)$', r'<h2>\1</h2>', content, flags=re.M)
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'_(.*?)_', r'<em>\1</em>', content)
        content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', content)
        content = '<p>' + content.replace('\n\n', '</p><p>') + '</p>'
        return content

    # Theme styles
    def get_theme_css(self):
        themes = {
            "default": """
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                nav { background: #f0f0f0; padding: 10px; margin-bottom: 20px; }
                nav a { margin-right: 10px; color: #333; }
            """,
            "crt": """
                body { background: #000; color: #0f0; font-family: 'Courier New', monospace; margin: 0; padding: 20px; }
                .crt { animation: crt-flicker 0.15s infinite; }
                .crt::after { 
                    content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                    background: repeating-linear-gradient(0deg, rgba(0,0,0,0.05) 0px, rgba(0,0,0,0.05) 1px, transparent 1px, transparent 2px);
                }
                @keyframes crt-flicker { 0% { opacity: 0.98; } 50% { opacity: 1.00; } 100% { opacity: 0.98; } }
            """,
            "dark": """
                body { background: #222; color: #fff; font-family: sans-serif; margin: 0; padding: 20px; }
                nav { background: #333; padding: 10px; }
                nav a { color: #ddd; margin-right: 10px; }
                a { color: #1e90ff; }
            """
        }
        
        # Animation CSS
        animations = """
            .animate-fade { animation: fade 1s ease-in; }
            .animate-bounce { animation: bounce 1s infinite; }
            .animate-pulse { animation: pulse 1s infinite; }
            @keyframes fade { from { opacity: 0; } to { opacity: 1; } }
            @keyframes bounce { 
                0%, 100% { transform: translateY(0); } 
                50% { transform: translateY(-10px); } 
            }
            @keyframes pulse { 
                0% { transform: scale(1); } 
                50% { transform: scale(1.05); } 
                100% { transform: scale(1); } 
            }
        """
        return f"<style>{themes.get(self.theme, themes['default'])}{animations}</style>"

    # Navigation
    def get_navigation(self):
        nav_items = []
        for page in self.pages:
            nav_items.append(f'<a href="{page["filename"]}">{html.escape(page["title"])}</a>')
        return f'<nav>{" ".join(nav_items)}</nav>'

    # Template
    def get_template(self, title, content):
        js_libs = "".join(f'<script src="{lib}"></script>' 
                         for lib in self.config.get("javascript_libs", []))
        class_attr = ' class="crt"' if self.theme == "crt" else ""
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)} - {html.escape(self.config["title"])}</title>
    {self.get_theme_css()}
    {js_libs}
</head>
<body{class_attr}>
    {self.get_navigation()}
    {content}
</body>
</html>"""

    # Generate site
    def generate(self):
        # Collect page info
        self.pages = []
        for md_file in self.input_dir.glob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            title_match = re.search(r'^# (.*)$', content, re.M)
            title = title_match.group(1) if title_match else md_file.stem
            self.pages.append({"title": title, "filename": f"{md_file.stem}.html"})

        # Generate pages
        for md_file in self.input_dir.glob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            title_match = re.search(r'^# (.*)$', content, re.M)
            title = title_match.group(1) if title_match else md_file.stem
            
            html_content = self.md_to_html(content)
            html_output = self.get_template(title, html_content)
            
            output_file = self.output_dir / f"{md_file.stem}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_output)
            print(f"Generated: {output_file}")

def main():
    generator = Pager()
    generator.generate()

if __name__ == "__main__":
    main()