import os
import re

MISTAKES = [
    {
        "id": 1,
        "description": "Using defer in a loop (can cause subtle bugs)",
        "pattern": r"\bfor\b[^{]*\{[^}]*\bdefer\b"
    },
    {
        "id": 2,
        "description": "Modifying a slice while ranging over it",
        "pattern": r"for\s+.*:=\s+range\s+.*\n.*append\("
    },
    {
        "id": 3,
        "description": "Ignoring errors from function calls",
        "pattern": r"\n\s*[_]*\s*=\s*[a-zA-Z_]+\([^)]*\)\s*\n"
    },
    {
        "id": 4,
        "description": "Unintended variable shadowing",
        "pattern": r"\bvar\s+\w+\s+\w+\s*=\s*.*\n\s*\w+\s*:=\s*.*"
    },
    {
        "id": 5,
        "description": "Overusing getters and setters",
        "pattern": r"func\s+Get\w+\s*\(\s*\)\s*\w+\s*{"
    },
    {
        "id": 6,
        "description": "Interface pollution: defining interfaces with too many methods",
        "pattern": r"type\s+\w+\s+interface\s*{\s*(\w+\s*\(.*\)\s*\w*\s*){5,}"
    },
    {
        "id": 7,
        "description": "Returning interfaces instead of concrete types",
        "pattern": r"func\s+\w+\s*\(.*\)\s+interface\s*{"
    },
    {
        "id": 8,
        "description": "Using 'any' type unnecessarily",
        "pattern": r"\bany\b"
    },
    {
        "id": 9,
        "description": "Not using the functional options pattern for configuration",
        "pattern": r"type\s+\w+Config\s+struct\s*{"
    },
    {
        "id": 10,
        "description": "Creating utility packages (e.g., 'utils', 'helpers')",
        "pattern": r'package\s+(utils|helpers)'
    },
    {
        "id": 11,
        "description": "Not checking for nil slices before use",
        "pattern": r"if\s+\w+\s*!=\s*nil\s*{"
    },
    {
        "id": 12,
        "description": "Using 'panic' for error handling",
        "pattern": r"\bpanic\("
    },
    {
        "id": 13,
        "description": "Not closing resources (e.g., files, HTTP responses)",
        "pattern": r"\b(os\.Open|http\.Get)\(.*\)"
    },
    {
        "id": 14,
        "description": "Using the default HTTP client without timeout",
        "pattern": r"http\.Get\("
    },
    {
        "id": 15,
        "description": "Not using the '-race' flag during testing",
        "pattern": r"go\s+test\b(?!.*-race)"
    }
]

def scan_go_file(filepath):
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            content = ''.join(lines)
            for mistake in MISTAKES:
                for match in re.finditer(mistake["pattern"], content, re.MULTILINE | re.DOTALL):
                    start_index = match.start()
                    line_number = content[:start_index].count('\n')
                    offending_line = lines[line_number].strip() if line_number < len(lines) else "<line unavailable>"
                    results.append({
                        "file": filepath,
                        "line": line_number + 1,
                        "mistake": mistake["description"],
                        "code": offending_line
                    })
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return results

def scan_project(root_dir):
    all_results = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.go'):
                path = os.path.join(subdir, file)
                all_results.extend(scan_go_file(path))
    return all_results

if __name__ == "__main__":
    import sys
    root = os.getcwd()
    print(f"Scanning Go project at {root}...\n")
    results = scan_project(root)
    if results:
        for res in results:
            print(f"[{res['file']}:{res['line']}] {res['mistake']}")
            print(f"  → {res['code']}")
    else:
        print("No common mistakes found!")
