# Clinic Management System (full stack)

Stack: Django REST Framework + SimpleJWT, MySQL (SQLite while developing), React (Vite) + Axios + Bootstrap.
Layout: backend/ (project "clinic") and frontend/.

## Roles (JWT login, role-based access)
- Admin: manages users and doctors, sees reports
- Receptionist: registers patients, books appointments, issues tokens, creates bills
- Doctor: sees own appointments and token queue, writes consultations and prescriptions, views patient history
- (Optional later) Pharmacist: sees prescriptions, marks them dispensed

## Apps and models
- accounts: User (role field: admin/receptionist/doctor), DoctorProfile (user, specialization, fee)
- patients: Patient (name, age, gender, phone, address, created_at)
- appointments: Appointment (patient, doctor, date, time, status), Token (appointment, number per doctor per day, status: waiting/in_consultation/done)
- consultations: Consultation (appointment, symptoms, diagnosis, notes), Prescription (consultation, medicine, dosage, duration)
- billing: Bill (appointment, consultation_fee, other_charges, total, paid_status, payment_mode)

## Rules
- Role-based permissions on every endpoint
- Token numbers reset daily per doctor
- Patient history = all past consultations and prescriptions for that patient
- Validation: no double booking of the same doctor at the same time; unique phone for patients

## Validations (backend, using serializers and model validation)

Patients
- name: required, 2 to 100 characters, letters and spaces only
- age: integer from 0 to 120
- gender: one of male, female, other
- phone: required, unique, exactly 10 digits
- address: optional, maximum 255 characters

Users and login
- username and email: required and unique, valid email format
- password: minimum 8 characters, not all numbers
- role: must be admin, receptionist or doctor
- wrong credentials return 401 with a clear message

Appointments
- date: cannot be in the past
- time: within clinic hours (for example 09:00 to 17:00)
- doctor and patient must exist
- the same doctor cannot have two appointments at the same date and time
- the same patient cannot book twice with the same doctor on the same day
- status can only move: booked, then done or cancelled (no changes after done)

Tokens
- token number is generated automatically, per doctor per day, and cannot be edited
- status can only move: waiting, in_consultation, done

Consultations and prescriptions
- only the doctor assigned to the appointment can create a consultation
- one consultation per appointment
- diagnosis required; medicine and dosage required for each prescription line

Billing
- consultation_fee and other_charges cannot be negative
- total is calculated by the server, not accepted from the client
- one bill per appointment; a paid bill cannot be edited
- payment_mode must be cash, card or upi

General
- role-based permissions on every endpoint (403 for the wrong role)
- return proper status codes: 400 for invalid data, 401 not logged in, 403 not allowed, 404 not found
- frontend also checks required fields and shows the backend error messages

## Frontend screens
- Login, then dashboard by role
- Receptionist: register/search patients, book appointment, token queue, billing
- Doctor: today's queue, consultation form, patient history
- Admin: manage users/doctors, daily summary