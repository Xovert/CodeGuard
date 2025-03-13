def collect_errors(error_dict):
    messages = []
    for key, value in error_dict.items():
        if isinstance(value, list):
            # Value is a list of error messages
            messages.extend(value)
        elif isinstance(value, dict):
            # Value is another nested dictionary - recurse
            messages.extend(collect_errors(value))
    return messages