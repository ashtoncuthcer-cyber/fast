

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from ..database import SessionDep
from .. import schemas, models, oauth2


router = APIRouter(
    prefix='/votes',
    tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: SessionDep,
    user: models.User = Depends(oauth2.get_current_user),
):
    found_vote = db.exec(
        select(models.Vote)
        .where(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)
    ).first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'User {user.id} has already voted on {vote.post_id}'
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'success'}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User {user.id} has not voted on {vote.post_id}'
            )
        db.delete(found_vote)
        db.commit()
        return {'message': 'successfully deleted'}