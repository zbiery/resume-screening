
from ..services.factory import AIServiceFactory
from ..services.schema import AIServiceInterface

from ..llm.prompts import system_prompt_candidate, system_prompt_job
from ..llm.functions import fn_candidate_analysis, fn_job_analysis


def analyze_candidate(candidate_data: str) -> dict:
    # Create service using factory (Groq or Azure OpenAI based on config)
    ai_service: AIServiceInterface = AIServiceFactory.create_service()

    # Run structured query
    return ai_service.structured_query(
        text=candidate_data,
        system_prompt=system_prompt_candidate,
        functions=fn_candidate_analysis
    )

def analyze_job(job_data: str) -> dict:
    # Create service using factory (Groq or Azure OpenAI based on config)
    ai_service: AIServiceInterface = AIServiceFactory.create_service()

    # Run structured query
    return ai_service.structured_query(
        text=job_data,
        system_prompt=system_prompt_job,
        functions=fn_job_analysis
    )
