from typing import Dict, List
from app.core.tool import Tool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        tid = tool.meta.id
        if tid in self._tools:
            raise ValueError(f"Tool '{tid}' is already registered")
        self._tools[tid] = tool

    def get(self, tool_id: str) -> Tool | None:
        return self._tools.get(tool_id)

    def all(self) -> List[Tool]:
        return list(self._tools.values())

    def categories(self) -> List[str]:
        seen = []
        for t in self._tools.values():
            if t.meta.category not in seen:
                seen.append(t.meta.category)
        return seen

    def search(self, query: str) -> List[Tool]:
        q = query.strip().lower()
        if not q:
            return self.all()
        scored: List[tuple[int, Tool]] = []
        for tool in self._tools.values():
            m = tool.meta
            haystack = " ".join((m.name, m.description, *m.keywords)).lower()
            if q not in haystack:
                continue
            score = 0
            if q in m.name.lower():
                score += 10
            if m.name.lower().startswith(q):
                score += 5
            scored.append((score, tool))
        scored.sort(key=lambda pair: -pair[0])
        return [t for _, t in scored]


registry = ToolRegistry()