from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING, NotRequired, TypedDict

import orjson
from litestar import Litestar, Request, get
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.static_files import StaticFilesConfig
from litestar.template.config import TemplateConfig

if TYPE_CHECKING:
    from litestar.datastructures import State

__all__ = ("APP",)


TEMPLATE_DIRECTORY = pathlib.Path(__file__).parent.parent / "templates"
STATIC_DIRECTORY = pathlib.Path(__file__).parent.parent / "static"
SPELLS = pathlib.Path(__file__).parent.parent / "resources" / "spells.json"


class Spell(TypedDict):
    name: str
    dungeon: NotRequired[str]
    trial: NotRequired[str]
    enemy: str


@get("/")
async def index() -> Template:
    return Template("base.html.jinja2")


@get("/blu/spells")
async def show_blu_spell_list(request: Request[str, str, State]) -> Template:
    with SPELLS.open("r", encoding="utf-8") as fp:
        data: dict[str, Spell] = orjson.loads(fp.read())

    return Template("spells.html.jinja2", context={"spells": data})


APP = Litestar(
    debug=True,
    route_handlers=[show_blu_spell_list],
    template_config=TemplateConfig(directory=TEMPLATE_DIRECTORY, engine=JinjaTemplateEngine),
    static_files_config=[StaticFilesConfig(path="static", directories=[STATIC_DIRECTORY])],
)
