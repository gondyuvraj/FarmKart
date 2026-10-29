import os
import django
from decimal import Decimal
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmkart.settings')
django.setup()

from products.models import Category, Product
from reviews.models import Review
from django.contrib.auth.models import User

# Ensure media directory exists
os.makedirs('media/products', exist_ok=True)

def generate_product_image(filename, title, subtitle, badge_text, bg_start, bg_end, accent_color):
    """Generate high-resolution e-commerce product graphic."""
    width, height = 700, 700
    img = Image.new('RGB', (width, height), color=bg_start)
    draw = ImageDraw.Draw(img)

    # Draw rounded-corner container card
    card_margin = 35
    draw.rounded_rectangle(
        [card_margin, card_margin, width - card_margin, height - card_margin],
        radius=25,
        fill='#ffffff',
        outline='#e2e8f0',
        width=3
    )

    # Top accent bar
    draw.rounded_rectangle(
        [card_margin, card_margin, width - card_margin, card_margin + 20],
        radius=10,
        fill=accent_color
    )

    # Inner decorative badge
    draw.rounded_rectangle(
        [card_margin + 30, card_margin + 40, card_margin + 240, card_margin + 80],
        radius=20,
        fill=accent_color
    )
    draw.text((card_margin + 45, card_margin + 50), f"★ {badge_text}", fill='#ffffff')

    # Brand / Category tag
    draw.text((card_margin + 40, card_margin + 105), subtitle.upper(), fill='#64748b')

    # Main Product Visual Box
    box_top = card_margin + 140
    box_bottom = height - card_margin - 130
    draw.rounded_rectangle(
        [card_margin + 30, box_top, width - card_margin - 30, box_bottom],
        radius=20,
        fill=bg_end,
        outline='#cbd5e1',
        width=2
    )

    # Central agricultural icon & title representation
    draw.text((width // 2 - 140, box_top + 60), "🌾 KISAN QUALITY 🌾", fill=accent_color)
    draw.text((width // 2 - 180, box_top + 130), title[:24], fill='#0f172a')
    draw.text((width // 2 - 130, box_top + 180), "100% Genuine Agri Inputs", fill='#475569')

    # Bottom Banner
    bot_y = height - card_margin - 90
    draw.rounded_rectangle(
        [card_margin + 30, bot_y, width - card_margin - 30, bot_y + 60],
        radius=12,
        fill='#f8fafc',
        outline='#e2e8f0',
        width=1
    )
    draw.text((card_margin + 50, bot_y + 20), "✓ Verified By Agronomists", fill='#16a34a')
    draw.text((width - card_margin - 220, bot_y + 20), "⚡ Fast Rural Dispatch", fill='#d97706')

    filepath = os.path.join('media', 'products', filename)
    img.save(filepath, 'WEBP', quality=90)
    return f"products/{filename}"

print("Creating product images and populating data...")

# 1. Categories
categories_data = [
    {
        'name': 'Crop Protection & Pesticides',
        'hindi_name': 'कीटनाशक एवं फसल सुरक्षा',
        'icon': '🛡️',
        'description': 'Targeted pest control, insecticides, fungicides, and weedicides to safeguard standing crops.'
    },
    {
        'name': 'Certified Seeds',
        'hindi_name': 'प्रमाणित बीज',
        'icon': '🌱',
        'description': 'High-germination, disease-resistant hybrid and open-pollinated field and vegetable seeds.'
    },
    {
        'name': 'Fertilizers & Plant Nutrition',
        'hindi_name': 'उर्वरक एवं पोषण',
        'icon': '🧪',
        'description': 'Water-soluble NPK, micronutrient chelates, and soil boosters for enhanced crop yields.'
    },
    {
        'name': 'Farming Tools & Sprayers',
        'hindi_name': 'कृषि औजार एवं स्प्रेयर',
        'icon': '🚜',
        'description': 'Battery knapsack sprayers, drip irrigation kits, weeding implements, and pruning equipment.'
    },
    {
        'name': 'Organic & Bio-Products',
        'hindi_name': 'जैविक उत्पाद',
        'icon': '🌿',
        'description': 'Eco-friendly neem formulations, bio-fertilizers, and enriched vermicompost.'
    },
]

cat_objects = {}
for cdata in categories_data:
    cat, _ = Category.objects.update_or_create(
        name=cdata['name'],
        defaults={
            'hindi_name': cdata['hindi_name'],
            'icon': cdata['icon'],
            'description': cdata['description']
        }
    )
    cat_objects[cat.name] = cat

# Also ensure legacy category names point properly if exists
legacy_pesticides = Category.objects.filter(name='Pesticides').first()
if legacy_pesticides:
    legacy_pesticides.hindi_name = 'कीटनाशक'
    legacy_pesticides.icon = '🛡️'
    legacy_pesticides.save()
    cat_objects['Pesticides'] = legacy_pesticides

legacy_fert = Category.objects.filter(name='fertilizer').first()
if legacy_fert:
    legacy_fert.name = 'Fertilizers & Plant Nutrition'
    legacy_fert.hindi_name = 'उर्वरक एवं पोषण'
    legacy_fert.icon = '🧪'
    legacy_fert.save()
    cat_objects['Fertilizers & Plant Nutrition'] = legacy_fert

# 2. Products Data
products_data = [
    {
        'name': 'PrimixSuper Insecticide (40% + 4% EC)',
        'hindi_name': 'प्रिमिक्स सुपर कीटनाशक',
        'category': cat_objects.get('Pesticides') or cat_objects['Crop Protection & Pesticides'],
        'brand': 'Dhanuka Agritech',
        'price': Decimal('2450.00'),
        'discount': Decimal('5.00'),
        'stock': 58,
        'unit': '1 Litre',
        'crop_type': 'Cotton, Chilli, Paddy, Soybean, Brinjal',
        'dosage': '2 ml per Litre of water (30-35 ml per 15L spray pump)',
        'application_method': 'Foliar Spray with Flat Fan Nozzle',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'rating': Decimal('4.8'),
        'review_count': 18,
        'description': 'PrimixSuper is a broad-spectrum, translaminar and contact insecticide formulated with Profenophos 40% + Cypermethrin 4% EC. It gives quick knockdown and reliable residual control against bollworms, aphids, jassids, and thrips in cash crops.',
        'image': 'products/primix-super-profenophos-40-cyper-4-ec-1000x1000.webp',
    },
    {
        'name': 'Kisan Gold HD-3086 Certified Wheat Seeds',
        'hindi_name': 'किसान गोल्ड गेहूं बीज (HD-3086)',
        'category': cat_objects['Certified Seeds'],
        'brand': 'National Seeds Corp (NSC)',
        'price': Decimal('1850.00'),
        'discount': Decimal('15.00'),
        'stock': 120,
        'unit': '40 Kg Bag',
        'crop_type': 'Wheat (गेहूं) - Rabi Season',
        'dosage': '40 Kg seed rate per Acre (Sowing depth 4-5 cm)',
        'application_method': 'Line Sowing with Seed Drill / Broadcasting',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'rating': Decimal('4.9'),
        'review_count': 32,
        'description': 'HD-3086 is India\'s top-yielding bread wheat variety with outstanding resistance to yellow and brown rust. Produces bold, amber grains with high chapati quality and protein content (12.5%). Matures uniformly in 120-130 days with average yield of 24-28 quintals per acre.',
        'image_gen': ('wheat_seeds_hd3086.webp', 'HD-3086 Wheat Seeds', 'Certified Hybrid Seeds', 'Top Yield 2026', '#fefce8', '#fef3c7', '#ca8a04')
    },
    {
        'name': 'IFFCO NPK 19:19:19 100% Water Soluble Fertilizer',
        'hindi_name': 'इफको एनपीके 19-19-19 घुलनशील खाद',
        'category': cat_objects['Fertilizers & Plant Nutrition'],
        'brand': 'IFFCO',
        'price': Decimal('1150.00'),
        'discount': Decimal('20.00'),
        'stock': 85,
        'unit': '1 Kg Pack',
        'crop_type': 'All Fruits, Vegetables, Cotton, Sugarcane, Wheat',
        'dosage': '4 - 5 Grams per Litre of water (Foliar) or 2-3 Kg per Acre (Drip)',
        'application_method': 'Drip Irrigation & Foliar Spray',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'rating': Decimal('4.7'),
        'review_count': 26,
        'description': 'Balanced formulation of primary plant nutrients (19% Nitrogen, 19% Phosphorus, 19% Potassium) in completely water-soluble form. Free from sodium and chlorine, accelerates vigorous root growth, healthy foliage, and fruit setting in all crop stages.',
        'image_gen': ('iffco_npk_191919.webp', 'NPK 19-19-19 Soluble', 'IFFCO Plant Nutrition', '20% OFF Deal', '#eff6ff', '#dbeafe', '#2563eb')
    },
    {
        'name': '16L Double Motor Battery Knapsack Sprayer',
        'hindi_name': '16 लीटर डबल मोटर बैटरी स्प्रे पंप',
        'category': cat_objects['Farming Tools & Sprayers'],
        'brand': 'KisanKraft Agro',
        'price': Decimal('3899.00'),
        'discount': Decimal('25.00'),
        'stock': 24,
        'unit': '1 Unit with Fast Charger & 4 Nozzles',
        'crop_type': 'Universal for field crops, orchards, and tea gardens',
        'dosage': '12V 12Ah Heavy-duty Lead Battery (6 Hours battery backup)',
        'application_method': 'Telescopic Brass Spray Lance with Pressure Regulator',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': False,
        'rating': Decimal('4.8'),
        'review_count': 19,
        'description': 'High-performance agricultural sprayer equipped with dual micro-motors generating up to 130 PSI pressure. Features ergonomic back cushion, chemical-resistant PP tank, continuous spray lock, voltmeter display, and a heavy brass lance for effortless spraying.',
        'image_gen': ('battery_sprayer_16l.webp', '16L Battery Sprayer', 'KisanKraft Double Motor', 'Top Rated Tool', '#faf5ff', '#f3e8ff', '#9333ea')
    },
    {
        'name': 'Pure Cold-Pressed Neem Oil (10,000 PPM Azadirachtin)',
        'hindi_name': 'शुद्ध नीम का तेल (जैविक कीटनाशक)',
        'category': cat_objects['Organic & Bio-Products'],
        'brand': 'BioKisan Organics',
        'price': Decimal('799.00'),
        'discount': Decimal('15.00'),
        'stock': 60,
        'unit': '1 Litre Bottle',
        'crop_type': 'Vegetables, Pulses, Mustard, Floriculture, Tea',
        'dosage': '3 to 5 ml per Litre of water with 1 ml liquid soap/emulsifier',
        'application_method': 'Foliar Spray during early morning or late evening',
        'is_organic': True,
        'is_featured': True,
        'is_best_seller': True,
        'rating': Decimal('4.9'),
        'review_count': 35,
        'description': '100% natural, unadulterated cold-pressed neem kernel oil enriched with high azadirachtin content (10,000 PPM). Acts as an anti-feedant, repellent, and growth disruptor against 200+ destructive agricultural pest species without harming beneficial honeybees.',
        'image_gen': ('neem_oil_organic.webp', 'Cold-Pressed Neem Oil', '100% Organic Certified', 'Bio-Pest Guard', '#f0fdf4', '#dcfce7', '#16a34a')
    },
    {
        'name': 'Enriched Bio-Vermicompost Organic Fertilizer',
        'hindi_name': 'केंचुआ जैविक खाद (पोषक तत्वों से भरपूर)',
        'category': cat_objects['Organic & Bio-Products'],
        'brand': 'GreenEarth Bio',
        'price': Decimal('550.00'),
        'discount': Decimal('10.00'),
        'stock': 90,
        'unit': '25 Kg Moisture-Proof Bag',
        'crop_type': 'Soil conditioning for all field crops, orchards, and nursery',
        'dosage': '1 to 2 Tons per Acre during soil preparation or bed making',
        'application_method': 'Direct Soil Incorporation / Basin Application',
        'is_organic': True,
        'is_featured': False,
        'is_best_seller': True,
        'rating': Decimal('4.9'),
        'review_count': 42,
        'description': 'A-grade vermicompost produced via Eisenia fetida earthworms. Rich in organic carbon, humic acid, and beneficial mycorrhizae. Enhances soil aeration, doubles moisture retention capacity, and provides slow-release micronutrients throughout the crop cycle.',
        'image_gen': ('vermicompost_organic_25kg.webp', 'Enriched Vermicompost', 'GreenEarth Bio-Soil', 'Soil Gold', '#fbfbfa', '#f0ede6', '#78350f')
    },
    {
        'name': 'Gravity Drip Irrigation Starter Kit (100 Plants)',
        'hindi_name': 'ड्रिप सिंचाई किट (100 पौधों के लिए)',
        'category': cat_objects['Farming Tools & Sprayers'],
        'brand': 'Jain Micro-Irrigation',
        'price': Decimal('2299.00'),
        'discount': Decimal('22.00'),
        'stock': 18,
        'unit': 'Complete DIY Kit (16mm Pipe + 100 Emitters + Connectors)',
        'crop_type': 'Vegetables (Tomato, Brinjal, Chilli), Orchards, Polyhouses',
        'dosage': 'Saves up to 70% irrigation water; operates at low gravity pressure',
        'application_method': 'Surface or Sub-surface Drip Line Laying',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': False,
        'rating': Decimal('4.7'),
        'review_count': 14,
        'description': 'Engineered micro-drip kit tailored for small-holder farmers and vegetable beds. Includes 100 meters of UV-stabilized 16mm LDPE mainline tubing, 100 pressure-compensating inline drippers (4 LPH), punch tool, screen filter, and tap connector for zero electricity gravity watering.',
        'image_gen': ('drip_irrigation_kit.webp', '100-Plant Drip Kit', 'Jain Water Saver', 'Save 70% Water', '#f0fdfa', '#ccfbf1', '#0d9488')
    },
    {
        'name': 'Syngenta Red Ruby F1 Hybrid Tomato Seeds',
        'hindi_name': 'सिंजेंटा रेड रूबी हाइब्रिड टमाटर बीज',
        'category': cat_objects['Certified Seeds'],
        'brand': 'Syngenta Seeds',
        'price': Decimal('899.00'),
        'discount': Decimal('12.00'),
        'stock': 80,
        'unit': '10 Grams (Approx 3,200 Seeds)',
        'crop_type': 'Tomato (टमाटर) - Kharif & Rabi',
        'dosage': '40-50 Grams per Acre nursery sowing',
        'application_method': 'Pro-tray nursery raising followed by field transplanting',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': True,
        'rating': Decimal('4.8'),
        'review_count': 23,
        'description': 'Premier indeterminate hybrid producing glossy, deep red oval-shaped tomatoes (90-100g). Exhibits high tolerance to Tomato Leaf Curl Virus (ToLCV) and Bacterial Wilt. Excellent firmness and shelf life suitable for long-distance transport to mandis.',
        'image_gen': ('syngenta_tomato_seeds.webp', 'Red Ruby F1 Tomato', 'Syngenta Hybrid Seeds', 'Viral Resistant', '#fef2f2', '#fee2e2', '#dc2626')
    }
]

for pdata in products_data:
    image_rel_path = pdata.get('image')
    if 'image_gen' in pdata:
        fname, t, sub, btext, bg1, bg2, acc = pdata['image_gen']
        image_rel_path = generate_product_image(fname, t, sub, btext, bg1, bg2, acc)

    prod, created = Product.objects.update_or_create(
        name=pdata['name'],
        defaults={
            'hindi_name': pdata.get('hindi_name', ''),
            'category': pdata['category'],
            'brand': pdata['brand'],
            'price': pdata['price'],
            'discount': pdata['discount'],
            'stock': pdata['stock'],
            'unit': pdata.get('unit', '1 Unit'),
            'crop_type': pdata.get('crop_type', ''),
            'dosage': pdata.get('dosage', ''),
            'application_method': pdata.get('application_method', 'Foliar Spray'),
            'is_organic': pdata.get('is_organic', False),
            'is_featured': pdata.get('is_featured', False),
            'is_best_seller': pdata.get('is_best_seller', False),
            'rating': pdata.get('rating', Decimal('4.8')),
            'review_count': pdata.get('review_count', 0),
            'description': pdata['description'],
            'image': image_rel_path,
        }
    )
    print(f"Product '{prod.name}' -> created: {created}, image: {prod.image}")

# 3. Add Verified Farmer Reviews
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin123')

farmer_users = [
    ('ramesh_patel', 'Ramesh Patel', 'Gujarat'),
    ('sukhdev_singh', 'Sukhdev Singh', 'Punjab'),
    ('santosh_yadav', 'Santosh Yadav', 'Madhya Pradesh'),
    ('babu_rao', 'Babu Rao', 'Maharashtra')
]

user_objs = []
for uname, fname, _ in farmer_users:
    u, _ = User.objects.get_or_create(username=uname, defaults={'first_name': fname, 'email': f'{uname}@kisan.in'})
    user_objs.append(u)

farmer_reviews = [
    ("HD-3086 Wheat Seeds are genuine. Germination was above 95% in my 4-acre field. Very strong tillering!", 5, "Wheat"),
    ("IFFCO 19-19-19 gave excellent lush green leaves within 4 days of foliar spray on my tomato crop.", 5, "Tomato"),
    ("Very fast delivery in our village! The battery sprayer is powerful and light on the back.", 5, "Cotton"),
    ("Pure neem oil. Used it on aphids and whitefly, pest count dropped dramatically without any chemical damage.", 5, "Chilli")
]

products = list(Product.objects.all())
for i, prod in enumerate(products):
    if not prod.reviews.exists():
        review_text, rating, crop = farmer_reviews[i % len(farmer_reviews)]
        farmer_user = user_objs[i % len(user_objs)]
        Review.objects.create(
            product=prod,
            user=farmer_user,
            rating=rating,
            comment=review_text,
            crop_used_on=crop,
            is_verified_farmer=True
        )

print("Data population completed successfully!")
