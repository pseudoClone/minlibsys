FROM astral/uv:python3.12-bookworm-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . .
EXPOSE 8000
CMD uv run manage.py makemigrations && uv run manage.py migrate && uv run manage.py runserver 0.0.0.0:8000