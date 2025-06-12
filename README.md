# Medical Records Odoo Module

![Medical Records Icon](static/description/icon.png)

## Overview

The **Medical Records** module for Odoo enables clinics, hospitals, and medical organizations to efficiently manage patient medical records, track medical histories, record accidents, procedures, treatments, allergies, and more. It is designed for extensibility, security, and ease of use, with robust role-based access control (RBAC) for administrators and users.

---

## Features

- **Patient Medical Records**: Create and manage detailed records for each patient, including demographics, allergies, and medical history.
- **Medical History Tracking**: Record and view all medical histories, including procedures, accidents, and treatments, per patient.
- **Accident Management**: Log new accidents, auto-generate accident numbers, and track severity, date, and place of treatment.
- **Procedures & Treatments**: Add and review all procedures and treatments performed for each patient.
- **Allergy & Disease Management**: Maintain lists of allergies and diseases, with admin-only editing rights.
- **Medical Expenses**: Track payments, particulars, and remarks for each patient.
- **Doctor Reports**: Aggregate and analyze medical data by doctor, including total patients, procedures, treatments, and accidents.
- **Role-Based Access Control (RBAC)**: 
  - **Clinic Manager**: Full control (add/edit/delete all records, manage disease types, edit patient history).
  - **Clinic User**: Limited (can only add new patient records, cannot edit disease types or existing patient history).
- **User Privilege Management**: Assign user roles from Odoo Settings > Users.
- **Demo Data**: Sample patients, users, and histories for easy testing.
- **PDF Reports**: Generate printable medical record reports.

---

## Installation

1. Copy the `custom_medical_module` directory to your Odoo `addons` folder.
2. Restart the Odoo server.
3. Update the app list in Odoo.
4. Install the **Medical Records** module from the Apps menu.

---

## Configuration

- **User Roles**: Go to Settings > Users and assign users to either `Clinic Manager` or `Clinic User`.
- **Disease/Allergy Lists**: Only Clinic Managers can add or edit disease and allergy types.
- **Access Rights**: Configured in `security/ir.model.access.csv` and `security/medical_groups.xml`.

---

## Usage

- **Create a Patient Record**: Go to Medical > Medical Records > Create.
- **Add Medical History**: From a patient record, click "New History" to add a new medical history entry.
- **Log Procedures, Accidents, Treatments**: Use the buttons in the medical history form to add new entries. All are shown in their respective tabs.
- **View/Print Reports**: Use the Reports menu or print from the patient record.
- **Manage Users**: Assign roles in Settings > Users.

---

## Demo Data

Demo data is provided in the `demo/` directory for quick testing:
- Sample users, patients, histories, procedures, and treatments.

---

## Security & RBAC

- **Clinic Manager** (`group_medical_admin`): Full create, read, update, delete rights on all models.
- **Clinic User** (`group_medical_user`): Can only create new patient records and histories, cannot edit or delete existing records, cannot manage disease types.
- **Groups are managed in**: `security/medical_groups.xml` and can be assigned in the Odoo UI.

---

## File Structure

- `models/` - Data models for records, histories, accidents, etc.
- `views/` - XML views for forms, lists, menus, and reports.
- `security/` - Access control and group definitions.
- `data/` - Initial data and sequences.
- `demo/` - Demo data for testing.
- `report/` - QWeb PDF report templates.
- `static/description/icon.png` - Module icon.

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and add tests if applicable.
4. Submit a pull request with a clear description of your changes.

---

## License

This module is licensed under the Odoo Proprietary License v1.0. See [LICENSE](LICENSE) for details.

---

## Author & Maintainer

- **Author**: Gemechisgk (Gemechis Kedir)
- **Website**: 

For support, open an issue on GitHub or contact the author via the website. 