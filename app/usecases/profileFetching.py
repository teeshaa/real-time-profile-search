import json
from datetime import datetime
from typing import AsyncGenerator

from colorama import Fore, Style

from app.config.coreConfig import core_config
from app.prompts.generalResponse import (GENERAL_RESPONSE_SYSTEM_PROMPT, GENERAL_RESPONSE_USER_PROMPT)
from app.prompts.profileGeneralResponse import (
    PROFILE_GENERAL_RESPONSE_SYSTEM_PROMPT,
    PROFILE_GENERAL_RESPONSE_USER_PROMPT)
from app.prompts.webSearch import (WEB_SEARCH_DECISION_SYSTEM_PROMPT, WEB_SEARCH_DECISION_USER_PROMPT)
from app.services.profile.contentModeration import ContentModerationService
from app.services.public.litellm import (completion_call,
                                         streaming_completion_call)
from app.services.public.tavily import run_web_search
from app.utils.jsonValidator import validate_json


class ProfileFetchingUsecase:
    def __init__(self):
        self.moderation_service = ContentModerationService()

    async def search_profiles_streaming(self, query: str) -> AsyncGenerator[str, None]:
        try:
            moderation_result = await self.moderation_service.moderate_content(query)
            
            if not moderation_result["safe"]:
                yield json.dumps({"type": "data", "data": f"I'm sorry {moderation_result['reason']}"})
                return

            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            messages = [
                {"role": "system", "content": WEB_SEARCH_DECISION_SYSTEM_PROMPT},
                {"role": "user", "content": WEB_SEARCH_DECISION_USER_PROMPT.format(
                    user_query=query,
                    current_date_time=current_datetime
                )}
            ]

            try:
                web_search_response = await completion_call(
                    messages=messages,
                    model=core_config.GROQ_QUERY_DECOMPOSITION_MODEL,
                )
                
                print(Fore.GREEN + "[LLM] Web Search Decision Response:" + Style.RESET_ALL, web_search_response)
                
                web_search_decision = validate_json(web_search_response)

                if not web_search_decision["web_search_needed"]:
                    messages = [
                        {"role": "system", "content": GENERAL_RESPONSE_SYSTEM_PROMPT},
                        {"role": "user", "content": GENERAL_RESPONSE_USER_PROMPT.format(
                            user_query=query,
                            previous_messages="None"
                        )}
                    ]

                    complete_response = ""
                    try:
                        async for chunk in streaming_completion_call(
                            messages=messages,
                            model=core_config.GENERAL_RESPONSE_MODEL,
                        ):
                            complete_response += chunk
                            yield json.dumps({"type": "data", "data": chunk})
                        
                        print(Fore.GREEN + "[LLM] General Response Complete:" + Style.RESET_ALL, complete_response)
                    except Exception as e:
                        print(Fore.RED + f"[ERROR] General Response streaming failed: {str(e)}" + Style.RESET_ALL)
                        yield json.dumps({"type": "error", "data": "Failed to generate general response"})
                else:
                    try:
                        search_results = await run_web_search(web_search_decision["search_queries"])
                        
                        urls = []
                        if "results" in search_results:
                            urls = [{"url": result.get("url", ""), "title": result.get("title", "")} for result in search_results["results"]]
                        
                        yield json.dumps({"type": "urls", "data": urls})
                        
                        messages = [
                            {"role": "system", "content": PROFILE_GENERAL_RESPONSE_SYSTEM_PROMPT},
                            {"role": "user", "content": PROFILE_GENERAL_RESPONSE_USER_PROMPT.format(
                                user_query=query,
                                web_context=json.dumps(search_results)
                            )}
                        ]

                        complete_response = ""
                        try:
                            async for chunk in streaming_completion_call(
                                messages=messages,
                                model=core_config.PROFILE_RESPONSE_MODEL,
                            ):
                                complete_response += chunk
                                yield json.dumps({"type": "data", "data": chunk})
                            
                        except Exception as e:
                            yield json.dumps({"type": "error", "data": "Failed to generate profile response"})
                    except Exception as e:
                        yield json.dumps({"type": "error", "data": "Failed to perform web search"})
            except Exception as e:
                yield json.dumps({"type": "error", "data": "Failed to analyze query"})
        except Exception as e:
            yield json.dumps({"type": "error", "data": "Failed to moderate content"})
            

