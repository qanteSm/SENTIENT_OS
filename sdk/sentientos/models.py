# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class InferenceRequest(BaseModel):
    device_id: str
    message: str
    context: Dict[str, Any] = Field(default_factory=dict)

class InferenceResponse(BaseModel):
    text: str
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    cache: str # 'hit' or 'miss'

class SystemConfig(BaseModel):
    app: str
    env: str
    models: Dict[str, str]
    actions_whitelist: List[str]
    cache_policy: Dict[str, Any]
    rate_limit: Dict[str, int]

class GameEvent(BaseModel):
    """Player activity event"""
    device_id: str
    event_type: str  # 'key_press', 'mouse_click', 'action_executed', etc.
    event_data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: Optional[str] = None
