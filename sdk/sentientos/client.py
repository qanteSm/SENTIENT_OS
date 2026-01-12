import httpx
import logging
from typing import Any, Dict, Optional
from .models import InferenceRequest, InferenceResponse, SystemConfig, GameEvent
from .exceptions import (
    SentientError, AuthenticationError, RateLimitError, 
    SecurityBlockError, CommunicationError
)

logger = logging.getLogger("sentientos_sdk")

class SentientClient:
    def __init__(self, base_url: str, token: str, device_id: str):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.device_id = device_id
        self._headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self._client = httpx.AsyncClient(base_url=self.base_url, headers=self._headers)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()

    async def close(self):
        await self._client.aclose()

    async def get_health(self) -> Dict[str, str]:
        try:
            resp = await self._client.get("/health")
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            raise CommunicationError(f"Health check failed: {e}")

    async def get_config(self) -> SystemConfig:
        try:
            resp = await self._client.get("/v1/config")
            resp.raise_for_status()
            return SystemConfig(**resp.json())
        except httpx.HTTPError as e:
            raise CommunicationError(f"Failed to fetch config: {e}")

    async def infer(self, message: str, context: Optional[Dict[str, Any]] = None) -> InferenceResponse:
        req = InferenceRequest(
            device_id=self.device_id,
            message=message,
            context=context or {}
        )
        
        try:
            resp = await self._client.post("/v1/inference", json=req.model_dump())
            
            if resp.status_code == 401:
                raise AuthenticationError("Invalid or expired token")
            elif resp.status_code == 403:
                detail = resp.json().get("detail", "")
                if "security protocol" in detail:
                    raise SecurityBlockError(f"Blocked by SENTIENT_OS: {detail}")
                raise AuthenticationError(f"Access forbidden: {detail}")
            elif resp.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            
            resp.raise_for_status()
            return InferenceResponse(**resp.json())
            
        except httpx.HTTPError as e:
            raise CommunicationError(f"Inference request failed: {e}")
        except Exception as e:
            if isinstance(e, SentientError):
                raise
            raise SentientError(f"Unexpected error: {e}")
    
    async def send_event(self, event_type: str, event_data: Dict[str, Any] = None) -> bool:
        """
        Send player activity event to server.
        
        Args:
            event_type: Type of event ('key_press', 'mouse_click', 'action_executed', etc.)
            event_data: Event-specific data
            
        Returns:
            True if successful
        """
        event = GameEvent(
            device_id=self.device_id,
            event_type=event_type,
            event_data=event_data or {}
        )
        
        try:
            resp = await self._client.post("/v1/events", json=event.model_dump())
            resp.raise_for_status()
            return True
        except httpx.HTTPError as e:
            logger.warning(f"Event logging failed: {e}")
            return False  # Don't crash game if logging fails
