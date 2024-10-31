# diky_frontend/Dockerfile
# Use the official Node.js image from the Docker Hub
FROM node:14

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json /app/
COPY package-lock.json /app/
RUN npm install

# Copy project files
COPY . /app/

# Build the app
RUN npm run build

# Install serve to serve the build
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Serve the app
CMD ["serve", "-s", "build"]