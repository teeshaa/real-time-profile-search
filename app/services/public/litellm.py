from typing import AsyncGenerator

from colorama import Fore, Style
from dotenv import load_dotenv
from litellm import acompletion

load_dotenv()


async def completion_call(
    messages: list,
    model: str,
) -> str:
    response = await acompletion(model=model, messages=messages)
    return response.choices[0].message.content


async def streaming_completion_call(
    messages: list,
    model: str,
) -> AsyncGenerator[str, None]:
    try:
        response = await acompletion(model=model, messages=messages, stream=True)
        
        buffer = ""
        word_count = 0
        target_words = 3
        
        async for chunk in response:
            try:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    buffer += content
                    
                    if ' ' in content or '\n' in content:
                        word_count += content.count(' ') + content.count('\n')
                        
                        if word_count >= target_words:
                            yield buffer
                            buffer = ""
                            word_count = 0
            except Exception as chunk_error:
                print(f"{Fore.RED}[ERROR] Chunk processing error: {str(chunk_error)}{Style.RESET_ALL}")
                continue
        
        if buffer:
            yield buffer
    except Exception as stream_error:
        print(f"{Fore.RED}[ERROR] Streaming error: {str(stream_error)}{Style.RESET_ALL}")
        yield f"Error in streaming: {str(stream_error)}"