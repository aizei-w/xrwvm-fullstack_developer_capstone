FROM node:18-bookworm-slim
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ENV PORT=3030
EXPOSE 3030
CMD ["node", "app.js"]
