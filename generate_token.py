# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""Generate JWT token for game client"""
from jose import jwt
from datetime import datetime, timedelta

# Server config (from docker-compose.yml)
JWT_SECRET = "local-dev-secret"
JWT_ALGO = "HS256"

# Token payload
payload = {
    "device_id": "game_client_001",
    "exp": datetime.utcnow() + timedelta(days=30),
    "iat": datetime.utcnow()
}

# Generate token
token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

print("=" * 70)
print("JWT TOKEN FOR GAME CLIENT")
print("=" * 70)
print(f"\nToken:\n{token}\n")
print("=" * 70)
print("\nCopy this token to config.yaml:")
print("server:")
print("  enabled: true")
print("  edge_url: http://localhost:8000")
print(f'  jwt_token: "{token}"')
print('  device_id: "game_client_001"')
print("=" * 70)
