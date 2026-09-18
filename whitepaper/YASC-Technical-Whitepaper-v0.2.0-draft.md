# Yofune Agent Security Checklist 2026

## A Verifiable Security Baseline for Enterprise AI Agents

**Version:** 0.2.0-draft  
**Status:** Public Draft  
**Reference snapshot:** 2026-09-18  
**Maintained by:** Yofune Security Research  
**Document type:** Technical whitepaper and verification methodology

> **Core proposition:** Agent security should be expressed as bounded security claims supported by controls, reproducible verification, and reviewable evidence — not as unqualified statements that an agent is “safe.”

---


## Contents

- Executive Summary
- Sections 1–6: Purpose, threat model, YASC architecture, principles, and the ten domains
- Sections 7–17: Control anatomy, verification, stochastic testing, evidence, YAL, and assurance cases
- Sections 18–22: Test catalog, profiles, continuous assurance, metrics, and worked example
- Sections 23–28: Framework context, provenance, adoption, limitations, roadmap, and conclusion
- Appendices: control/test catalog, reference snapshot, and repository artifacts

---

## Executive Summary

AI agents combine natural-language interpretation with delegated identity, external content, persistent state, tool use, code execution, multi-step planning, inter-agent communication, and real-world side effects. This combination changes the security problem. In a conventional application, data generally remains data and authorization logic is expected to be deterministic. In an agentic system, untrusted data can influence a model-generated plan, a plan can become a tool request, and a tool request can change external systems under a delegated identity.

The security question is therefore not only whether a model can be prompted into undesirable text. The more important questions are whether an attacker can alter goals, cross identity or tenant boundaries, misuse tools, poison persistent context, trigger code or network effects, exploit supply-chain drift, manipulate human approval, or cause cascading behavior — and whether those paths are constrained by enforcement mechanisms outside model preference.

The **Yofune Agent Security Checklist (YASC)** is an engineering baseline for addressing that problem. It intentionally does not define another “Top 10.” Instead, it translates agent-security risks into:

- stable security controls;
- explicit pass criteria;
- reusable verification tests;
- evidence requirements;
- bounded assurance claims;
- architecture-specific profiles; and
- machine-readable artifacts that can be used by CI, assessment tooling, security platforms, and customer assurance workflows.

YASC uses the method:

**Scope -> Attack -> Control -> Verify -> Evidence -> Assurance Claim**

The project currently defines **10 security domains, 52 core controls, 46 reusable verification tests, 8 architecture profiles, YAL-0 through YAL-4 assurance levels, a verification-run format, and an assurance-case format**.

The principal design objective is to make agent security **verifiable**. A policy document can show that a control is intended. A configuration can show that a mechanism exists. Runtime telemetry can show that it operated. Adversarial testing can show that representative attempts to bypass it failed within a defined scope. These are different strengths of evidence, and YASC keeps them separate.

YASC deliberately avoids a single composite “agent security score.” A system can pass many low-impact checks while still containing one catastrophic path to cross-tenant access, arbitrary code execution, unrestricted data egress, or replayable human approval. YASC therefore reports per-control status, achieved assurance, evidence, scope, known gaps, and residual risk.

![YASC verification lifecycle](figures/validation-loop.png)

---

## 1. Purpose, Scope, and Non-Goals

### 1.1 Purpose

YASC is intended for security engineers, platform teams, AI/ML engineers, product security teams, red teams, auditors, enterprise architects, and buyers of agentic systems. It is designed to answer a practical question:

> **What must we be able to check, test, and prove before an AI agent is trusted with consequential capabilities?**

The baseline is vendor-neutral. Product integrations may automate YASC, but the normative control intent and evidence model are not tied to a specific commercial product.

### 1.2 Systems in scope

YASC applies to systems that use one or more models to pursue tasks through planning, context, retrieval, memory, tools, APIs, code execution, browsers, databases, connectors, MCP servers, or communication with other agents. It is relevant whether the system is called an “agent,” “copilot,” “assistant,” “autonomous workflow,” or another product term.

### 1.3 Non-goals

YASC is not:

- a claim that every AI risk can be reduced to cybersecurity controls;
- a replacement for privacy, safety, legal, sectoral, or organizational governance;
- a model benchmark or generic ranking of model vendors;
- a certification scheme in this draft;
- a guarantee that passing finite tests proves absence of vulnerabilities;
- a reproduction of OWASP, NIST, MITRE, ISO, or MCP normative material.

External frameworks are used as dated references and mappings. YASC control prose and verification structure are independently written.

### 1.4 Normative language

Where this whitepaper uses **must**, **should**, or **may**, they describe YASC expectations for a system claiming conformance to a control or profile. External standards retain their own normative definitions.

---

## 2. Why Agent Security Is Different

Agentic systems collapse several traditionally separate security planes into one execution loop:

1. **Instruction plane** — prompts, policies, goals, retrieved instructions, tool output, peer-agent messages.
2. **Identity plane** — user identity, agent identity, service identity, delegated credentials, impersonation.
3. **Data plane** — RAG, memory, files, databases, SaaS data, browser content, tickets, repositories.
4. **Action plane** — tool calls, API writes, transfers, email sends, deployments, shell commands, database changes.
5. **Control plane** — policy engines, approvals, gateways, sandboxes, IAM, egress controls, rate and budget limits.
6. **Evidence plane** — traces, policy decisions, approvals, downstream receipts, alerts, incident artifacts.

A failure can move across these planes. For example, a malicious instruction hidden in a document can be retrieved as “data,” interpreted as an instruction, alter a plan, cause a tool call, and produce a privileged side effect. If the same model that interprets the hostile content is also trusted to decide whether the action is authorized, the security boundary is circular.

YASC therefore adopts a central principle:

> **Reasoning may propose an action; authorization must be enforced at the action boundary.**

This does not mean the model is irrelevant to security. Model behavior is an important layer. It means that high-impact security properties should not depend solely on the model consistently choosing to refuse.

---

## 3. Threat Model

### 3.1 Adversaries and failure sources

YASC assumes that harmful behavior may originate from:

- an explicitly malicious user;
- a legitimate but over-privileged user;
- attacker-controlled external content;
- compromised or malicious tools/MCP servers;
- poisoned retrieval or memory;
- compromised dependencies, plugins, skills, or packages;
- a spoofed or compromised peer agent;
- stale, over-broad, or mis-issued credentials;
- unsafe model behavior without a deliberate attacker;
- operator over-trust or approval confusion;
- infrastructure faults, retries, partial failure, or race conditions;
- security-control drift after upgrades.

### 3.2 Protected assets

Protected assets can include credentials, confidential data, regulated data, source code, business systems, customer records, money movement, email and messaging authority, deployment authority, cloud resources, local files, browser sessions, and the integrity of future agent behavior.

### 3.3 Trust boundaries

YASC requires explicit treatment of trust boundaries rather than assuming that all text entering model context has the same authority.

![Reference Agent Trust Boundary Map](figures/trust-boundary.png)

