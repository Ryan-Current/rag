from prompt_analysis import PromptAnalyzer, PromptAnalysis
from chat_history import ChatHistory
from prompt_responder import PromptResponder
from internet_functions import InternetSearcher
from local_files_functions import VectorFileDatabase
from concurrent.futures import ThreadPoolExecutor
import os

chat_history = ChatHistory()

analyzer = PromptAnalyzer(chat_history=chat_history)
responder = PromptResponder(chat_history=chat_history)
internet_searcher = InternetSearcher()
vector_database_searcher = VectorFileDatabase()

def respond(prompt: str = '', internet_context: str = '', file_context: str = ''): 
    stream = responder.stream_respose(prompt, internet_context=internet_context, document_context=file_context)
    print(f'Response: ', end='')
    response = ''
    for chunk in stream:
        part = chunk['message']['content']
        print(part, end="", flush=True)
        response = response + part
    
    chat_history.add_response(response)
    print()


def search_internet(prompt: str = ''):
    return internet_searcher.search_internet(prompt)

def search_files(prompt: str = ''):
    return vector_database_searcher.search_file(prompt)

def analyze(prompt: str=''):
    print('Thinking...')

    analysis = analyzer.analyze(prompt)

    file_context = ''
    internet_context = ''

    if analysis.requires_search:
        print(f'Gathering more infomation...')

        with ThreadPoolExecutor(max_workers=2) as executor:
            query = analysis.query if analysis.query and analysis.query != '' else prompt

            file_search_thread = executor.submit(search_files, query)
            # Uncomment to enable internet searching
            # internet_search_thread = executor.submit(search_internet, query)

            file_context = file_search_thread.result()
            # Uncomment to enable internet searching
            # internet_context = internet_search_thread.result()
    
    respond(prompt, file_context=file_context, internet_context=internet_context)
    
while(True):
    prompt = input('Prompt: ')

    if prompt.strip() == '/bye' or prompt.strip() == 'exit' or prompt.strip() == '/exit':
        break

    if prompt.strip() == '/reset' or prompt.strip() == '/clear' or prompt.strip() == '/clear_chat':
        chat_history.clear_history()
        continue

    if prompt.strip() == '/add' or prompt.strip() == '/add_file':
        path = input('Path: ')
        if os.path.isfile(path.strip()):
            vector_database_searcher.add_file(path=path.strip())
            print('File added')
        else:
            print('File not found') 
        continue 

    analyze(prompt=prompt)

    print('\n')


    


