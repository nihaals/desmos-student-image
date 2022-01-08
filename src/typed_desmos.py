from typing import TypedDict


class Coords(TypedDict):
    x: float
    y: float


class Point(TypedDict):
    color: str
    coords: Coords


class Stroke(TypedDict):
    color: str
    coords: list[Coords]


class SaveSketchData(TypedDict):
    points: list[Point]
    strokes: list[Stroke]


class SaveUpdatePayload(TypedDict):
    sketchData: SaveSketchData


class SavePayload(TypedDict):
    classId: str
    editToken: str
    finish: bool
    studentId: str
    update: dict[str, str]
