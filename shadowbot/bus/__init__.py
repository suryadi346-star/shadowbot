"""Message bus module for decoupled channel-agent communication."""

from shadowbot.bus.events import InboundMessage, OutboundMessage
from shadowbot.bus.queue import MessageBus

__all__ = ["MessageBus", "InboundMessage", "OutboundMessage"]
