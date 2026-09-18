from app.models import Ticket


def close_ticket(ticket: Ticket) -> Ticket:
    if ticket.status == "Closed":
        raise ValueError("Ticket is already closed")

    ticket.status = "Closed"
    return ticket


def reopen_ticket(ticket: Ticket) -> Ticket:
    if ticket.status == "Open":
        raise ValueError("Ticket is already opened")

    ticket.status = "Open"
    return ticket