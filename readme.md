# Llama 3 RAG

This Python library leverages Ollama to perform Retrieval-Augmented Generation (RAG) by combining information from uploaded documents and the internet. By searching for information before providing a response, it decreases the likelyhood of the assistant providing false information. 

Ollama must be installed and running.

## CLI information

| Commmand(s) | Description |
| --- | --- |
| `/bye`, `exit`,  `/exit` | exit the application |
| `/clear_chat`, `/clear` | removes the agents knowledge of the previous chats |
| `/add_file`, `/add` | enters 'add file mode' where you will be prompted for a path of a file to upload |

## Internet Searching

For internet searching to be enabled, you must complete the information in `config_template.json` and rename the file to `config.json`. For this, you will need to get an api key from [serper](https://serpapi.com/), which currently gives new users access to 2,500 free searches. 

Once you've filled out the necessary information, you must uncomment 2 lines from the `analyze()` function of the `rag.py` file, which are marked with comments. 