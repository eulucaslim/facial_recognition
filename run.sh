#!/bin/bash

# Iniciar o servidor Uvicorn usando as variáveis de ambiente
uvicorn main:app --host "$FR_HOST" --port "$FR_PORT"

#Dar permissão para executar
#chmod +x start.sh

#executar script
#./start.sh