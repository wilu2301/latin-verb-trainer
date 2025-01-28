FROM node:18 AS vite-builder

COPY ui /ui
WORKDIR /ui

RUN npm install
RUN npm run build

FROM python:3.10

ENV MONGO_HOST=mongodb://localhost:27017
ENV MONGO_DB=latein



COPY backend /app
WORKDIR /app


COPY --from=vite-builder /ui/build /app/static

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000


# Start the FastAPI application
CMD ["fastapi","run"]