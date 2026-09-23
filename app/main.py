from fastapi import FastAPI
from app.schemas import ProjectCreate
from app.schemas import ProjectResponse
from fastapi import FastAPI, HTTPException

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


@app.get("/projects", response_model=list[ProjectResponse])
def get_projects():
    return projects


@app.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int):
    for project in projects:
        if project["id"] == project_id:
            return project

    raise HTTPException(
        status_code=404,
        detail='Project not found'
    )


def find_project(projects: list[dict], project_id: int) -> dict | None:
    for project in projects:
        if project['id'] == project_id:
            return project

    raise HTTPException(
        detail='Project not found'
    )

