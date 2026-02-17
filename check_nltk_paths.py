import nltk
import os

print("NLTK Data Paths:")
for path in nltk.data.path:
    print(f"  - {path}")
    if os.path.exists(path):
        print(f"    (Exists) Contents: {os.listdir(path)}")
    else:
        print("    (Does not exist)")

print("\nChecking for punkt_tab...")
try:
    nltk.data.find('tokenizers/punkt_tab')
    print("  Found 'punkt_tab'")
except LookupError:
    print("  'punkt_tab' NOT found")

print("\nChecking for punkt...")
try:
    nltk.data.find('tokenizers/punkt')
    print("  Found 'punkt'")
except LookupError:
    print("  'punkt' NOT found")
