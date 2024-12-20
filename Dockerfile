# Usa l'immagine ufficiale di Python come base
FROM python:3.11-slim

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia i file di dipendenze
COPY /requirements.txt /app/

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice
COPY / /app/

# Imposta la variabile d'ambiente per il database
ENV PYTHONUNBUFFERED 1

# Comando per avviare il server Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]