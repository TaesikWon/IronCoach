# === frontend/Dockerfile ===
FROM node:20-alpine AS build

WORKDIR /frontend

# 1️⃣ 패키지 설치
COPY package*.json ./
RUN npm install

# 2️⃣ 소스 복사 및 빌드
COPY . .
RUN npm run build

# --- nginx 단계 ---
FROM nginx:alpine

# 3️⃣ Nginx 설정 (SPA 라우팅 대응 가능)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 4️⃣ 빌드 결과 복사
COPY --from=build /frontend/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
