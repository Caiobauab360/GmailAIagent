# main.py
# Agente de IA para Gmail e Google Calendar usando Gemini

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import google.generativeai as genai

# Escopos necessários para Gmail e Calendar
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
]

CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
GEMINI_API_KEY = 'AIzaSyB3nZTwNEU__hGk07yV9MG2TpMZxSbSFoc'

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)

def authenticate_google():
    """Autentica com o Google e retorna as credenciais."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    # Se não houver credenciais válidas, faz login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva as credenciais para as próximas execuções
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_gmail_service(creds):
    """Retorna o serviço do Gmail autenticado."""
    return build('gmail', 'v1', credentials=creds)


def get_calendar_service(creds):
    """Retorna o serviço do Google Calendar autenticado."""
    return build('calendar', 'v3', credentials=creds)


def get_recent_emails(gmail_service, max_results=5):
    """Busca os e-mails mais recentes da caixa de entrada."""
    results = gmail_service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        msg_data = gmail_service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = msg_data['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(Sem Assunto)')
        from_ = next((h['value'] for h in headers if h['name'] == 'From'), '(Remetente desconhecido)')
        body = get_email_body(msg_data['payload'])
        emails.append({'subject': subject, 'from': from_, 'body': body})
    return emails


def get_email_body(payload):
    """Extrai o corpo do e-mail, mesmo se multipart."""
    import base64
    import quopri
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            elif part['mimeType'].startswith('multipart/'):
                return get_email_body(part)
    else:
        data = payload['body'].get('data')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    return '(Sem corpo de texto)'


def summarize_email_with_gemini(email_body, subject):
    """Resume o conteúdo do e-mail usando Gemini."""
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = f"""
        Resuma o seguinte e-mail de forma concisa e clara:
        
        Assunto: {subject}
        Conteúdo: {email_body}
        
        Forneça um resumo em português com os pontos principais em até 3 frases.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao resumir: {str(e)}"


def get_upcoming_events(calendar_service, max_results=5):
    """Busca os próximos eventos do Google Calendar."""
    from datetime import datetime, timedelta
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indica UTC
    events_result = calendar_service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    return events


def format_event_time(event):
    """Formata a data e hora do evento."""
    start = event['start'].get('dateTime', event['start'].get('date'))
    if 'T' in start:  # Evento com hora
        from datetime import datetime
        dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y às %H:%M')
    else:  # Evento sem hora (dia inteiro)
        from datetime import datetime
        dt = datetime.fromisoformat(start)
        return dt.strftime('%d/%m/%Y (dia inteiro)')


if __name__ == "__main__":
    print("Agente de IA para Gmail e Google Calendar - Inicializando...")
    creds = authenticate_google()
    gmail_service = get_gmail_service(creds)
    calendar_service = get_calendar_service(creds)
    print("Autenticação realizada com sucesso!")

    print("\nLendo os 5 e-mails mais recentes da caixa de entrada...")
    emails = get_recent_emails(gmail_service, max_results=5)
    for i, email in enumerate(emails, 1):
        print(f"\nEmail {i}:")
        print(f"Assunto: {email['subject']}")
        print(f"De: {email['from']}")
        print(f"Corpo:\n{email['body'][:500]}{'...' if len(email['body']) > 500 else ''}")
        
        # Resumir com Gemini
        print(f"\n📝 Resumo (Gemini):")
        summary = summarize_email_with_gemini(email['body'], email['subject'])
        print(summary)
        print("-" * 50)

    print("\n📅 Próximos eventos do Google Calendar:")
    events = get_upcoming_events(calendar_service, max_results=5)
    if not events:
        print("Nenhum evento próximo encontrado.")
    else:
        for i, event in enumerate(events, 1):
            start = format_event_time(event)
            print(f"\nEvento {i}:")
            print(f"📅 {event['summary']}")
            print(f"🕐 {start}")
            if 'description' in event:
                print(f"📝 {event['description'][:200]}{'...' if len(event['description']) > 200 else ''}")
            print("-" * 30) 