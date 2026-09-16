import re
from typing import Literal, TypeAlias

from mcstatus.motd.components import (
    BedrockFormatting,
    BedrockMinecraftColor,
    JavaFormatting,
    JavaMinecraftColor,
)

ServerTypeRaw: TypeAlias = Literal["je", "be"]
ServerType: TypeAlias = Literal[ServerTypeRaw, "auto"]

CODE_COLOR = {
    "0": "#000000",
    "1": "#0000AA",
    "2": "#00AA00",
    "3": "#00AAAA",
    "4": "#AA0000",
    "5": "#AA00AA",
    "6": "#FFAA00",
    "7": "#AAAAAA",
    "8": "#555555",
    "9": "#5555FF",
    "a": "#55FF55",
    "b": "#55FFFF",
    "c": "#FF5555",
    "d": "#FF55FF",
    "e": "#FFFF55",
    "f": "#FFFFFF",
    "g": "#DDD605",
}
STROKE_COLOR = {
    "0": "#000000",
    "1": "#00002A",
    "2": "#002A00",
    "3": "#002A2A",
    "4": "#2A0000",
    "5": "#2A002A",
    "6": "#2A2A00",
    "7": "#2A2A2A",
    "8": "#151515",
    "9": "#15153F",
    "a": "#153F15",
    "b": "#153F3F",
    "c": "#3F1515",
    "d": "#3F153F",
    "e": "#3F3F15",
    "f": "#3F3F3F",
    "g": "#373501",
}
# 基岩版专属颜色覆盖及新增的材质色（mcstatus 14 拆分 Java/基岩枚举后，
# BedrockMinecraftColor 相比 Java 版多了下列颜色，缺失会导致渲染查表 KeyError）
CODE_COLOR_BEDROCK = {
    **CODE_COLOR,
    "g": "#FFAA00",
    "7": "#C6C6C6",  # 基岩版灰色的前景色与 Java 版不同
    "h": "#E3D4D1",  # MATERIAL_QUARTZ
    "i": "#CECACA",  # MATERIAL_IRON
    "j": "#443A3B",  # MATERIAL_NETHERITE
    "m": "#971607",  # MATERIAL_REDSTONE
    "n": "#B4684D",  # MATERIAL_COPPER
    "p": "#DEB12D",  # MATERIAL_GOLD
    "q": "#119F36",  # MATERIAL_EMERALD
    "s": "#2CBAA8",  # MATERIAL_DIAMOND
    "t": "#21497B",  # MATERIAL_LAPIS
    "u": "#9A5CC6",  # MATERIAL_AMETHYST
    "v": "#EB7214",  # MATERIAL_RESIN
}
STROKE_COLOR_BEDROCK = {
    **STROKE_COLOR,
    "g": "#2A2A00",
    "7": "#313131",
    "h": "#383534",
    "i": "#333232",
    "j": "#110E0E",
    "m": "#250501",
    "n": "#2D1A13",
    "p": "#372C0B",
    "q": "#04280D",
    "s": "#0B2E2A",
    "t": "#08121E",
    "u": "#261731",
    "v": "#3B1D05",
}
STYLE_BBCODE = {
    "l": ["[b]", "[/b]"],
    "m": ["[del]", "[/del]"],
    "n": ["[u]", "[/u]"],
    "o": ["[i]", "[/i]"],
    "k": ["[obfuscated]", "[/obfuscated]"],  # placeholder
}
OBFUSCATED_PLACEHOLDER_REGEX = re.compile(
    r"\[obfuscated\](?P<inner>.*?)\[/obfuscated\]",
)

# mcstatus 14 起颜色/格式枚举按 Java 与基岩版拆分（JavaMinecraftColor/BedrockMinecraftColor 等），
# 渲染时按当前版本的枚举分别查表
# Java 版颜色枚举不含 "g"（MINECOIN_GOLD 属于基岩版专属颜色），构建时需排除
ENUM_CODE_COLOR = {
    JavaMinecraftColor(k): v for k, v in CODE_COLOR.items() if k != "g"
}
ENUM_STROKE_COLOR = {
    JavaMinecraftColor(k): v for k, v in STROKE_COLOR.items() if k != "g"
}
ENUM_CODE_COLOR_BEDROCK = {BedrockMinecraftColor(k): v for k, v in CODE_COLOR_BEDROCK.items()}
ENUM_STROKE_COLOR_BEDROCK = {
    BedrockMinecraftColor(k): v for k, v in STROKE_COLOR_BEDROCK.items()
}
# 基岩版不支持删除线（m）与下划线（n），构建其 BBCode 样式表时需跳过
ENUM_STYLE_BBCODE = {JavaFormatting(k): v for k, v in STYLE_BBCODE.items()}
ENUM_STYLE_BBCODE_BEDROCK = {
    BedrockFormatting(k): v for k, v in STYLE_BBCODE.items() if k not in ("m", "n")
}

GAME_MODE_MAP = {"Survival": "生存", "Creative": "创造", "Adventure": "冒险"}
# 格式化代码字母需覆盖 Java 版格式码与基岩版材质色字母（h/i/j/m/n/p/q/s/t/u/v）
FORMAT_CODE_REGEX = r"§[0-9a-v]"
