"""Refresh shared blocks in every skill and copy the dashboard template reference.

Each SKILL.md can include a shared block between markers:
    <!-- shared:before-you-start -->
    ...replaced from shared/blocks/before-you-start.md...
    <!-- /shared:before-you-start -->

Skills that include the dashboard-format block get references/dashboard-template.md.

Usage: python3 scripts/sync.py
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "plugins/devplan/skills"
BLOCKS = ROOT / "shared/blocks"
TEMPLATE = (ROOT / "shared/dashboard-template.html").read_text()

REFERENCE = f"""# Devplan dashboard template

Copy this page and fill it in. Keep the `<head>`, `<style>` and `<script>` exactly as they are. The comments name each pattern and when to use it; delete them, and every pattern you don't use, before publishing.

```html
{TEMPLATE.rstrip()}
```
"""

pat = re.compile(r"<!-- shared:([\w-]+) -->\n.*?<!-- /shared:\1 -->", re.S)
problems = []
for skill in sorted(SKILLS.iterdir()):
    md = skill / "SKILL.md"
    text = md.read_text()

    def fill(m):
        name = m.group(1)
        block = (BLOCKS / f"{name}.md").read_text().strip()
        return f"<!-- shared:{name} -->\n{block}\n<!-- /shared:{name} -->"

    new = pat.sub(fill, text)
    if new != text:
        md.write_text(new)
    ref = skill / "references/dashboard-template.md"
    if "<!-- shared:dashboard-format -->" in new:
        ref.parent.mkdir(exist_ok=True)
        ref.write_text(REFERENCE)
    elif ref.exists():
        ref.unlink()
        if not any(ref.parent.iterdir()):
            ref.parent.rmdir()
    left = re.findall(r"\{\{[A-Z_]+[:}]", new)
    if left:
        problems.append((skill.name, left))
    print("synced", skill.name)

if problems:
    sys.exit(f"unexpanded placeholders: {problems}")
