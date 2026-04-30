# gen_rpt

一个可直接放在 GitHub repo 中运行的 **Deep Research 研究报告生成器**。

你可以在 GitHub Actions 里输入一段“选题描述”，然后自动完成这条链路：

1. 用 DeepSeek 生成研究计划
2. 自动做公开网页检索与资料抓取
3. 按 Deep Research 风格组织章节
4. 自动生成咨询风格图卡与数据图表
5. 输出图文并茂的 HTML 研究报告
6. 把报告直接写回当前 repo 的 `reports/` 目录

## 现在已经支持什么

- **Action 输入一句话选题**，自动生成完整研究报告
- **图文并茂**：正文中会自动穿插咨询风格图卡与图表
- **写回 repo**：不是 artifact，而是直接 commit 到仓库
- **DeepSeek Secret 配置位**：支持你自己去 Settings 里配置 API Secret
- **本地运行**：也可以不走 Actions，直接本地 CLI 生成

## 项目结构

```text
gen_rpt/
├── .github/workflows/generate_deep_research.yml
├── gen_rpt/
│   ├── __init__.py
│   ├── deepseek_client.py
│   ├── web_fetch.py
│   ├── graphics.py
│   ├── report_renderer.py
│   ├── research_pipeline.py
│   └── main.py
├── reports/
├── requirements.txt
├── .env.example
└── README.md
```

## 工作流说明

仓库里已经带了一个手动触发的 GitHub Actions：

- Workflow 名称：`Generate Deep Research Report`
- 触发方式：`Actions -> Generate Deep Research Report -> Run workflow`
- 输入参数：
  - `topic`：你的研究选题，可以直接输入一段话
  - `slug`：可选，自定义输出目录名
  - `language`：默认 `zh`
  - `model`：默认 `deepseek-chat`

运行完成后，生成结果会写入：

```text
reports/YYYY-MM-DD-your-topic-slug/
  report.html
  report_payload.json
  research_plan.json
  sources.json
  assets/
    card-1.png
    card-2.png
    chart-1.png
    chart-2.png
```

## DeepSeek API Secret 配置

你要的 Secret 配置入口已经按标准方式预留好了，变量名是：

```bash
DEEPSEEK_API_KEY
```

请到仓库里这样配置：

1. 打开仓库
2. 进入 `Settings`
3. 进入 `Secrets and variables`
4. 点击 `Actions`
5. 新建 secret
6. Name 填：`DEEPSEEK_API_KEY`
7. Value 填你的 DeepSeek API Key

这样 workflow 运行时就会自动读取。

## 本地运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

然后把 `.env` 里的：

```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

改成你自己的 key。

### 3. 执行生成

```bash
export DEEPSEEK_API_KEY=你的key
python -m gen_rpt.main \
  --topic "生成一份关于 AI Agent 市场演进、竞争格局与商业化路径的深度研究报告" \
  --language zh \
  --model deepseek-chat \
  --out-root reports
```

## 报告生成逻辑

当前实现参考了通用的 Deep Research Agent 工作流思路：

- **Plan**：先让模型拆研究目标、读者、章节和检索词
- **Search**：对公开网页做搜索与内容抓取
- **Read**：抽取网页正文，整理为资料池
- **Synthesize**：让模型输出结构化报告 JSON
- **Render**：自动渲染 HTML 报告、咨询风格图卡和图表

## 视觉风格说明

为了满足“图文并茂”的目标，当前实现加入了两类视觉元素：

- **咨询风格图卡**：适合在正文较长时插入，强化关键洞察
- **数据图表**：支持 bar / line / pie 三种基础图表

图卡是程序自动生成的，风格偏咨询汇报页，不依赖额外图片模型。

## 当前版本的边界

当前版本已经能跑通从选题到报告落库的主链路，但你也应该知道它的边界：

- 公开网页搜索依赖通用搜索页面结构，后续可继续增强稳定性
- 图表数据主要来自模型对公开资料的结构化整理，复杂定量研究可继续叠加专门数据源
- 当前输出主格式是 `HTML`，后续可以继续扩展 `Markdown / PDF / PPTX`
- 当前“咨询风格配图”是程序化图卡，不是扩散模型生成的写实图片

## 下一步建议

如果你接下来还要继续迭代，我建议可以继续往这几个方向加：

1. 增加 Tavily / SerpAPI / Firecrawl 等更稳定的检索与抓取层
2. 增加多轮反思和证据校验，提高 Deep Research 质感
3. 增加表格、时间线、市场地图等更丰富的可视化组件
4. 增加 Markdown / PDF / PPTX 多格式导出
5. 增加“章节级二次补图”能力，让每个章节都能更像咨询报告

## 作者

- [@yt-feng](https://github.com/yt-feng)

---

如果你下一步要我继续，我建议直接做两件事：

- 给这个 repo 再补一个 **自动导出 PDF** 的版本
- 或者继续补一个 **更强的 Deep Research 多轮检索/反思 agent** 版本
