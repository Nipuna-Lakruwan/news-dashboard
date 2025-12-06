# Lanka News Dashboard

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Cache-red?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

A DevOps demonstration project showcasing **Microservices Architecture** and **Redis caching** with a Streamlit web application. This project simulates a high-traffic news dashboard to demonstrate the performance benefits of caching (reducing load times from seconds to milliseconds).

## Project Overview

This application demonstrates:

- **Redis Caching**: Fast data retrieval using Redis as an in-memory layer.
- **Docker Compose**: Orchestrating multi-container environments.
- **Service Discovery**: Internal networking between containers.
- **Performance Comparison**: Visual demonstration of cache hits vs. cache misses.

## Architecture

The application consists of two services running in a private Docker network:

1. **news-app**: Python/Streamlit application (Port 8501) - The Frontend.
2. **redis-db**: Redis cache database (Port 6379) - The Backend Storage.

## Prerequisites

- Docker Desktop installed and running.
- **No Python installation required** (runs entirely in containers).

## Quick Start

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Nipuna-Lakruwan/news-dashboard.git
   cd news-dashboard

````

2.  **Start the application**:

    ```bash
    docker-compose up
    ```

3.  **Access the dashboard**:
    Open your browser and navigate to: `http://localhost:8501`

4.  **Stop the application**:

    ```bash
    docker-compose down
    ```

## How It Works

### Cache Flow

1.  **First Request** (Cache Miss):

      - User clicks "Refresh News".
      - App checks Redis cache → Empty.
      - Simulates a **slow API fetch** (3-second delay).
      - Stores result in Redis with a **60-second TTL** (Time To Live).

2.  **Subsequent Requests** (Cache Hit):

      - User clicks "Refresh News" again within 60s.
      - App finds data in Redis.
      - Returns **instantly** (0ms delay).

### News Data

The application displays mock data for:

  - **Headline**: Main news story.
  - **Breaking**: Critical alerts.
  - **Sports**: Match updates.

## Technical Details

### Container Configuration

  - **App Container**: Exposes port 8501. Depends on `redis-db`.
  - **Redis Container**: Uses official `redis:alpine` image (lightweight).
  - **Networking**: Containers communicate via Docker Compose's internal DNS (hostname: `redis-db`).

### Cache Settings

  - **Expiration Time**: 60 seconds.
  - **Key Name**: `lanka_news`.

## Development & Debugging

### Modifying the Application

If you edit `app.py`, you must rebuild the container:

```bash
docker-compose up --build
```

### Accessing Redis CLI

To manually inspect keys inside the running container:

```bash
docker exec -it news-dashboard-redis-db-1 redis-cli
```

Common commands:

  - `KEYS *` : List all cached keys.
  - `TTL lanka_news` : See how many seconds are left before expiration.

## Future Improvements (Roadmap)

  - [ ] **Data Persistence**: Add Docker Volumes (`-v`) to persist Redis data after container shutdown.
  - [ ] **Real API Integration**: Replace the mock data with a real request to a News API.
  - [ ] **Load Balancing**: Add Nginx to distribute traffic across multiple app containers.

## License

This project is created for educational purposes.

-----

**Built for DevOps learning**
