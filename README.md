# Multi-Tenant Agent System

## Overview
This project implements a multi-tenant agent system using Python and FastAPI. The system allows multiple tenants (users or organizations) to interact with an AI-like agent while maintaining strict data isolation. Each tenant’s interactions are stored separately, ensuring no data leakage between tenants. The system uses an in-memory store for simplicity but is designed to be extensible for production use with a database and real LLM integration.

### Key Features
- **Tenant Isolation**: Each tenant’s data is stored separately using a tenant ID.
- **Session Management**: Maintains conversation history per tenant for context-aware responses.
- **FastAPI Server**: Provides a scalable HTTP API for agent interactions.
- **Simulated LLM**: Includes a placeholder LLM response generator, ready for integration with a real LLM API.
- **Extensibility**: Easily adaptable for databases, authentication, and external tool integration.

## Prerequisites
- Python 3.8+
- Dependencies: `fastapi`, `uvicorn`, `pydantic`
- Optional: A tool like `curl`, Postman, or any HTTP client for testing.

## Installation
1. **Clone the Repository** (if applicable):
   ```bash
   git clone https://github.com/pranjulya/multi-tenant-agent-SOP.git
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn pydantic
   ```

3. **Run the Server**:
   ```bash
   python script.py
   ```
   The server will start at `http://localhost:8000`.

## Usage
The system provides two main API endpoints for interacting with the agent and retrieving tenant history.

### 1. Interact with the Agent
- **Endpoint**: `POST /agent/interact`
- **Description**: Send a message to the agent for a specific tenant and receive a response.
- **Request Body**:
  ```json
  {
    "tenant_id": "tenant1",
    "message": "Hello, what's the weather?"
  }
  ```
- **Example**:
  ```bash
  curl -X POST "http://localhost:8000/agent/interact" -H "Content-Type: application/json" -d '{"tenant_id":"tenant1","message":"Hello, what'\''s the weather?"}'
  ```
- **Response**:
  ```json
  {
    "tenant_id": "tenant1",
    "response": "Agent response to 'Hello, what's the weather?' with context: "
  }
  ```

### 2. Retrieve Tenant History
- **Endpoint**: `GET /agent/history/{tenant_id}`
- **Description**: Retrieve the interaction history for a specific tenant.
- **Example**:
  ```bash
  curl "http://localhost:8000/agent/history/tenant1"
  ```
- **Response**:
  ```json
  {
    "tenant_id": "tenant1",
    "history": [
      {
        "message": "Hello, what's the weather?",
        "response": "Agent response to 'Hello, what's the weather?' with context: "
      }
    ]
  }
  ```

## API Details
### Data Model
- **UserRequest** (Pydantic model):
  - `tenant_id: str`: Unique identifier for the tenant (e.g., "tenant1").
  - `message: str`: The user’s input message to the agent.

### Endpoints
- **POST /agent/interact**:
  - Input: `UserRequest` JSON object.
  - Output: JSON object with `tenant_id` and `response`.
  - Behavior: Processes the message, generates a response using tenant-specific context, and stores the interaction.
- **GET /agent/history/{tenant_id}**:
  - Input: `tenant_id` as a path parameter.
  - Output: JSON object with `tenant_id` and `history` (list of interactions).
  - Behavior: Returns the tenant’s interaction history or a 404 error if the tenant is not found.

## Project Structure
- **script.py**: Main application file containing the FastAPI server, tenant data store, and agent logic.
- **tenant_data**: In-memory dictionary storing tenant-specific interaction history (replace with a database in production).
- **simulate_llm_response**: Placeholder function for generating agent responses (replace with real LLM integration).

## Extending the System
To make the system production-ready, consider the following enhancements:
1. **Database Integration**:
   - Replace the in-memory `tenant_data` dictionary with a database like PostgreSQL, MongoDB, or Redis for persistent storage.
   - Example: Use SQLAlchemy for PostgreSQL to store tenant interactions.
2. **LLM Integration**:
   - Integrate with a real LLM API (e.g., OpenAI, AWS Bedrock) in the `simulate_llm_response` function.
   - Example: Use LangChain to manage LLM calls with tenant-specific context.
3. **Authentication**:
   - Add JWT-based authentication to secure tenant access.
   - Use a header like `Tenant-ID` for tenant identification, validated with API tokens.
4. **Rate Limiting**:
   - Implement rate limiting (e.g., using `fastapi-limiter`) to prevent overuse by a single tenant.
5. **Tool Integration**:
   - Add support for tenant-specific tools (e.g., JIRA, Slack) using a Model Context Protocol (MCP) approach.
   - Example: Implement a tool-calling mechanism where the agent can query external APIs based on tenant configuration.
6. **Logging and Monitoring**:
   - Add logging (e.g., with `logging` module) and monitoring (e.g., Prometheus) for observability.

## Limitations
- **In-Memory Storage**: The current implementation uses an in-memory dictionary, which is not persistent and unsuitable for production.
- **Simulated LLM**: The `simulate_llm_response` function is a placeholder and does not provide real AI capabilities.
- **No Authentication**: Tenant IDs are passed in the request body without validation, posing a security risk.
- **Scalability**: The in-memory store and single-threaded server may not scale well under heavy load.

## Future Improvements
- Add support for WebSocket-based real-time interactions.
- Implement tenant-specific configuration (e.g., custom prompts, tools).
- Support multi-language responses for global tenants.
- Add error handling for edge cases (e.g., invalid tenant IDs, large payloads).
- Deploy the system on a cloud provider (e.g., AWS, GCP) with auto-scaling.

## License
This project is licensed under the MIT License.

## Contact
For questions or contributions, please reach out via the repository’s issue tracker or contact the maintainer.
