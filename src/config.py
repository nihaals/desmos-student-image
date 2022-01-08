import json
from pathlib import Path
from typing import TypedDict


class Config(TypedDict):
    class_id: str
    edit_token: str
    student_id: str
    sketch_field_id: str
    image_path: str
    preserve_aspect_ratio: bool
    clear_screen: bool


with open(Path(__file__).parent.parent.joinpath("config.json")) as fp:
    config: Config = json.load(fp)

class_id = config["class_id"]
student_id = config["student_id"]
sketch_field_id = config["sketch_field_id"]
image_path = config["image_path"]
preserve_aspect_ratio = config["preserve_aspect_ratio"]
clear_screen = config["clear_screen"]

assert class_id
assert student_id
assert sketch_field_id
if clear_screen is False:
    assert image_path
