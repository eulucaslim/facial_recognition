FROM python3.11-alpine

WORKDIR /face_reco

COPY . .

RUN pip install -r face_reco/requirements.txt

EXPOSE 3005

CMD ["fastapi", "run", "main.py", "--port", "3005"]