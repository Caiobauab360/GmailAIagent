"""
Ferramentas para Gmail e Google Calendar
"""

import base64
from datetime import datetime
from typing import List, Dict, Any
from abc import ABC, abstractmethod


class Tool(ABC):
    """Classe base para ferramentas."""
    
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