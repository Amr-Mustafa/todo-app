FROM node:14.17.4 as build-stage
RUN npm install -g http-server
RUN mkdir app
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

#FROM nginx:latest as production-stage
#COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["http-server", "dist"]
