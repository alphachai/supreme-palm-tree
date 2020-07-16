import logging
from typing import List

import pydantic
from decouple import config
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from app.db import Base
from app.utils import exception_to_str

logger = logging.getLogger()


def commit(db: Session):
    try:
        db.commit()
        return True
    except IntegrityError as e:
        if config("DEBUG"):
            # Do not expose schema in production.
            detail = exception_to_str(e)
        else:
            detail = e.__class__
        raise HTTPException(
            status_code=400,
            detail=f"Your request violated the database schema: {detail}",
        ) from e


def create(db: Session, model: Base, **kwargs):
    """Create a new entity given a model.

    Args:
        db (Session):
        model (app.db.Base):
        **kwargs: fields which will be passed to the model constructor
    """
    logger.info(f"Creating: {model}<{kwargs}>")
    entity = model(**kwargs)
    db.add(entity)
    commit(db)
    db.refresh(entity)
    return entity


def read(db: Session, model: Base, skip: int, limit: int):
    """List all entities for a given model.

    Args:
        db (Session):
        model (app.db.Base):
        skip (int): lower bound of results
        limit (int): page size
    """
    query = db.query(model).offset(skip).limit(limit)
    if query.count() == 0:
        raise HTTPException(status_code=404, detail=f"No entities exist for {model}")
    return query.all()


def update(db: Session, query: Query, data: pydantic.BaseModel):
    query.update(data.dict(exclude_unset=True))
    return commit(db)


def delete(db: Session, model: Base, ids: List[int]):
    query = db.query(model).filter(model.id.in_(ids))
    query.delete(synchronize_session=False)
    return commit(db)
