from ragflow_async_sdk.apis.base import BaseAPI
from ragflow_async_sdk.models.system import SystemHealth


class SystemAPI(BaseAPI):
    """
    System-related API endpoints.
    """

    async def healthz(self) -> SystemHealth:
        """
        Check the health status of the system.

        This endpoint does not require authentication.

        Returns:
            SystemHealth: Parsed system health information.
        """
        resp = await self._client.raw_get("/v1/system/healthz")
        data = resp.json()
        return SystemHealth.from_raw(data)
