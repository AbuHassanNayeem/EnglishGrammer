import os
import re
from pathlib import Path

def extract_headlines(file_path):
    """Extract all headlines from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        headlines = []
        lines = content.split('\n')
        
        for line in lines:
            # Match markdown headers (# Header, ## Header, etc.)
            match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headlines.append({
                    'level': level,
                    'title': title,
                    'line': line
                })
        
        return headlines
    except Exception as e:
        return []

def traverse_directory(root_path):
    """Traverse directory tree and extract headlines from all files."""
    root = Path(root_path)
    results = {}
    
    # Get all markdown files
    for file_path in sorted(root.rglob('*')):
        if file_path.is_file():
            relative_path = file_path.relative_to(root)
            headlines = extract_headlines(file_path)
            
            if headlines:
                results[str(relative_path)] = headlines
    
    return results

def format_output(results):
    """Format the results in a hierarchical structure."""
    output = []
    output.append("=" * 80)
    output.append("HEADLINE EXTRACTION REPORT")
    output.append("=" * 80)
    output.append("")
    
    for file_path, headlines in results.items():
        output.append("─" * 80)
        output.append(f"📄 FILE: {file_path}")
        output.append("─" * 80)
        
        if headlines:
            for headline in headlines:
                indent = "  " * (headline['level'] - 1)
                marker = "•" if headline['level'] == 1 else "◦"
                output.append(f"{indent}{marker} [{headline['level']}] {headline['title']}")
        else:
            output.append("  (No headlines found)")
        
        output.append("")
    
    output.append("=" * 80)
    output.append(f"SUMMARY: Processed {len(results)} files")
    output.append("=" * 80)
    
    return "\n".join(output)

if __name__ == "__main__":
    root_dir = r"d:\Study\English Gramer\Sentence Patterns"
    
    print("Traversing directory tree...")
    results = traverse_directory(root_dir)
    
    print(f"Found {len(results)} files with content")
    
    # Generate output
    output = format_output(results)
    
    # Save to file
    output_file = os.path.join(root_dir, "HEADLINE_EXTRACTION_REPORT.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"\nReport saved to: {output_file}")
    print("\n" + "=" * 80)
    print("Preview (first 100 lines):")
    print("=" * 80)
    print("\n".join(output.split("\n")[:100]))
