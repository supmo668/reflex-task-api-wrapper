"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
import asyncio

from .states import MonitorState

# Frontend components
def task_status_display():
    websocket_command = f"wscat -c ws://localhost:8000/ws/tasks/{MonitorState.client_token}"
    tasks_command = f"curl http://localhost:8000/tasks/{MonitorState.client_token}"
    
    return rx.vstack(
        rx.heading("Task Monitor"),
        rx.text("Client Token: ", MonitorState.client_token),
        rx.text("API Access:"),
        rx.hstack(
            rx.code_block(tasks_command, language="bash", can_copy=True),
        ),
        rx.text("WebSocket Connection:"),
        rx.code_block(websocket_command, language="bash", can_copy=True),
        rx.button(
            "Start New Task",
            on_click=MonitorState.long_running_task,
        ),
        rx.divider(),
        rx.heading("Active Tasks"),
        rx.foreach(
            MonitorState.current_active_tasks,
            lambda task: rx.vstack(
                rx.text(f"Task ID: {task.id}"),  # Use task.id consistently
                rx.text(f"Status: {task.status}"),
                rx.progress(value=task.progress, max=100),
                rx.text("Monitor this task:"),
                rx.code_block(
                    f"wscat -c ws://localhost:8000/ws/tasks/{MonitorState.client_token}/{task.id}",
                    language="bash",
                    can_copy=True,
                ),
                padding="2",
            )
        ),
        rx.heading("Completed Tasks"),
        rx.foreach(
            MonitorState.completed_tasks,
            lambda task: rx.vstack(
                rx.text(f"Status: {task.status}"),
                rx.text(f"Task ID: {task.id}"),
                padding="2",
            )
        ),
        spacing="4",
    )

def index():
    return rx.center(
        task_status_display()
    )

app = rx.App()
app.add_page(index)

# Now, setup API routes
from .api import setup_api
setup_api(app)

