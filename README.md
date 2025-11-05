
# Medical Appointment Reservation System

This project is a web-based platform designed to facilitate online **appointment booking between patients and medical specialists**. The system ensures controlled and organized reservations so that each doctor can manage a limited number of appointments per month.

> **Current Status:**  
> We are currently in **Phase 1** of the project.  
> The system is being developed step-by-step and will be expanded with new features in future phases.

---

## ✅ Main Roles in the System

| Role | Description |
|------|-------------|
| **Admin** | Manages the entire platform, doctors, patients, specialties, and system configurations. |
| **Doctor** | Has a profile, manages appointment requests, confirms or rejects reservations, and reviews schedule. |
| **Patient** | Requests appointments, views reservation history, and manages upcoming appointments. |

---

## 🎯 Phase 1 Scope (Completed Features)

- Basic project setup using **Django**
- User management system (Authentication & Role Assignment)
- Core database design and **ERD** completed
- Models created:
  - `User`
  - `Doctor`
  - `Patient`
  - `MedicalSpecialty`
  - `Reservation`
  - `Configs`
  - `Wallet` & `Transaction` (prepared for future payment support)
- Initial admin panel configuration
- Project structure organized into modular Django apps

---

## 🏗 Technologies Used

| Layer | Tools & Frameworks |
|------|---------------------|
| Backend | Python, Django |
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Database | PostgreSQL |
| Version Control | Git & GitLab |
| Architecture | MVT (Model-View-Template) |

---

## 📦 Project Structure (High-Level)
    reservation_system/
    │
    ├── accounts/          # User, Doctor, Patient
    ├── specialties/       # Medical specialties data
    ├── reservations/      # Appointment logic
    ├── core/              # System configs & shared utilities
    └── templates/         # Global templates (public pages)
---

## 👥 Team Collaboration Notes

- The project is being developed collaboratively.
- All commits should follow GitLab workflow standards.
- Each phase will be delivered and reviewed before proceeding.
- Members : RAMIN,ATEFEH,NILOUFAR,HOSEIN,ZAHRA

---

## 💡 Summary

This system is currently in **Phase 1**, focused on:
- Github
- Database design
- Core model implementation
- Base admin panel setup

As development continues, the system will gradually evolve into a fully-featured appointment management platform.

---

GROUP_1 🤝