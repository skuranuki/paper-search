# Use an official Node runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install the dependencies
RUN npm install --legacy-peer-deps && \ 
    npm install vue@3 vue-router@4 vuex@4 && \
    npm install -g http-server && \
    npm install katex

# Copy the rest of the application code
COPY . .

# Build the app for production
RUN npm run build

# Expose port 8080
EXPOSE 8080

ENV NODE_ENV=development

# Serve the app
CMD ["http-server", "dist"]
