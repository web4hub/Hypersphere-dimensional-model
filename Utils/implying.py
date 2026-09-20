from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
# ============================================================
# Q-LANG SEMANTIC REGISTRY
# ============================================================
@dataclass
class QDefinition:
    name: str
    kind: str
    meaning: str
    capabilities: list[str] = field(default_factory=list)
    implementation: Callable[..., Any] | None = None
class SemanticRegistry:
    def __init__(self):
        self.definitions: dict[str, QDefinition] = {}
        self.operators: dict[str, QDefinition] = {}
    # --------------------------------------------------------
    # Define a Q-Lang object/concept
    # --------------------------------------------------------
    def define(
        self,
        name: str,
        kind: str,
        meaning: str,
        capabilities: list[str] | None = None,
        implementation: Callable[..., Any] | None = None,
    ):
        definition = QDefinition(
            name=name,
            kind=kind,
            meaning=meaning,
            capabilities=capabilities or [],
            implementation=implementation,
        )
        self.definitions[name] = definition
        return definition
    # --------------------------------------------------------
    # Define an operator
    # --------------------------------------------------------
    def define_operator(
        self,
        symbol: str,
        meaning: str,
        implementation: Callable[..., Any],
    ):
        definition = QDefinition(
            name=symbol,
            kind="operator",
            meaning=meaning,
            implementation=implementation,
        )
        self.operators[symbol] = definition
        return definition
    # --------------------------------------------------------
    # Look up meaning
    # --------------------------------------------------------
    def meaning(self, name: str) -> str:
        if name in self.definitions:
            return self.definitions[name].meaning
        if name in self.operators:
            return self.operators[name].meaning
        raise KeyError(f"Unknown Q-Lang concept: {name}")
    # --------------------------------------------------------
    # Execute an operator
    # --------------------------------------------------------
    def execute_operator(self, symbol: str, left: Any, right: Any):
        if symbol not in self.operators:
            raise KeyError(f"Unknown operator: {symbol}")
        operator = self.operators[symbol]
        if operator.implementation is None:
            raise RuntimeError(
                f"Operator {symbol!r} has no implementation"
            )
        return operator.implementation(left, right)
# ============================================================
# Q-LANG RUNTIME
# ============================================================
class QRuntime:
    def __init__(self):
        self.registry = SemanticRegistry()
        self.objects: dict[str, Any] = {}
    # --------------------------------------------------------
    # Create a runtime object
    # --------------------------------------------------------
    def create(self, name: str, value: Any):
        if name not in self.registry.definitions:
            raise NameError(
                f"Q-Lang concept {name!r} has not been defined"
            )
        self.objects[name] = value
        return value
    # --------------------------------------------------------
    # Resolve an object
    # --------------------------------------------------------
    def get(self, name: str):
        if name not in self.objects:
            raise NameError(f"Unknown Q-Lang object: {name}")
        return self.objects[name]
    # --------------------------------------------------------
    # Execute an operator
    # --------------------------------------------------------
    def operate(self, left: Any, symbol: str, right: Any):
        return self.registry.execute_operator(
            symbol,
            left,
            right,
        )
# ============================================================
# Q-LANG ENGINE
# ============================================================
class QLang:
    def __init__(self):
        self.runtime = QRuntime()
    # --------------------------------------------------------
    # Q definition
    # --------------------------------------------------------
    def define(
        self,
        name: str,
        kind: str,
        meaning: str,
        capabilities: list[str] | None = None,
    ):
        return self.runtime.registry.define(
            name=name,
            kind=kind,
            meaning=meaning,
            capabilities=capabilities,
        )
    # --------------------------------------------------------
    # Define an executable operator
    # --------------------------------------------------------
    def operator(
        self,
        symbol: str,
        meaning: str,
        implementation: Callable[..., Any],
    ):
        return self.runtime.registry.define_operator(
            symbol,
            meaning,
            implementation,
        )
    # --------------------------------------------------------
    # Explain a concept
    # --------------------------------------------------------
    def explain(self, name: str):
        if name in self.runtime.registry.definitions:
            definition = self.runtime.registry.definitions[name]
        elif name in self.runtime.registry.operators:
            definition = self.runtime.registry.operators[name]
        else:
            raise NameError(f"Unknown Q-Lang concept: {name}")
        return {
            "name": definition.name,
            "kind": definition.kind,
            "meaning": definition.meaning,
            "capabilities": definition.capabilities,
        }
# ============================================================
# EXAMPLE
# ============================================================
if __name__ == "__main__":
    q = QLang()
    # --------------------------------------------------------
    # Define a new concept dynamically
    # --------------------------------------------------------
    q.define(
        name="Agent",
        kind="Object",
        meaning="An autonomous computational entity",
        capabilities=[
            "reason",
            "plan",
            "execute",
            "verify",
        ],
    )
    # --------------------------------------------------------
    # Define another concept
    # --------------------------------------------------------
    q.define(
        name="Knowledge",
        kind="Object",
        meaning="Structured information with semantic meaning",
        capabilities=[
            "store",
            "retrieve",
            "infer",
        ],
    )
    # --------------------------------------------------------
    # Define a NEW operator
    #
    # A ⊕ B
    #
    # means "merge"
    # --------------------------------------------------------
    q.operator(
        symbol="⊕",
        meaning="Merge two objects",
        implementation=lambda a, b: {
            **a,
            **b,
        },
    )
    # --------------------------------------------------------
    # Create runtime objects
    # --------------------------------------------------------
    q.runtime.create(
        "Agent",
        {
            "name": "RODA",
            "type": "AI",
        },
    )
    q.runtime.create(
        "Knowledge",
        {
            "domain": "Q-Lang",
            "version": 1,
        },
    )
    # --------------------------------------------------------
    # Execute the dynamically defined operator
    # --------------------------------------------------------
    agent = q.runtime.get("Agent")
    knowledge = q.runtime.get("Knowledge")
    result = q.runtime.operate(
        agent,
        "⊕",
        knowledge,
    )
    print("RESULT:")
    print(result)
    # --------------------------------------------------------
    # Ask the language what something means
    # --------------------------------------------------------
    print("\nMEANING:")
    print(q.explain("Agent"))
    print("\nOPERATOR:")
    print(q.explain("⊕"))
