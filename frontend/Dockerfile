# Estágio de construção (Build)
FROM node:18-alpine AS build
WORKDIR /app

# Copia pacotes e instala as dependências
COPY package*.json ./
RUN npm install

# Copia todo o código angular e faz a compilação de produção
COPY . .
RUN npm run build --configuration=production

# Estágio de servidor Servidor (Nginx)
FROM nginx:alpine

# Copiar os arquivos gerados no estágio anterior para o nginx
COPY --from=build /app/dist/frontend /usr/share/nginx/html

# Copiar arquivo de configuração para suportar rotas Single Page Application
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