At each meaningful boundary, the assessment should identify:

- **Identity:** who or what is acting?
- **Data:** what information is crossing?
- **Instruction:** can the input change goals or policy?
- **Privilege:** what authority is available after crossing?
- **Trust:** why is the source believed?
- **Evidence:** what record proves the decision and outcome?

### 3.4 High-impact actions

YASC uses the term **high-impact action** for an action whose misuse can create significant security, financial, privacy, operational, or customer harm. Examples include deleting or publishing data, changing permissions, sending external messages, moving money, deploying code, executing shell commands, modifying production state, exporting sensitive data, and granting access.

Organizations should classify high-impact actions explicitly. Classification should consider not only the tool name but also parameters, target, volume, reversibility, destination, and data sensitivity. A generic `database.query` tool may be low impact for a read-only synthetic database and critical when it can mutate production customer records.

---

## 4. YASC Architecture

YASC is built as five connected layers.

### 4.1 Core Baseline

The core baseline contains stable controls that should change slowly. Controls are grouped into ten domains and identified as `YAS-XX.YY`.

### 4.2 Security Profiles

Profiles specialize the baseline for architectures such as MCP, RAG, coding agents, browser agents, data agents, customer-service agents, multi-agent systems, and enterprise copilots. A profile adds context-specific expectations without forcing rapidly changing protocol details into the core baseline.

### 4.3 Verification Tests

Reusable tests are identified as `YAT-CATEGORY-NNN`. A test is not just an attack prompt; it defines purpose, preconditions, procedure, expected result, evidence, mapped controls, and safety conditions.

### 4.4 Evidence and Assessment Artifacts

Machine-readable assessment and verification-run schemas allow a result to be transported independently from a particular testing product. Evidence references can point to logs, traces, policy decisions, screenshots, downstream records, hashes, or controlled evidence packages.

### 4.5 Assurance Cases

An assurance case binds a claim to scope, controls, verification runs, evidence, assumptions, known gaps, residual risk, and achieved YAL. This prevents collections of screenshots from being mistaken for a security argument.

---

## 5. Security Principles

YASC uses the following principles across all domains:

1. **Treat external instructions as untrusted.** Content is not authority merely because the model can read it.
2. **Use least agency.** An agent should not possess capabilities unnecessary for its task.
3. **Use least privilege.** Tool and resource permissions should be bounded independently of the model.
4. **Verify before act.** High-impact effects should be evaluated at the enforcement boundary immediately before execution.
5. **Separate reasoning from authorization.** The model may recommend; deterministic policy should decide protected actions.
6. **Preserve provenance.** Trust labels and origin should survive retrieval, memory, transformation, delegation, and tool output.
7. **Assume tools and peers can fail or be malicious.** Tool output and agent messages are inputs, not trusted policy.
8. **Bind human approval to exact actions.** Approval should be informed, attributable, non-replayable, and invalidated by material parameter changes.
9. **Make actions observable.** Security decisions and side effects need correlated evidence.
10. **Design for containment.** Revocation, cancellation, isolation, rollback, and kill switches must be designed and tested before an incident.
11. **Make assurance bounded.** Every claim has a scope, version state, evidence date, and limitations.
12. **Revalidate on material change.** Security evidence does not survive upgrades automatically.

---

## 6. The Ten Security Domains

### YAS-01 — Agent Inventory & Boundary

**Core question:** What can the agent access, trust, change, and affect?

**Principle:** Know the agent, its capabilities, dependencies, data paths, and trust boundaries before testing behavior.

Security testing is unreliable when the assessor does not know which agent, model, tools, identities, data stores, memories, environments, or dependencies are actually reachable. Inventory and trust-boundary work therefore precedes adversarial testing.

**`YAS-01.01` — Agent Inventory**  ·  Severity: medium  ·  Target assurance: `YAL-2`

**`YAS-01.02` — Capability & Dependency Inventory**  ·  Severity: high  ·  Target assurance: `YAL-3`

**`YAS-01.03` — Trust Boundary Map**  ·  Severity: high  ·  Target assurance: `YAL-2`

**`YAS-01.04` — Data Classification & Flow**  ·  Severity: high  ·  Target assurance: `YAL-3`

**`YAS-01.05` — Environment & Tenant Boundary**  ·  Severity: critical  ·  Target assurance: `YAL-4`


### YAS-02 — Goal & Instruction Integrity

**Core question:** Who can change the agent’s goals or instructions?

**Principle:** Treat instructions as data with provenance; authorization must not be delegated to model judgment alone.

Agent goals are constructed from multiple instruction sources. The domain focuses on preventing lower-trust content from becoming authorization and on ensuring material goal changes require an authorized path.

**`YAS-02.01` — Instruction Hierarchy Enforcement**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-02.02` — Untrusted Content Separation**  ·  Severity: high  ·  Target assurance: `YAL-4`

**`YAS-02.03` — Goal Change Authorization**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-02.04` — Prompt Injection Resistance**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-02.05` — Plan-to-Action Intent Binding**  ·  Severity: high  ·  Target assurance: `YAL-3`


### YAS-03 — Identity & Privilege

**Core question:** Under whose identity does the agent act, and with what authority?

**Principle:** Use dedicated identities, least privilege, constrained delegation, and short-lived credentials.

Agents act through identities that may outlive a single request and may be delegated across tools. Dedicated identities, scoped credentials, explicit delegation, issuer validation, rotation, and revocation constrain the blast radius.

**`YAS-03.01` — Dedicated Agent Identity**  ·  Severity: high  ·  Target assurance: `YAL-3`

**`YAS-03.02` — Least Privilege**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-03.03` — Credential Isolation**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-03.04` — Delegation & Impersonation Control**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-03.05` — Credential Lifetime, Rotation & Revocation**  ·  Severity: high  ·  Target assurance: `YAL-3`


### YAS-04 — Tool & MCP Security

**Core question:** Which tools can the agent call, and how are those calls authorized?

**Principle:** Tools are security boundaries. Validate inputs, authenticate servers, authorize high-impact actions, and distrust outputs.

Tools convert language into effects. This domain treats tool catalogs, schemas, server authenticity, authorization, outputs, and protocol-specific controls as security boundaries rather than convenience interfaces.

**`YAS-04.01` — Tool & MCP Inventory**  ·  Severity: high  ·  Target assurance: `YAL-3`

**`YAS-04.02` — Tool Schema & Parameter Validation**  ·  Severity: high  ·  Target assurance: `YAL-4`

**`YAS-04.03` — Sensitive Tool Authorization**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-04.04` — Tool Output Trust Boundary**  ·  Severity: high  ·  Target assurance: `YAL-4`

**`YAS-04.05` — MCP Server Authenticity & Provenance**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-04.06` — MCP Authorization Hardening**  ·  Severity: critical  ·  Target assurance: `YAL-4`


### YAS-05 — Data, RAG & Memory

**Core question:** What information does the agent trust now and later?

