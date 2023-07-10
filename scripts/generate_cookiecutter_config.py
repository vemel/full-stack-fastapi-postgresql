import json
from pathlib import Path
from typing import Dict, Any

import yaml


cookie_path = Path("./cookiecutter.json")
out_path = Path("./{{cookiecutter.project_slug}}/cookiecutter-config-file.yml")

cookie_config: Dict[str, Any] = json.load(cookie_path.open())
config_out: Dict[str, Any] = {}

for key, value in cookie_config.items():
    if key.startswith("_"):
        config_out[key] = value
    else:
        config_out[key] = "{{ cookiecutter." + key + " }}"
config_out["_template"] = "./"

data = yaml.dump({"default_context": config_out}, line_break=None, width=200, sort_keys=False)
out_path.write_text(data)
