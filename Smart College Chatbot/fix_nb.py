import json
from pathlib import Path

path = Path('SmartCollegeBot.ipynb')
nb = json.loads(path.read_bytes().decode('utf-8'))
changed = 0
for c in nb['cells']:
    if c.get('cell_type') == 'code':
        new_source = []
        for line in c['source']:
            new_source.append(line.replace("print('Confidence:', f{confidence:.2%})", "print('Confidence:', f'{confidence:.2%}')"))
        if new_source != c['source']:
            c['source'] = new_source
            changed += 1
path.write_text(json.dumps(nb, indent=2))
print(f'Updated {changed} cells.')
