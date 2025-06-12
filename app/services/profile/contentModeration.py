import json

from colorama import Fore, Style

from app.config.coreConfig import core_config
from app.prompts.moderation import MODERATION_SYSTEM_PROMPT
from app.services.public.litellm import completion_call
from app.utils.jsonValidator import validate_json


class ContentModerationService:
    def __init__(self):
        pass

    async def moderate_content(self, query: str):
        """
        Moderate content using LLM to ensure queries are safe and appropriate
        """
        print(f"{Fore.YELLOW}Moderating query: {query}{Style.RESET_ALL}")
        
        try:
            messages = [
                {"role": "system", "content": MODERATION_SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ]

            response_text = await completion_call(
                messages=messages,
                model=core_config.GROQ_MODERATION_MODEL,
            )

            try:
                moderation_response = validate_json(response_text)

                print(f"{Fore.GREEN}Moderation response: {moderation_response}{Style.RESET_ALL}")
                return moderation_response
            
            except json.JSONDecodeError:
                print(f"{Fore.RED}Failed to parse moderation JSON: {response_text}{Style.RESET_ALL}")
                return {"safe": False, "reason": "Unable to verify content safety"}

        except Exception as e:
            print(f"{Fore.RED}Moderation service error: {str(e)}{Style.RESET_ALL}")
            return {"safe": False, "reason": "Content moderation service unavailable"}