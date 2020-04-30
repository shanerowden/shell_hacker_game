from markdown2 import Markdown
from story.paths import *

md = Markdown()
md_files = Pathing("*.md")

def dump_html_from_md(fname: str):
    return md.convert(md_files.paths[fname].read_text())

def write_to_html(data: str):
    with open("markdowntest123.html", "w") as fo:
        fo.write(data)


raw = dump_html_from_md("mission1phase1-clock.md")
write_to_html(raw)