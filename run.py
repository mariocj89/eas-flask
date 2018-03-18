#!/usr/bin/env python3.6
import os

os.environ["EAS_SETTINGS"] = "eas/settings/dev.py"

from eas import factories
app = factories.create_app()
app.run(host='0.0.0.0', port=8080, debug=True)
