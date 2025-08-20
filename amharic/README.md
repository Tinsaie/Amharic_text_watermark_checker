# Amharic Image Text Comparison & Correction Tool

This tool provides a full workflow for extracting Amharic text from images, comparing text layouts and content, rendering corrected text, and visualizing layout/text differences.  
It is ideal for OCR research, document verification, and Amharic text QA.

## Features

- **OCR Extraction:** Accurate Amharic text and layout extraction from images using Tesseract.
- **Text Reconstruction:** Rebuilds text with original line and word spacing.
- **Comparison:** Detects and visualizes line-by-line and word-by-word differences (including spacing).
- **Font Rendering:** Renders Amharic text to images with Abyssinica SIL font.
- **Visual Diff:** Highlights spacing errors, word mismatches, and corrections directly on images.
- **Modular Scripts:** Easy to run step-by-step or integrate as a pipeline.

## Directory Structure

```
amharic-image-diff/
├── README.md
├── requirements.txt
├── ocr_extract.py
├── compare_texts.py
├── render_text.py
├── visualize_diff.py
└── fonts/
    └── AbyssinicaSIL-Regular.ttf
```

## Setup

1. **Install Python dependencies**
   ```sh
   pip install -r requirements.txt
   ```

2. **Install Tesseract and Amharic language pack**
   ```sh
   sudo apt-get update
   sudo apt-get install tesseract-ocr tesseract-ocr-amh
   ```

3. **Download Abyssinica SIL font**
   ```sh
   mkdir -p fonts
   wget -O fonts/AbyssinicaSIL-Regular.ttf https://github.com/google/fonts/raw/main/ofl/abyssinicasil/AbyssinicaSIL-Regular.ttf
   ```

## Usage

### 1. OCR Extraction

Extract Amharic text from an image and reconstruct the layout:

```sh
python ocr_extract.py --image <input_image.png> --output <output_text.txt>
```

### 2. Compare Texts

Compare two text files line-by-line, showing all layout and character differences:

```sh
python compare_texts.py --original <original.txt> --new <compared.txt>
```

### 3. Render Text to Image

Render a text file back to an image using Amharic font:

```sh
python render_text.py --input <text.txt> --output <output_image.png> --font fonts/AbyssinicaSIL-Regular.ttf --size 28
```
(Font size is customizable.)

### 4. Visualize Differences

Overlay differences (spacing, word errors, corrections) on images:

```sh
python visualize_diff.py --original <original_image.png> --compared <compared_image.png> --font fonts/AbyssinicaSIL-Regular.ttf
```

## Example Workflow

1. OCR extract text from original and corrected images.
2. Compare the extracted texts.
3. Render the corrected text to image.
4. Visualize the difference between the two images.

## Requirements

- Python 3.x
- Tesseract OCR (with Amharic language pack)
- Abyssinica SIL font

## License

Apache License 2.0

## Credits

- Tesseract OCR
- Abyssinica SIL Font (Google Fonts)
