---
version: "1.0.0"
type: "state_maintenance_protocol"
priority: "critical"

state_file: ".kilo/STATE.md"
template_file: ".kilo/templates/STATE.template.md"

update_strategy: "incremental_patch"
structure_policy: "canonical"

runtime:
  os: "Windows 11"
  shell: "cmd.exe"
  python: "python.exe"
---

# STATE MAINTENANCE PROTOCOL

## PURPOSE

STATE.md IS:

- persistent operational memory
- runtime identity source
- architectural snapshot
- continuity layer between sessions
- known failures registry

STATE.md IS NOT:

- README replacement
- roadmap
- brainstorming area
- speculative planning
- narrative documentation

---

# GOLDEN RULE

SOURCE CODE IS THE ONLY SOURCE OF TRUTH.

IF:
- code says X
- STATE says Y

THEN:
- STATE MUST BECOME X

---

# STRUCTURE POLICY

STATE STRUCTURE IS CANONICAL.

DO NOT:
- reorder sections
- rename sections
- collapse sections
- rewrite entire document
- replace tables with prose

PRESERVE:
- YAML header
- section order
- table formatting
- operational directives
- runtime identity

---

# UPDATE POLICY

ONLY UPDATE:

- versions
- metrics
- active components
- runtime details
- bugs
- workarounds
- recent decisions
- operational truths

PREFERRED STRATEGY:
- patch
- append
- incremental modifications

AVOID:
- full rewrites
- aesthetic refactors
- stylistic rewrites
- narrative expansion

---

# REQUIRED SECTIONS

STATE.md MUST CONTAIN:

1. Runtime Identity
2. Critical Runtime Constraints
3. Known Agent Failure Patterns
4. Recovery Protocol
5. Bootstrap Load Order
6. System State
7. Operational Truths
8. Active Components
9. Embedding Configuration
10. Memory Architecture
11. Ontological Structure
12. Hybrid Retrieval Configuration
13. Recent Design Decisions
14. Known Bugs and Workarounds
15. Operational Directives
16. Context Role

---

# UPDATE WORKFLOW

1. Read current STATE.md
2. Read STATE.template.md
3. Validate canonical structure
4. Compare against source code
5. Patch changed values only
6. Append new decisions chronologically
7. Preserve formatting
8. Preserve tables
9. Validate YAML header
10. Save incrementally

---

# VALIDATION RULES

BEFORE SAVING:

VERIFY:
- section order
- UTF-8 compatibility
- runtime identity
- Windows assumptions
- version consistency
- active components
- config references

NEVER:
- hallucinate modules
- invent architecture
- document nonexistent features
- assume Linux compatibility

---

# KNOWN FAILURE PATTERNS

FREQUENT FAILURES:

| Failure | Correct Behavior |
|---|---|
| Uses python3 | Use python.exe |
| Generates bash commands | Use cmd.exe |
| Assumes Linux paths | Use pathlib + Windows |
| Uses PowerShell syntax | Forbidden |
| Rewrites STATE structure | Preserve canonical layout |
| Converts tables to prose | Preserve tables |

---

# STABILITY DIRECTIVE

STRUCTURAL STABILITY HAS PRIORITY OVER AESTHETIC IMPROVEMENTS.