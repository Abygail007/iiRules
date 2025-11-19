from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.agent import Agent
from app.models.device import Device
from app.models.user import User
from app.schemas.agent import AgentCreate, AgentUpdate, AgentOut
from app.api.routes_auth import get_current_user


router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)


@router.post("/", response_model=AgentOut, status_code=status.HTTP_201_CREATED)
def create_agent(
    agent_in: AgentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AgentOut:
    # On vérifie que le device existe bien
    device = db.query(Device).filter(Device.id == agent_in.device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device inexistant pour cet agent",
        )

    agent = Agent(**agent_in.model_dump())
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


@router.get("/", response_model=List[AgentOut])
def list_agents(
    device_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[AgentOut]:
    query = db.query(Agent)
    if device_id is not None:
        query = query.filter(Agent.device_id == device_id)
    agents = query.order_by(Agent.id).all()
    return agents


@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AgentOut:
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent introuvable",
        )
    return agent


@router.put("/{agent_id}", response_model=AgentOut)
def update_agent(
    agent_id: int,
    agent_in: AgentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AgentOut:
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent introuvable",
        )

    data = agent_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(agent, field, value)

    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent introuvable",
        )

    db.delete(agent)
    db.commit()
    return None
