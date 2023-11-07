FROM python:3.8.18-slim

WORKDIR /app

RUN apt update
RUN apt install gcc python3-dev -y

COPY ["pyproject.toml", "poetry.toml", "poetry.lock", "predict.py", "train.py","./"]
COPY ["assets/", "./assets/"]

RUN pip install poetry
RUN poetry install --no-root --without dev


EXPOSE 6969

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:6969", "predict:app"]