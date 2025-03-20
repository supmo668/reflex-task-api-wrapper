# Reflex Task Monitoring Template

A production-ready template for monitoring long-running tasks in Reflex applications with real-time updates via WebSocket and REST API endpoints.

## Features

- 🔄 Real-time task progress monitoring
- 🌐 REST API endpoints for task status
- 📡 WebSocket streaming for live updates
- 🎯 Multiple concurrent task tracking
- 🚦 Task lifecycle management
- 🔍 Separate views for active and completed tasks

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/reflex-task-api
cd reflex-task-api

# Install dependencies
pip install reflex
pip install -r requirements.txt

# Run the application
reflex run
```

## Usage

### As a Web Application

1. Open `http://localhost:3000` in your browser
2. Use the "Start New Task" button to create new tasks
3. Monitor task progress in real-time
4. View completed tasks history

### REST API

Get all tasks for a client:
```bash
curl http://localhost:8000/tasks/{client_token}
```

Get specific task status:
```bash
curl http://localhost:8000/tasks/{client_token}/{task_id}
```

### WebSocket API

Connect to WebSocket for all tasks updates:
```bash
wscat -c ws://localhost:8000/ws/tasks/{client_token}
```

Monitor specific task:
```bash
wscat -c ws://localhost:8000/ws/tasks/{client_token}/{task_id}
```

When monitoring a specific task, you'll receive updates only for that task:
```json
{
    "type": "state_update",
    "status": "Processing",
    "progress": 50,
    "created_at": 1234567890.123
}
```

## Task Monitoring Integration

### Using the Task Monitoring Decorator

```python
from reflex_task_api.task_wrapper import monitored_background_task

class YourState(rx.State):
    @monitored_background_task()
    async def your_long_running_task(self, task: Any):
        await task.update(progress=0, status="Starting...")
        # Your task logic here
        await task.update(progress=50, status="Processing...")
        # More task logic
        await task.update(progress=100, status="Complete!")
```

## Task Monitoring System

### Automatic Features (Handled by Decorator)

The `@monitored_background_task()` decorator automatically handles:

- ✨ Task ID Generation: Creates a unique ID for each task
- 📝 Task Registration: Adds task to the state's task registry
- 🚀 Initial State: Sets up task with STARTING status
- ✅ Task Completion: Updates task to FINISHED state when done
- ❌ Error Handling: Captures exceptions and marks task as ERROR
- 🧹 Cleanup: Marks task as inactive upon completion/error

### Manual Requirements (In Your Task Function)

Your task function needs to:

1. Accept the task context parameter:
```python
@monitored_background_task()
async def your_task(self, task: Any):  # task parameter is required
    # your code here
```

2. Update progress and status at key points:
```python
@monitored_background_task()
async def your_task(self, task: Any):
    # Start
    await task.update(progress=0, status="Starting data processing")
    
    # Update during processing
    await task.update(
        progress=50, 
        status="Processing batch 1/2"
    )
    
    # Updates are automatic for completion/errors
    # No need for final update
```

### Example Implementation

```python
@monitored_background_task()
async def process_data(self, task: Any):
    """Example of a properly monitored task."""
    try:
        # Initial progress
        await task.update(progress=0, status="Loading data")
        
        # Processing updates
        for i in range(5):
            # Do some work
            await asyncio.sleep(1)
            
            # Update progress
            await task.update(
                progress=(i + 1) * 20,
                status=f"Processing batch {i + 1}/5"
            )
            
        # No need for completion update - handled automatically
            
    except Exception as e:
        # No need for error handling - handled automatically
        raise
```

## Task States

Tasks can be in the following states:
- `NOT_STARTED`: Initial state
- `STARTING`: Task is being initialized
- `PROCESSING`: Task is executing
- `FINISHED`: Task completed successfully
- `ERROR`: Task encountered an error

## API Response Format

```json
{
    "active_tasks": [
        {
            "status": "Processing",
            "progress": 50,
            "created_at": 1234567890.123
        }
    ],
    "all_tasks": {
        "task_id": {
            "status": "Processing",
            "progress": 50,
            "created_at": 1234567890.123
        }
    }
}
```

## WebSocket Updates

```json
{
    "type": "state_update",
    "active_tasks": [...],
    "all_tasks": {...}
}
```

## Project Structure

```
reflex_task_api/
├── models.py         # Task data structures
├── states.py        # Application state management
├── task_wrapper.py  # Task monitoring decorator
├── api.py          # API endpoints
└── reflex_task_api.py  # Frontend components
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
