def require_bot_tools(func):
    func._require_bot_tools = True
    return func
