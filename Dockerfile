FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gcc \
    g++ \
    make \
    libpq-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

RUN rustup default stable && \
    rustc --version && \
    cargo --version

WORKDIR /app

COPY requirements.txt .

RUN cat requirements.txt | grep -v "pywinpty" | grep -v "jupyter" | grep -v "ipykernel" | grep -v "ipython" | grep -v "ipywidgets" | grep -v "notebook" > requirements-clean.txt && \
    mv requirements-clean.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
