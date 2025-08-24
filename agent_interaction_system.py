from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, List
import uuid

app = FastAPI()

# In-memory store for tenant data (use a database in production)
tenant_data: Dict[str, List[Dict]] = {}

class UserRequest(BaseModel):
    tenant_id: str
    message: str

def simulate_llm_response(message: str, tenant_context: List[Dict]) -> str:
    """Simulate an LLM response based on tenant context."""
    # In a real system, this would call an LLM API with tenant context
    context_summary = " ".join([f"{item['message']}: {item['response']}" for item in tenant_context])
    return f"Agent response to '{message}' with context: {context_summary}"

@app.post("/agent/interact")
async def interact_with_agent(request: UserRequest):
    """Handle tenant-specific agent interactions."""
    tenant_id = request.tenant_id
    message = request.message

    # Initialize tenant data if not exists
    if tenant_id not in tenant_data:
        tenant_data[tenant_id] = []

    # Simulate agent processing with tenant-specific context
    response = simulate_llm_response(message, tenant_data[tenant_id])

    # Store interaction in tenant's memory
    tenant_data[tenant_id].append({"message": message, "response": response})

    return {"tenant_id": tenant_id, "response": response}

@app.get("/agent/history/{tenant_id}")
async def get_tenant_history(tenant_id: str):
    """Retrieve tenant-specific interaction history."""
    if tenant_id not in tenant_data:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {"tenant_id": tenant_id, "history": tenant_data[tenant_id]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)