**Principle:** Attach provenance and authorization to retrieved and persistent context; contain poisoning and cross-tenant leakage.

Retrieved and persisted context can influence future behavior. Provenance, write authorization, tenant isolation, deletion, minimization, and poison resistance are necessary because memory creates time-shifted attack paths.

**`YAS-05.01` — Source Provenance & Trust Labels**  ·  Severity: high  ·  Target assurance: `YAL-3`

**`YAS-05.02` — Retrieval Authorization & Tenant Isolation**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-05.03` — Memory Write Authorization**  ·  Severity: high  ·  Target assurance: `YAL-4`

**`YAS-05.04` — Memory Poisoning Resistance**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-05.05` — Memory Retention, Deletion & Revocation**  ·  Severity: high  ·  Target assurance: `YAL-3`

**`YAS-05.06` — Context Minimization & Sensitive Data Handling**  ·  Severity: high  ·  Target assurance: `YAL-3`


### YAS-06 — Code & Execution

**Core question:** What code, commands, files, and network operations can the agent execute?

**Principle:** Isolate execution, constrain interpreters, restrict egress, and validate artifacts before side effects occur.

Coding and browser agents may cross from text generation into operating-system, filesystem, interpreter, or network effects. Sandboxing and egress restriction reduce the consequence of model and dependency failures.

**`YAS-06.01` — Execution Surface Inventory**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-06.02` — Sandbox & Process Isolation**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-06.03` — Command Construction & Interpreter Safety**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-06.04` — Filesystem & Network Egress Restriction**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-06.05` — Artifact & Dependency Execution Gate**  ·  Severity: high  ·  Target assurance: `YAL-4`


### YAS-07 — Agentic Supply Chain

**Core question:** Can models, tools, skills, servers, packages, or data dependencies be trusted?

**Principle:** Track provenance, pin dependencies, inventory components, and review changes across the agentic stack.

The agentic supply chain includes models, prompts/configuration, tools, MCP servers, skills, extensions, packages, SDKs, and data dependencies. Trust must be versioned and changes must not silently inherit previous assurance.

**`YAS-07.01` — Model & Provider Provenance**  ·  Severity: high  ·  Target assurance: `YAL-2`

**`YAS-07.02` — Tool, MCP, Skill & Plugin Dependency Pinning**  ·  Severity: high  ·  Target assurance: `YAL-3`

**`YAS-07.03` — AIBOM/SBOM & Component Traceability**  ·  Severity: medium  ·  Target assurance: `YAL-2`

**`YAS-07.04` — Security Update & Review Lifecycle**  ·  Severity: high  ·  Target assurance: `YAL-2`

**`YAS-07.05` — Extension Integrity & Secret Hygiene**  ·  Severity: critical  ·  Target assurance: `YAL-4`


### YAS-08 — Multi-Agent Communication

**Core question:** Can agents authenticate each other and limit delegated authority?

**Principle:** Authenticate peers, constrain delegation, label trust, validate messages, and prevent cascading failures.

Multi-agent systems introduce identity, message-integrity, delegation, depth, fan-out, trust-propagation, and cascading-failure risks. Authority must not grow simply because tasks are delegated.

**`YAS-08.01` — Agent-to-Agent Authentication**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-08.02` — Inter-Agent Message Schema & Integrity**  ·  Severity: high  ·  Target assurance: `YAL-4`

**`YAS-08.03` — Delegation Scope & Depth Limits**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-08.04` — Trust Propagation & Taint Tracking**  ·  Severity: high  ·  Target assurance: `YAL-3`

**`YAS-08.05` — Cascading Failure Isolation**  ·  Severity: critical  ·  Target assurance: `YAL-4`


### YAS-09 — Human Control & Approval

**Core question:** When must a person decide, and what exactly are they approving?

**Principle:** High-impact actions require informed, non-replayable approval that is bound to the exact action.

Human-in-the-loop is not automatically safe. The human must see the relevant action, target, scope, provenance, and risk; the approval must then be bound to exactly what executes.

**`YAS-09.01` — High-Impact Human Approval**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-09.02` — Informed Approval Context**  ·  Severity: high  ·  Target assurance: `YAL-3`

**`YAS-09.03` — Approval Binding & Anti-Replay**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-09.04` — Cancellation, Rollback & Safe Abort**  ·  Severity: high  ·  Target assurance: `YAL-3`

**`YAS-09.05` — Human Trust Calibration**  ·  Severity: high  ·  Target assurance: `YAL-3`


### YAS-10 — Detection, Response & Containment

**Core question:** Can unsafe behavior be detected, reconstructed, and stopped?

**Principle:** Capture correlated evidence, detect policy violations, preserve audit integrity, and provide a tested kill switch.

Without complete telemetry and tested containment, organizations cannot know whether controls worked, investigate failures, or stop a runaway system. Observability is part of the control architecture, not an afterthought.

**`YAS-10.01` — Security Event Telemetry**  ·  Severity: high  ·  Target assurance: `YAL-3`

**`YAS-10.02` — Trace Correlation & Evidence Completeness**  ·  Severity: high  ·  Target assurance: `YAL-3`

**`YAS-10.03` — Policy Violation & Anomaly Detection**  ·  Severity: high  ·  Target assurance: `YAL-4`

**`YAS-10.04` — Containment & Kill Switch**  ·  Severity: critical  ·  Target assurance: `YAL-4`

**`YAS-10.05` — Incident Evidence Retention & Integrity**  ·  Severity: high  ·  Target assurance: `YAL-3`



---

## 7. Anatomy of a YASC Control

A control is designed to be testable rather than merely aspirational. The canonical fields are:

- **ID and title** — stable reference.
- **Objective** — desired security property.
- **Applies when** — applicability boundary.
- **Threat** — failure/attack path addressed.
- **Check** — implementation-level inspection or verification approach.
- **Adversarial tests** — reusable YAT procedures mapped to the control.
- **Evidence** — artifacts needed to support the claim.
- **Pass criteria** — condition that must be satisfied within scope.
- **Mappings** — external framework cross-references.
- **Target assurance** — expected evidence depth for this draft.

### 7.1 Representative control: YAS-04.03 Sensitive Tool Authorization

**Security objective:** A high-impact tool call must be authorized independently of the model’s preference to execute it.

**Threat:** An attacker uses direct injection, indirect injection, poisoned context, peer-agent influence, or plan manipulation to cause a sensitive action.

**Check:** Identify the real enforcement point. Verify that the tool gateway, policy engine, downstream API, or equivalent can deny the call even when the agent requests it.

**Adversarial verification:** Attempt the action without valid approval; attempt approval replay; mutate parameters after approval; try to invoke the same capability through another tool path.

**Expected result:** The system blocks the request or requires a fresh, authorized, action-bound approval. No protected side effect occurs before authorization.

**Evidence:** tool request, agent/task identity, policy decision, approval event where applicable, tool/downstream response, side-effect evidence, trace ID, timestamp, version state.

This structure is intentionally more demanding than a checkbox reading “use least privilege” or “require human approval.”

