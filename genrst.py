import pypandoc


with open('README.rst', 'wb') as f:
    f.write(pypandoc.convert('README.md', 'rst').encode('utf-8'))
