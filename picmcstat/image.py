import re
from dataclasses import dataclass, replace
from functools import lru_cache
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

Color = str | tuple[int, int, int] | tuple[int, int, int, int]

FONT_DIRS = (
    Path.home() / ".fonts",
    Path("/usr/share/fonts"),
    Path("/usr/local/share/fonts"),
    Path("C:/Windows/Fonts"),
)
FALLBACK_FONTS = (
    "Microsoft YaHei",
    "Noto Sans CJK SC",
    "Noto Sans SC",
    "WenQuanYi Micro Hei",
    "DejaVu Sans",
)


def _font_paths(name: str):
    path = Path(name).expanduser()
    if path.is_file():
        yield path
        return

    normalized = re.sub(r"[^a-z0-9]", "", name.lower())
    for directory in FONT_DIRS:
        if not directory.is_dir():
            continue
        for candidate in directory.rglob("*"):
            if candidate.suffix.lower() not in {".ttf", ".otf", ".ttc"}:
                continue
            candidate_name = re.sub(r"[^a-z0-9]", "", candidate.stem.lower())
            if normalized in candidate_name or candidate_name in normalized:
                yield candidate


@lru_cache(maxsize=256)
def _load_font(
    names: tuple[str, ...], size: int, bold: bool, italic: bool
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in (*names, *FALLBACK_FONTS):
        style = " Bold Italic" if bold and italic else " Bold" if bold else " Italic" if italic else ""
        for path in (*_font_paths(name + style), *_font_paths(name)):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def load_font(
    names: list[str], size: int, bold: bool = False, italic: bool = False
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    return _load_font(tuple(map(str, names)), size, bold, italic)


def _color(value: Color) -> Color:
    return value


def _text_bbox(text: str, font: ImageFont.ImageFont, stroke_width: int = 0):
    return ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox(
        (0, 0), text, font=font, stroke_width=stroke_width
    )


class BuildImage:
    def __init__(self, image: Image.Image):
        self.image = image

    @classmethod
    def open(cls, fp: Any) -> "BuildImage":
        return cls(Image.open(fp).convert("RGBA"))

    @classmethod
    def new(cls, mode: str, size: tuple[int, int], color: Color | None = None):
        return cls(Image.new(mode, size, color))

    @property
    def width(self) -> int:
        return self.image.width

    @property
    def height(self) -> int:
        return self.image.height

    @property
    def size(self) -> tuple[int, int]:
        return self.image.size

    def paste(self, source: "BuildImage | Image.Image", box, alpha: bool = False):
        source_image = source.image if isinstance(source, BuildImage) else source
        if alpha:
            mask = source_image.getchannel("A") if source_image.mode == "RGBA" else None
            self.image.paste(source_image, box, mask)
        else:
            self.image.paste(source_image, box)

    def resize_height(self, height: int, inside: bool = False, resample=None):
        if inside and self.height <= height:
            return BuildImage(self.image.copy())
        width = round(self.width * height / self.height)
        return BuildImage(self.image.resize((width, height), resample or Image.Resampling.LANCZOS))

    def draw_text(
        self,
        box: tuple[float, float, float, float],
        text: str,
        *,
        halign: str = "left",
        fill: Color = "black",
        max_fontsize: int = 30,
        font_families: list[str] | None = None,
        stroke_ratio: float = 0,
        stroke_fill: Color | None = None,
    ):
        left, top, right, bottom = box
        max_width = max(1, int(right - left))
        max_height = max(1, int(bottom - top))
        font_size = max_fontsize
        font = load_font(font_families or [], font_size)
        stroke_width = round(font_size * stroke_ratio)
        bbox = _text_bbox(text, font, stroke_width)
        while font_size > 1:
            font = load_font(font_families or [], font_size)
            stroke_width = round(font_size * stroke_ratio)
            bbox = _text_bbox(text, font, stroke_width)
            if bbox[2] - bbox[0] <= max_width and bbox[3] - bbox[1] <= max_height:
                break
            font_size -= 1
        draw = ImageDraw.Draw(self.image)
        x = left if halign == "left" else left + (max_width - (bbox[2] - bbox[0])) / 2
        draw.text(
            (round(x), round(top - bbox[1])),
            text,
            font=font,
            fill=fill,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill or fill,
        )

    def convert(self, mode: str) -> "BuildImage":
        return BuildImage(self.image.convert(mode))

    def save(self, format: str) -> BytesIO:
        output = BytesIO()
        self.image.save(output, format=format.upper())
        output.seek(0)
        return output


@dataclass(frozen=True)
class TextSegment:
    text: str
    color: Color
    stroke: Color | None
    bold: bool = False
    italic: bool = False
    underline: bool = False
    delete: bool = False


TAG_RE = re.compile(r"\[(?P<tag>/?(?:color|stroke|b|i|u|del))(?:=(?P<value>[^\]]+))?\]")


class Text2Image:
    def __init__(
        self,
        segments: list[TextSegment],
        font_size: int,
        font_families: list[str],
        stroke_ratio: float = 0,
    ):
        self.segments = segments
        self.font_size = font_size
        self.font_families = font_families
        self.stroke_ratio = stroke_ratio
        self._lines: list[list[TextSegment]] | None = None

    @classmethod
    def from_bbcode_text(cls, text: str, **kwargs) -> "Text2Image":
        default_color = kwargs.get("fill", "#FFFFFF")
        default_stroke = kwargs.get("stroke_fill")
        font_size = int(kwargs.get("font_size", 30))
        font_families = list(kwargs.get("font_families") or [])
        stroke_ratio = float(kwargs.get("stroke_ratio", 0))
        state = TextSegment("", default_color, default_stroke)
        segments: list[TextSegment] = []
        pos = 0
        stack: list[tuple[str, Any]] = []

        def current() -> TextSegment:
            result = state
            for tag, value in stack:
                if tag == "color":
                    result = replace(result, color=value)
                elif tag == "stroke":
                    result = replace(result, stroke=value)
                elif tag == "b":
                    result = replace(result, bold=True)
                elif tag == "i":
                    result = replace(result, italic=True)
                elif tag == "u":
                    result = replace(result, underline=True)
                elif tag == "del":
                    result = replace(result, delete=True)
            return result

        for match in TAG_RE.finditer(text):
            if match.start() > pos:
                style = current()
                segments.append(replace(style, text=text[pos : match.start()]))
            raw_tag = match.group("tag")
            if raw_tag.startswith("/"):
                tag = raw_tag[1:]
                for index in range(len(stack) - 1, -1, -1):
                    if stack[index][0] == tag:
                        stack.pop(index)
                        break
            else:
                value = match.group("value")
                if raw_tag in {"color", "stroke"} and value:
                    stack.append((raw_tag, value))
                elif raw_tag in {"b", "i", "u", "del"}:
                    stack.append((raw_tag, True))
            pos = match.end()
        if pos < len(text):
            segments.append(replace(current(), text=text[pos:]))
        return cls([x for x in segments if x.text], font_size, font_families, stroke_ratio)

    @property
    def _lines_or_default(self):
        return self._lines or [self.segments]

    def _font(self, segment: TextSegment):
        return load_font(
            self.font_families,
            self.font_size,
            bold=segment.bold,
            italic=segment.italic,
        )

    def _segment_width(self, segment: TextSegment) -> float:
        font = self._font(segment)
        stroke_width = round(self.font_size * self.stroke_ratio) if segment.stroke else 0
        return _text_bbox(segment.text, font, stroke_width)[2]

    @property
    def longest_line(self) -> float:
        return max((self._line_width(line) for line in self._lines_or_default), default=0)

    @property
    def width(self) -> float:
        return self.longest_line

    @property
    def height(self) -> int:
        font = load_font(self.font_families, self.font_size)
        bbox = _text_bbox("Ag", font, round(self.font_size * self.stroke_ratio))
        return max(1, len(self._lines_or_default) * (bbox[3] - bbox[1]))

    def _line_width(self, line: list[TextSegment]) -> float:
        return sum(self._segment_width(x) for x in line)

    def wrap(self, max_width: float):
        lines: list[list[TextSegment]] = [[]]
        for segment in self.segments:
            parts = segment.text.split("\n")
            for index, part in enumerate(parts):
                if part:
                    current = ""
                    for char in part:
                        candidate = current + char
                        if current and self._line_width(lines[-1] + [replace(segment, text=candidate)]) > max_width:
                            lines[-1].append(replace(segment, text=current))
                            lines.append([])
                            current = char
                        else:
                            current = candidate
                    if current:
                        lines[-1].append(replace(segment, text=current))
                if index < len(parts) - 1:
                    lines.append([])
        self._lines = lines
        return self

    def draw_on_image(self, image: Image.Image, pos: tuple[float, float]):
        draw = ImageDraw.Draw(image)
        y = round(pos[1])
        line_height = self.height // max(1, len(self._lines_or_default))
        for line in self._lines_or_default:
            x = round(pos[0])
            for segment in line:
                font = self._font(segment)
                stroke_width = round(self.font_size * self.stroke_ratio) if segment.stroke else 0
                draw.text(
                    (x, y),
                    segment.text,
                    font=font,
                    fill=_color(segment.color),
                    stroke_width=stroke_width,
                    stroke_fill=_color(segment.stroke or segment.color),
                )
                bbox = _text_bbox(segment.text, font, stroke_width)
                segment_width = bbox[2] - bbox[0]
                line_width = max(1, self.font_size // 12)
                if segment.underline:
                    underline_y = y + line_height * 3 // 4
                    draw.line(
                        (x, underline_y, x + segment_width, underline_y),
                        fill=segment.color,
                        width=line_width,
                    )
                if segment.delete:
                    delete_y = y + line_height // 2
                    draw.line(
                        (x, delete_y, x + segment_width, delete_y),
                        fill=segment.color,
                        width=line_width,
                    )
                x += round(segment_width)
            y += line_height
