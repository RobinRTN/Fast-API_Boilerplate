# Use the official Node.js 18 LTS version
FROM node:18-alpine AS builder

ARG VITE_APP_PRODUCTION

ENV VITE_APP_PRODUCTION=${VITE_APP_PRODUCTION}

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Clear npm cache to avoid stale dependency issues
RUN npm cache clean --force

# Install dependencies and ensure `package-lock.json` is created
RUN npm install --legacy-peer-deps

# Copy the rest of the application files
COPY . .

# Build the Vite application
RUN npm run build

# Use a lightweight Node.js image for production
FROM node:18-alpine AS runner

# Set working directory
WORKDIR /app

# Assuming the default Vite build output directory (`dist`) is used:
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/package-lock.json ./package-lock.json

# Install a simple HTTP server to serve static files
RUN npm install -g serve

# Expose the application port
EXPOSE 3000

# Run the server to serve the static site
CMD ["serve", "-s", "dist", "-l", "3000"]
