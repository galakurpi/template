FROM node:20.0.0-slim

# Set working directory
WORKDIR /app

# Copy package files first (for better caching)
COPY package*.json ./
COPY rollup.config.js ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# If you only need to build, keep the build command
CMD ["npm", "run", "build"]