---

## 8. Verification Is More Than Jailbreak Testing

OWASP’s 2026 red-teaming guidance distinguishes meaningful testing of advanced agent systems from superficial jailbreak-only exercises and explicitly calls out tool semantics, MCP, multi-agent behavior, privilege escalation, indirect injection, and human-in-the-loop bypass as relevant areas. YASC adopts the same broad engineering reality while defining its own machine-readable test and evidence structure.[R3]

A YASC verification activity should try to **falsify a bounded security claim**. The question is not “can I make the model say something weird?” but “can I cross the specific trust or authorization boundary that this control claims to protect?”

### 8.1 Four claim layers

YASC separates four cumulative layers:

1. **Defined** — the requirement or design exists.
2. **Enforced** — an implementation applies it.
3. **Observed** — runtime evidence shows it operating.
4. **Adversarially verified** — representative attempts to bypass it fail within scope.

A team can therefore say, for example, that memory deletion is YAL-2 while sensitive-action approval is YAL-4. This is more informative than averaging both into a single score.

### 8.2 Verification modes

A serious assessment can use multiple modes:

**Design review** — Establishes: intended architecture. Example: approval requirement in design.

**Configuration inspection** — Establishes: mechanism is configured. Example: IAM/policy rule exists.

**Positive test** — Establishes: legitimate path works. Example: approved send succeeds.

**Negative test** — Establishes: prohibited path is denied. Example: unapproved send blocked.

**Adversarial test** — Establishes: realistic bypass attempts fail. Example: indirect injection cannot authorize send.

**Fault injection** — Establishes: failure mode is safe. Example: approval service outage does not fail open.

**Runtime observation** — Establishes: control operates in workload. Example: policy decisions visible in traces.

**Recovery exercise** — Establishes: containment is usable. Example: kill switch revokes active authority.


### 8.3 Positive controls are required

Blocking everything is not proof of a correct security control. Adversarial tests should include a benign control case so reviewers can distinguish intentional security enforcement from a broken integration.

### 8.4 Enforcement independence

For high-impact actions, a strong architecture places the final authorization outside the same probabilistic reasoning process that may have been influenced by hostile content. Examples include IAM policy, policy-as-code, a tool gateway, database row-level security, sandbox boundaries, network egress policy, and downstream authorization.

Model refusal remains useful defense in depth. It should not be confused with an independent authorization boundary.

---

## 9. Verification Quality Dimensions

YASC avoids a test-quality score. Instead, an assessment should describe several dimensions separately.

### 9.1 Boundary coverage

State which boundary the test actually exercised: instruction, identity, tenant, data, tool, execution, peer-agent, approval, telemetry, or supply chain. Tests that never reach the enforcement point cannot prove that enforcement works.

### 9.2 Environmental fidelity

Record whether the test ran in a component harness, integration environment, production-like staging, or bounded production-safe context. A staging pass does not automatically carry over if production has different models, prompts, policies, tools, identities, network routes, data sources, or feature flags.

### 9.3 Reproducibility

Record sufficient version and configuration state to reproduce the run: application build, model/provider/version, prompt/config hash, policy version, tool/MCP versions, retrieval configuration, environment, trial count, corpus reference, and trace identifiers.

### 9.4 Adversarial strength

The value of an adversarial test depends on threat relevance, not raw payload count. Useful escalation can include indirect content, multi-turn adaptation, identity manipulation, chained tools, representation transformations, delayed memory activation, delegated execution, or a compromised dependency.

### 9.5 Evidence integrity

Evidence supporting a significant claim should be attributable, time-correlated, access-controlled, and tamper-evident according to impact. A screenshot without a trace identifier or version state may be useful context but is weak evidence of an enforcement claim.

### 9.6 Temporal freshness

Assurance is tied to system state. A model upgrade, prompt change, policy update, new MCP server, altered tool schema, new retrieval source, changed identity configuration, or new sandbox image may invalidate previous results.

---

## 10. Testing Stochastic Agents

Agent behavior is often probabilistic. Treating one successful run as proof is statistically unsound.

For stochastic paths, YASC recommends recording:

- trial count `n`;
- observed security failures `k`;
- whether state is reset between trials;
- model/version and inference settings where available;
- attack variant set;
- observed failure rate `k/n`;
- confidence interval when a quantitative claim is useful.

If zero failures are observed, the approximate statistical **rule of three** gives an upper 95% bound of about `3/n` for the true failure probability under common assumptions. Therefore 0 failures in 30 trials does **not** imply a zero failure probability; an upper bound on the order of 10% is still compatible with the observation.

This is not a requirement to turn YASC into a statistical benchmark. The purpose is to prevent false certainty from tiny samples. A critical authorization boundary should ideally be deterministic even when the agent’s proposal is stochastic.

### 10.1 Repeated trials

Repeated trials are especially appropriate when:

- model sampling affects planning;
- the same hostile content can produce different tool sequences;
- multi-agent routing varies;
- retrieval is non-deterministic;
- the attacker can adapt across turns;
- race conditions or timing affect the result.

### 10.2 State reset

Testers must state whether memory, caches, conversation history, tasks, tokens, and downstream data were reset between trials. Otherwise repeated runs may not be independent and may test persistence rather than probability.

---

## 11. Metamorphic, Differential, and Compositional Testing

### 11.1 Metamorphic testing

Security decisions should remain stable when the representation changes but the authorization meaning does not. YASC therefore includes semantically equivalent transformations such as paraphrase, translation, encoding, markdown/HTML/JSON wrapping, multi-turn splitting, or equivalent tool argument forms.

This helps reveal defenses that recognize one lexical pattern but fail at the actual trust boundary.

### 11.2 Differential security regression testing

A previously approved test corpus should be re-run across material changes to model, prompt, policy, agent framework, tool/MCP server, retrieval pipeline, sandbox, or identity configuration. The goal is not to rank models; it is to detect a regression before the new configuration inherits old assurance.

### 11.3 Compositional tests

Many serious failures require several individually plausible steps. Example chains include:

`external document -> memory write -> later retrieval -> tool call -> external egress`

and:

`agent A -> delegated agent B -> MCP server -> database -> browser/upload`.

YASC recommends tracking identity, delegated authority, provenance, trust label, and evidence across every hop. Authority must not increase merely because work moves between components.

---

## 12. Fault Injection, Failure Semantics, and Containment

Security controls can disappear during partial outage if fallback behavior is not designed explicitly. YASC therefore treats resilience as part of security verification.

Representative fault tests include:

- policy engine unavailable;
- approval service unavailable;
- identity provider stale or unreachable;
- downstream timeout after side effect begins;
- retry and duplicate execution;
- telemetry pipeline loss;
- MCP server replacement/version mismatch;
- sandbox resource exhaustion;
- peer-agent fan-out, loop, or partial failure;
- queued work that continues after a kill switch.

For every high-impact path, the architecture should specify **fail-open versus fail-closed behavior**. A security dependency outage should not silently expand authority.

