from pathlib import Path

from flask import Flask

app = Flask(__name__)

_INDEX_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''

_USER_LINE_HTML = '''
<li>
    <a href="/users/{user_id}">user {user_id}</a>
</li>
'''

_USER_TABLE_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user}</title>
    </head>
    <body>
        <table>
            {thoughts}
        </table>
    </body>
</html>
'''

_USER_THOUGHT_HTML = '''
<tr>
    <td>{date}</td>
    <td>{thought}</td>
</tr>
'''


def run_webserver(address, data_dir):
    @app.route('/')
    def get_index_html():
        users_html = [_USER_LINE_HTML.format(user_id=user_dir.name) for user_dir in Path(data_dir).iterdir()]
        return 200, _INDEX_HTML.format(users='\n'.join(users_html))

    @app.route('/users/([0-9]+)')
    def get_user_html(user_id):
        thoughts_html = []
        for thought_file in Path(data_dir, user_id).iterdir():
            date = thought_file.name[:-4].replace('_', ' ')[::-1].replace('-', ':', 2)[::-1]
            with open(thought_file, 'rb') as f:
                thought = f.read().decode()
            thoughts_html.append(_USER_THOUGHT_HTML.format(date=date, thought=thought))
        return 200, _USER_TABLE_HTML.format(user=user_id, thoughts='\n'.join(thoughts_html))

    host, port = address.split(':')
    app.run(host=host, port=int(port))
