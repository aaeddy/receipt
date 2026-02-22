from PIL import Image, ImageDraw, ImageFont

def create_icon():
    size = 192
    img = Image.new('RGB', (size, size), '#4A90E2')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype('C:\\Windows\\Fonts\\simhei.ttf', 80)
    except:
        font = ImageFont.load_default()
    
    text = '收据'
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 20
    
    draw.text((x, y), text, fill='white', font=font)
    
    draw.rectangle([30, 140, 162, 160], fill='white', outline='white')
    
    img.save('data/icon.png')
    print('图标已生成：data/icon.png')

def create_presplash():
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), '#4A90E2')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype('C:\\Windows\\Fonts\\simhei.ttf', 120)
    except:
        font = ImageFont.load_default()
    
    text = '收据生成器'
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    img.save('data/presplash.png')
    print('启动画面已生成：data/presplash.png')

if __name__ == '__main__':
    create_icon()
    create_presplash()
