import json

import requests

import config
from image import Image
from typed_desmos import Point, SavePayload, SaveUpdatePayload

session = requests.Session()
session.headers.update(
    {
        "accept": "*/*",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "content-type": "application/json",
        "origin": "https://student.desmos.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": f"https://student.desmos.com/activitybuilder/student/{config.student_id}",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    },
)

response = session.post(
    f"https://student.desmos.com/response/claim/{config.student_id}",
    headers={"pillow-frontend-version": "1"},
    json={"force": False},
)
if response.status_code != 200:
    print("Failed to get edit token")
    print(response)
    print(response.text)
    exit()
edit_token = response.json()["editToken"]

points: list[Point]
if config.clear_screen is True:
    points = []
else:
    image = Image()
    points = list(image.get_points())
update: SaveUpdatePayload = {"sketchData": {"points": points, "strokes": []}}

request_data: SavePayload = {
    "classId": config.class_id,
    "editToken": edit_token,
    "finish": False,
    "studentId": config.student_id,
    "update": {
        config.sketch_field_id: json.dumps(
            update,
            separators=(",", ":"),
        ),
    },
}

r = requests.post(
    f"https://student.desmos.com/response/save/{config.student_id}",
    # "http://localhost:1234/post",
    json=request_data,
)

print(r)
print(r.text)
