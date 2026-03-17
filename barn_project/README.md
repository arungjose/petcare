# 🐾 BARN — Pet Care Platform

**BARN** is a full-featured Django web application — a comprehensive pet ecosystem for finding, buying, adopting, and caring for pets.

---

## 🚀 Quick Setup (5 minutes)

### 1. Prerequisites
- Python 3.10+ installed
- pip package manager

### 2. Install Dependencies
```bash
cd barn_project
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py makemigrations accounts
python manage.py makemigrations pets
python manage.py makemigrations services
python manage.py makemigrations store
python manage.py makemigrations core
python manage.py migrate
```

### 4. Seed Initial Data (Categories, Breeds, Services)
```bash
python manage.py seed_data
```
This populates:
- Pet categories (Dogs, Cats, Birds, Rabbits, Fish) + 50+ breeds
- Service categories (Grooming, Vet, Training, Boarding) + 10 services
- Store categories (Food, Accessories, etc.)

### 5. Create Admin Superuser
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser. 🎉

---

## 📁 Project Structure

```
barn_project/
├── barn_project/        # Django settings & URLs
├── accounts/            # Custom user model, buyer & seller auth
├── core/                # Home, About, Contact pages
├── pets/                # Pet listings, adoption, inquiries
├── services/            # Grooming, Vet, Training, Boarding
├── store/               # Products, Cart, Checkout
├── templates/           # All HTML templates
│   ├── base.html
│   ├── core/
│   ├── accounts/
│   ├── pets/
│   ├── services/
│   └── store/
├── static/
│   ├── css/main.css     # Complete custom CSS (no framework)
│   └── js/main.js       # Vanilla JS
├── media/               # User-uploaded files
├── manage.py
└── requirements.txt
```

---

## 🔑 Key Features

### Dual Authentication
| Buyer | Seller / Breeder |
|-------|-----------------|
| Browse all pets | List unlimited pets |
| Contact sellers | Seller dashboard |
| Book services | Manage listings |
| Shop store | Public breeder profile |
| Adoption inquiries | Verification badge |

### Seller Registration Collects:
- Full business name & address
- **Breeder/Seller License Number**
- License document upload (PDF/image)
- Government ID upload
- KCI / kennel club membership
- Years in business & specialization
- Business phone, email, website
- Social media links (Instagram, Facebook)
- Admin review & verification system

### Admin Panel
Visit **http://127.0.0.1:8000/admin/**
- Approve/reject seller applications
- Manage all pet listings
- View service bookings
- Manage store orders
- Feature products

---

## 🎨 Design
- **Palette:** Deep Teal (#0f7b6c) + Coral Red (#e8401c) + Warm Cream
- **Fonts:** Playfair Display (headings) + DM Sans (body)
- **Fully responsive** — mobile, tablet, desktop
- Custom CSS only — no Bootstrap/Tailwind dependency
- Smooth animations and hover effects

---

## 📧 Seller Contact (mailto)
Pet detail pages include pre-filled mailto links:
```
mailto:seller@email.com?subject=Inquiry about PetName&body=Hi, I am interested...
```

---

## 🛡️ Admin Actions
```
/admin/accounts/sellerprofile/  → Approve or Reject sellers
/admin/pets/pet/                → Manage all listings
/admin/store/product/           → Feature products
/admin/services/servicebooking/ → Manage bookings
```

---

## 🌱 Adding Real Data
After seeding categories:
1. Log into admin and create a superuser seller account
2. Or register as a seller via the website
3. Use **List a Pet** to add pet listings with photos
4. Add products via Django admin → Store → Products
5. Mark products as **featured** to show on homepage

---

## ⚙️ Production Checklist
- [ ] Change `SECRET_KEY` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure AWS S3 / Cloudinary for media
- [ ] Set up email backend (SMTP)
- [ ] Run `python manage.py collectstatic`

---

Made with ❤️ for pets everywhere — **BARN Pet Platform**
