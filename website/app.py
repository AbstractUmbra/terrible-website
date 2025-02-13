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


ROOT_DIRECTORY = pathlib.Path(__file__).parent.parent
TEMPLATE_DIRECTORY = ROOT_DIRECTORY / "templates"
STATIC_DIRECTORY = ROOT_DIRECTORY / "static"
SPELLS = ROOT_DIRECTORY / "resources" / "spells.json"


class Spell(TypedDict):
    name: str
    dungeon: NotRequired[str]
    trial: NotRequired[str]
    totem: NotRequired[bool]
    enemy: str


@get("/")
async def index() -> Template:  # noqa: RUF029 # needed for litestar callbacks
    return Template("base.html.jinja2")


@get("/blu/spells")
async def show_blu_spell_list(request: Request[str, str, State]) -> Template:  # noqa: RUF029 # needed for litestar callbacks
    with SPELLS.open("r", encoding="utf-8") as fp:
        data: dict[str, Spell] = orjson.loads(fp.read())
        data.pop("$schema")

    return Template("spells.html.jinja2", context={"spells": data})


APP = Litestar(
    route_handlers=[index, show_blu_spell_list],
    template_config=TemplateConfig(directory=TEMPLATE_DIRECTORY, engine=JinjaTemplateEngine),
    static_files_config=[StaticFilesConfig(path="static", directories=[STATIC_DIRECTORY])],
)
