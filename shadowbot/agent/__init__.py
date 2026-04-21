"""Agent core module."""

from shadowbot.agent.context import ContextBuilder
from shadowbot.agent.hook import AgentHook, AgentHookContext, CompositeHook
from shadowbot.agent.loop import AgentLoop
from shadowbot.agent.memory import Dream, MemoryStore
from shadowbot.agent.skills import SkillsLoader
from shadowbot.agent.subagent import SubagentManager

__all__ = [
    "AgentHook",
    "AgentHookContext",
    "AgentLoop",
    "CompositeHook",
    "ContextBuilder",
    "Dream",
    "MemoryStore",
    "SkillsLoader",
    "SubagentManager",
]
