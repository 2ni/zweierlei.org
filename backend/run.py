# -*- coding: utf-8 -*-

"""
run app on prod with this script
"""

from app import create_app, config

import sys, os

debug = False
host = '0.0.0.0'
if '--debug' in sys.argv:
    host = '127.0.0.1'
    debug = True

port = int(os.getenv("PORT", "5000"))

app = create_app(config.base_config)

if __name__ == '__main__':
    app.run(debug=debug, host=host, port=port)
