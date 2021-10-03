FROM node:16-alpine3.11 as build-deps

WORKDIR /app

COPY ./src/front/src ./src
COPY ./src/front/package.json ./package.json
COPY ./src/front/public ./public
COPY ./src/front/tsconfig.json ./tsconfig.json
COPY ./src/front/webpack.config.js ./webpack.config.js
RUN npm install
RUN npm run build --production

FROM nginx:1.21.0-alpine

COPY --from=build-deps /app/build /var/www
COPY --from=build-deps /app/build/ /usr/share/nginx/html
COPY ./nginx/conf.d/default.conf /etc/nginx/conf.d/
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]