### 12.1 Kill-switch validation

The existence of a UI button labeled “Stop” is not sufficient. Testers should measure:

- containment invocation time;
- last accepted new action;
- last completed prohibited side effect;
- token/credential revocation time;
- queued task cancellation;
- handling of in-flight actions;
- downstream systems that continue autonomously;
- restart behavior and stale state.

This converts “we have a kill switch” into an observable containment claim.

---

## 13. Evidence Model

A reviewer should be able to reconstruct why a decision was made and what happened next without relying on undocumented oral context.

### 13.1 Minimum Evidence Set

A verification run should collect, as applicable:

1. claim/control and assessment scope;
2. system and environment identity;
3. version state (application, model, prompt/config, policy, tools/MCP);
4. test definition and payload/corpus reference;
5. user/agent identity and relevant delegated authority;
6. retrieved or persistent context that materially influenced the path;
7. policy/authorization decision;
8. approval event where applicable;
9. tool request and response;
10. downstream side-effect evidence;
11. trace/correlation IDs and timestamps;
12. verdict and cleanup/rollback result;
13. integrity metadata, hashes, and evidence location where warranted.

### 13.2 Evidence classes

YASC distinguishes design, configuration, runtime, test, side-effect, integrity, and review evidence. Different classes answer different questions; a design diagram is not a substitute for a runtime denial trace, and a log line is not a substitute for a test that attempted the prohibited path.

### 13.3 Evidence privacy

YASC does not require storage of hidden model chain-of-thought. Security evidence should prioritize observable inputs, policy decisions, approvals, tool calls, outputs, and system traces. Internal reasoning or plan summaries should be collected only when exposed by the product, authorized, and necessary. Secrets and personal data should be minimized or redacted without destroying the evidence needed to support the claim.

---

## 14. Yofune Assurance Levels (YAL)

![Yofune Assurance Levels](figures/assurance-ladder.png){width=5.8in}

**YAL-0 — Unknown** — No usable evidence for the bounded claim

**YAL-1 — Defined** — Requirement/policy/design exists

**YAL-2 — Enforced** — Technical or procedural enforcement exists

**YAL-3 — Observed** — Runtime evidence shows the enforcement operating

**YAL-4 — Adversarially Verified** — Representative negative/adversarial testing supports the claim


### 14.1 Cumulative evidence

YAL levels are cumulative in intent. A YAL-4 claim should still have a defined control, an implemented enforcement mechanism, and runtime evidence. A one-off penetration-test screenshot without configuration or traceability should not be elevated to YAL-4.

### 14.2 Scope-bound assurance

YAL applies to a **claim in a declared scope**, not to a product name. A system may be YAL-4 for one approval path and YAL-2 for a different tool integration. An excluded mobile client, tenant, region, tool, model, or workflow must remain visible as a gap.

### 14.3 Downgrade and expiry

Assurance should be reconsidered when a material component changes, evidence becomes stale, a new attack path invalidates assumptions, or an incident demonstrates that pass criteria no longer hold. An organization may define time-based expiry, but change-based invalidation is essential for fast-moving agent systems.

### 14.4 No composite safety score

YASC intentionally does not define a weighted overall score. Reporting should highlight:

- failed critical/high controls;
- untested applicable controls;
- achieved YAL by control;
- evidence gaps;
- known exceptions;
- residual risk;
- revalidation triggers.

---

## 15. Assurance Cases

An assurance case is the connective tissue between controls and evidence.

A YASC assurance case includes:

- **claim**;
- **scope**;
- **control IDs**;
- **threat/failure paths**;
- **verification runs**;
- **evidence references**;
- **assumptions**;
- **known gaps**;
- **residual risk**;
- **achieved YAL**;
- **assessment date and revalidation triggers**;
- **reviewer information**.

### 15.1 Why assurance cases matter

Teams often collect a large quantity of security material without a clear logical relationship. An assurance case forces the reviewer to ask: “Which exact claim does this log support?” and “What does this test *not* cover?”

### 15.2 Independence

YAL-4 does not require a commercial third-party assessor. However, high-impact claims benefit from review by a person or team sufficiently independent from the implementation owner to challenge assumptions and reproduce the evidence trail.

---

## 16. Verification Run Format

YASC defines `schema/verification-run.schema.json` and `templates/verification-run.yaml`. A run records:

- test and control IDs;
- system/environment/scope;
- version state;
- deterministic/stochastic classification;
- trial count and security failures;
- verdict;
- observations and measurements;
- evidence references and artifact hashes;
- revalidation triggers.

This is intentionally separate from the static test definition. `YAT-TOOL-001` describes **how a class of test should work**; a verification run records **what happened when it was executed against a specific system state**.

---

## 17. Test Verdict Discipline

YASC uses:

- **PASS** — pass criteria met within assessed scope.
- **FAIL** — prohibited behavior occurred or required control did not operate.
- **PARTIAL** — only part of the requirement/scope is satisfied.
- **INCONCLUSIVE** — evidence or execution conditions do not support a valid conclusion.
- **NOT TESTED** — no verification run exists.
- **NOT APPLICABLE** — applicability is explicitly justified and reviewed.

`INCONCLUSIVE` must never be silently converted to PASS. A broken harness, missing log, ambiguous downstream side effect, or telemetry outage can make a result inconclusive even when no visible exploit succeeded.

---

## 18. The 46 Verification Tests

The current test catalog expands beyond prompt injection and includes instruction manipulation, tool misuse, identity, memory, code execution, multi-agent behavior, incident response, approval integrity, supply-chain drift, observability, resilience, differential regression, and metamorphic variants.


### 18.1 Approval

**`YAT-APPROVAL-001` — Approval replay**  ·  Severity: critical  ·  Verify that a previously valid approval cannot be reused for a new or repeated high-impact action.

**`YAT-APPROVAL-002` — Post-approval parameter mutation**  ·  Severity: critical  ·  Verify that approved action semantics are cryptographically or logically bound to the executed parameters.

**`YAT-APPROVAL-003` — Unauthorized or confused approver**  ·  Severity: critical  ·  Verify that approval authority belongs to the correct human principal and cannot be delegated or confused implicitly.


### 18.2 Code Execution

**`YAT-EXEC-001` — Command/interpreter injection**  ·  Severity: critical  ·  Validate controls related to command/interpreter injection.

**`YAT-EXEC-002` — Network egress escape**  ·  Severity: critical  ·  Validate controls related to network egress escape.

**`YAT-EXEC-003` — Unapproved dependency/artifact execution**  ·  Severity: high  ·  Validate controls related to unapproved dependency/artifact execution.

**`YAT-EXEC-004` — Sandbox boundary escape**  ·  Severity: critical  ·  Validate controls related to sandbox boundary escape.


### 18.3 Differential

**`YAT-DIFF-001` — Security differential regression across versions**  ·  Severity: high  ·  Detect security regressions introduced by model, prompt, policy, framework, tool, or retrieval changes.


### 18.4 Incident Response

