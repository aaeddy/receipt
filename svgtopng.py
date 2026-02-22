from playwright.sync_api import sync_playwright
import time

def svg_to_png_playwright(svg_path, png_path, width=800, height=600):
    """使用Playwright渲染SVG"""
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': width, 'height': height})
        
        # 读取SVG文件
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        # 创建HTML内容
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ margin: 0; padding: 0; }}
                svg {{ width: 100%; height: 100%; }}
            </style>
        </head>
        <body>
            {svg_content}
        </body>
        </html>
        """
        
        # 设置内容
        page.set_content(html_content)
        time.sleep(0.5)  # 等待渲染
        
        # 截图
        page.screenshot(path=png_path)
        
        browser.close()
        print(f"Playwright渲染完成: {png_path}")

# 使用
svg_to_png_playwright('receipt_20260222_141238.svg', 'output.png')
