import pytesseract
import cv2
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import os

def get_lines_with_words_and_boxes(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    data = pytesseract.image_to_data(img_rgb, output_type=pytesseract.Output.DICT, lang="amh")
    n = len(data['level'])
    lines = {}
    for i in range(n):
        if int(data['conf'][i]) > 60 and data['text'][i].strip() != '':
            key = (data['block_num'][i], data['par_num'][i], data['line_num'][i])
            if key not in lines:
                lines[key] = {'words': [], 'boxes': []}
            x, y, w, h_box = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            word = data['text'][i].strip()
            box = (x, y, x + w, y + h_box)
            lines[key]['words'].append(word)
            lines[key]['boxes'].append(box)
    sorted_lines = sorted(lines.values(), key=lambda l: l['boxes'][0][1] if l['boxes'] else 0)
    return sorted_lines

def get_words_and_boxes(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    data = pytesseract.image_to_data(img_rgb, output_type=pytesseract.Output.DICT, lang="amh")
    words, boxes = [], []
    n = len(data['text'])
    for i in range(n):
        if int(data['conf'][i]) > 70 and data['text'][i].strip() != '':
            x, y, w, h_box = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            words.append(data['text'][i].strip())
            boxes.append((x, y, x + w, y + h_box))
    return words, boxes

def visualize_diff(original_image_path, compared_image_path, font_path):
    orig_lines = get_lines_with_words_and_boxes(original_image_path)
    comp_lines = get_lines_with_words_and_boxes(compared_image_path)
    words_orig, boxes_orig = get_words_and_boxes(original_image_path)
    words_comp, boxes_comp = get_words_and_boxes(compared_image_path)
    max_lines = max(len(orig_lines), len(comp_lines))
    while len(orig_lines) < max_lines:
        orig_lines.append({'words': [], 'boxes': []})
    while len(comp_lines) < max_lines:
        comp_lines.append({'words': [], 'boxes': []})
    original_img_pil = Image.open(original_image_path).convert("RGB")
    draw = ImageDraw.Draw(original_img_pil)
    COLOR_SPACE_ERROR = 'blue'
    COLOR_TEXT_DIFF = 'red'
    COLOR_TEXT_CORRECTION = 'green'
    font = ImageFont.truetype(font_path, 20)
    for i in range(max_lines):
        orig_words = orig_lines[i]['words']
        orig_boxes = orig_lines[i]['boxes']
        comp_words = comp_lines[i]['words']
        comp_boxes = comp_lines[i]['boxes']
        if len(orig_words) < 2 and len(comp_words) < 2:
            continue
        def word_gaps(boxes):
            return [boxes[j][0] - boxes[j-1][2] for j in range(1, len(boxes))]
        orig_gaps = word_gaps(orig_boxes) if len(orig_boxes) >= 2 else []
        comp_gaps = word_gaps(comp_boxes) if len(comp_boxes) >= 2 else []
        gap_threshold = 7
        min_gaps = min(len(orig_gaps), len(comp_gaps))
        for gap_idx in range(min_gaps):
            gap_diff = abs(orig_gaps[gap_idx] - comp_gaps[gap_idx])
            if gap_diff > gap_threshold:
                x_prev_right = orig_boxes[gap_idx][2]
                x_next_left = orig_boxes[gap_idx + 1][0]
                x_line = (x_prev_right + x_next_left) // 2
                y_top = min(orig_boxes[gap_idx][1], orig_boxes[gap_idx + 1][1])
                y_bot = max(orig_boxes[gap_idx][3], orig_boxes[gap_idx + 1][3])
                draw.line([(x_line, y_top), (x_line, y_bot)], fill=COLOR_SPACE_ERROR, width=4)
                draw.line([(x_line - 5, y_top - 5), (x_line + 5, y_top - 5)], fill=COLOR_SPACE_ERROR, width=3)
    corrections = {}
    matched_comp_indices = set()
    for i, word_o in enumerate(words_orig):
        best_match_idx = None
        min_distance = float('inf')
        for j, word_c in enumerate(words_comp):
            if j in matched_comp_indices:
                continue
            dist = abs(i - j)
            if dist < min_distance:
                min_distance = dist
                best_match_idx = j
        if best_match_idx is not None:
            word_c = words_comp[best_match_idx]
            if word_o != word_c:
                corrections[i] = (word_o, word_c)
                matched_comp_indices.add(best_match_idx)
    for i, (orig_word, comp_word) in corrections.items():
        x1, y1, x2, y2 = boxes_orig[i]
        draw.rectangle([x1, y1, x2, y2], outline=COLOR_TEXT_DIFF, width=2)
        draw.text((x1, y1 - 25), orig_word, fill=COLOR_TEXT_DIFF, font=font)
        draw.text((x1, y2 + 5), comp_word, fill=COLOR_TEXT_CORRECTION, font=font)
    compared_img = Image.open(compared_image_path).convert("RGB")
    combined_width = original_img_pil.width + compared_img.width
    combined_height = max(original_img_pil.height, compared_img.height)
    combined_img = Image.new("RGB", (combined_width, combined_height))
    combined_img.paste(original_img_pil, (0, 0))
    combined_img.paste(compared_img, (original_img_pil.width, 0))
    plt.figure(figsize=(16, 12))
    plt.imshow(combined_img)
    plt.axis("off")
    plt.title("Blue:horizontal spacing Errors   Red:Word differences   Green:corrections")
    plt.show()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Visualize differences between two Amharic text images.")
    parser.add_argument('--original', required=True, help='Original rendered image')
    parser.add_argument('--compared', required=True, help='Compared rendered image')
    parser.add_argument('--font', default='fonts/AbyssinicaSIL-Regular.ttf', help='Font file path')
    args = parser.parse_args()
    visualize_diff(args.original, args.compared, args.font)