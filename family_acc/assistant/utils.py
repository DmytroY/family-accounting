from django.apps import apps

def generate_ai_system_prompt():
    # Project's core business logic
    prompt = (
        "You are a concise financial assistant for a family accounting app. "
        "IMPORTANT: Provide only short, high-level summaries. Do not provide "
        "detailed breakdowns or long explanations unless specifically asked.\n\n"
        "Data Structure (Star-scheme): Income is positive, expenses are negative.\n"
        "Current Schema:\n"
    )
    
    # Add DB schem by programmatically inspect models
    app_config = apps.get_app_config('transactions')
    for model_name, model in app_config.models.items():
        prompt += f"- Table: {model_name.capitalize()}\n"
        for field in model._meta.fields:
            prompt += f"  * Field: {field.name} ({field.get_internal_type()})\n"
            
    return prompt