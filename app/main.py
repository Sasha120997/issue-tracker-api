from fastapi import FastAPI
from app.schemas import ProjectCreate
from app.schemas import ProjectResponse
from app.schemas import ProjectUpdate
from fastapi import HTTPException
from fastapi import Response, status
from app.schemas import TicketResponse
from app.schemas import TicketCreate
from typing import Literal

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str,str]:
    return {"message": "Issue Tracker API"}


projects: list[dict] = []
next_project_id = 1

tickets: list[dict] = []
next_ticket_id = 1


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


def find_project(project_id: int) -> dict | None:
    for project in projects:
        if project["id"] == project_id:
            return project

    return None


@app.patch(
    "/projects/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
):
    for project in projects:
        if project["id"] == project_id:
            updates = project_update.model_dump(exclude_unset=True)

            project.update(updates)

            return project
    raise HTTPException(
        status_code=404,
        detail="Project not found",
    )


@app.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(project_id: int):
    for index, project in enumerate(projects):
        if project["id"] == project_id:
            projects.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=404,
        detail="Project not found",
    )


@app.post(
    "/tickets",
    response_model=TicketResponse,
    status_code=201,
)
def create_ticket(ticket: TicketCreate):
    global next_ticket_id

    project = find_project(ticket.project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    new_ticket = {
        "id": next_ticket_id,
        "title": ticket.title,
        "description": ticket.description,
        "project_id": ticket.project_id,
        "status": "open",
    }

    tickets.append(new_ticket)
    next_ticket_id += 1

    return new_ticket


@app.get(
    "/tickets",
    response_model=list[TicketResponse],
)
def get_tickets(
    status: Literal["open", "closed"] | None = None,
    project_id: int | None = None,
):
    result = tickets

    if status is not None:
        result = [
            ticket
            for ticket in result
            if ticket["status"] == status
        ]

    if project_id is not None:
        result = [
            ticket
            for ticket in result
            if ticket["project_id"] == project_id
        ]

    return result


def find_ticket(ticket_id: int) -> dict | None:
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    return None


@app.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse,
)
def get_ticket(ticket_id: int):
    ticket = find_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return ticket


@app.patch(
    "/tickets/{ticket_id}/close",
    response_model=TicketResponse,
)
def close_ticket(ticket_id: int):
    ticket = find_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    if ticket["status"] == "closed":
        raise HTTPException(
            status_code=400,
            detail="Ticket is already closed",
        )

    ticket["status"] = "closed"

    return ticket