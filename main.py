import re
import uuid
from io import BytesIO
from pathlib import Path

from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register
from astrbot.core.utils.astrbot_path import get_astrbot_data_path

from .picmcstat.config import set_config
from .picmcstat.const import ServerType
from .picmcstat.draw import draw


@register("PicMCMotd", "Midnight-2004", "查询 Minecraft 服务器 MOTD 和在线状态的插件", "0.0.2")
class PicMCMotdPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        set_config(config)

        plugin_data_path = Path(get_astrbot_data_path()) / "plugin_data" / self.name
        self.temp_path = plugin_data_path / "temp"
        self.temp_path.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """清理上次运行留下的临时图片。"""
        for file in self.temp_path.glob("*.jpg"):
            try:
                file.unlink()
            except OSError:
                logger.warning(f"清理临时图片失败: {file}")

    async def _draw_to_file(self, host: str, svr_type: ServerType) -> Path | str:
        try:
            image = await draw(host.strip(), svr_type)
        except Exception:
            logger.exception("出现未知错误")
            return "出现未知错误，请检查后台输出"

        return self._save_image(image)

    def _save_image(self, image: BytesIO) -> Path:
        self.temp_path.mkdir(parents=True, exist_ok=True)
        image.seek(0)

        path = self.temp_path / f"{uuid.uuid4().hex}.jpg"
        path.write_bytes(image.getvalue())
        return path

    async def _reply_query_result(
        self,
        event: AstrMessageEvent,
        host: str,
        svr_type: ServerType,
    ):
        result = await self._draw_to_file(host, svr_type)
        if isinstance(result, Path):
            yield event.image_result(str(result))
        else:
            yield event.plain_result(result)

    @filter.command("motd")
    async def motd(self, event: AstrMessageEvent, host: str = ""):
        """查询 Minecraft 服务器状态图；按配置自动检测或默认 Java 版。"""
        svr_type: ServerType = "auto" if self.config.get("enable_auto_detect", True) else "je"
        async for result in self._reply_query_result(event, host, svr_type):
            yield result

    @filter.command("motdje")
    async def motdje(self, event: AstrMessageEvent, host: str = ""):
        """查询 Minecraft Java 版服务器状态图。"""
        async for result in self._reply_query_result(event, host, "je"):
            yield result

    @filter.command("motdpe", alias={"motdbe"})
    async def motdpe(self, event: AstrMessageEvent, host: str = ""):
        """查询 Minecraft 基岩版服务器状态图。"""
        async for result in self._reply_query_result(event, host, "be"):
            yield result

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def shortcuts(self, event: AstrMessageEvent):
        """处理配置中的正则快捷指令。"""
        message = event.message_str
        if not message:
            return

        for shortcut in self.config.get("shortcuts", []):
            regex = shortcut.get("regex", "")
            host = shortcut.get("host", "")
            svr_type = shortcut.get("type", "auto")
            if not regex or not host or svr_type not in {"je", "be", "auto"}:
                continue
            try:
                if not re.search(regex, message):
                    continue
            except re.error as e:
                logger.warning(f"快捷指令正则无效: {regex}: {e}")
                continue
            if not self._shortcut_whitelist_allowed(event, shortcut.get("whitelist")):
                continue

            async for result in self._reply_query_result(
                event,
                host,
                svr_type,  # type: ignore[arg-type]
            ):
                yield result
            event.stop_event()
            return

    def _shortcut_whitelist_allowed(
        self,
        event: AstrMessageEvent,
        whitelist: list[int | str] | None,
    ) -> bool:
        if not whitelist:
            return True

        group_id = getattr(event.message_obj, "group_id", "")
        return str(group_id) in {str(x) for x in whitelist}

    async def terminate(self):
        """插件卸载/停用时清理临时图片。"""
        for file in self.temp_path.glob("*.jpg"):
            try:
                file.unlink()
            except OSError:
                logger.warning(f"清理临时图片失败: {file}")
