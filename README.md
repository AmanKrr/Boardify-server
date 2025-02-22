# Bordify Server

Bordify Server is a backend service built with **FastAPI** that enables the creation and management of **public and private rooms** for real-time collaboration. It serves as the core backend for the **Bordify** project, handling authentication, room management, and real-time communication.

## Features

- **Public & Private Rooms**: Create and manage rooms with different visibility settings.
- **FastAPI-Based Backend**: High-performance, asynchronous API.
- **WebSockets Support**: Real-time communication for seamless collaboration.
- **User Authentication**: Secure access control for private rooms.
- **Scalable Architecture**: Designed to handle multiple users efficiently.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/amankrr/bordify-server.git
   cd bordify-server
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up the environment variables:

   - Create a `.env` file based on `.env.example` and update necessary configurations.

5. Run the server:

   ```sh
   uvicorn main:app --reload

   or

   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## WebSockets

- **`ws://server-url/ws/public`** – Connect to a public space for real-time updates.
- **`ws://server-url/ws/{room_id}`** – Connect to a room for real-time updates.
