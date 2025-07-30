import os
import json
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled,Runner
from typing import Optional, Union # for class ConversationRecommendation(BaseModel):
# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL") 
API_KEY = os.getenv("API_KEY") 
MODEL_NAME = os.getenv("MODEL_NAME") 

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set BASE_URL, API_KEY, and MODEL_NAME."
    )
    

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)

# --- Models for structured outputs ---
class SkillGapRecommendation(BaseModel):
    target_job: str
    user_skills: List[str]
    required_skills: List[str]
    missing_skills: List[str]
    recommendation_reason: str  # e.g., "To qualify for a data analyst role, you need SQL and Power BI."

class JobFindeRecommendation(BaseModel):
    job_title: str
    company_name: str
    location: str
    required_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    application_link: str
    recommendation_reason: str  # e.g., "Your skills match 3 out of 5 required for this role."

class CourseRecommendation(BaseModel):
    skill: str
    course_title: str
    provider: str  # e.g., Coursera, Udemy
    link: str
    price: float
    duration_hours: int  # Optional but useful
    recommendation_reason: str  # e.g., "Covers SQL from beginner to advanced."

class ConversationRecommendation(BaseModel):
    user_query: str
    detected_intent: str  # e.g., "find_job", "skill_gap", "course_recommendation"
    routed_agent: str     # e.g., "SkillGapAgent", "JobFinderAgent", "CourseRecommenderAgent"
    agent_response: str   # Plain response from the routed agent
    timestamp: Optional[str] = None  # Optional: when the request was handled
    log_message: Optional[str] = None  # e.g., "Routed to JobFinderAgent based on intent 'find_job'"