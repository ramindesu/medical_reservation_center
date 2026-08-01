# Medical Appointment Reservation System

This project is a web-based platform designed to facilitate online **appointment booking between patients and medical specialists**. The system ensures controlled and organized reservations so that each doctor can manage a limited number of appointments per month.

> **Current Status:**  
> We are currently in **Phase 2** of the project.  
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

## 🎯 Phase 2 Scope (Current / In Progress)

**Phase 2** focuses on enhancing the platform with more **user-friendly features and functional improvements**:

- **Frontend Improvements**
  - Responsive and interactive UI for Patients and Doctors
  - Public pages: Home, About Us, Contact Us
  - Dashboard for Admins and Doctors

- **Appointment Management Enhancements**
  - Automatic appointment conflict detection
  - Appointment approval/rejection workflow for Doctors
  - Calendar view for appointments
- **System Features**
  - Logging and audit trail for critical actions
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
- Members : RAMIN, ATEFEH, NILOUFAR, GHAZAAL

---

## 💡 Summary

The system is evolving from **Phase 1** to **Phase 2**, adding:

- Improved UI/UX
- Appointment management enhancements
- Notifications and calendar views
- Preparations for online payments

As development continues, the system will gradually evolve into a fully-featured appointment management platform.

---

GROUP_1 🤝


