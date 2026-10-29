# FarmKart — Agricultural E-Commerce & Kisan Advisory Platform 🌾🚜

A full-stack agricultural e-commerce platform built with **Python & Django**, powered by **MongoDB**, and styled with **modern Vanilla CSS & JavaScript**. Designed specifically for farmers and agricultural suppliers.

---

## 🌟 Key Highlights & Features

- **🛒 E-Commerce Storefront:**
  - Dynamic product catalog with category, price, and organic filters
  - Live search by product name, Hindi name, brand, or crop type
  - Detailed product pages with dosage guidelines, application methods, and customer ratings
  - Session-based persistent shopping cart with free delivery threshold indicator
  - Seamless checkout (Cash on Delivery / UPI / Kisan Credit Card)
  - Printable tax invoices & order receipts
  - Customer self-service order cancellation before transit (with automatic stock restock)
  - Customer Wishlist management

- **📊 Admin Control Center (`/admin-panel/`):**
  - Live revenue analytics & order fulfillment pipeline metrics
  - Low stock & out-of-stock inventory alerts
  - Complete Product CRUD with quick inline stock adjustments
  - Category CRUD with Hindi translations & visual icons
  - Order fulfillment workflow (Placed → Confirmed → Shipped → Delivered → Cancelled)
  - Courier tracking number & delivery estimation updates
  - Customer review moderation & automatic star rating recalculation
  - Dynamic store broadcast announcement ticker

- **🧮 Kisan Fertilizer & Advisory Calculator (`/calculator/`):**
  - Tailored dosage calculator for major Indian crops (Wheat, Paddy/Rice, Cotton, Sugarcane, Potato, Mustard, Vegetables)
  - Stage-by-stage application guidelines (Basal, CRI, Flowering, Tillering)
  - Automatic Acre-to-Bags conversion for Urea, DAP, MOP, and Zinc

- **🔌 REST API Endpoint (`/api/products/`):**
  - JSON API for mobile app integrations and third-party agri-services

---

## 🛠️ Technology Stack

- **Backend:** Python 3.14+, Django 6.1, Django REST Framework
- **Database:** MongoDB (via official `django-mongodb-backend` & `pymongo`)
- **Frontend:** Django Templates (HTML5/CSS3), Vanilla CSS, Vanilla JavaScript
- **Graphics & Media:** Pillow
- **Environment Management:** `python-dotenv`

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+** (tested on Python 3.14)
- **MongoDB** (local service at `mongodb://localhost:27017/` or MongoDB Atlas connection string)

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/FarmKart.git
cd FarmKart
```

### 3. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Ensure your MongoDB connection settings in `.env`:
```env
MONGODB_HOST=mongodb://localhost:27017/
MONGODB_NAME=FarmKart
SECRET_KEY=your-custom-secret-key-for-development
```

### 6. Run Migrations & Seed Data
```bash
# Apply database schema
python manage.py migrate

# (Optional) Seed realistic agricultural catalog data and graphics
python populate_farmkart_data.py
```

### 7. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 8. Run Verification Test Suite
```bash
python test_full_suite.py
```
> All tests across template compilation, public routes, admin dashboard, and full CRUD operations should return **`[PASS]`**.

### 9. Start the Server
```bash
python manage.py runserver
```

---

## 🌐 Application URLs

| Interface | URL | Description |
| :--- | :--- | :--- |
| **Storefront** | `http://127.0.0.1:8000/` | Main agricultural marketplace & home page |
| **Agri Calculator** | `http://127.0.0.1:8000/calculator/` | Kisan Fertilizer dosage & crop calculator |
| **Admin Control Center** | `http://127.0.0.1:8000/admin-panel/` | Business metrics, orders & inventory management |
| **Django Admin** | `http://127.0.0.1:8000/admin/` | Default Django superuser admin backend |
| **REST API** | `http://127.0.0.1:8000/api/products/` | JSON product catalog endpoint |

---

## 📁 Project Structure

```
FarmKart/
│
├── accounts/          # Customer/Farmer authentication & user profiles
├── admin_panel/       # Executive dashboard, stock alerts, order fulfillment
├── cart/              # Session cart management & free delivery calculations
├── farmkart/          # Core Django project config (settings, routing, wsgi)
├── mongo_migrations/  # MongoDB schema migrations
├── orders/            # Checkout, invoicing, status tracking & stock restoration
├── payments/          # Payment configuration & integration endpoints
├── products/          # Catalog, search, filters, wishlist & fertilizer calculator
├── reviews/           # Farmer reviews, star ratings & recalculation logic
├── static/            # CSS stylesheets and client-side JavaScript
├── templates/         # HTML5 Django templates (modular layout)
├── test_full_suite.py # Automated end-to-end verification test suite
├── populate_farmkart_data.py # Initial database seeder script
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
