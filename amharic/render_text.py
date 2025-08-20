from PIL import Image, ImageDraw, ImageFont
import os

def text_file_to_image(text_path, output_path='output.png', font_path='fonts/AbyssinicaSIL-Regular.ttf', font_size=28):
    with open(text_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    width = 1200
    line_height = font_size + 12
    height = line_height * len(lines) + 40
    font = ImageFont.truetype(font_path, font_size)
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)
    y = 20
    for line in lines:
        draw.text((20, y), line.strip(), font=font, fill="black")
        y += line_height
    img.save(output_path)
    print(f"Image saved to: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Render Amharic text file to image.")
    parser.add_argument('--input', required=True, help='Input text file')
    parser.add_argument('--output', default='output.png', help='Output image file')
    parser.add_argument('--font', default='fonts/AbyssinicaSIL-Regular.ttf', help='Font file path')
    parser.add_argument('--size', type=int, default=28, help='Font size')
    args = parser.parse_args()
    text_file_to_image(args.input, args.output, args.font, args.size)