# astrbot_plugin_picmcmotd

PicMCMotd 是一个 AstrBot 插件，用于查询 Minecraft 服务器 MOTD 和在线状态，并将结果绘制成图片返回。插件支持 Java 版和基岩版服务器，也可以自动检测服务器类型。

本插件复刻自 [`nonebot_plugin_picmcstat`](https://github.com/lgc-NB2Dev/nonebot-plugin-picmcstat)。

## 功能

- 查询 Minecraft Java 版服务器 MOTD、版本、协议、在线人数、延迟等信息。
- 查询 Minecraft 基岩版服务器 MOTD、版本、在线人数、地图、游戏模式、延迟等信息。
- 支持自动检测 Java 版或基岩版服务器。
- 将查询结果绘制为图片发送。
- 支持通过配置添加正则快捷指令。
- 支持 DNS 和 SRV 记录解析。

## 指令

指令前缀使用 AstrBot 配置文件中定义的唤醒词，默认为 `/`。

| 指令 | 说明 |
| --- | --- |
| `/motd <服务器地址>` | 查询服务器状态。默认自动检测服务器类型；若关闭自动检测，则按 Java 版查询。 |
| `/motdje <服务器地址>` | 强制按 Minecraft Java 版服务器查询。 |
| `/motdpe <服务器地址>` | 强制按 Minecraft 基岩版服务器查询。 |
| `/motdbe <服务器地址>` | `/motdpe` 的别名，强制按基岩版服务器查询。 |
| `/motd` `/motdje` `/motdpe` | 显示使用帮助图。 |

服务器地址必须与指令之间使用空格分隔，例如：

```text
/motd mc.example.com
/motdje mc.example.com:25565
/motdpe be.example.com:19132
```

## 配置

插件提供 `_conf_schema.json`，可在 AstrBot WebUI 中配置：

- `font`：绘图使用的字体列表。
- `show_addr`：是否显示测试地址。
- `show_delay`：是否显示测试延迟。
- `show_mods`：是否显示 Mod 列表。
- `shortcuts`：正则快捷指令列表。
- `resolve_dns`：是否解析 DNS 记录。
- `resolve_dns_ipv6`：是否优先解析并尝试 IPv6。
- `query_twice`：是否查询两次以改善延迟显示。
- `java_protocol_version`：Java 版查询[协议版本](https://zh.minecraft.wiki/w/%E5%8D%8F%E8%AE%AE%E7%89%88%E6%9C%AC?variant=zh-cn)。
- `enable_auto_detect`：`/motd` 是否自动检测服务器类型。

## 依赖

插件根目录已包含 `requirements.txt`，AstrBot 安装插件时会自动安装依赖：

```text
mcstatus>=12.0.5,<13
dnspython>=2.7.0
Pillow
pil-utils>=0.2.2
punycode>=0.2.1
```

## 截图

![1](https://raw.githubusercontent.com/8kateam/8ka-material/refs/heads/main/picmcmotd/picmcmotd1.png)

![2](https://raw.githubusercontent.com/8kateam/8ka-material/refs/heads/main/picmcmotd/picmcmotd2.png)

![3](https://raw.githubusercontent.com/8kateam/8ka-material/refs/heads/main/picmcmotd/picmcmotd3.png)

## 致谢

- **[`nonebot_plugin_picmcstat`](https://github.com/lgc-NB2Dev/nonebot-plugin-picmcstat)** — 上游项目，本仓库自此复刻而来

- **[`opencode`](https://opencode.ai/)** — 本仓库大部分迁移工作由该 AI 编程工具辅助完成
