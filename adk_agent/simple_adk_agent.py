#!/usr/bin/env python3
"""
Agente de IA simplificado que simula a estrutura do ADK
Usando apenas as bibliotecas que já funcionam
"""

import os
import sys
import pickle
import base64
from datetime import datetime
from typing import List, Dict, Any
from abc import ABC, abstractmethod

# Google APIs
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Gemini
import google.generativeai as genai

# Configurações
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
]
CREDENTIALS_FILE = '../credentials.json'
TOKEN_FILE = 'token.json'
GEMINI_API_KEY = 'AIzaSyB3nZTwNEU__hGk07yV9MG2TpMZxSbSFoc'

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)


class Tool(ABC):
    """Classe base para ferramentas (simula o ADK)."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Executa a ferramenta."""
        pass


class GmailTool(Tool):
    """Ferramenta para ler e-mails do Gmail."""
    
    def __init__(self, gmail_service):
        super().__init__(
            name="read_gmail",
            description="Lê os e-mails mais recentes da caixa de entrada do Gmail"
        )
        self.gmail_service = gmail_service
    
    def execute(self, max_results: int = 5) -> List[Dict[str, Any]]:
        """Executa a leitura dos e-mails."""
        try:
            results = self.gmail_service.users().messages().list(
                userId='me', 
                labelIds=['INBOX'], 
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for msg in messages:
                msg_data = self.gmail_service.users().messages().get(
                    userId='me', 
                    id=msg['id'], 
                    format='full'
                ).execute()
                
                headers = msg_data['payload'].get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(Sem Assunto)')
                from_ = next((h['value'] for h in headers if h['name'] == 'From'), '(Remetente desconhecido)')
                body = self._get_email_body(msg_data['payload'])
                
                emails.append({
                    'subject': subject,
                    'from': from_,
                    'body': body
                })
            
            return emails
        except Exception as e:
            return [{'error': f'Erro ao ler e-mails: {str(e)}'}]
    
    def _get_email_body(self, payload):
        """Extrai o corpo do e-mail."""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                elif part['mimeType'].startswith('multipart/'):
                    return self._get_email_body(part)
        else:
            data = payload['body'].get('data')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        return '(Sem corpo de texto)'


class CalendarTool(Tool):
    """Ferramenta para acessar o Google Calendar."""
    
    def __init__(self, calendar_service):
        super().__init__(
            name="read_calendar",
            description="Lê os próximos eventos do Google Calendar"
        )
        self.calendar_service = calendar_service
    
    def execute(self, max_results: int = 5) -> List[Dict[str, Any]]:
        """Executa a leitura dos eventos."""
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            events_result = self.calendar_service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            formatted_events = []
            
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                if 'T' in start:
                    dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%d/%m/%Y às %H:%M')
                else:
                    dt = datetime.fromisoformat(start)
                    formatted_time = dt.strftime('%d/%m/%Y (dia inteiro)')
                
                formatted_events.append({
                    'summary': event['summary'],
                    'time': formatted_time,
                    'description': event.get('description', '')
                })
            
            return formatted_events
        except Exception as e:
            return [{'error': f'Erro ao ler eventos: {str(e)}'}]


class SimpleAgent:
    """Agente simplificado que simula o ADK."""
    
    def __init__(self, name: str, description: str, tools: List[Tool]):
        self.name = name
        self.description = description
        self.tools = tools
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def run(self, prompt: str) -> str:
        """Executa o agente com um prompt."""
        try:
            # Coletar dados das ferramentas
            tool_results = {}
            for tool in self.tools:
                if tool.name == "read_gmail":
                    tool_results['emails'] = tool.execute(max_results=3)
                elif tool.name == "read_calendar":
                    tool_results['events'] = tool.execute(max_results=3)
            
            # Preparar detalhes dos e-mails
            email_details = ""
            if tool_results.get('emails'):
                email_details = "\nDetalhes dos e-mails:\n"
                for i, email in enumerate(tool_results['emails'], 1):
                    email_details += f"\n{i}. Assunto: {email['subject']}\n"
                    email_details += f"   De: {email['from']}\n"
                    email_details += f"   Conteúdo: {email['body'][:200]}...\n"
            
            # Preparar detalhes dos eventos
            event_details = ""
            if tool_results.get('events'):
                event_details = "\nPróximos eventos:\n"
                for i, event in enumerate(tool_results['events'], 1):
                    event_details += f"\n{i}. {event['summary']} - {event['time']}\n"
                    if event.get('description'):
                        event_details += f"   Descrição: {event['description'][:100]}...\n"
            
            # Criar prompt completo
            full_prompt = f"""
            {prompt}
            
            Dados disponíveis:
            - E-mails: {len(tool_results.get('emails', []))} mensagens
            - Eventos: {len(tool_results.get('events', []))} eventos
            {email_details}
            {event_details}
            
            Analise os dados e forneça insights úteis em português.
            """
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Erro ao executar agente: {str(e)}"


def authenticate_google():
    """Autentica com o Google e retorna as credenciais."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds


def create_simple_agent():
    """Cria o agente simplificado."""
    
    # Autenticar com Google
    print("🔐 Autenticando com Google...")
    creds = authenticate_google()
    
    # Criar serviços
    gmail_service = build('gmail', 'v1', credentials=creds)
    calendar_service = build('calendar', 'v3', credentials=creds)
    
    # Criar ferramentas
    gmail_tool = GmailTool(gmail_service)
    calendar_tool = CalendarTool(calendar_service)
    
    # Criar agente
    agent = SimpleAgent(
        name="Gmail Calendar Assistant",
        description="Assistente pessoal que lê e-mails e gerencia calendário",
        tools=[gmail_tool, calendar_tool]
    )
    
    return agent


def main():
    """Função principal."""
    print("🤖 Iniciando Agente Simplificado (estilo ADK)...")
    
    try:
        # Criar agente
        agent = create_simple_agent()
        print("✅ Agente criado com sucesso!")
        
        # Exemplo de uso
        prompt = """
        Analise meus e-mails e eventos do calendário.
        Forneça um resumo executivo do meu dia e recomendações.
        """
        
        print(f"\n🤖 Executando: {prompt}")
        response = agent.run(prompt)
        
        print(f"\n📋 Resposta do Agente:\n{response}")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 