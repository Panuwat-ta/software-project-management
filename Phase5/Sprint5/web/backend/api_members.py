"""Members API: thin REST wrapper over MemberManager."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from . import deps

router = APIRouter(prefix="/api/members", tags=["members"])

VALID_TIERS = ("Regular", "Silver", "Gold", "Platinum")


class MemberIn(BaseModel):
    """Member payload (tier normalised, never errors)."""

    member_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    tier: str = "Regular"


def to_dict(member) -> dict:
    """Serialise a domain Member for JSON responses."""
    return {
        "member_id": member.member_id,
        "name": member.name,
        "tier": member.tier,
        "discount_rate": member.discount_rate,
    }


@router.get("", response_model=list)
def list_members() -> list:
    """List every member ordered by id."""
    return [to_dict(m) for m in deps.get_members().find_all()]


@router.post("", status_code=201)
def upsert_member(payload: MemberIn) -> dict:
    """Insert or overwrite a member (unknown tier -> Regular)."""
    manager = deps.get_members()
    manager.save_member(
        deps.domain.Member(
            payload.member_id.strip(),
            payload.name.strip(),
            payload.tier,
        )
    )
    saved = manager.find_by_id(payload.member_id.strip())
    if saved is None:
        raise HTTPException(500, "Failed to persist member!")
    return to_dict(saved)


@router.get("/tiers")
def list_tiers() -> list:
    """List valid tiers with their discount rates."""
    return [
        {"tier": name, "discount_rate": rate}
        for name, rate in [
            ("Regular", 0.0),
            ("Silver", 0.05),
            ("Gold", 0.10),
            ("Platinum", 0.15),
        ]
    ]


@router.get("/{member_id}")
def get_member(member_id: str) -> dict:
    """Fetch one member; 404 when missing (never SQL)."""
    found = deps.get_members().find_by_id(member_id)
    if found is None:
        raise HTTPException(404, "Member not found!")
    return to_dict(found)


@router.delete("/{member_id}")
def delete_member(member_id: str) -> dict:
    """Delete a member; 404 when the id is unknown."""
    removed = deps.get_members().delete_member(member_id)
    if not removed:
        raise HTTPException(404, "Member not found!")
    return {"deleted": member_id}
