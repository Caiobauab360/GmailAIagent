#!/usr/bin/env python3
"""
Exemplo simples do uso do Agent Development Kit (ADK)
"""

from agent import Agent
from agent.tools import Tool
from agent.models import Model
from agent.memory import Memory


class SimpleEmailTool(Tool):
    """Ferramenta simples para simular leitura de e-mails."""
    
    def __init__(self):
        super().__init__(
            name="check_emails",
            description="Verifica se há novos e-mails importantes"
        )
    
    def execute(self) -> dict:
        """Simula a verificação de e-mails."""
        return {
            "status": "success",
            "emails_count": 3,
            "important_emails": [
                "Reunião de projeto às 14h",
                "Relatório mensal pronto",
                "Atualização de segurança"
            ]
        }


class SimpleCalendarTool(Tool):
    """Ferramenta simples para simular acesso ao calendário."""
    
    def __init__(self):
        super().__init__(
            name="check_calendar",
            description="Verifica os próximos eventos do calendário"
        )
    
    def execute(self) -> dict:
        """Simula a verificação do calendário."""
        return {
            "status": "success",
            "events_count": 2,
            "upcoming_events": [
                "Reunião de equipe - 15:00",
                "Apresentação cliente - 16:30"
            ]
        }


def main():
    """Demonstra o uso básico do ADK."""
    print("🤖 Exemplo Simples do Agent Development Kit")
    
    # Criar ferramentas
    email_tool = SimpleEmailTool()
    calendar_tool = SimpleCalendarTool()
    
    # Criar agente
    agent = Agent(
        name="Simple Assistant",
        description="Assistente simples para demonstração do ADK",
        tools=[email_tool, calendar_tool],
        model=Model.GEMINI_PRO,
        memory=Memory()
    )
    
    print("✅ Agente criado com sucesso!")
    
    # Exemplo de interação
    prompt = """
    Verifique meus e-mails e eventos do calendário.
    Depois, me dê um resumo do meu dia.
    """
    
    print(f"\n🤖 Executando: {prompt}")
    response = agent.run(prompt)
    
    print(f"\n📋 Resposta do Agente:\n{response}")


if __name__ == "__main__":
    main() 