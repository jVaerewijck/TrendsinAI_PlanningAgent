## OLLAMA setup
1) download ollama 
Download de ollama installer voor het juiste platform (bijvoorbeeld Windows) via https://ollama.com/download en volg de instructies in de installer.

2) download model
Llama 3.2 wordt gebruikt als model in de ollama server (https://ollama.com/library/llama3.2/tags)

````
ollama pull llama3.2
````

Dit kan gedownload worden in een windows powershell terminal wanneer ollama is geïnstalleerd vanuit vorige stap. 


## run ollama
ollama serve in terminal, kan zijn dat volgende error verschijnt:
```
ollama serve Error: listen tcp 127.0.0.1:11434: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.
```
dan sluit je de ollama die lokaal runt door rechts te klikken op het ollama icoontje in de taskbalk rechtsonderaan in windows

pip install -r requirements.txt