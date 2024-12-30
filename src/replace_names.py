import os
import glob

def replace_in_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = content.replace('producto:', 'comercio:')
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

template_dir = 'comercio/templates/comercio'
for filename in glob.glob(os.path.join(template_dir, '*.html')):
    replace_in_file(filename)
