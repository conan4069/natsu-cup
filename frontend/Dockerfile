# frontend/Dockerfile
FROM node:20-alpine

WORKDIR /app

# Instalar dependencias solo si package.json cambia
COPY package*.json ./
RUN npm install

# No necesitamos copiar el código fuente aquí ya que usaremos volumen

EXPOSE 3000

# Configurar para permitir hot reload
ENV CHOKIDAR_USEPOLLING=true
ENV HOST=0.0.0.0

CMD ["npm", "run", "dev", "--", "--host"]