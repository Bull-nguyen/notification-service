# notification-service

A lightweight Python integration designed to handle inbound voice webhooks and trigger automated transactional voice notifications using the Telnyx Call Control API.

## System Architecture

```text
[User / Customer] 
       │ (Inbound Call / Trigger Event)
       ▼
[Telnyx Cloud Platform] ◄──(REST API: Outbound Call / TTS)──┐
       │                                                    │
       │ (HTTP POST Webhook Events)                         │
       ▼                                                    │
[Python Flask Webhook Server] ──────────────────────────────┘
