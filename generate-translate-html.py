import os
from utils import markdown_to_html_tags

file_in = open('TRANSLATING.md', 'r', encoding='utf-8')
file_out = open('./templates/translating.html', "w+", encoding='utf8')
file_out.write(str(markdown_to_html_tags(file_in.read())))
file_out.close()
file_in.close()
