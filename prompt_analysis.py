# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from chat_history import ChatHistory
# from ollama_functions import OllamaFunctions
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

class PromptAnalysis(BaseModel):
    # contains_contemporary_data: bool \
    #     = Field(description='A boolean value that indicates if the response to the prompt will need up to date information', 
    #             default=False) 
    
    requires_search: bool \
        = Field(description='A boolean value that indicates if the response to the prompt will require a search for more information', 
                default=False)
    

    query: str \
        = Field(description='The query to search, if contemporary or internet information is required.', 
                default='')


class PromptAnalyzer(): 

    PROMPT_TEMPLATE = '''
        Analyze the following question and determine if you are able to respond 
        to the prompt. You can retrieve more information only if the prompt 
        requires current data, or data that you are not confident in. 

        CHAT_HISTORY:

        {chat_history}
        
        PROMPT: 
        
        {prompt}
    '''
    
    def __init__(self, chat_history: ChatHistory, model: str = 'llama3'):
        self.chat_history = chat_history
        self.model = OllamaFunctions(model=model, format="json", temperature=0).with_structured_output(PromptAnalysis)

    def analyze(self, prompt: str) -> PromptAnalysis:
        return self.model.invoke(self.PROMPT_TEMPLATE.format(
            chat_history=self.chat_history.get_history(),
            prompt=prompt
        ))


