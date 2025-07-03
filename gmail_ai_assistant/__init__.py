"""
Gmail AI Assistant - Assistente de IA para Gmail e Google Calendar
"""

__version__ = "1.0.0"
__author__ = "Seu Nome"
__email__ = "seu.email@exemplo.com"

from .agent import GmailAIAgent
from .tools import GmailTool, CalendarTool

__all__ = ["GmailAIAgent", "GmailTool", "CalendarTool"] 