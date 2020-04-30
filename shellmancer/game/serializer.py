from markdown2 import Markdown
from story.paths import *

md = Markdown()
raw = md.convert("*BOO*")
print(raw)
phases = dict()
