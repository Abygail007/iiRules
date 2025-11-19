from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.device import Device
from app.models.user import User
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceOut
from app.api.routes_auth import get_current_user


router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)


@router.post("/", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
def create_device(
    device_in: DeviceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DeviceOut:
    device = Device(**device_in.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@router.get("/", response_model=List[DeviceOut])
def list_devices(
    organisation_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[DeviceOut]:
    query = db.query(Device)
    if organisation_id is not None:
        query = query.filter(Device.organisation_id == organisation_id)
    devices = query.order_by(Device.id).all()
    return devices


@router.get("/{device_id}", response_model=DeviceOut)
def get_device(
    device_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DeviceOut:
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device introuvable",
        )
    return device


@router.put("/{device_id}", response_model=DeviceOut)
def update_device(
    device_id: int,
    device_in: DeviceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DeviceOut:
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device introuvable",
        )

    data = device_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(device, field, value)

    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(
    device_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device introuvable",
        )

    db.delete(device)
    db.commit()
    return None
