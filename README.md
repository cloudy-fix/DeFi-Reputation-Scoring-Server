AI Engineer Challenge: DeFi Reputation Scoring Server

Overview



This project is a production-ready AI microservice that calculates wallet reputation scores by processing DeFi transaction data from a Kafka stream. It is designed to be scalable, robust, and easily deployable via Docker.

Solution Components



&nbsp;   app/main.py: The main FastAPI application. It sets up API endpoints for health checks and statistics, and runs a background task to consume messages from Kafka, process them with the AI model, and publish results.



&nbsp;   app/ai\_model.py: Contains the core AI scoring logic extracted from the provided Jupyter Notebook (dex\_scoring\_model.ipynb).



&nbsp;   app/models.py: Defines Pydantic models for data validation, ensuring a robust data pipeline.



&nbsp;   requirements.txt: Lists all Python dependencies required by the application.



&nbsp;   Dockerfile: A multi-stage Dockerfile to build a lightweight container image for the application.



Getting Started

Prerequisites



&nbsp;   Docker installed on your machine.



&nbsp;   A running Kafka instance. You can use Docker to set up a local Kafka instance for testing:



docker-compose up -d



Setup and Running the Server



&nbsp;   Clone the repository and navigate into the project directory:



&nbsp;   git clone https://github.com/your-username/my-defi-server.git

&nbsp;   cd my-defi-server



&nbsp;   Build the Docker image:



&nbsp;   docker build -t zeru-ai-server .



&nbsp;   Run the Docker container:



&nbsp;   docker run -p 8000:8000 zeru-ai-server



&nbsp;   The server will now be running on http://localhost:8000.



Testing the Solution



You can use the test\_challenge.py script provided in the challenge to validate your implementation.



&nbsp;   Run the test script:



&nbsp;   python test\_challenge.py



&nbsp;   Verify the output: The script will check the server's health, AI model logic, and performance. A successful run will show all tests passing.


## Production Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Operations Guide](docs/OPERATIONS.md)
- [Architecture Diagram](docs/diagrams/architecture.mmd)
- [Workflow Diagram](docs/diagrams/workflow.mmd)
- [Security Policy](SECURITY.md)
- [Contributing Guide](CONTRIBUTING.md)
