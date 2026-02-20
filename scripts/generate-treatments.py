#!/usr/bin/env python3
"""Generate colored and reversed treatment variants from light templates."""
import os
import re
import sys


def make_colored(html, category):
    """Colored treatment: secondary background, keep dark text."""
    # Update template comment to reflect colored treatment
    html = re.sub(r'(Template: \S+)-light', r'\1-colored', html)

    # Find the slide div and add/modify background
    # Strategy: if the slide div has a style attribute, prepend background-color
    # If it doesn't, add a style attribute with background-color
    if 'style="' in html.split('class="slide')[1].split('>')[0]:
        # Has existing style on slide div - prepend background-color
        html = re.sub(
            r'(class="slide[^"]*")\s*style="',
            r'\1 style="background-color: var(--color-secondary); ',
            html,
            count=1
        )
    else:
        # No style on slide div - add one
        html = html.replace(
            'class="slide',
            'class="slide" style="background-color: var(--color-secondary);',
            1
        )
        # Fix the double quote issue if class had more content
        html = html.replace('" style="background-color: var(--color-secondary);"', '" style="background-color: var(--color-secondary);"')

    return html


def make_reversed(html, category):
    """Reversed treatment: primary dark background, light text."""
    # Update template comment
    html = re.sub(r'(Template: \S+)-light', r'\1-reversed', html)

    # Swap text colors
    html = html.replace('var(--color-text)', 'var(--color-text-reversed)')
    html = html.replace('var(--color-muted)', 'rgba(255,255,255,0.6)')

    # Swap background to primary (dark)
    html = html.replace('var(--color-background)', 'var(--color-primary)')

    # Add dark background to slide div if not already present
    if 'background' not in html.split('class="slide')[1].split('>')[0]:
        if 'style="' in html.split('class="slide')[1].split('>')[0]:
            html = re.sub(
                r'(class="slide[^"]*")\s*style="',
                r'\1 style="background-color: var(--color-primary); ',
                html,
                count=1
            )
        else:
            html = html.replace(
                'class="slide',
                'class="slide" style="background-color: var(--color-primary);',
                1
            )

    return html


def process_directory(template_dir):
    """Process all light templates in a directory to generate variants."""
    category = os.path.basename(template_dir)
    light_files = sorted(f for f in os.listdir(template_dir) if f.endswith('-light.html'))

    if not light_files:
        print(f"  No light templates found in {template_dir}")
        return 0

    count = 0
    for filename in light_files:
        filepath = os.path.join(template_dir, filename)
        with open(filepath) as f:
            light_html = f.read()

        # Generate colored variant
        colored_name = filename.replace('-light.html', '-colored.html')
        colored_path = os.path.join(template_dir, colored_name)
        with open(colored_path, 'w') as f:
            f.write(make_colored(light_html, category))
        print(f"  Created {colored_name}")
        count += 1

        # Generate reversed variant
        reversed_name = filename.replace('-light.html', '-reversed.html')
        reversed_path = os.path.join(template_dir, reversed_name)
        with open(reversed_path, 'w') as f:
            f.write(make_reversed(light_html, category))
        print(f"  Created {reversed_name}")
        count += 1

    return count


if __name__ == '__main__':
    dirs = sys.argv[1:] if len(sys.argv) > 1 else ['templates/title']
    total = 0
    for d in dirs:
        print(f"Processing {d}/")
        total += process_directory(d)
    print(f"\nTotal: {total} files created")
