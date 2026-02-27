WAREHOUSE MANAGEMENT SYSTEM (DJANGO)

======================================================================
PROJECT OVERVIEW
======================================================================

A full-stack Warehouse Management System built using Django to manage
hardware devices, employee allocations, and administrative workflows.

The system allows administrators to manage devices (GPU, CPU, RAM, SSD),
assign them to employees, monitor availability, and track allocation
status in a structured and scalable manner.

This project demonstrates modular Django architecture, separation of
concerns, role-based access control, and reproducible database setup
using migrations and a custom seed command.

  ----------------------
  PROJECT ARCHITECTURE
  ----------------------

The application follows a multi-app Django architecture:

-   accounts → Custom user management
-   inventory → Device model & availability tracking
-   allocations → Device assignment & business logic
-   adminpanel → Admin dashboard & management features
-   warehouse_system → Core project configuration

This structure supports scalability and clean backend design.

  ---------------
  CORE FEATURES
  ---------------

AUTHENTICATION & ROLE MANAGEMENT - Admin login - Employee login -
Role-based dashboards

INVENTORY MANAGEMENT - Add, edit, and manage devices - Device
categories: GPU, CPU, RAM, SSD - Track device status: • Available •
Assigned • Maintenance

ALLOCATION WORKFLOW - Employees can request devices - Admin can
approve/reject requests - Track assigned devices - Fine/penalty handling
supported

ADMIN DASHBOARD - Manage users - Manage devices - Monitor allocation
requests

  ------------
  TECH STACK
  ------------

-   Python 3
-   Django
-   SQLite (default)
-   HTML5, CSS
-   Django Templates
-   Service-layer pattern (allocations/services.py)

  -------------------
  ENVIRONMENT SETUP
  -------------------

This project uses a Python virtual environment to isolate dependencies.
All required packages are listed in requirements.txt.

  --------------------------
  INSTALLATION & RUN GUIDE
  --------------------------

1)  Clone Repository

    git clone
    https://github.com/yourusername/warehouse-management-system.git cd
    warehouse-management-system

2)  Create Virtual Environment

    python -m venv venv

3)  Activate Virtual Environment

    Windows: venv

    Mac/Linux: source venv/bin/activate

4)  Install Dependencies

    pip install -r requirements.txt

5)  Apply Migrations

    python manage.py migrate

6)  Seed Sample Data

    python manage.py seed_data

    Default Admin Credentials: Username: admin Password: admin123

7)  Run Development Server

    python manage.py runserver

    Visit: http://127.0.0.1:8000/

  -------------------
  DESIGN HIGHLIGHTS
  -------------------

-   Modular multi-app Django architecture
-   Separation of business logic (service layer pattern)
-   Role-based access control
-   Reproducible database using migrations + seed command
-   Clean template organization
-   Backend-oriented scalable design

  ---------------------
  FUTURE IMPROVEMENTS
  ---------------------

-   PostgreSQL integration
-   REST API using Django REST Framework
-   Token-based authentication
-   Email notifications for approvals
-   Docker containerization
-   Cloud deployment (Render / AWS)

  --------
  AUTHOR
  --------

Kunal Singh Backend Developer (Django)
