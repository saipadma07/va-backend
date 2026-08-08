# SIA – Multimodal AI Assistant

SIA (Smart Interactive Assistant) is a multimodal AI assistant that combines conversational AI, voice interaction, visual processing, and an interactive Unity-based avatar interface.

## Overview

The project consists of a Python/FastAPI backend responsible for AI processing and a Unity-based frontend that provides the interactive user interface and avatar experience.

The system integrates multiple AI components to process user inputs and generate intelligent responses through an interactive multimodal interface.

## Key Features

- LLM-powered conversational interaction
- Voice-based interaction
- Visual input and processing
- OCR-based information extraction
- Interactive Unity avatar
- Backend API services using FastAPI
- Integration with Groq-hosted LLMs
- Live2D-based avatar interaction
- Dockerized backend setup

## Tech Stack

### Backend
- Python
- FastAPI
- Groq / LLM integration
- Computer Vision
- OCR
- Docker

### Frontend
- Unity
- C#
- Live2D Cubism

## Project Structure

```text
SIA-Multimodal-AI-Assistant/
│
├── app/
│   └── Backend application and AI processing
│
├── unity-frontend/
│   ├── Assets/
│   ├── Packages/
│   └── ProjectSettings/
│
├── Dockerfile
├── requirements.txt
└── test_tts.py 

# Architchture
                 ┌─────────────────────┐
                 │   Unity Frontend    │
                 │      C# / Avatar    │
                 └──────────┬──────────┘
                            │
                            │ API Requests
                            ▼
                 ┌─────────────────────┐
                 │    FastAPI Backend  │
                 │       Python        │
                 └──────────┬──────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
          LLM /          Vision /       Voice
        Groq Client      OCR Processing  Processing

Backend

The backend is implemented using Python and FastAPI and contains components for AI model interaction, vision processing, and communication with the Unity frontend.

Unity Frontend

The frontend is developed using Unity and C#. It provides the interactive avatar interface and connects to the backend services for AI-powered interactions.

The project also uses Live2D Cubism components for avatar animation and interaction.

Running the Project
Backend

Install the required Python dependencies:

pip install -r requirements.txt

Start the FastAPI application using the project's configured entry point.

Unity Frontend

Open the unity-frontend directory as a Unity project using a compatible Unity version.

Configure the required backend/API settings before running the application.

Project Status

The repository contains the backend implementation and Unity frontend source files for the SIA multimodal AI assistant.

Technologies

Python • FastAPI • LLMs • Computer Vision • OCR • Docker • Unity • C# • Live2D Cubism


