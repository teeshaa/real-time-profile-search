import json

def validate_json(json_string: str):

    json_string = json_string.strip()
    
    if "```json" in json_string:
        json_string = json_string.split("```json")[1]
        if "```" in json_string:
            json_string = json_string.rsplit("```", 1)[0]
            
    json_string = json_string.strip()
    
    try:
        response = json.loads(json_string)

        return response
    except json.JSONDecodeError as e:
        raise e
