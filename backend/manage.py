from app import create_app, config
from flask_script import (Server, Shell, Manager, prompt_bool)

def _make_context():
    return dict(
        app=create_app(config.dev_config),
    )

app = create_app(config=config.dev_config)

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()
