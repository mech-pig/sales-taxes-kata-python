FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/app
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml .
COPY src/ ./src
RUN poetry install --no-dev
ENTRYPOINT ["receipt"]
