<p align="center">
  <img src="assets/brand/yofune-mark-web.png" alt="Yofune" width="150">
</p>

<p align="center"><strong>Chengdu Yofune Ariake Technology Co., Ltd.</strong><br>
<a href="https://yofunesec.com/">yofunesec.com</a> · <a href="mailto:contact@yofunesec.com">contact@yofunesec.com</a></p>

# Yofune Agent Security Checklist（YASC）

> **一套可验证的 AI Agent 安全基线。**  
> 用 Control、Verification、Evidence 和有边界的 Assurance Claim 表达 Agent 安全。

YASC 的目标不是再定义一套“十大风险”，而是把已有风险转化为 **可检查、可测试、可留证、可复核、可机器读取** 的控制标准。Git 仓库是 Source of Truth，PDF、网站、Excel、客户报告和 KUROSHIO 对接都应该从同一份数据生成。

当前版本：**1.0.0 / Stable Baseline + Executable Reference Harness**  
参考快照日期：**2026-09-18**

## v1.0 已包含什么

- 10 个安全 Domain，52 条 Core Controls；
- 58 个 Verification Test，覆盖 Prompt/Tool/Identity/Memory/Execution/Multi-Agent 以及 Approval、Supply Chain、Observability、Resilience、Differential、Metamorphic 等验证面；
- YAL-0 到 YAL-4 五级 Assurance，并增加 Verification Plan / Run、Evidence Manifest、Assurance Case 与有边界的 Conformance Claim；
- MCP、RAG、Coding Agent、Browser Agent、Data Agent、客服 Agent、Multi-Agent、Enterprise Copilot 共 8 个 Profile；
- OWASP Agentic Top 10 2026、NIST AI RMF / GenAI Profile、MITRE ATLAS 的 Crosswalk；
- `controls.yaml` / `tests.yaml`、JSON Schema、CSV/JSON/Markdown 生成器；
- GitHub Actions 校验、GitHub Pages 静态交互式 Checklist；
- **Agent Adapter / MCP Adapter / Evidence Collector / 实际 Test Runner / Assessment Builder / HTML/PDF 报告生成器 / CI Security Gate；**
- 贡献制度、版本制度、安全披露流程、Release Manifest。


## 技术白皮书

- **英文 PDF：** [`whitepaper/YASC-Technical-Whitepaper-v1.0.0.pdf`](whitepaper/YASC-Technical-Whitepaper-v1.0.0.pdf)
- **中文评审 PDF：** [`whitepaper/YASC-Technical-Whitepaper-v1.0.0.zh-CN.pdf`](whitepaper/YASC-Technical-Whitepaper-v1.0.0.zh-CN.pdf)
- **英文/中文 DOCX：** 位于 [`whitepaper/`](whitepaper/)
- **中文 Markdown：** [`docs/whitepaper.zh-CN.md`](docs/whitepaper.zh-CN.md)


- 完整英文技术白皮书：[`docs/whitepaper.md`](docs/whitepaper.md)
- 中文技术白皮书：[`docs/whitepaper.zh-CN.md`](docs/whitepaper.zh-CN.md)
- 验证模型：[`docs/validation-model.md`](docs/validation-model.md)
- 证据模型：[`docs/evidence-model.md`](docs/evidence-model.md)
- Assurance Case：[`docs/assurance-case.md`](docs/assurance-case.md)
- 来源、原创性与外部依据：[`docs/provenance.md`](docs/provenance.md)

本版把“验证”从攻击样例提升为独立方法体系：区分 Defined / Enforced / Observed / Adversarially Verified，并加入随机性重复试验、Metamorphic/Differential Testing、故障注入、Kill Switch 竞态、证据完整性、Evidence Freshness 与变更触发再验证。

## v1.0 可执行验证栈

- `verification-plan`：在执行前固定 Scope、Test、Oracle、Trial、Evidence、Safety 与 Independence；
- `verification-run`：记录某一次测试对某个精确系统版本到底发生了什么；
- `evidence-manifest`：对证据做 SHA-256 Manifest，并记录来源与完整性信息；
- `assurance-case`：说明哪些证据支持什么有边界的安全 Claim；
- `conformance-claim`：用于分享 scoped Control/Profile/Baseline Result；v1.0 仍不把 PASS 表述为“系统已被认证为绝对安全”；
- `scripts/yasc_harness.py` / `yasc`：可执行 CLI，负责 Adapter 调用、Test Runner、Evidence、Assessment、Report 和 CI Gate；
- `harness/yasc_harness/adapters/`：OpenAI Responses、Anthropic Messages、LangGraph、CrewAI、Generic HTTP、MCP stdio/HTTP 以及 deterministic mock target；
- `harness/scenarios/core.yaml`：58 个 YAT 的自动化/指导式场景注册表；
- `.github/actions/yasc-security-gate/`：可复用 CI Security Gate。

方法文档：[`docs/test-procedure.md`](docs/test-procedure.md)、[`docs/evidence-integrity.md`](docs/evidence-integrity.md)、[`docs/conformance.md`](docs/conformance.md)、[`docs/coverage-model.md`](docs/coverage-model.md)。

