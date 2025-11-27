Medical Appointment Reservation System

This project is a web-based platform designed to facilitate online appointment booking between patients and medical specialists. The system ensures controlled and organized reservations so that each doctor can manage a limited number of appointments per month.

Current Status:
All four phases of the project have been completed. The system is fully functional with admin and doctor panels, appointment management, and advanced features.

⸻

✅ Main Roles in the System

Role	Description
Admin	Manages the entire platform, doctors, patients, specialties, and system configurations.
Doctor	Has a profile, manages appointment requests, confirms or rejects reservations, and reviews schedule.
Patient	Requests appointments, views reservation history, and manages upcoming appointments.


⸻

🎯 Phase 1 — Core Foundation (Completed)
	•	Basic project setup using Django
	•	User management system (Authentication & Role Assignment)
	•	Core database design and ERD completed
	•	Models created: User, Doctor, Patient, MedicalSpecialty, Reservation, Configs, Wallet & Transaction
	•	Initial admin panel configuration
	•	Modular project structure with separate Django apps

⸻

🎯 Phase 2 — Functional Expansion (Completed)
	•	Frontend Improvements
	•	Responsive UI for Patients and Doctors
	•	Public pages: Home, About Us, Contact Us
	•	Admin and Doctor dashboards
	•	Appointment Management Enhancements
	•	Automatic appointment conflict detection
	•	Appointment approval/rejection workflow for Doctors
	•	Calendar view for appointments
	•	System Features
	•	Logging and audit trail for critical actions

⸻

🎯 Phase 3 — Advanced Interaction & Automation (Completed)
	•	Notifications
	•	Email & SMS notifications for appointment requests, approvals, and upcoming appointments
	•	Calendar & Scheduling
	•	Full calendar integration for doctors
	•	Monthly/weekly/daily schedule views
	•	Automatic appointment limit enforcement
	•	Payments Integration
	•	Online payment gateway
	•	Wallet-based payments
	•	Invoice generation
	•	Advanced Features
	•	Auto-cancellation rules
	•	Waiting list system for fully booked doctors

⸻

🎯 Phase 4 — Optimization, Security & Deployment (Completed)
	•	Performance & Security
	•	Role-based access control (RBAC)
	•	API rate limiting
	•	CSRF/XSS protection
	•	Query optimization & caching
	•	Production-Level Features
	•	Docker containerization
	•	Nginx + Gunicorn deployment
	•	PostgreSQL optimized configuration
	•	Error logging with Sentry
	•	CI/CD pipelines
	•	User Experience Improvements
	•	Dark/Light mode
	•	Accessibility improvements
	•	Multi-language support

⸻

🏗 Technologies Used

Layer	Tools & Frameworks
Backend	Python, Django
Frontend	HTML, CSS, JavaScript, Bootstrap
Database	PostgreSQL
Version Control	Git & GitLab
Architecture	MVT (Model-View-Template)


⸻

📦 Project Structure (High-Level)

reservation_system/
│
├── accounts/          # User, Doctor, Patient
├── specialties/       # Medical specialties data
├── reservations/      # Appointment logic
├── core/              # System configs & shared utilities
└── templates/         # Global templates (public pages)


⸻

👥 Team Collaboration Notes
	•	The project was developed collaboratively.
	•	All commits followed GitLab workflow standards.
	•	Members : RAMIN, ATEFEH, NILOUFAR, HOSEIN, ZAHRA

⸻

💡 Summary

The system is fully functional across all four phases, including:
	•	Core models & authentication
	•	Dashboards and appointment management
	•	Notifications, calendar views, and payment system
	•	Security, optimization, and deployment readiness

GROUP_1 🤝