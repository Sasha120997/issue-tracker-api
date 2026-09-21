from fastapi import FastAPI
from app.schemas import ProjectCreate
from app.schemas import ProjectResponse

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str,str]:
    return {"message": "Issue Tracker API"}


projects: list[dict]=[]
next_project_id = 1


@app.post("/projects", response_model=ProjectResponse, status_code=201)
def create_project(project:ProjectCreate) -> dict:
    global next_project_id

    new_project = {
        "id": next_project_id,
        "name": project.name,
        "description": project.description
    }

    projects.append(new_project)
    next_project_id += 1

    return new_project
