#!/usr/bin/env python3
"""
Agente de IA para Gmail e Google Calendar usando Agent Development Kit (ADK)
"""

import os
import sys
from typing import List, Dict, Any
from datetime import datetime, timedelta
import base64
import pickle

# ADK imports
from agent import Agent
from agent.tools import Tool
from agent.models import Model
from agent.memory import Memory

# Google API imports
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Configurações
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
]
CREDENTIALS_FILE = '../credentials.json'
TOKEN_FILE = 'token.json'


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


def create_gmail_calendar_agent():
    """Cria o agente com as ferramentas do Gmail e Calendar."""
    
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
    agent = Agent(
        name="Gmail Calendar Assistant",
        description="Assistente pessoal que lê e-mails e gerencia calendário",
        tools=[gmail_tool, calendar_tool],
        model=Model.GEMINI_PRO,  # Usar Gemini Pro
        memory=Memory()
    )
    
    return agent


def main():
    """Função principal."""
    print("🤖 Iniciando Agente de IA para Gmail e Calendar (ADK)...")
    
    try:
        # Criar agente
        agent = create_gmail_calendar_agent()
        print("✅ Agente criado com sucesso!")
        
        # Exemplo de uso
        print("\n📧 Lendo e-mails...")
        emails = agent.tools[0].execute(max_results=3)
        
        print("\n📅 Lendo eventos do calendário...")
        events = agent.tools[1].execute(max_results=3)
        
        # Usar o agente para processar informações
        prompt = f"""
        Analise os seguintes dados e forneça um resumo executivo:
        
        E-mails recebidos: {len(emails)}
        Próximos eventos: {len(events)}
        
        Forneça insights sobre sua agenda e comunicações recentes.
        """
        
        response = agent.run(prompt)
        print(f"\n🤖 Resposta do Agente:\n{response}")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 