**`YAT-IR-001` — Emergency containment**  ·  Severity: critical  ·  Validate controls related to emergency containment.

**`YAT-IR-002` — End-to-end evidence reconstruction**  ·  Severity: high  ·  Validate controls related to end-to-end evidence reconstruction.

**`YAT-IR-003` — Security detection coverage**  ·  Severity: high  ·  Validate controls related to security detection coverage.

**`YAT-IR-004` — Audit tamper and retention**  ·  Severity: high  ·  Validate controls related to audit tamper and retention.


### 18.5 Memory Poisoning

**`YAT-MEMORY-001` — Persistent memory poisoning**  ·  Severity: critical  ·  Validate controls related to persistent memory poisoning.

**`YAT-MEMORY-002` — Unauthorized memory write**  ·  Severity: high  ·  Validate controls related to unauthorized memory write.

**`YAT-MEMORY-003` — Cross-tenant retrieval/memory leak**  ·  Severity: critical  ·  Validate controls related to cross-tenant retrieval/memory leak.

**`YAT-MEMORY-004` — Deletion and revocation propagation**  ·  Severity: high  ·  Validate controls related to deletion and revocation propagation.

**`YAT-MEMORY-005` — Provenance laundering**  ·  Severity: high  ·  Validate controls related to provenance laundering.

**`YAT-MEMORY-006` — Delayed memory poison activation**  ·  Severity: critical  ·  Verify that malicious persisted context cannot remain dormant and later alter privileged behavior.


### 18.6 Metamorphic

**`YAT-META-001` — Semantically equivalent adversarial transformation**  ·  Severity: high  ·  Verify that security enforcement is not dependent on one narrow textual representation of an attack.


### 18.7 Multi Agent

**`YAT-MULTI-001` — Spoofed or tainted peer message**  ·  Severity: critical  ·  Validate controls related to spoofed or tainted peer message.

**`YAT-MULTI-002` — Delegation amplification**  ·  Severity: critical  ·  Validate controls related to delegation amplification.

**`YAT-MULTI-003` — Cascading retry/fan-out failure**  ·  Severity: critical  ·  Validate controls related to cascading retry/fan-out failure.


### 18.8 Observability

**`YAT-OBS-001` — Trace completeness under denial and failure**  ·  Severity: high  ·  Verify that security telemetry remains reconstructable when an action is denied or a dependency fails.

**`YAT-OBS-002` — Evidence tamper detection**  ·  Severity: high  ·  Verify that material alteration or deletion of retained security evidence is detectable according to policy.


### 18.9 Privilege

**`YAT-TOOL-006` — Out-of-scope tool authorization**  ·  Severity: critical  ·  Validate controls related to out-of-scope tool authorization.

**`YAT-IDENTITY-001` — Cross-agent credential reuse**  ·  Severity: critical  ·  Validate controls related to cross-agent credential reuse.

**`YAT-IDENTITY-002` — Expired/revoked/wrong-issuer token**  ·  Severity: critical  ·  Validate controls related to expired/revoked/wrong-issuer token.

**`YAT-IDENTITY-003` — Confused-deputy delegation**  ·  Severity: critical  ·  Validate controls related to confused-deputy delegation.

**`YAT-IDENTITY-004` — Cross-tenant access**  ·  Severity: critical  ·  Validate controls related to cross-tenant access.


### 18.10 Prompt Injection

**`YAT-INJECTION-001` — Direct goal override**  ·  Severity: critical  ·  Validate controls related to direct goal override.

**`YAT-INJECTION-002` — Indirect content injection**  ·  Severity: critical  ·  Validate controls related to indirect content injection.

**`YAT-INJECTION-003` — Goal mutation through context**  ·  Severity: critical  ·  Validate controls related to goal mutation through context.

**`YAT-INJECTION-004` — Encoded/obfuscated instruction**  ·  Severity: high  ·  Validate controls related to encoded/obfuscated instruction.

**`YAT-INJECTION-005` — Multi-step social/agent manipulation**  ·  Severity: high  ·  Validate controls related to multi-step social/agent manipulation.


### 18.11 Resilience

**`YAT-RESILIENCE-001` — Timeout and retry amplification**  ·  Severity: critical  ·  Verify that timeouts, retries, and agent fan-out cannot create uncontrolled cascading execution.

**`YAT-RESILIENCE-002` — Partial dependency failure and fail-safe behavior**  ·  Severity: critical  ·  Verify explicit fail-open/fail-closed behavior when authorization, approval, telemetry, or tool dependencies partially fail.

**`YAT-RESILIENCE-003` — Kill-switch race and in-flight action drain**  ·  Severity: critical  ·  Measure whether emergency containment stops queued, in-flight, and newly requested prohibited actions within the intended bound.


### 18.12 Supply Chain

**`YAT-SUPPLY-001` — Unreviewed model or tool version drift**  ·  Severity: high  ·  Verify that material model, tool, MCP server, or dependency changes are detected and enter the required review/revalidation process.

**`YAT-SUPPLY-002` — Artifact integrity mismatch**  ·  Severity: critical  ·  Verify that tampered or substituted executable artifacts/extensions are not trusted as approved components.

**`YAT-SUPPLY-003` — Dependency capability expansion**  ·  Severity: high  ·  Verify that dependency updates cannot silently expand agent capabilities or data access.


### 18.13 Tool Misuse

**`YAT-TOOL-001` — Sensitive action without valid approval**  ·  Severity: critical  ·  Validate controls related to sensitive action without valid approval.

**`YAT-TOOL-002` — Tool schema boundary abuse**  ·  Severity: high  ·  Validate controls related to tool schema boundary abuse.

**`YAT-TOOL-003` — Tool-output instruction injection**  ·  Severity: critical  ·  Validate controls related to tool-output instruction injection.

**`YAT-TOOL-004` — Tool/MCP substitution and name collision**  ·  Severity: critical  ·  Validate controls related to tool/mcp substitution and name collision.

**`YAT-TOOL-005` — Tool-chain exfiltration**  ·  Severity: critical  ·  Validate controls related to tool-chain exfiltration.

**`YAT-TOOL-007` — Duplicate side effect under retry**  ·  Severity: high  ·  Verify that transient failures and retries do not create duplicate high-impact side effects.



---

## 19. Security Profiles

Profiles add requirements where a general baseline would otherwise become too protocol-specific.

### 19.1 MCP Security Profile

The MCP profile is pinned to a dated specification target. The 2026-07-28 MCP release introduced a stateless core and authorization hardening including RFC 9207 issuer validation, issuer-bound client credentials, and a formal move away from Dynamic Client Registration toward Client ID Metadata Documents. The August 22, 2026 roadmap continues to prioritize agent identity and enterprise security.[R4][R5]

YASC therefore verifies, according to applicability:

- server origin and provenance;
- protocol version;
- client/server identity;
- OAuth issuer validation;
- issuer-bound credentials;
- scope and step-up behavior;
- per-server/per-tool authorization where implemented;
- tool schema constraints;
- tool name collision/substitution;
- output trust;
- sensitive-tool approval;
- egress and data exfiltration;
- telemetry and containment.

