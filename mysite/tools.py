from pathlib import Path
import json

p = Path()
p = p.home().joinpath(".jiejie/mysql/mysite.json")

data = json.loads(p.read_text())

