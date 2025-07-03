"""
Agente principal para Gmail e Google Calendar
"""

import os
import pickle
from typing import List, Dict, Any
import google.generativeai as genai
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from .tools import GmailTool, CalendarTool


class GmailAIAgent:
    """Agente de IA para Gmail e Google Calendar."""
    
    def __init__(self, credentials_file: str = "credentials.json", token_file: str = "token.json", 
                 gemini_api_key: str = None):
        """
        Inicializa o agente.
        
        Args:
            credentials_file: Caminho para o arquivo credentials.json
            token_file: Caminho para salvar o token de autenticação
            gemini_api_key: Chave da API do Gemini (opcional, pode usar variável de ambiente)
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        
        # Escopos necessários
        self.scopes = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/calendar.readonly',
        ]
        
        # Configurar Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None
        
        # Inicializar serviços
        self.gmail_service = None
        self.calendar_service = None
        self.gmail_tool = None
        self.calendar_tool = None
        
        # Autenticar
        self._authenticate()
    
    def _authenticate(self):
        """Autentica com o Google."""
        creds = None
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
                creds = flow.run_local_server(port=0)
            
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        # Criar serviços
        self.gmail_service = build('gmail', 'v1', credentials=creds)
        self.calendar_service = build('calendar', 'v3', credentials=creds)
        
        # Criar ferramentas
        self.gmail_tool = GmailTool(self.gmail_service)
        self.calendar_tool = CalendarTool(self.calendar_service)
    
    def run(self, prompt: str, max_emails: int = 3, max_events: int = 3) -> str:
        """
        Executa o agente com um prompt.
        
        Args:
            prompt: Prompt para o agente
            max_emails: Número máximo de e-mails para ler
            max_events: Número máximo de eventos para ler
            
        Returns:
            Resposta do agente
        """
        if not self.model:
            return "Erro: API Key do Gemini não configurada. Configure GEMINI_API_KEY ou passe gemini_api_key no construtor."
        
        try:
            # Coletar dados das ferramentas
            emails = self.gmail_tool.execute(max_results=max_emails)
            events = self.calendar_tool.execute(max_results=max_events)
            
            # Preparar detalhes dos e-mails
            email_details = ""
            if emails:
                email_details = "\nDetalhes dos e-mails:\n"
                for i, email in enumerate(emails, 1):
                    email_details += f"\n{i}. Assunto: {email['subject']}\n"
                    email_details += f"   De: {email['from']}\n"
                    email_details += f"   Conteúdo: {email['body'][:200]}...\n"
            
            # Preparar detalhes dos eventos
            event_details = ""
            if events:
                event_details = "\nPróximos eventos:\n"
                for i, event in enumerate(events, 1):
                    event_details += f"\n{i}. {event['summary']} - {event['time']}\n"
                    if event.get('description'):
                        event_details += f"   Descrição: {event['description'][:100]}...\n"
            
            # Criar prompt completo
            full_prompt = f"""
            {prompt}
            
            Dados disponíveis:
            - E-mails: {len(emails)} mensagens
            - Eventos: {len(events)} eventos
            {email_details}
            {event_details}
            
            Analise os dados e forneça insights úteis em português.
            """
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Erro ao executar agente: {str(e)}"
    
    def get_emails(self, max_results: int = 5) -> List[Dict[str, Any]]:
        """Retorna os e-mails mais recentes."""
        return self.gmail_tool.execute(max_results=max_results)
    
    def get_events(self, max_results: int = 5) -> List[Dict[str, Any]]:
        """Retorna os próximos eventos."""
        return self.calendar_tool.execute(max_results=max_results) 