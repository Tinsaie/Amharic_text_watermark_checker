import pytesseract
from PIL import Image
import cv2
from collections import defaultdict
import os

def extract_text(image_path, lang='amh', output_txt='vvv.txt'):
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    image = cv2.imread(image_path)
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(image_pil, lang=lang, config=custom_config, output_type=pytesseract.Output.DICT)
    lines = defaultdict(list)
    line_positions = []
    line_map = {}
    for i in range(len(data['level'])):
        word = data['text'][i].strip()
        if word:
            key = (data['block_num'][i], data['par_num'][i], data['line_num'][i])
            lines[key].append({
                'text': word,
                'left': data['left'][i],
                'width': data['width'][i]
            })
    for key in lines:
        top_positions = [data['top'][i] for i in range(len(data['text']))
                         if data['text'][i].strip() and
                         (data['block_num'][i], data['par_num'][i], data['line_num'][i]) == key]
        avg_top = sum(top_positions) // len(top_positions) if top_positions else 0
        line_positions.append((avg_top, key))
        line_map[key] = lines[key]
    line_positions.sort()
    output = ""
    last_top = None
    for avg_top, key in line_positions:
        words = sorted(line_map[key], key=lambda x: x['left'])
        if last_top is not None:
            vertical_gap = avg_top - last_top
            if vertical_gap > 40:
                output += "\n"
        last_top = avg_top
        line_text = words[0]['text']
        for j in range(1, len(words)):
            prev = words[j - 1]
            curr = words[j]
            gap = curr['left'] - (prev['left'] + prev['width'])
            spaces = ' ' * max(1, gap // 10)
            line_text += spaces + curr['text']
        output += line_text + "\n"
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Extracted text saved to {output_txt}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract Amharic text from image with layout info.")
    parser.add_argument('--image', required=True, help='Image file path')
    parser.add_argument('--output', default='vvv.txt', help='Output text file path')
    parser.add_argument('--lang', default='amh', help='Tesseract language')
    args = parser.parse_args()
    extract_text(args.image, args.lang, args.output)