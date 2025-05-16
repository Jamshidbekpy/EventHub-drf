# EventHub-drf
for UIC exam

## UZB

# EventHub Proyekti

Bu EventHub proyekti bo'lib, men buni 4 ta app ochib qildim.

3 ta app sof DRF da qilindi: `base`, `accounts`, `events`  
1 ta app esa template bilan qilindi, ya'ni an'anaviy Django uslubida.

---

## Qilingan ishlar

### 1) base app
- `BaseModel` uchun ishlatildi.

---

### 2) accounts app

**Model: `CustomUser`**

- a) **Register** → Foydalanuvchi ro'yxatdan o'tadi va bazaga qo'shiladi (`is_active=False`). Tasdiq uchun Superuserga email yuboriladi.
- b) **Activation** → Foydalanuvchi emaildan havola olib ustiga bosib tasdiqlaydi (`is_active=True`).
- c) `CustomUser` modelida `is_organizer_pending` atributi mavjud.
- d) Foydalanuvchi bo'lib o'tgan obyekt organizer darajasi uchun email orqali ariza yuboradi.
- e) Superuser emailidagi havolani ustiga bossagina `is_organizer_pending=True` bo'ladi va shu zahoti foydalanuvchi emailiga statusi ko'tarilgani haqida xabar boradi.
- f) Yuqoridagi `e` banddagi jarayon **signal** bilan amalga oshirilgan.
- g) Login, logout va boshqa autentifikatsiya funksiyalari **JWT** orqali ishlangan.
- h) Qo‘shimcha fake foydalanuvchi va organizer yaratish uchun **management commands** yozilgan.

**APILAR:**
###### api/register/
###### api/activate/"uidb64"/"token"/
###### api/confirm-organizer/
###### api/activate-organizer/"uidb64"/"token"/
###### api/token/
###### api/token/refresh/
###### api/logout/


---

### 3) events app

**Model: `Event`, `EventParticipant`**

- a) List va Create uchun 1 ta API chiqarilgan. Create faqat tashkilotchi tomonidan amalga oshiriladi va `perform_create` orqali `owner` qilib saqlanadi.
- b) Retrieve, Update va Delete uchun 1 ta API chiqarilgan. Update va Delete faqat `owner` tomonidan amalga oshiriladi. Retrieve esa barcha uchun ochiq.Delete event bo'ladi, agar owner bo'lsa , hamda Eventga foydalanuvchi qo'shilmagan bo'lsa.
- c) Tadbirga foydalanuvchi ro'yxatdan o'tadi. Bu vaqtda `EventParticipant` modelidagi `is_active=False` bo'ladi. Emailga xabar yuboriladi.
- d) Foydalanuvchi emailiga tashkilotchidan havola yuboriladi, u havola orqali bosgach `is_active=True` holatga o‘tadi.
- e) Huddi shu holat tadbirdan chiqish uchun ham ishlatiladi (Logout Event), email notification bilan.
- f) **Management command:**  
  `python manage.py send_reminders` → Tadbir bugun yoki ertaga bo‘lsa, ro‘yxatdan o‘tgan foydalanuvchilarga eslatma yuboradi.
- g) Bu jarayonlar **generator** orqali filterlanadi va **thread** yordamida foydalanuvchilarga parallel email yuboriladi.
- h) Agar tadbir kuni, lokatsiyasi yoki boshqa filtrlari o‘zgarsa, barcha foydalanuvchilarga ogohlantirish yuboriladi.
- i) `h` banddagi ishlar **signal** bilan bajariladi.
- j) Qo‘shimcha **management command** orqali fake Eventlar yaratish mumkin.

**APILAR:**

###### api/events/
###### api/events/str:slug/
###### api/events/str:slug/register/
###### api/events/activate/"uidb64"/"token"/
###### api/events/str:slug/cancel/
###### api/events/confirm-logout/"uidb64"/"token"/


---

### 4) events2 app (Template asosida)

- Bu qismda Eventlar ro‘yxati (`list`) hamda Eventning detali (`detail`) ko‘rsatilgan.
- 2 ta template yozilgan.

**URLS:**

###### events-list
###### event-detail


---

## 5) Umumiy foydalanilgan texnologiyalar va imkoniyatlar

- a) Permissions
- b) JWT Authentication
- c) Threads
- d) Signals
- e) Custom Management Commands
- f) Email
- g) Templates
- h) Django & Django Rest Framework (DRF)

Ushbu bilim va texnologiyalardan foydalanilgan.









## ENG


# EventHub Project

This is the **EventHub** project, which is divided into 4 separate Django apps.

Three apps are built using pure **Django REST Framework** (`base`, `accounts`, `events`),  
and one app is built using **traditional Django with templates** (`events2`).

---

## Implemented Features

### 1) base app
- Used for defining a common abstract `BaseModel`.

---

### 2) accounts app

**Model: `CustomUser`**

- a) **Register** → A user can register, and their data is added to the database (`is_active=False`). An email is sent to the superuser for activation.
- b) **Activation** → The user receives an activation link via email, and after clicking it, their account becomes active (`is_active=True`).
- c) The `CustomUser` model includes a boolean field `is_organizer_pending`.
- d) A user can apply to become an organizer. An application is sent to the superuser via email.
- e) When the superuser clicks the confirmation link, `is_organizer_pending=True` is set, and the user receives an email notifying them of the role upgrade.
- f) The process described in (e) is handled via **Django signals**.
- g) Login, logout, and other authentication features are implemented using **JWT**.
- h) Additional **management commands** are created to generate fake users and organizers.

**API Endpoints:**
###### api/register/
###### api/activate/"uidb64"/"token"/
###### api/confirm-organizer/
###### api/activate-organizer/"uidb64"/"token"/
###### api/token/
###### api/token/refresh/
###### api/logout/

---

### 3) events app

**Models: `Event`, `EventParticipant`**

- a) A combined API for listing and creating events is available. Only organizers can create events, and ownership is assigned via `perform_create`.
- b) A single API supports retrieve, update, and delete operations. Update and delete are restricted to the event owner, while retrieve is public.
- c) When a user registers for an event, a new `EventParticipant` is created with `is_active=False`. An email notification is sent.
- d) The user receives an email from the organizer containing an activation link. Upon clicking, `is_active=True` is set.
- e) The same process applies for event unregistration (logout from event), with email notifications.
- f) **Management Command:**  
  `python manage.py send_reminders` → Sends reminders to users for events occurring today or tomorrow.
- g) Events are filtered using **generators**, and notifications are sent in parallel using **threads**.
- h) If event details such as date or location are changed, all participants receive a parallel notification using threads.
- i) The behavior described in (h) is also implemented using **Django signals**.
- j) A management command is available to generate fake events.

**API Endpoints:**
###### api/events/
###### api/events/str:slug/
###### api/events/str:slug/register/
###### api/events/activate/"uidb64"/"token"/
###### api/events/str:slug/cancel/
###### api/events/confirm-logout/"uidb64"/"token"/


---

### 4) events2 app (Template-based)

- This part uses Django templates to display a list of events and event details.
- Two templates are used.

**URLs:**
###### events-list
###### event-detail


---

## 5) Technologies and Features Used

- a) Permissions
- b) JWT Authentication
- c) Threads
- d) Signals
- e) Custom Management Commands
- f) Email System
- g) Templates
- h) Django & Django Rest Framework (DRF)

These technologies and concepts were used to build the project.