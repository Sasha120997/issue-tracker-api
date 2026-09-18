from app.models import Ticket
from app.services import close_ticket
from app.services import reopen_ticket
import pytest


def test_close_ticket() -> None:
    ticket = Ticket(id=1, title="Bug")

    result = close_ticket(ticket)

    assert result.status == "Closed"


def test_close_ticket_already_closed() -> None:
    ticket = Ticket(id=1, title="Bug", status="Closed")

    with pytest.raises(ValueError):
        close_ticket(ticket)


def test_reopen_ticket() -> None:
    ticket = Ticket(id=1, title='Bug', status="Closed")

    result = reopen_ticket(ticket)

    assert result.status == "Open"


def test_cannot_reopen_ticket() -> None:
    ticket = Ticket(id=1, title='Bug', status="Open")

    with pytest.raises(ValueError):
        reopen_ticket(ticket)
