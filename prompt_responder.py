import ollama
from chat_history import ChatHistory

class PromptResponder():

    FULL_CONTEXT_PROMPT_TEMPLATE = '''
        Respond to the following prompt with the data that you searched for in mind."

        {context}

        PROMPT:

        {prompt}
    '''

    DOCUMENTS_CONTEXT_TEMPLATE = '''
        DOCUMENTS CONTEXT: 

        {context}
    '''

    INTERNET_CONTEXT_TEMPLATE = '''
        INTERNET CONTEXT: 

        {context}
    '''

    def __init__(self, chat_history: ChatHistory, model: str = 'llama3'):
        self.chat_history = chat_history
        self.model = model

    def _get_prompt(self, prompt: str, document_context: str = '', internet_context: str = ''):
        context = ''

        if document_context != '':
            context = self.DOCUMENTS_CONTEXT_TEMPLATE.format(context=document_context)
        
        if internet_context != '':
            context = context + '\n' + self.INTERNET_CONTEXT_TEMPLATE.format(context=internet_context)

        if context != '':
            prompt = self.FULL_CONTEXT_PROMPT_TEMPLATE.format(context=context, prompt=prompt) 

        return prompt

    def stream_respose(self, prompt: str, document_context: str = '', internet_context: str = ''):
        prompt = self._get_prompt(prompt, document_context, internet_context)
        self.chat_history.add_prompt(prompt)
        return ollama.chat(
            model=self.model,
            messages=self.chat_history.history,
            stream=True
        )
    
    def respond(self, prompt: str, document_context: str = '', internet_context: str = ''):
        prompt = self._get_prompt(prompt, document_context, internet_context)
        self.chat_history.add_prompt(prompt)
        return ollama.chat(
            model=self.model,
            messages=self.chat_history.history,
            stream=False
        )