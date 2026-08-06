# astrbot_plugin_picmcmotd

PicMCMotd 是一个 AstrBot 插件，用于查询 Minecraft 服务器 MOTD 和在线状态，并将结果绘制成图片返回。插件支持 Java 版和基岩版服务器，也可以自动检测服务器类型。

本插件基于上游项目 [`nonebot_plugin_picmcstat`](https://github.com/lgc-NB2Dev/nonebot-plugin-picmcstat) 开发。

## 功能

- 查询 Minecraft Java 版服务器 MOTD、版本、协议、在线人数、延迟等信息。
- 查询 Minecraft 基岩版服务器 MOTD、版本、在线人数、地图、游戏模式、延迟等信息。
- 支持自动检测 Java 版或基岩版服务器。
- 将查询结果绘制为图片发送。
- 支持通过配置添加正则快捷指令。
- 支持 DNS 和 SRV 记录解析。

## 指令

指令实际前缀由 AstrBot 配置文件中的唤醒词管理，默认为 `/`。帮助图中的展示前缀可通过插件配置项 `command_prefix` 单独设置，该配置仅影响帮助图渲染。

| 指令 | 说明 |
| --- | --- |
| `/motd` `/motdje` `/motdpe` | 显示使用帮助图。 |
| `/motd <服务器地址>` | 查询服务器状态。默认自动检测服务器类型；若关闭自动检测，则按 Java 版查询。 |
| `/motdje <服务器地址>` | 强制按 Minecraft Java 版服务器查询。 |
| `/motdpe <服务器地址>` | 强制按 Minecraft 基岩版服务器查询。 |
| `/motdbe <服务器地址>` | `/motdpe` 的别名，强制按基岩版服务器查询。 |

服务器地址必须与指令之间使用空格分隔，例如：

```text
/motd mc.example.com
/motdje mc.example.com:25565
/motdpe be.example.com:19132
```

## 配置

插件提供 `_conf_schema.json`，可在 AstrBot WebUI 中配置：

| 配置项 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `font` | `["Minecraft AE Pixel", "Unifont"]` | 指定绘图所用的字体列表，如需使用其他字体，请参考下方“字体安装”一节。 |
| `show_icon` | `true` | 是否显示服务器图标。 <br> 开启后优先渲染服务器返回的图标，服务器无图标或图标解析失败时回退到默认图标；关闭后始终使用默认图标。 |
| `show_motd` | `true` | 是否显示服务器 MOTD 文本。关闭后会显示 `motd1` 和 `motd2` 配置的提示文案。 |
| `motd1` | `插件已关闭 Motd 信息渲染` | MOTD 关闭时显示的第一行文本。 |
| `motd2` | `如需开启请联系 Bot 管理员` | MOTD 关闭时显示的第二行文本。 |
| `show_addr` | `false` | 是否显示测试地址。 |
| `show_delay` | `true` | 是否显示测试延迟。 |
| `show_mods` | `false` | 是否显示 Java 版服务器返回的 Mod 列表。 |
| `show_playerlist` | `true` | 是否显示 Java 版服务器返回的玩家列表。 |
| `shortcuts` | 空 | 正则快捷指令列表，可使用 AstrBot WebUI 快速添加。 |
| `resolve_dns` | `true` | 是否由插件解析 DNS 记录后再进行查询。 <br> 如果你的服务器在运行 Clash 等拦截了 DNS 解析的软件，且查询部分地址时遇到了问题，请尝试关闭此配置项。<br> 此配置项不影响 Java 服务器的 SRV 记录解析。 |
| `resolve_dns_ipv6` | `false` | 是否优先解析并尝试 IPv6。 <br> 当启用此配置项时，会优先尝试使用 IPv6 地址进行连接，如连接失败则自动回落到 IPv4。<br> 此配置项依赖 `resolve_dns`，若 `resolve_dns` 为 `false`，插件不会解析 DNS 记录，本配置项将不生效。 |
| `query_twice` | `true` | 是否查询两次以改善延迟显示。 <br> 由于第一次测得的延迟一般不准，所以做了这个配置，开启后每次查询时，会丢掉第一次的结果再查询一次，且使用第二次查询到的结果。 |
| `query_timeout` | `10` | 单次 Java 版或基岩版查询的总超时时间，单位为秒，包含 DNS 解析和状态请求。可设置范围为 `1` 至 `60`。 |
| `java_protocol_version` | `776` | Java 版查询时发送的[协议版本](https://zh.minecraft.wiki/w/%E5%8D%8F%E8%AE%AE%E7%89%88%E6%9C%AC?variant=zh-cn)。 <br> [Java 版正式版协议版本列表](https://8ka.hk/pvn) |
| `enable_auto_detect` | `true` | `/motd` 是否自动检测服务器类型。 <br> 关闭后将始终作为 Java 版服务器查询。 |
| `command_prefix` | `/` | 帮助图中显示的指令前缀。仅影响帮助图渲染，实际前缀由 AstrBot 配置管理。 |

## 字体安装

为获得更接近游戏内原版的字体效果，建议安装 Minecraft AE Pixel 或 Unifont 字体。请从以下链接下载对应字体文件，将其安装至操作系统后，先重启 Bot，再从插件配置中添加或修改对应的字体名称。

- Minecraft AE Pixel 字体下载：[Github](https://github.com/8kateam/astrbot_plugin_picmcmotd/releases/download/0.0.1/Minecraft.AE.ttf)
- Unifont 字体下载：[Unifont 官方网站](https://www.unifoundry.com/unifont/index.html) | [GNU Ftp Server](https://ftp.gnu.org/gnu/unifont/) | [Github](https://github.com/8kateam/astrbot_plugin_picmcmotd/releases/download/0.0.1/unifont-17.0.05.otf)

## 截图

> 下方截图中，Bot 回复消息内所呈现的图片字体均为 Minecraft AE。

![1](https://raw.githubusercontent.com/8kateam/8ka-material/refs/heads/main/picmcmotd/picmcmotd1.png)

![2](https://raw.githubusercontent.com/8kateam/8ka-material/refs/heads/main/picmcmotd/picmcmotd2.png)

![3](https://raw.githubusercontent.com/8kateam/8ka-material/refs/heads/main/picmcmotd/picmcmotd3.png)

## 更新日志

有关本项目的完整更新记录，请参阅 [CHANGELOG.md](/CHANGELOG.md) 文档。

## 依赖

插件根目录已包含 `requirements.txt`，AstrBot 安装插件时会自动安装依赖：

```text
mcstatus>=12.0.5,<13
dnspython>=2.7.0
Pillow>=12.0.0
```

## 致谢

- [`nonebot_plugin_picmcstat`](https://github.com/lgc-NB2Dev/nonebot-plugin-picmcstat) - 上游项目，本仓库自此复刻并重构内容。
- [OpenCode](https://opencode.ai/) - 本项目部分代码使用此 AI 编程工具协助完成，并经由人工审阅。

## LICENSE

本插件基于上游项目 [`nonebot_plugin_picmcstat`](https://github.com/lgc-NB2Dev/nonebot-plugin-picmcstat) (MIT License) 开发。

本项目新增及修改的部分，采用 [GNU Affero General Public License v3.0](/LICENSE) 授权。

完整的 MIT 许可证文本[见此](/LICENSE-UPSTREAM)。
