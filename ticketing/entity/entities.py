from _decimal import Decimal
from datetime import datetime
from typing import Optional, List


# 초대장
class Invitation:
    __local_datetime: datetime


# 티켓
class Ticket:
    __fee: Decimal

    def get_fee(self) -> Decimal:
        return self.__fee


# 관람객의 소지품을 담을 가방
class Bag:
    __amount: Decimal
    invitation: Invitation
    ticket: Ticket

    def __init__(self, amount: Decimal, invitation: Optional[Invitation] = None) -> None:
        self.__amount = amount
        self.invitation = invitation

    def __has_invitation(self) -> bool:
        return self.invitation is None

    def __set_ticket(self, ticket: Ticket) -> None:
        self.ticket = ticket

    def __minus_amount(self, amount: Decimal) -> None:
        self.__amount -= amount

    def hold(self, ticket: Ticket) -> Decimal:
        if self.__has_invitation():
            self.__set_ticket(ticket=ticket)
            return Decimal("0")

        self.__set_ticket(ticket=ticket)
        self.__minus_amount(amount=ticket.get_fee())
        return ticket.get_fee()


# 관람객
class Audience:
    __bag: Bag

    def __init__(self, bag: Bag) -> None:
        self.__bag = bag

    def buy(self, ticket: Ticket) -> Decimal:
        return self.__bag.hold(ticket=ticket)


# 매표소
class TicketOffice:
    __amount: Decimal
    __tickets: List[Ticket]

    def __init__(self, amount: Decimal, tickets: List[Ticket]) -> None:
        self.__amount = amount
        self.__tickets = tickets

    def get_ticket(self) -> Ticket:
        return self.__tickets.pop(0)

    def __plus_amount(self, amount: Decimal) -> None:
        self.__amount += amount

    def sell_ticket(self, ticket: Ticket) -> None:
        self.__plus_amount(amount=ticket.get_fee())


# 판매원
class TicketSeller:
    __ticket_office: TicketOffice

    def __init__(self, ticket_office: TicketOffice) -> None:
        self.__ticket_office = ticket_office

    def sell_to_audience(self, audience: Audience) -> None:
        ticket: Ticket = self.__ticket_office.get_ticket()
        audience.buy(ticket=ticket)

        self.__ticket_office.sell_ticket(ticket=ticket)


# 소극장
class Theater:
    __ticket_seller: TicketSeller

    def __init__(self, ticket_seller: TicketSeller) -> None:
        self.__ticket_seller = ticket_seller

    def enter(self, audience: Audience) -> None:
        self.__ticket_seller.sell_to_audience(audience=audience)
