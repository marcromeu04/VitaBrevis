FROM node:20-alpine

WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 3000

# Comando
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
