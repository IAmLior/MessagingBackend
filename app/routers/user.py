from handlers import user as userHandler
from models import request, user as userModel
from fastapi import APIRouter

class userRouter:
    def __init__(self):
        self.user_handler = userHandler.UserHandler()
        self.router = APIRouter()
        self.router.add_api_route("/users/register", self.register_user, methods=["POST"], response_model=userModel.User)
        self.router.add_api_route("/users/block", self.block_user, methods=["POST"])

    def register_user(self, request: request.RegisterUserRequest):
        return self.user_handler.register_user(request.username)

    def block_user(self, request: request.BlockUserRequest):
        return self.user_handler.block_user(request.user_id, request.block_user_id)