FROM node:18-bookworm-slim AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x /app/entrypoint.sh
COPY --from=frontend-builder /frontend/build ./frontend/build
RUN python manage.py collectstatic --noinput || true
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
