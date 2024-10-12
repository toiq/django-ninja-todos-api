from django.contrib import admin

from .models import Profile, Todo, TodoList

# Register your models here.


# TodoList Admin
@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created", "updated")
    list_filter = ("user", "created", "updated")  # Filter by user and date fields
    search_fields = ("name", "description")  # Search by name and description
    ordering = ("-created",)  # Order by creation date (most recent first)
    date_hierarchy = "created"  # Adds date hierarchy for easier date navigation


# Todo Admin
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "todo_list",
        "is_completed",
        "due_date",
        "created",
        "updated",
    )
    list_filter = (
        "todo_list",
        "is_completed",
        "due_date",
    )  # Filter by todo list, completion status, and due date
    search_fields = ("title", "description")  # Enable search by title and description
    ordering = ("-created",)  # Order by creation date
    date_hierarchy = "due_date"  # Date hierarchy based on the todo's due date


# Profile Admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "dark_mode", "created", "updated")
    list_filter = ("dark_mode", "created", "updated")  # Filter by dark mode and dates
    search_fields = ("user__username",)  # Search by the username (foreign key)
    ordering = ("-created",)  # Order by creation date
