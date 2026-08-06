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
        value = self.get("font", ["Minecraft AE Pixel", "Unifont"])
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
    def show_icon(self) -> bool:
        return bool(self.get("show_icon", True))

    @property
    def show_motd(self) -> bool:
        return bool(self.get("show_motd", True))

    @property
    def motd1(self) -> str:
        return str(self.get("motd1", "插件已关闭 Motd 信息渲染"))

    @property
    def motd2(self) -> str:
        return str(self.get("motd2", "如需开启请联系 Bot 管理员"))

    @property
    def show_playerlist(self) -> bool:
        return bool(self.get("show_playerlist", True))

    @property
    def shortcuts(self) -> list[ShortcutType]:
        return self.get("shortcuts", []) or []

    @property
    def resolve_dns(self) -> bool:
        return bool(self.get("resolve_dns", True))

    @property
    def resolve_dns_ipv6(self) -> bool:
        return bool(self.get("resolve_dns_ipv6", False))

    @property
    def query_twice(self) -> bool:
        return bool(self.get("query_twice", True))

    @property
    def query_timeout(self) -> int:
        try:
            value = int(self.get("query_timeout", 10))
        except (TypeError, ValueError):
            return 10
        return value if 1 <= value <= 60 else 10

    @property
    def java_protocol_version(self) -> int:
        return int(self.get("java_protocol_version", 776))

    @property
    def enable_auto_detect(self) -> bool:
        return bool(self.get("enable_auto_detect", True))


config = ConfigProxy()


def set_config(astrbot_config: AstrBotConfig):
    config.bind(astrbot_config)
