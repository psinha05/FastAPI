from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from model import Gender, Role, User

app = FastAPI()

db: List[User] = [
    User(
        id = "a1fe65a1-786b-47df-bf04-590fee98a188",
        first_name= "Harsh",
        last_name= "Sinha",
        gender = Gender.male,
        roles = [Role.admin, Role.user]       

    ),

     User(
        id = "971c10eb-62ea-4612-9f34-acaa16512a1e",
        first_name= "Maxxi",
        last_name= "Planck",
        gender = Gender.female,
        roles = [Role.student]       

    ),

    User(
        id = "971c10eb-62ea-4612-9f34-acaa16513b2d",
        first_name= "Adam",
        last_name= "Smith",
        gender = Gender.male,
        roles = [Role.student]       
    )

]

class UserUpdateRequest(BaseModel):
      first_name: Optional[str]
      last_name: Optional[str]
      roles: Optional[List[Role]]
      


@app.get("/")
def root():
    return {"Hello": "FastAPI"} 


@app.get("/app/v1/users")
async def get_users():
    return db


@app.post("/app/v1/users")
async def register_user(user:User):
    db.append(user)
    return {"register user id": user.id}

@app.delete("/app/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
           db.remove(user)
           return
        
    raise HTTPException(
         status_code=404,
         detail=f"user with id: {user_id} does not exists"
    )
    
@app.put("/app/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
           if user_update.first_name is not None:
               user.first_name = user_update.first_name
           if user_update.last_name is not None:
               user.last_name = user_update.last_name
           if user_update.roles is not None:
               user.roles= user_update.roles       
           return        
    raise HTTPException(
         status_code=404,
         detail=f"user with id: {user_id} does not exists"
    )

    



