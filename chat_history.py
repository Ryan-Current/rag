class ChatHistory:

    def __init__(self):
        self.history = []


    def clear_history(self):
        self.history = []
    
    def add_prompt(self, prompt: str = ''):
        self.history.append(
            {
                'role': 'user', 
                'content': prompt
            }
        )

    def add_response(self, response: str = ''):
        self.history.append(
            {
                'role': 'assistant',
                'content': response
            }
        )
    def get_history(self):
        return ''.join(str(x) + '\n\n' for x in self.history)