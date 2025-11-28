# task-management-system
Python task manager using Factory, Observer, and Singleton design patterns
# 🎯 TaskFlow: Design Patterns in Action

Welcome to my coding playground! This file contains **two complete systems** that showcase different aspects of my programming skills.

## 🗂️ What's Inside This File

### System 1: Task Management Engine 🎯
*(Starts around line 370)*
A sophisticated task manager built with three powerful design patterns:

**🏭 Factory Pattern** - Creates different task types (Design, Review, Deployment) intelligently
**👀 Observer Pattern** - Automatically notifies users when their tasks update  
**👑 Singleton Pattern** - Ensures only one TaskManager runs the show

### System 2: Sensor Aggregation System 📡  
*(First part of the file)*
A high-performance data processing system that handles multiple sensor readings simultaneously with smart load balancing.

## 🎮 Why Two Systems in One File?

In the real world, developers often work on multiple related systems. This demonstrates my ability to:
- **Organize complex code** in a single codebase
- **Work on different problem domains** simultaneously
- **Apply appropriate architectures** for different needs

## 🏗️ Task System Highlights

### The Smart Factory
```python
# Instead of remembering how to create each task type:
task = TaskFactory.create_task("design", "Design new logo", jordan)
