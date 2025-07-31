# AsynNotify

## Cenário: Sistema de Notificações Assíncronas
💡 Contexto geral:
Você está desenvolvendo um sistema distribuído para enviar notificações a usuários em diferentes canais (email, SMS, push) de forma desacoplada e assíncrona.

### Arquitetura de Microserviços
#### 1. notification-request-service
Responsável por receber pedidos de notificação e publicar um evento.

Endpoints:
POST /notify: recebe requisições com:

```json

{
  "user_id": "123",
  "message": "Seu agendamento foi confirmado.",
  "channel": "email"  // ou "sms", "push"
}
```
Comportamento:
- Valida os dados

- Cria um objeto NotificationRequest

- Publica um evento NotificationRequested

#### 2. notification-dispatcher-service
Escuta o evento NotificationRequested e despacha a notificação pelo canal solicitado.

Comportamento:
- Simula o envio da notificação (log, por exemplo)

Apresenta logs como: Enviando email para user_id=123: "Seu agendamento foi confirmado."

🔸 Comunicação:
Simulada via queue.Queue do Python (para treinar eventos de forma leve)