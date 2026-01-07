# Copyright 2026 Oliver
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

from typing import Any

from ..apis.base import BaseAPI
from ..utils.validators import require_params


class SessionAPI(BaseAPI):

    async def generate_related_questions(
        self,
        agent_id: str,
        question: str,
        industry: str
    ) -> list[str]:
        """
        Generate 5-10 alternative questions from the user's original query.

        Args:
            agent_id: The ID of the agent.
            question: The original user question.
            industry: The industry/context of the question.

        Returns:
            List of generated related questions.

        Raises:
            RAGFlowAPIError: If API call fails.
            RAGFlowValidationError: If parameters are missing.
        """
        require_params(agent_id=agent_id, question=question, industry=industry)

        url = "/sessions/related_questions"
        payload: dict[str, Any] = {
            "question": question,
            "industry": industry
        }

        resp = await self._client.post(url, json=payload)
        resp = self._handle_response(resp)

        data = resp.get("data", [])
        cleaned_data = [q.strip() for q in data]
        return cleaned_data
