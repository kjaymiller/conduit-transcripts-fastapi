This is a FastAPI application that allows you to search and view transcripts from each episode of [Conduit](https://relay.fm/conduit).

It also has an AI bot (locally powered by Llama3 via Ollama) that will take those results and generate a short summary for you.

## Database Services

- PostgreSQL - individual transcription and episode data
- OpenSearch®️ - application search and logging data
- Redis - AI Coach session management
- Grafana - resource monitoring
  
All database services are powered by the Aiven Platform. [Sign up](https://go.aiven.io/jay-signup) for $400 off your first month and try the fastest and easiest way to setup your own Data and AI platform 

## Usage and License

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/kjaymiller/conduit-transcripts">Conduit Podcast Transcripts</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://relay.fm/conduit">Jay Miller, Kathy Campbell, original downloads from whisper work done by Pilix</a> is licensed under <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution-NonCommercial-ShareAlike 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1"></a></p>