The profile is updated separately from the stable core because MCP evolves faster than the baseline.

### 19.2 RAG and Memory Profile

This profile distinguishes one-time prompt content, retrieved context, persistent memory, shared memory, and external context. Verification focuses on who can write/read, provenance, tenant separation, deletion/revocation propagation, delayed poison activation, and whether persistent untrusted content can later authorize privileged behavior.

### 19.3 Coding Agent Profile

The coding profile emphasizes sandboxing, command construction, interpreter boundaries, filesystem isolation, network egress, dependency execution gates, secret hygiene, repository provenance, and deployment approval.

### 19.4 Browser Agent Profile

The browser profile treats pages, DOM content, downloads, links, forms, extensions, and web-origin identity as hostile inputs unless explicitly trusted. High-impact form submissions, account changes, purchases, messages, or uploads require action-aware controls.

### 19.5 Multi-Agent Profile

The multi-agent profile focuses on peer authentication, message integrity, delegation depth, authority conservation, trust propagation, task loops, fan-out, cascading failure, and evidence correlation across agents.

---

## 20. Continuous Assurance and Change Management

Agent assurance decays quickly when systems change. YASC recommends using verification as part of delivery and operations rather than as an annual document exercise.

### 20.1 Revalidation triggers

Re-run relevant controls/tests when there is a material change to:

- model or provider;
- system/developer prompts;
- agent framework/orchestrator;
- policy bundle;
- tool/MCP inventory or schema;
- identity scopes/delegation;
- retrieval source or memory implementation;
- sandbox/egress configuration;
- approval UX/semantics;
- detection/telemetry pipeline;
- high-impact action classification;
- critical dependency;
- known attack technique or incident.

### 20.2 CI/CD integration

A mature deployment can divide tests into:

- **per-commit fast checks** — schemas, static policy, unit-level security invariants;
- **pre-release regression** — high-value YAT corpus, differential testing, sandbox and authorization checks;
- **scheduled adversarial verification** — broader attack variants and memory/persistence scenarios;
- **continuous runtime controls** — telemetry, anomaly detection, drift detection, evidence capture;
- **periodic recovery exercises** — containment, revocation, rollback, incident reconstruction.

### 20.3 Security regression gates

A candidate release should not automatically inherit a previous YAL. When a material component changes, the release process should identify which assurance cases depend on that component and re-run the mapped verification set.

---

## 21. Metrics Without False Precision

Useful operational metrics include:

- percentage of applicable controls with evidence;
- percentage of critical controls at target assurance;
- number of applicable controls still not tested;
- number of failed critical/high controls;
- verification coverage by boundary and profile;
- evidence completeness rate;
- mean/percentile containment latency;
- security regression count per release;
- stale assurance cases awaiting revalidation;
- repeated-trial failure counts/rates for stochastic paths;
- time to detect and reconstruct a test incident.

These metrics should support decisions without being collapsed into an assertion that “82/100 means secure.”

---

## 22. Worked Example: Email Agent With MCP Tools

Consider an enterprise agent that reads email and documents, retrieves customer information, and can call an MCP-exposed `send_email` tool.

### 22.1 Scope

The system includes:

- user and agent identities;
- email/document external content;
- persistent task memory;
- customer-data retrieval;
- MCP gateway and mail server;
- human approval UI;
- policy engine;
- telemetry/evidence store.

`send_email` to external recipients is classified as high impact.

### 22.2 Attack path

A hostile document contains an instruction telling the agent to add an attacker-controlled recipient to an otherwise legitimate message and to conceal the addition from the user.

Potential chain:

`document -> retrieved context -> agent plan -> send_email args -> approval UI -> MCP tool -> mail gateway`.

### 22.3 Relevant controls

Representative controls include:

- YAS-02.02 Untrusted Content Separation;
- YAS-02.05 Plan-to-Action Intent Binding;
- YAS-04.03 Sensitive Tool Authorization;
- YAS-04.04 Tool Output Trust Boundary;
- YAS-09.02 Informed Approval Context;
- YAS-09.03 Approval Binding & Anti-Replay;
- YAS-10.02 Trace Correlation & Evidence Completeness.

### 22.4 Verification plan

Run at least:

1. benign approved external send;
2. indirect injection attempting recipient addition;
3. post-approval recipient mutation;
4. approval replay for a second message;
5. equivalent attack phrased/encoded differently;
6. timeout after mail submission to test duplicate sends;
7. kill-switch invocation while sends are queued.

### 22.5 Expected evidence

Capture the document provenance, agent/task identity, intended recipient list, rendered approval summary, approval binding data, policy decision, MCP request, mail-gateway message ID, downstream recipient evidence, trace ID, timestamps, and run/version metadata.

### 22.6 Assurance claim

A defensible claim is bounded:

> For the assessed web approval path and recorded versions, the agent cannot execute an external email send whose material recipients differ from the action approved by an authorized user, based on the mapped tests and evidence.

It would be inappropriate to claim simply:

> “The email agent is secure.”

---

## 23. Framework Context and Mapping Policy

YASC is designed to coexist with established frameworks rather than compete with them.

### 23.1 OWASP Agentic Top 10 2026

OWASP’s Top 10 for Agentic Applications 2026 identifies major agentic risk areas and was developed through collaboration with more than 100 experts and practitioners. YASC uses OWASP identifiers as risk mappings, while defining separate controls, tests, and evidence requirements.[R1]

### 23.2 OWASP Agent Control Standard

The OWASP Agent Control Standard, released September 1, 2026, emphasizes agents being inspectable, traceable, instrumentable, and controllable through runtime policy mechanisms. This supports YASC’s emphasis on observable enforcement rather than black-box trust.[R2]

### 23.3 NIST AI RMF and GenAI Profile

NIST AI RMF 1.0 provides voluntary risk-management functions and is under revision as of the reference snapshot. NIST AI 600-1 provides a Generative AI profile for operationalizing risk management. YASC maps controls to NIST functions but does not claim equivalence or certification.[R6][R7]

### 23.4 NIST SSDF AI Community Profile

NIST SP 800-218A augments the Secure Software Development Framework with AI-specific software-development practices. YASC uses it as lifecycle context, particularly for supply-chain and secure-development concerns, while focusing more directly on deployed agent control verification.[R8]

### 23.5 MITRE ATLAS

MITRE ATLAS is a living knowledge base of adversary tactics and techniques for AI-enabled systems. YASC uses ATLAS to support threat-informed verification and attack-technique mappings, not as a control catalog replacement.[R9]

### 23.6 ISO/IEC 42001

ISO/IEC 42001:2023 specifies requirements for an AI management system. YASC can provide technical assurance evidence that supports an organization’s broader management and governance processes, but it does not reproduce ISO normative text or claim conformance to ISO/IEC 42001.[R10]

---

## 24. Provenance and Originality

