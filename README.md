# Complex Wireline Channel Protection

This project implements a comprehensive solution for securing wireline channels using cryptographic methods and intrusion detection/prevention systems.

## Prerequisites

- Docker & Docker Compose
- Git

## Setup

1. Clone the repository and copy `.env`:
   ```bash
   git clone https://github.com/MaksTsymbal/network-security-system.git
   cd project-root
   cp .env.example .env
   ```
2. Start all services:
   ```bash
   docker-compose up --build -d
   ```
3. Verify endpoints:
   - FastAPI docs: http://localhost:8000/docs
   - Kibana UI:    http://localhost:5601
   - Grafana UI:  http://localhost:3000

## Testing IDS

```bash
python3 scripts/generate_attack.py
```
