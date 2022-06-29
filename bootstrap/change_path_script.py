import os
import re

dir_path = os.path.join(os.getcwd(), 'export')

for file in os.listdir(dir_path):
    if file.split('.')[-1] == 'html':
        filepath = os.path.join(dir_path, file)
        content = ''
        new_content = ''
        with open(filepath, 'r+') as stream:
            content = stream.readlines()
        for line in content:
            if line.find('assets'):
                line = line.replace('"assets/', '"../static/')
            if re.search('href=".*.html"', line):
                filename = re.search('"\S*.html"', line)
                line = line.replace(filename[0],
                                    '"templates/' + filename[0][1:-1] + '"')
            new_content += line
        with open(filepath, 'r+') as stream:
            stream.write(new_content)
