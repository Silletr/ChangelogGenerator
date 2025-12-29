echo '[1. INSTALLING IMPORTANT FOR WORK LIB]'
pip3 install -r requirements.txt

echo '[2. INSTALLING NEED MODEL: phi3:mini]'
(ollama serve &) && ollama run phi3:mini
