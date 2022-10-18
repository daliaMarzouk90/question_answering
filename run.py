from distutils.command.config import config
import os
from config import *
from config.config import *

if __name__ == '__main__':
    host = os.environ.get('IP', APP_IP)
    port = int(os.environ.get('PORT', APP_PORT))
    app.run(host=host, port=port)
    app.run()