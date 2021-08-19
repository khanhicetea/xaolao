FROM python:3.9-slim

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.7

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy only requirements to cache them in docker layer
WORKDIR /xaolao
COPY poetry.lock pyproject.toml /xaolao/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /xaolao
EXPOSE 8000

COPY ./xaolao /xaolao

CMD ["uvicorn", "xaolao.app:app", "--host", "0.0.0.0", "--port", "8000"]