Harness 说明：[`harness/README.md`](harness/README.md)、[`docs/harness-architecture.md`](docs/harness-architecture.md)、[`docs/adapters.md`](docs/adapters.md)、[`docs/ci-security-gate.md`](docs/ci-security-gate.md)。

Release 与发布说明：[`releases/v1.0.0/RELEASE_NOTES.md`](releases/v1.0.0/RELEASE_NOTES.md)、[`PUBLISHING.md`](PUBLISHING.md)。GitHub CLI 完成授权后，可以用 `./scripts/publish_github.sh OWNER/yofune-agent-security-checklist --public` 一次完成 main 推送、Pages workflow source 配置与 `v1.0.0` tag 推送。

## 方法论

```text
Scope → Attack → Control → Verify → Evidence → Assurance → Revalidate
```

每条 Control 都包含：适用范围、威胁、检查方法、对抗测试、证据要求、Pass Criteria、Framework Mapping 和目标 YAL。

## Assurance Level

| 等级 | 含义 |
|---|---|
| YAL-0 | Unknown：没有可用证据 |
| YAL-1 | Defined：有制度/设计 |
| YAL-2 | Enforced：已有技术或流程控制 |
| YAL-3 | Observed：可从日志/Trace 证明控制正在生效 |
| YAL-4 | Adversarially Verified：经过主动攻击验证仍然有效 |

我们**不建议给 Agent 一个总安全分**。单个高风险控制失败可能比 49 条低风险控制通过更重要。

## 10 个 Domain

- **YAS-01 Agent Inventory & Boundary** — What can the agent access, trust, change, and affect?
- **YAS-02 Goal & Instruction Integrity** — Who can change the agent’s goals or instructions?
- **YAS-03 Identity & Privilege** — Under whose identity does the agent act, and with what authority?
- **YAS-04 Tool & MCP Security** — Which tools can the agent call, and how are those calls authorized?
- **YAS-05 Data, RAG & Memory** — What information does the agent trust now and later?
- **YAS-06 Code & Execution** — What code, commands, files, and network operations can the agent execute?
- **YAS-07 Agentic Supply Chain** — Can models, tools, skills, servers, packages, or data dependencies be trusted?
- **YAS-08 Multi-Agent Communication** — Can agents authenticate each other and limit delegated authority?
- **YAS-09 Human Control & Approval** — When must a person decide, and what exactly are they approving?
- **YAS-10 Detection, Response & Containment** — Can unsafe behavior be detected, reconstructed, and stopped?


## 快速开始

校验标准并启动交互式 Checklist：

```bash
python -m pip install -r requirements-dev.txt
make check
python -m http.server 8000 -d site
```

运行 v1.0 可执行验证闭环：

```bash
python -m pip install -e ".[pdf]"
make harness-smoke
make harness-mcp-smoke
```

真实 Target 示例已经包含 OpenAI Responses、Anthropic Messages、LangGraph、CrewAI、Generic HTTP Agent 与 MCP。Provider Adapter 默认只观测模型提出的 Tool Call，不由 Harness 自动执行副作用；Provider Model 名称通过 `${OPENAI_MODEL}` / `${ANTHROPIC_MODEL}` 环境变量提供，避免把会变化的模型 ID 硬编码进标准。

也可以直接执行：

```bash
yasc run --plan examples/plans/smoke.yaml --target examples/targets/mock-secure.yaml \
  --out build/yasc/runs --evidence build/yasc/evidence
yasc gate --plan examples/plans/smoke.yaml --runs build/yasc/runs \
  --policy examples/gate-policy.yaml --out build/yasc/gate.json
yasc report --plan examples/plans/smoke.yaml --runs build/yasc/runs \
  --gate-result build/yasc/gate.json --html build/yasc/assessment.html --pdf build/yasc/assessment.pdf
```

然后打开 `http://localhost:8000`。Smoke Flow 同时会生成 Yofune 品牌的 Assessment Report 和带 SHA-256 Manifest 的 Evidence Package。 MCP Smoke Flow 会通过真实的 stdio Adapter 初始化仓库内 MCP Fixture、执行 `tools/list`、收集证据并通过 Critical Severity Gate；它不会调用任何 MCP Tool。

机器可读真源：[`schema/controls.yaml`](schema/controls.yaml)  
测试真源：[`schema/tests.yaml`](schema/tests.yaml)  
MCP Profile：[`profiles/mcp/README.md`](profiles/mcp/README.md)

## 版本与维护

- Major：风险模型/结构发生明显变化；
- Minor：新增 Control / Profile / Verification 能力；
- Patch：文字、链接、Mapping 等非破坏性修复。

每个版本必须记录 Reference Snapshot，避免把“当前映射”误当成永久映射。

**Maintained by Yofune Security Research.**  
发布方：**Chengdu Yofune Ariake Technology Co., Ltd.**  
官网：https://yofunesec.com/  
联系：contact@yofunesec.com
