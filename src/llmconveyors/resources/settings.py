"""Settings resource — profile, preferences, API keys, BYO key, usage, webhook."""

from __future__ import annotations

from typing import Any

from llmconveyors.models.settings import (
    APIKeyInfo,
    Preferences,
    Profile,
    UsageSummary,
    WebhookSecretResponse,
)
from llmconveyors.resources._base import AsyncResource, SyncResource


class SettingsResource(SyncResource):
    """Synchronous settings resource."""

    def get_profile(self) -> Profile:
        data = self._client.get("/settings/profile")
        return Profile.model_validate(data)

    def get_preferences(self) -> Preferences:
        data = self._client.get("/settings/preferences")
        return Preferences.model_validate(data)

    def update_preferences(self, request: dict[str, Any]) -> Preferences:
        data = self._client.post("/settings/preferences", json=request)
        return Preferences.model_validate(data)

    def create_api_key(self, request: dict[str, Any]) -> APIKeyInfo:
        data = self._client.post("/settings/platform-api-keys", json=request)
        return APIKeyInfo.model_validate(data)

    def list_api_keys(self) -> list[APIKeyInfo]:
        data = self._client.get("/settings/platform-api-keys")
        if isinstance(data, list):
            return [APIKeyInfo.model_validate(k) for k in data]
        return []

    def revoke_api_key(self, key_hash: str) -> None:
        self._client.delete(f"/settings/platform-api-keys/{key_hash}")

    def rotate_api_key(self, key_hash: str, request: dict[str, Any] | None = None) -> APIKeyInfo:
        data = self._client.post(
            f"/settings/platform-api-keys/{key_hash}/rotate", json=request or {}
        )
        return APIKeyInfo.model_validate(data)

    def get_api_key_usage(self, key_hash: str) -> Any:
        return self._client.get(f"/settings/platform-api-keys/{key_hash}/usage")

    def get_byo_key(self) -> Any:
        return self._client.get("/settings/api-key")

    def set_byo_key(self, request: dict[str, Any]) -> Any:
        return self._client.post("/settings/api-key", json=request)

    def remove_byo_key(self) -> None:
        self._client.delete("/settings/api-key")

    def get_usage_logs(self, *, offset: int = 0, limit: int = 50) -> Any:
        return self._client.get("/settings/usage-logs", params={"offset": offset, "limit": limit})

    def get_usage_summary(self, *, offset: int = 0, limit: int = 50) -> UsageSummary:
        data = self._client.get(
            "/settings/usage-summary", params={"offset": offset, "limit": limit}
        )
        return UsageSummary.model_validate(data)

    def get_webhook_secret(self) -> WebhookSecretResponse:
        data = self._client.get("/settings/webhook-secret")
        return WebhookSecretResponse.model_validate(data)

    def rotate_webhook_secret(self) -> WebhookSecretResponse:
        data = self._client.post("/settings/webhook-secret/rotate", json={})
        return WebhookSecretResponse.model_validate(data)


class AsyncSettingsResource(AsyncResource):
    """Asynchronous settings resource."""

    async def get_profile(self) -> Profile:
        data = await self._client.get("/settings/profile")
        return Profile.model_validate(data)

    async def get_preferences(self) -> Preferences:
        data = await self._client.get("/settings/preferences")
        return Preferences.model_validate(data)

    async def update_preferences(self, request: dict[str, Any]) -> Preferences:
        data = await self._client.post("/settings/preferences", json=request)
        return Preferences.model_validate(data)

    async def create_api_key(self, request: dict[str, Any]) -> APIKeyInfo:
        data = await self._client.post("/settings/platform-api-keys", json=request)
        return APIKeyInfo.model_validate(data)

    async def list_api_keys(self) -> list[APIKeyInfo]:
        data = await self._client.get("/settings/platform-api-keys")
        if isinstance(data, list):
            return [APIKeyInfo.model_validate(k) for k in data]
        return []

    async def revoke_api_key(self, key_hash: str) -> None:
        await self._client.delete(f"/settings/platform-api-keys/{key_hash}")

    async def rotate_api_key(
        self, key_hash: str, request: dict[str, Any] | None = None
    ) -> APIKeyInfo:
        data = await self._client.post(
            f"/settings/platform-api-keys/{key_hash}/rotate", json=request or {}
        )
        return APIKeyInfo.model_validate(data)

    async def get_api_key_usage(self, key_hash: str) -> Any:
        return await self._client.get(f"/settings/platform-api-keys/{key_hash}/usage")

    async def get_byo_key(self) -> Any:
        return await self._client.get("/settings/api-key")

    async def set_byo_key(self, request: dict[str, Any]) -> Any:
        return await self._client.post("/settings/api-key", json=request)

    async def remove_byo_key(self) -> None:
        await self._client.delete("/settings/api-key")

    async def get_usage_logs(self, *, offset: int = 0, limit: int = 50) -> Any:
        return await self._client.get(
            "/settings/usage-logs", params={"offset": offset, "limit": limit}
        )

    async def get_usage_summary(self, *, offset: int = 0, limit: int = 50) -> UsageSummary:
        data = await self._client.get(
            "/settings/usage-summary", params={"offset": offset, "limit": limit}
        )
        return UsageSummary.model_validate(data)

    async def get_webhook_secret(self) -> WebhookSecretResponse:
        data = await self._client.get("/settings/webhook-secret")
        return WebhookSecretResponse.model_validate(data)

    async def rotate_webhook_secret(self) -> WebhookSecretResponse:
        data = await self._client.post("/settings/webhook-secret/rotate", json={})
        return WebhookSecretResponse.model_validate(data)
