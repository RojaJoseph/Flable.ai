"""
Script to fix all imports in backend files
Converts 'from X' to 'from X'
"""

import os
import re

def fix_imports_in_file(filepath):
    """Fix imports in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace all 'from ' with 'from '
        original_content = content
        content = re.sub(r'from backend\.', 'from ', content)
        
        # Replace all 'import ' with 'import '
        content = re.sub(r'import backend\.', 'import ', content)
        
        # Only write if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {filepath}")
            return True
        else:
            print(f"  Skipped: {filepath}")
            return False
    except Exception as e:
        print(f"✗ Error in {filepath}: {e}")
        return False

def fix_all_imports(directory):
    """Recursively fix imports in all Python files"""
    fixed_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip venv and __pycache__
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', 'node_modules', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if fix_imports_in_file(filepath):
                    fixed_count += 1
    
    return fixed_count

if __name__ == "__main__":
    backend_dir = os.path.dirname(__file__)
    print("=" * 60)
    print("FIXING IMPORTS IN BACKEND")
    print("=" * 60)
    print()
    
    count = fix_all_imports(backend_dir)
    
    print()
    print("=" * 60)
    print(f"✓ Fixed {count} files!")
    print("=" * 60)
