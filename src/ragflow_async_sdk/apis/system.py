from ragflow_async_sdk.apis.base import BaseAPI
from ragflow_async_sdk.models.system import SystemHealth


class SystemAPI(BaseAPI):

    async def healthz(self) -> SystemHealth:
        """
        Check system health status.

        This endpoint does not require authorization.
        """
        resp = await self._client.raw_get(
            "/v1/system/healthz",
        )

        data = resp.json()
        return SystemHealth.from_raw(data)
