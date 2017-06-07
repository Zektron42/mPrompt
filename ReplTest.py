from pygments.lexers import PythonLexer

import pydoc

import re

from prompt_toolkit import prompt
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.buffer import Buffer

history = InMemoryHistory()

def toolbar_tokens(cli):
#    help(cli.current_buffer)
    result = cli.current_buffer.text
    matches = re.findall('[_a-zA-Z0-9\.]+\(', result[:cli.current_buffer.cursor_position])
    final = 'None'
    if matches:
        match = matches[-1][:-1]
        final = match
        if match in globals().keys():
            final = match
            if hasattr(globals()[match], '__doc__'):
                final = pydoc.render_doc(globals()[match]).split('\n')[2]
    return [(Token.Toolbar, final)]

def title():
    return 'MPrompt'

style = style_from_dict({Token.Toolbar: '#ffffff bg:#333333',})

myCompleter = WordCompleter(globals().keys())

while True:
    text = prompt('[Py] ',
                  lexer=PygmentsLexer(PythonLexer),
                  history=history,
                  get_bottom_toolbar_tokens=toolbar_tokens,
                  completer=myCompleter,
                  get_title=title)
    if text.startswith('!'):
        print(f'[CMD] {text}')
    elif text.startswith('?'):
        print(f'help({text})')
