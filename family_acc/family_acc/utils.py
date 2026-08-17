from django.apps import apps

def generate_ai_system_prompt():
    # Project's core business logic
    prompt = (
        "You are a financial assistant for a family accounting app. "
        "The data structure uses a Star-scheme. Important: Income transactions "
        "have positive amounts, and expenses have negative amounts.\n\n"
        "Here is the current database schema:\n"
    )
    
    # Add DB schem by programmatically inspect models
    app_config = apps.get_app_config('transactions')
    for model_name, model in app_config.models.items():
        prompt += f"- Table: {model_name.capitalize()}\n"
        for field in model._meta.fields:
            prompt += f"  * Field: {field.name} ({field.get_internal_type()})\n"
            
    return prompt