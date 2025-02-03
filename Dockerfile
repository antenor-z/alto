FROM python:3.10-slim

WORKDIR /app/

COPY requirements.txt /app/requirements.txt

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["python3", "-u", "-m", "gunicorn", "-c", "gunicorn_config.py", "app:app"]
