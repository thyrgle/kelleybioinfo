from pathlib import Path
import os
import hug


"""@hug.get('/dist/bundle.js', output=hug.output_format.text)
def bundle():
    '''Serve the "main" ReactJS file'''
    path = os.path.join(Path(__file__).parent.resolve(), 'dist')
    path = os.path.join(path, 'bundle.js')
    with open(path, 'r') as bundle:
        return bundle.read()"""

@hug.static('/', output=hug.output_format.file)
def index():
    '''Serve the index page'''
    return ('.' ,)


if __name__ == '__main__':
    hug.API(__name__).http.serve()
