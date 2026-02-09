# Stage 1: Build the Next.js application
FROM node:20-alpine as builder

WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the frontend application
COPY frontend/ .

# Build the Next.js application
RUN npm run build

# Stage 2: Serve the Next.js application
FROM node:20-alpine as runner

WORKDIR /app

# Copy the necessary files for the Next.js application to run
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/next.config.ts ./next.config.ts
COPY --from=builder /app/src ./src


# Expose the port Next.js runs on
EXPOSE 3000

# Command to run the Next.js application in production mode
CMD ["npm", "start"]
