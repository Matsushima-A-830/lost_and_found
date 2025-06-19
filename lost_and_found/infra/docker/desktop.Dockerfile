FROM node:18-slim AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

FROM node:18-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["npm", "run", "preview"]
