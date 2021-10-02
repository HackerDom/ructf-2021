FROM node:16-alpine3.11

COPY ./src/front/src ./src
COPY ./src/front/package.json ./package.json
COPY ./src/front/public ./public
COPY ./src/front/tsconfig.json ./tsconfig.json
COPY ./src/front/webpack.config.js ./webpack.config.js
RUN npm install
RUN npm run build --production

