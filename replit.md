# Overview

This is a Flask-based email inbox manager application that provides AI-powered email processing capabilities. The application serves as a mock email management system with integrated OpenAI functionality for intelligent email analysis and processing. It includes a predefined set of sample emails covering various categories like technical support, billing confirmations, business collaborations, security alerts, and newsletters.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
- **Flask** - Lightweight Python web framework chosen for its simplicity and rapid development capabilities
- **RESTful API Design** - Standard REST endpoints for email operations with JSON responses
- **Environment-based Configuration** - OpenAI API key managed through environment variables for security

## AI Integration
- **OpenAI GPT-5 Integration** - Latest OpenAI model (released August 7, 2025) for advanced email processing
- **Conditional Client Initialization** - OpenAI client only initialized when API key is available, preventing crashes in development
- **Error Handling** - Graceful degradation when AI services are unavailable

## Data Management
- **In-Memory Data Store** - Mock email data stored in Python list structure for rapid prototyping
- **Structured Email Schema** - Each email contains id, sender, subject, body, and timestamp fields
- **Sample Data Coverage** - Diverse email types to test various processing scenarios

## Frontend Architecture
- **Server-Side Rendering** - Uses Flask's render_template_string for dynamic HTML generation
- **JSON API Responses** - RESTful endpoints return structured JSON for API consumers
- **Minimal Dependencies** - No complex frontend framework, keeping the application lightweight

# External Dependencies

## AI Services
- **OpenAI API** - GPT-5 model for email content analysis, categorization, and intelligent responses
- **OpenAI Python Client** - Official SDK for seamless API integration

## Web Framework
- **Flask** - Python micro web framework for HTTP handling and routing
- **Werkzeug** - WSGI utility library (Flask dependency) for request/response handling

## Development Environment
- **Environment Variables** - OPENAI_API_KEY for secure API key management
- **Python Runtime** - Standard Python environment with pip package management