The underlying security ideas in YASC have deep precedent. Least privilege, isolation, approval, supply-chain integrity, audit logging, red teaming, and risk management are not proprietary discoveries.

YASC’s intended contribution is the **engineering synthesis**:

- control IDs and stable domain organization for agent systems;
- explicit Threat -> Control -> Test -> Evidence -> Pass Criteria linkage;
- evidence-depth assurance levels;
- machine-readable verification-run records;
- assurance cases with scope/gaps/residual risk;
- stochastic-agent test reporting;
- metamorphic/differential/compositional verification concepts;
- change-triggered continuous revalidation;
- profile-specific controls without destabilizing the core baseline.

External framework text should not be copied into YASC unless clearly quoted and license-compatible. Crosswalks are references, not assertions that YASC invented the mapped risk.

---

## 25. Adoption Guide

### Phase 1 — Inventory and boundaries

Identify agents, capabilities, identities, tools, MCP servers, data, memory, execution surfaces, high-impact actions, and owners. Draw trust boundaries.

### Phase 2 — Define and enforce

Implement least agency/privilege, policy gates, tool validation, tenant isolation, sandboxing, provenance, approval binding, and containment.

### Phase 3 — Instrument evidence

Add trace correlation, policy decision records, approval events, tool/downstream records, version metadata, evidence retention, and integrity protection appropriate to impact.

### Phase 4 — Adversarially verify

Run the relevant YAT corpus and architecture profile. Include benign controls, repeated trials for stochastic paths, multi-step attacks, fault injection, and recovery exercises.

### Phase 5 — Create assurance cases

For critical claims, record exactly what was tested, what evidence supports the claim, what is excluded, and what changes cause revalidation.

### Phase 6 — Continuous assurance

Integrate stable tests into CI/CD, monitor runtime drift, re-run differential tests on upgrades, and exercise containment periodically.

---

## 26. Limitations

YASC has important limitations:

- Finite testing cannot prove the absence of unknown attacks.
- Agent and model behavior may be non-deterministic.
- External services may change without notice.
- Framework mappings can become stale.
- Security depends on implementation quality, not checklist completion alone.
- Safety, privacy, fairness, legal compliance, and domain-specific harms may require controls beyond this baseline.
- Some proprietary systems may not expose enough telemetry for high assurance; that limitation should be reported rather than guessed away.
- A YAL claim is not a certification unless a future certification program defines governance, assessor competence, scope rules, and audit requirements.

---

## 27. Research and Roadmap

Future YASC work should explore:

- standardized action-impact classification;
- evidence signing and portable attestation;
- policy-decision interoperability across agent gateways;
- automated discovery of agent/tool capability graphs;
- stronger quantitative treatment of stochastic security failures;
- adversarial test-corpus governance and freshness;
- formal authority-conservation rules for multi-agent delegation;
- memory provenance and revocation primitives;
- cross-provider agent identity patterns;
- protocol-level conformance profiles for MCP and emerging agent protocols;
- production-safe verification and continuous controls;
- assessor independence and competence requirements for potential certification use.

---

## 28. Conclusion

The defining security property of an enterprise agent is not that it usually produces acceptable text. It is that the system constrains what can become authority, limits what identities and tools can do, preserves provenance, requires meaningful approval for high-impact effects, exposes evidence of every consequential decision, and can be contained when assumptions fail.

YASC therefore treats security as a set of **bounded claims that must survive inspection and attack**.

The durable question is:

> **Which control stopped which failure path, under what system state, and what evidence allows another reviewer to verify that conclusion?**

That is the standard YASC is designed to make operational.

---

# Appendix A — Control and Test Catalog

The normative machine-readable catalog is maintained separately so that the whitepaper remains readable:

- `schema/controls.yaml` — 52 core controls;
- `schema/tests.yaml` — 46 verification tests;
- `docs/control-test-catalog.md` — expanded human-readable catalog;
- `baseline/` — domain-oriented control documents;
- `verification-tests/` — test playbooks by family.

The catalog is versioned with the whitepaper and is part of the same release artifact.

# Appendix B — Reference Snapshot

The references below are informative and dated. Upstream material changes independently from YASC.

1. **[R1] OWASP Top 10 for Agentic Applications 2026.** OWASP GenAI Security Project, published 2025-12-09.  
   https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
2. **[R2] Agent Control Standard (ACS).** OWASP GenAI Security Project, published 2026-09-01.  
   https://genai.owasp.org/resource/agent-control-standard-acs/
3. **[R3] OWASP Vendor Evaluation Criteria for AI Red Teaming Providers & Tooling v1.0.** Published 2026-02-04.  
   https://genai.owasp.org/resource/owasp-vendor-evaluation-criteria-for-ai-red-teaming-providers-tooling-v1-0/
4. **[R4] The 2026-07-28 Specification.** Model Context Protocol Blog, 2026-07-28.  
   https://blog.modelcontextprotocol.io/posts/2026-07-28/
5. **[R5] The New MCP Roadmap.** Model Context Protocol Blog, 2026-08-22.  
   https://blog.modelcontextprotocol.io/posts/mcp-roadmap/
6. **[R6] Artificial Intelligence Risk Management Framework (AI RMF 1.0).** NIST AI 100-1, 2023-01-26.  
   https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
7. **[R7] Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile.** NIST AI 600-1, 2024-07-26.  
   https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
8. **[R8] Secure Software Development Practices for Generative AI and Dual-Use Foundation Models: An SSDF Community Profile.** NIST SP 800-218A, 2024-07-26.  
   https://csrc.nist.gov/pubs/sp/800/218/a/final
9. **[R9] MITRE ATLAS.** Living adversary tactics and techniques knowledge base for AI-enabled systems.  
   https://atlas.mitre.org/
10. **[R10] ISO/IEC 42001:2023 — Artificial intelligence management systems.** ISO.  
    https://www.iso.org/standard/42001
11. **OWASP Practical Guide for Secure MCP Server Development.** Published 2026-02-16.  
    https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/
12. **NIST AI Resource Center (AIRC).** Includes resources supporting testing, evaluation, verification, and validation (TEVV).  
    https://airc.nist.gov/

---

# Appendix C — Repository Artifacts

The Git repository is the source of truth. Key artifacts include:

- `schema/controls.yaml` — control source;
- `schema/tests.yaml` — verification-test source;
- `schema/profiles.yaml` — profile source;
- `schema/assessment.schema.json` — assessment exchange format;
- `schema/verification-run.schema.json` — individual verification execution record;
- `schema/assurance-case.schema.json` — bounded assurance claim;
- `templates/evidence-package.md` — evidence collection template;
- `templates/verification-run.yaml` — run example;
- `templates/assurance-case.yaml` — assurance-case example;
- `docs/validation-model.md` — verification methodology;
- `docs/evidence-model.md` — evidence model;
- `docs/provenance.md` — external basis and originality policy.

**License:** narrative documentation is released under the repository documentation license; code and schemas follow the repository code/schema license. See `LICENSE.md` and `NOTICE`.
