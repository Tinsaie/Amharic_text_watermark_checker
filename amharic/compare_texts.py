from difflib import SequenceMatcher

def compare_layout_lines(original_lines, new_lines):
    max_lines = max(len(original_lines), len(new_lines))
    for i in range(max_lines):
        orig_line = original_lines[i] if i < len(original_lines) else ''
        new_line  = new_lines[i] if i < len(new_lines) else ''
        if orig_line != new_line:
            print(f"\nDifference at line {i+1}:")
            print(f" • Original : '{orig_line}'")
            print(f" • New      : '{new_line}'")
            matcher = SequenceMatcher(None, orig_line, new_line)
            for tag, o_start, o_end, w_start, w_end in matcher.get_opcodes():
                if tag != 'equal':
                    print(f"   ⤷ {tag.upper()}:")
                    print(f"     - Original[{o_start}:{o_end}]: '{orig_line[o_start:o_end]}'")
                    print(f"     - New     [{w_start}:{w_end}]: '{new_line[w_start:w_end]}'")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Compare two Amharic text files line by line.")
    parser.add_argument('--original', required=True, help='Original text file')
    parser.add_argument('--new', required=True, help='Compared text file')
    args = parser.parse_args()
    with open(args.original, encoding='utf-8') as f:
        original_text = f.read()
    with open(args.new, encoding='utf-8') as f:
        new_text = f.read()
    original_lines = original_text.strip().splitlines()
    new_lines      = new_text.strip().splitlines()
    compare_layout_lines(original_lines, new_lines)
    if len(original_lines) != len(new_lines):
        print(f"\nVertical spacing mismatch: original has {len(original_lines)} lines, new has {len(new_lines)} lines")