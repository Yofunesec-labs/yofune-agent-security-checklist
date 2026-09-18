# Crosswalk — MITRE ATLAS

MITRE ATLAS is a living knowledge base of adversary tactics and techniques for AI systems. YASC uses ATLAS on the **attack-technique** side of the model, while YASC controls specify what to enforce and what evidence to collect.

This draft intentionally avoids pretending that every YASC control has a stable one-to-one ATLAS technique. Instead, mappings are maintained for technique families that are directly useful and supported by the reviewed snapshot.

| ATLAS technique | YASC relevance |
|---|---|
| `AML.T0051` Prompt Injection | YAS-02 instruction integrity; YAS-04 tool-output trust; YAS-05 poisoned context |
| `AML.T0010.001` ML Supply Chain Compromise: ML Software | YAS-07 software/tool/extension provenance and integrity |
| `AML.T0010.002` ML Supply Chain Compromise: Data | YAS-05 source provenance/poisoning and YAS-07 data supply chain |

Future releases may expand technique-level mappings after snapshot review. Do not infer certification from this crosswalk.
