from typing import List, Optional
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.security import django_auth
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from pydantic import ValidationError

from api.schemas import (
    SignInSchema,
    SignUpSchema,
    TodoListSchemaIn,
    TodoListSchemaOut,
    TodoSchemaIn,
    TodoSchemaOut,
)
from .models import Todo, TodoList

api = NinjaAPI(auth=django_auth, title="Todos django-ninja API")


@api.post("/register", auth=None, tags=["Authentication"])
def register(request, payload: SignUpSchema):
    """Register a new user"""
    try:
        user = User(
            username=payload.username,
            email=payload.email,
        )
        user.set_password(payload.password)
        user.full_clean()
        user.save()
    except ValidationError as e:
        return {"success": False, "message": str(e)}
    except Exception as e:
        return {"success": False, "message": "An error occurred: " + str(e)}

    return {"success": True, "message": "User registered successfully"}


@api.get("/set-csrf-token", auth=None, tags=["Authentication"])
def get_csrf_token(request):
    """Get CSRF Token"""
    return {"csrftoken": get_token(request)}


@api.post("/login", auth=None, tags=["Authentication"])
def login_view(request, payload: SignInSchema):
    """Login a user"""
    user = authenticate(request, username=payload.username, password=payload.password)
    if user is not None:
        login(request, user)
        id = User.objects.get(username=user.username).pk
        return {"success": True, "id": id}
    return {"success": False, "message": "Invalid credentials"}


@api.post("/logout", tags=["Authentication"])
def logout_view(request):
    """Logout the authenticated user"""
    logout(request)
    return {"message": "Logged out"}


@api.get("/user", tags=["User Management"])
def user(request):
    """Get logged-in user information"""
    return {
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
    }


@api.delete("/delete-user", tags=["User Management"])
def delete_user(request):
    """Delete the authenticated user account"""
    user = request.user  # Get the currently authenticated user
    if user.is_authenticated:
        user.delete()  # Delete the user instance
        return {"success": True, "message": "User account deleted successfully."}
    return {"success": False, "message": "User not authenticated."}


@api.get("/todo-lists", tags=["TodoList Management"], response=list[TodoListSchemaOut])
def todo_list(request):
    """Get all todo lists"""
    todo_list = TodoList.objects.all()
    return todo_list


@api.get(
    "/todo-list/{id}",
    tags=["TodoList Management"],
    response=Optional[TodoListSchemaOut],
)
def todo_list_by_id(request, id: int):
    """Get a todo list by ID"""
    todo_list = get_object_or_404(TodoList, pk=id)
    return todo_list


@api.post(
    "/todo-list/", tags=["TodoList Management"], response=Optional[TodoListSchemaOut]
)
def add_todo_list(request, data: TodoListSchemaIn):
    """Create a new todo list"""
    try:
        new_todo_list = TodoList(**data.dict())
        new_todo_list.save()
    except Exception as e:
        print({"Error": e})
        return None
    return new_todo_list


@api.put(
    "/todo-list/{id}",
    tags=["TodoList Management"],
    response=Optional[TodoListSchemaOut],
)
def update_todo_list(request, id: int, data: TodoListSchemaIn):
    """Update a todo list by ID"""
    todo_list = get_object_or_404(TodoList, pk=id)
    for attr, value in data.dict().items():
        setattr(todo_list, attr, value)
    todo_list.save()
    return todo_list


@api.delete("/todo-list/{id}", tags=["TodoList Management"])
def delete_todo_list(request, id: int):
    """Delete a todo list by ID"""
    todo_list = get_object_or_404(TodoList, pk=id)
    todo_list.delete()
    return {"success": True, "message": "Todo list deleted successfully."}


@api.post("/todo/", response=TodoSchemaOut, tags=["Todo Management"])
def create_todo(request, data: TodoSchemaIn):
    """Create a new todo"""
    todo = Todo(**data.dict())
    todo.save()
    return todo


@api.get("/todos/", response=List[TodoSchemaOut], tags=["Todo Management"])
def list_todos(request):
    """Retrieve all todos"""
    todos = Todo.objects.all()
    return todos


@api.get("/todo/{id}/", response=TodoSchemaOut, tags=["Todo Management"])
def get_todo(request, id: int):
    """Retrieve a todo by ID"""
    todo = get_object_or_404(Todo, id=id)
    return todo


@api.put("/todo/{id}/", response=TodoSchemaOut, tags=["Todo Management"])
def update_todo(request, id: int, data: TodoSchemaIn):
    """Update a todo by ID"""
    todo = get_object_or_404(Todo, id=id)
    for attr, value in data.dict().items():
        setattr(todo, attr, value)
    todo.save()
    return todo


@api.delete("/todo/{id}/", tags=["Todo Management"])
def delete_todo(request, id: int):
    """Delete a todo by ID"""
    todo = get_object_or_404(Todo, id=id)
    todo.delete()
    return {"success": True, "message": "Todo deleted successfully."}
