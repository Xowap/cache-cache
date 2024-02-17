ARG PYTHON_DOCKER_IMAGE=3.12
ARG POETRY_VERSION=1.7.1

# Use build layer
FROM python:${PYTHON_DOCKER_IMAGE} as builder

ARG PYTHON_DOCKER_IMAGE
ARG POETRY_VERSION

ENV POETRY_HOME=/opt/poetry

RUN echo PYTHON_DOCKER_IMAGE=${PYTHON_DOCKER_IMAGE} POETRY_VERSION=${POETRY_VERSION}

RUN if [ -z "${PYTHON_DOCKER_IMAGE##*alpine*}" ]; then \
        echo "Installing required packages for alpine image"; \
        apk update; \
        apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo; \
    else \
        echo "Skipping installation of required packages for alpine image"; \
    fi

# Install poetry
ADD https://install.python-poetry.org /opt/get-poetry.py
RUN pip3 install --no-cache-dir --upgrade pip
RUN python /opt/get-poetry.py --version ${POETRY_VERSION}

# Use runtime layer
FROM python:${PYTHON_DOCKER_IMAGE} as python-poetry

# Disable creation of virtual environments to reduce image size
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME=/opt/poetry \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Copy poetry into image
COPY --from=builder /opt/poetry /opt/poetry
ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN pip3 install --no-cache-dir --upgrade pip

CMD ["python3"]

FROM python-poetry

WORKDIR /usr/src/app

COPY poetry.lock ./
COPY pyproject.toml ./

RUN poetry install --no-root

COPY ./ ./

RUN poetry install

CMD [ "poetry", "run", "python", "-m", "gunicorn", "--access-logfile", "-", "-b", "0.0.0.0:8000", "cache_cache:app" ]
