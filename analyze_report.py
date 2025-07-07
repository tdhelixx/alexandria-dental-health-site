#!/usr/bin/env python3
import re

# Read the corrected report
with open('wp-featured-image-setter/corrected_fifu_featured_images_report.txt', 'r') as f:
    content = f.read()

# Extract all post_ids
post_ids = re.findall(r'post_id="(\d+)"', content)
unique_post_ids = set(post_ids)

print(f'Total entries in report: {len(post_ids)}')
print(f'Unique post IDs: {len(unique_post_ids)}')
print(f'Duplicate entries: {len(post_ids) - len(unique_post_ids)}')

# Count duplicates per post_id
from collections import Counter
post_id_counts = Counter(post_ids)
duplicates = {pid: count for pid, count in post_id_counts.items() if count > 1}

print(f'\nPosts with multiple images:')
for pid, count in sorted(duplicates.items(), key=lambda x: int(x[0])):
    print(f'  Post ID {pid}: {count} images')

print(f'\nTotal unique posts that will get featured images: {len(unique_post_ids)}') 