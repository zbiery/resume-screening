from ..services.factory import AIServiceFactory
from ..services.schema import AIServiceInterface

from ..llm.prompts import system_prompt_candidate, system_prompt_job
from ..llm.functions import fn_candidate_analysis, fn_job_analysis

from ..common.logger import get_logger

logger = get_logger(__name__)

class Analyzer:
    def __init__(self, ai_service: AIServiceInterface):
        self.ai_service = ai_service

    @classmethod
    async def create(cls):
        ai_service = await AIServiceFactory.create_service()
        return cls(ai_service)
    
    async def close(self):
        if hasattr(self.ai_service, "close") and callable(getattr(self.ai_service, "close")):
            await self.ai_service.close()

    async def analyze_candidate(self, candidate_data: str) -> dict:
        return await self.ai_service.structured_query(
            text=candidate_data,
            system_prompt=system_prompt_candidate,
            functions=fn_candidate_analysis,
        )

    async def analyze_job(self, job_data: str) -> dict:
        return await self.ai_service.structured_query(
            text=job_data,
            system_prompt=system_prompt_job,
            functions=fn_job_analysis,
        )
