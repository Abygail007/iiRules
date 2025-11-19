from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.agent import Agent
from app.models.device import Device
from app.schemas.agent import AgentCreate, AgentRead, AgentUpdate

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("/", response_model=List[AgentRead])
def list_agents(db: Session = Depends(get_db)) -> List[AgentRead]:
    agents = db.query(Agent).order_by(Agent.id).all()
    return agents


@router.get("/{agent_id}", response_model=AgentRead)
def get_agent(agent_id: int, db: Session = Depends(get_db)) -> AgentRead:
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent non trouvé",
        )
    return agent


@router.post("/", response_model=AgentRead, status_code=status.HTTP_201_CREATED)
def create_agent(agent_in: AgentCreate, db: Session = Depends(get_db)) -> AgentRead:
    # 1) vérifier que le device existe
    device = db.query(Device).filter(Device.id == agent_in.device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device inexistant pour cet agent",
        )

    # 2) vérifier qu'il n'y a pas déjà un agent lié à ce device (1:1)
    existing = db.query(Agent).filter(Agent.device_id == agent_in.device_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un agent existe déjà pour ce device",
        )

    agent = Agent(
        device_id=agent_in.device_id,
        install_key=agent_in.install_key,
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


@router.put("/{agent_id}", response_model=AgentRead)
def update_agent(
    agent_id: int, agent_in: AgentUpdate, db: Session = Depends(get_db)
) -> AgentRead:
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent non trouvé",
        )

    update_data = agent_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)

    db.commit()
    db.refresh(agent)
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: int, db: Session = Depends(get_db)) -> None:
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent non trouvé",
        )

    db.delete(agent)
    db.commit()
    return None
