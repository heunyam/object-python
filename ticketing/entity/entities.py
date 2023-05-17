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

    def has_invitation(self) -> bool:
        return self.invitation is None

    def set_ticket(self, ticket: Ticket) -> None:
        self.ticket = ticket

    def minus_amount(self, amount: Decimal) -> None:
        self.__amount -= amount

    def plus_amount(self, amount: Decimal) -> None:
        self.__amount += amount


# 관람객
class Audience:
    __bag: Bag

    def __init__(self, bag: Bag) -> None:
        self.__bag = bag

    def buy(self, ticket: Ticket) -> Decimal:
        if self.__bag.has_invitation():
            self.__bag.set_ticket(ticket=ticket)
            return Decimal("0")

        self.__bag.set_ticket(ticket=ticket)
        self.__bag.minus_amount(amount=ticket.get_fee())
        return ticket.get_fee()


# 매표소
class TicketOffice:
    __amount: Decimal
    __tickets: List[Ticket]

    def __init__(self, amount: Decimal, tickets: List[Ticket]) -> None:
        self.__amount = amount
        self.__tickets = tickets

    def get_ticket(self) -> Ticket:
        return self.__tickets.pop(0)

    def minus_amount(self, amount: Decimal) -> None:
        self.__amount -= amount

    def plus_amount(self, amount: Decimal) -> None:
        self.__amount += amount


# 판매원
class TicketSeller:
    __ticket_office: TicketOffice

    def __init__(self, ticket_office: TicketOffice) -> None:
        self.__ticket_office = ticket_office

    def get_ticket(self) -> Ticket:
        return self.__ticket_office.get_ticket()

    def sell_to_audience(self, audience: Audience) -> None:
        ticket = self.get_ticket()
        amount_paid = audience.buy(ticket=ticket)

        self.__ticket_office.plus_amount(amount=amount_paid)


# 소극장
class Theater:
    __ticket_seller: TicketSeller

    def __init__(self, ticket_seller: TicketSeller) -> None:
        self.__ticket_seller = ticket_seller

    def enter(self, audience: Audience) -> None:
        self.__ticket_seller.sell_to_audience(audience=audience)
