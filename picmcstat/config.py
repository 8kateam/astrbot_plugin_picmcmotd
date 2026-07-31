from typing import Any, Literal, TypedDict

from astrbot.api import AstrBotConfig

ServerType = Literal["je", "be", "auto"]


class ShortcutType(TypedDict, total=False):
    regex: str
    host: str
    type: ServerType
    whitelist: list[int | str]


class ConfigProxy:
    def __init__(self):
        self._config: AstrBotConfig | dict[str, Any] = {}

    def bind(self, config: AstrBotConfig):
        self._config = config

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    @property
    def font(self) -> list[str]:
        value = self.get("font", ["Minecraft Seven", "unifont"])
        return value if isinstance(value, list) else [value]

    @property
    def show_addr(self) -> bool:
        return bool(self.get("show_addr", False))

    @property
    def show_delay(self) -> bool:
        return bool(self.get("show_delay", True))

    @property
    def show_mods(self) -> bool:
        return bool(self.get("show_mods", False))

    @property
    def reply_target(self) -> bool:
        return bool(self.get("reply_target", True))

    @property
    def shortcuts(self) -> list[ShortcutType]:
        return self.get("shortcuts", []) or []

    @property
    def resolve_dns(self) -> bool:
        return bool(self.get("resolve_dns", True))

    @property
    def resolve_dns_ipv6(self) -> bool:
        return bool(self.get("resolve_dns_ipv6", True))

    @property
    def query_twice(self) -> bool:
        return bool(self.get("query_twice", True))

    @property
    def java_protocol_version(self) -> int:
        return int(self.get("java_protocol_version", 776))

    @property
    def enable_auto_detect(self) -> bool:
        return bool(self.get("enable_auto_detect", True))


config = ConfigProxy()


def set_config(astrbot_config: AstrBotConfig):
    config.bind(astrbot_config)
