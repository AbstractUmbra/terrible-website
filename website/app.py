from __future__ import annotations

import pathlib
from typing import NotRequired, TypedDict

import orjson
from litestar import Litestar, get
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.logging import LoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.response import Template
from litestar.static_files import StaticFilesConfig
from litestar.template.config import TemplateConfig

from .config import Config
from .utils import load_config_type, resolve_docker_config

__all__ = ("APP",)


ROOT_DIRECTORY = pathlib.Path(__file__).parent.parent
TEMPLATE_DIRECTORY = ROOT_DIRECTORY / "templates"
STATIC_DIRECTORY = ROOT_DIRECTORY / "static"
SPELLS = ROOT_DIRECTORY / "resources" / "spells.json"
CARDS = ROOT_DIRECTORY / "resources" / "cards.json"

APP_CONFIG = load_config_type(resolve_docker_config(env_var_name="CONFIG_PATH"), Config)


class Spell(TypedDict):
    name: str
    dungeon: NotRequired[str]
    trial: NotRequired[str]
    totem: NotRequired[bool]
    enemy: str


class _CardGemstones(TypedDict):
    area: str
    npc: str
    cost: int


class Card(TypedDict):
    name: str
    event: NotRequired[str]
    npc: NotRequired[str]
    dungeon: NotRequired[str]
    trial: NotRequired[str]
    enemy: NotRequired[str]
    pack: NotRequired[str]
    gemstones: NotRequired[_CardGemstones]


@get("/")
async def index() -> Template:  # noqa: RUF029 # needed for litestar callbacks
    return Template("base.html.jinja2")


@get("/blu/spells")
async def show_blu_spell_list() -> Template:  # noqa: RUF029 # needed for litestar callbacks
    with SPELLS.open("r", encoding="utf-8") as fp:
        data: dict[str, Spell] = orjson.loads(fp.read())
        data.pop("$schema")

    return Template("spells.html.jinja2", context={"spells": data})


@get("/cards")
async def show_card_list() -> Template:  # noqa: RUF029 # needed for litestar callbacks
    with CARDS.open("r", encoding="utf-8") as fp:
        data: dict[str, Card] = orjson.loads(fp.read())
        data.pop("$schema")

    return Template("cards.html.jinja2", context={"cards": data})


APP = Litestar(
    debug=APP_CONFIG.debug,
    route_handlers=[index, show_blu_spell_list, show_card_list],
    middleware=[ServerSideSessionConfig().middleware, LoggingMiddlewareConfig().middleware],
    csrf_config=APP_CONFIG.csrf.to_litestar(),
    cors_config=APP_CONFIG.cors.to_litestar(),
    allowed_hosts=APP_CONFIG.allowed_hosts.to_litestar(),
    compression_config=APP_CONFIG.compression.to_litestar(),
    response_cache_config=APP_CONFIG.response_cache.to_litestar(),
    logging_config=LoggingConfig(
        disable_stack_trace={404}, log_exceptions="always", root={"level": "INFO", "handlers": ["queue_listener"]}
    ),
    template_config=TemplateConfig(directory=TEMPLATE_DIRECTORY, engine=JinjaTemplateEngine),
    static_files_config=[StaticFilesConfig(path="static", directories=[STATIC_DIRECTORY])],
)
