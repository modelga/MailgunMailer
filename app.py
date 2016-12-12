#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform
from app import app

if __name__ == '__main__':
    if platform.system() == "Darwin":
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=8090)
