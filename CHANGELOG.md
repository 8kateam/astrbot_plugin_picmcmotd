## 1.2.0

修复基岩版服务器查询报错（`AttributeError: 'BedrockStatusVersion' object has no attribute 'version'`）：mcstatus 13 重构响应对象时，`BedrockStatusVersion` 的版本号字段由 `version` 更名为 `name`，更新 `draw_bedrock` 中的遗留调用为 `res.version.name`。

## 1.1.0

升级 `mcstatus` 依赖至 14.2.0（`mcstatus>=14.2.0,<15`），适配 v13/v14 的破坏性变更：

- `mcstatus.status_response` 模块更名为 `mcstatus.responses`，Forge 数据的 TypedDict 移至 `mcstatus.responses._raw`，更新相应导入。
- `MinecraftColor`/`Formatting` 枚举按 Java 与基岩版拆分为 `JavaMinecraftColor`/`BedrockMinecraftColor`/`JavaFormatting`/`BedrockFormatting`，MOTD 换行拆分与 BBCode 渲染改为按服务器版本使用对应枚举查表。
- MOTD transformer 已迁入私有模块，`PlainTransformer` 改从 `mcstatus.motd._transformers` 导入，并显式适配其不再有默认值的 `bedrock` 参数。
- 新增的 `InvalidFormatting` 组件（无效格式码）按官方行为直接忽略。
- 补全基岩版专属渲染色表（`h`~`v` 材质色及基岩版灰色），避免基岩版 MOTD 渲染时查表失败。

## 1.0.1

修复渲染彩虹字体时的字符间距过大问题。

## 1.0.0

正式版发布。

- 添加已测试平台的说明。
- 添加 logo 图标。

## 0.1.0

- 重构绘图模块，移除已停更的 `pil-utils` 和 `punycode` 依赖项，使插件能与 Astrbot 4.27.0+ 兼容。

## 0.0.4

- 添加 `command_prefix` 配置项，定义帮助图中显示的指令前缀。仅影响帮助图渲染，实际前缀由 AstrBot 配置管理。
- 尝试修复 Ipv6 查询问题

## 0.0.3

- 修复2个可能影响插件运行稳定性的问题。
- 添加配置项 `query_timeout`，设置服务器查询超时时间，默认为10秒。

## 0.0.2

- 添加 `show_icon`、`show_motd`、`motd1`、`motd2`、`show_playerlist` 配置项，具体用途请查看 README.md 中 **配置** 一节的内容。

## 0.0.1

首个可用版本。
