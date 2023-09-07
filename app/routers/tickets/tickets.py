from utilities.request_utils import RequestUtils
from internal.zendesk.dependencies import ZendeskStrConstants, ZendeskDictConstants
import json
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends
from typing import Optional, List
from fastapi import Query
from internal.okta.okta import Okta

ticket_router = APIRouter()


class TicketListMeta(BaseModel):
    has_more: bool
    after_cursor: Optional[str] = None
    before_cursor: Optional[str] = None


class Ticket(BaseModel):
    assignee_id: Optional[int] = Field(None, description="The agent currently assigned to the ticket")
    created_at: Optional[str] = Field(None, description="When this record was created")
    collaborator_ids: Optional[List] = Field(None, description="The ids of users currently CC'ed on the ticket")
    custom_fields: Optional[List] = Field(None, description="Custom fields for the ticket")
    custom_status_id: Optional[int] = Field(None, description="The custom ticket status id of the ticket")
    description: Optional[str] = Field(None, description="The first comment on the ticket")
    due_at: Optional[str] = Field(None, description="If this is a ticket of type 'task' it has a due date. Due date format uses ISO 8601 format")
    email_cc_ids: Optional[List] = Field(None, description="The ids of agents or end users currently CC'ed on the ticket")
    external_id: Optional[str] = Field(None, description="An id you can use to link Zendesk Support tickets to local records")
    follower_ids: Optional[List] = Field(None, description="The ids of agents currently following the ticket")
    group_id: Optional[int] = Field(None, description="The group this ticket is assigned to")
    id: Optional[int] = Field(None, description="Automatically assigned when the ticket is created")
    organization_id: Optional[int] = Field(None, description="The organization of the requester. You can only specify the ID of an organization associated with the requester")
    priority: Optional[str] = Field(None, description="The urgency with which the ticket should be addressed. ALlowed values are 'urgent', 'high', 'normal', or 'low'")
    recipient: Optional[str] = Field(None, description="The original recipient e-mail address of the ticket. Notification emails for the ticket are sent from this address")
    requester_id: int = Field(None, description="The user who requested this ticket")
    satisfaction_rating: Optional[object] = Field(None, description="The satisfaction rating of the ticket, if it exists, or the state of satisfaction, 'offered' or 'unoffered'. The value is null for plan types that don't support CSA")
    status: Optional[str] = Field(None, description="The state of the ticket. If your account has activated custom ticket statuses, this is the ticket's status category. Allowed values are 'new', 'open', 'pending', 'hold', 'solved', or 'closed'")
    subject: Optional[str] = Field(None, description="The value of the subject field for this ticket")
    submitter_id: Optional[int] = Field(None, description="The user who submitted the ticket. The submitter always becomes the author of the first comment on the ticket")
    tags: Optional[List] = Field(None, description="The array of tags applied to this ticket")
    ticket_form_id: Optional[int] = Field(None, description="Enterprise only. The id of the ticket form to render for the ticket")
    type: Optional[str] = Field(None, description="The type of this ticket. Allowed values are 'propblem', 'incident', 'question', or 'task'")
    updated_at: Optional[str] = Field(None, description="When this record last got updated")
    url: Optional[str] = Field(None, description="The API url of this ticket")


class TicketList(BaseModel):
    tickets: List[Ticket]
    meta: TicketListMeta


@ticket_router.get("/tickets",
                   tags=["tickets"],
                   summary="List all tickets",
                   description="List all tickets on account",
                   response_model=TicketList
                   )
def tickets(page_size: Optional[int] = Query(100, description="Page size")): # add -> valid: bool = Depends(Okta.validate), to require clientID/secret
    base_url = ZendeskStrConstants.list_tickets_url.value
    url = f'{base_url}?page[size]={page_size}'

    response = json.loads(RequestUtils.get(url=url,
                                       headers=ZendeskDictConstants.api_header.value).text)
    ticket_data = response['tickets']
    meta = TicketListMeta(
        has_more=response['meta']['has_more'],
        after_cursor=response['meta']['after_cursor'],
        before_cursor=response['meta']['before_cursor']
    )
    return TicketList(tickets=ticket_data, meta=meta)
