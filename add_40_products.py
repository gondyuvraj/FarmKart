import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from decimal import Decimal
from PIL import Image, ImageDraw

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmkart.settings')
import django
django.setup()

from products.models import Category, Product
from reviews.models import Review
from django.contrib.auth.models import User

os.makedirs('media/products', exist_ok=True)

def generate_image(filename, title, subtitle, badge_text, bg_start, bg_end, accent_color):
    width, height = 700, 700
    img = Image.new('RGB', (width, height), color=bg_start)
    draw = ImageDraw.Draw(img)

    card_margin = 35
    draw.rounded_rectangle(
        [card_margin, card_margin, width - card_margin, height - card_margin],
        radius=25,
        fill='#ffffff',
        outline='#cbd5e1',
        width=3
    )

    # Top accent header
    draw.rounded_rectangle(
        [card_margin, card_margin, width - card_margin, card_margin + 22],
        radius=10,
        fill=accent_color
    )

    # Badge box
    draw.rounded_rectangle(
        [card_margin + 25, card_margin + 35, card_margin + 260, card_margin + 75],
        radius=18,
        fill=accent_color
    )
    draw.text((card_margin + 40, card_margin + 46), f"★ {badge_text}", fill='#ffffff')

    # Brand tag
    draw.text((card_margin + 30, card_margin + 95), subtitle.upper(), fill='#64748b')

    # Central Box
    box_top = card_margin + 125
    box_bottom = height - card_margin - 110
    draw.rounded_rectangle(
        [card_margin + 25, box_top, width - card_margin - 25, box_bottom],
        radius=20,
        fill=bg_end,
        outline='#94a3b8',
        width=2
    )

    draw.text((width // 2 - 140, box_top + 50), "🌾 100% GENUINE AGRI INPUT 🌾", fill=accent_color)
    draw.text((width // 2 - 190, box_top + 120), title[:26], fill='#0f172a')
    draw.text((width // 2 - 150, box_top + 175), "Certified Rural Doorstep Delivery", fill='#475569')

    # Bottom Seal
    bot_y = height - card_margin - 80
    draw.rounded_rectangle(
        [card_margin + 25, bot_y, width - card_margin - 25, bot_y + 55],
        radius=12,
        fill='#f8fafc',
        outline='#cbd5e1',
        width=1
    )
    draw.text((card_margin + 45, bot_y + 18), "✓ Kisan Call Center Verified (1800-180-1551)", fill='#166534')

    file_path = os.path.join('media/products', filename)
    img.save(file_path, quality=90)
    return f"products/{filename}"


# Retrieve or create base categories
cat_fert = Category.objects.filter(name='Fertilizers & Plant Nutrition').first()
if not cat_fert:
    cat_fert = Category.objects.create(
        name='Fertilizers & Plant Nutrition',
        hindi_name='उर्वरक एवं पोषण',
        icon='🌱',
        description='Macro and micro nutrient fertilizers, water-soluble NPK, and bio-nutrients.'
    )

cat_pest = Category.objects.filter(name='Crop Protection & Pesticides').first() or Category.objects.filter(name='Pesticides').first()
if not cat_pest:
    cat_pest = Category.objects.create(
        name='Crop Protection & Pesticides',
        hindi_name='कीटनाशक एवं फसल सुरक्षा',
        icon='🛡️',
        description='Chemical and biological insecticides, fungicides, and weedicides.'
    )

cat_seeds = Category.objects.filter(name='Certified Seeds').first()
if not cat_seeds:
    cat_seeds = Category.objects.create(
        name='Certified Seeds',
        hindi_name='प्रमाणित बीज',
        icon='🌾',
        description='Government and university tested high-yield certified crop and vegetable seeds.'
    )

cat_tools = Category.objects.filter(name='Farming Tools & Sprayers').first()
if not cat_tools:
    cat_tools = Category.objects.create(
        name='Farming Tools & Sprayers',
        hindi_name='कृषि औजार एवं स्प्रेयर',
        icon='🚜',
        description='Modern knapsack battery sprayers, pruning shears, soil meters, and protective gear.'
    )

cat_organic = Category.objects.filter(name='Organic & Bio-Products').first()
if not cat_organic:
    cat_organic = Category.objects.create(
        name='Organic & Bio-Products',
        hindi_name='जैविक उत्पाद',
        icon='🌿',
        description='100% residue-free organic bio-stimulants, vermicompost, neem oil, and Trichoderma.'
    )

users = list(User.objects.filter(is_staff=False))
if not users:
    admin_u = User.objects.filter(is_superuser=True).first()
    users = [admin_u]

# 40 Products Data across all categories
products_data = [
    # --- 10 FERTILIZERS & PLANT NUTRITION ---
    {
        'category': cat_fert,
        'name': 'IFFCO Nano Urea Liquid',
        'hindi_name': 'इफको नैनो यूरिया तरल',
        'brand': 'IFFCO',
        'price': 240,
        'discount': 8,
        'stock': 120,
        'unit': '500 ml Bottle',
        'crop_type': 'Wheat, Paddy, Maize, Sugarcane, Cotton',
        'dosage': '4 ml per Litre of water (Foliar spray at tillering and branching)',
        'application_method': 'Foliar Spray',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'Proprietary nanotechnology nitrogen fertilizer replacing one 45 kg bag of conventional urea. Enhances chlorophyll synthesis, increases tillering, and minimizes soil water pollution with zero leaching losses.',
        'img_args': ('nano_urea.jpg', 'IFFCO Nano Urea Liquid', 'IFFCO Agro', 'PATENTED NANO TECH', '#f0fdf4', '#dcfce7', '#16a34a')
    },
    {
        'category': cat_fert,
        'name': 'IFFCO Nano DAP Liquid',
        'hindi_name': 'इफको नैनो डीएपी तरल',
        'brand': 'IFFCO',
        'price': 600,
        'discount': 10,
        'stock': 85,
        'unit': '500 ml Bottle',
        'crop_type': 'All Cereals, Pulses, Oilseeds, Vegetables',
        'dosage': '5 ml per Litre for seed treatment; 4 ml / Litre for foliar spray',
        'application_method': 'Seed Treatment & Spray',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'Advanced bio-available Nano DAP provides critical phosphorus and nitrogen during early seedling establishment. Promotes deep root anchoring and flowering vigor with 90%+ nutrient absorption efficiency.',
        'img_args': ('nano_dap.jpg', 'IFFCO Nano DAP Liquid', 'IFFCO Agro', 'HIGH PHOSPHORUS', '#eff6ff', '#dbeafe', '#2563eb')
    },
    {
        'category': cat_fert,
        'name': 'Mahadhan 12-61-00 (Mono Ammonium Phosphate)',
        'hindi_name': 'महाधन 12-61-00 (एमएपी)',
        'brand': 'Mahadhan Deepak Fertilisers',
        'price': 285,
        'discount': 12,
        'stock': 95,
        'unit': '1 Kg Pack',
        'crop_type': 'Pomegranate, Grapes, Tomato, Potato, Cotton',
        'dosage': '5 gm per Litre water or 3-5 kg per Acre via drip irrigation',
        'application_method': 'Fertigation & Drip',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': True,
        'description': '100% water-soluble specialty fertilizer having highest phosphorus content (61%). Essential during the initial vegetative and flower initiation phase to stimulate vigorous root elongation and uniform bloom.',
        'img_args': ('mahadhan_1261.jpg', 'Mahadhan 12-61-00', 'Mahadhan', '100% WATER SOLUBLE', '#fefce8', '#fef08a', '#ca8a04')
    },
    {
        'category': cat_fert,
        'name': 'Mahadhan 00-52-34 (Mono Potassium Phosphate)',
        'hindi_name': 'महाधन 00-52-34 (एमकेपी)',
        'brand': 'Mahadhan Deepak Fertilisers',
        'price': 295,
        'discount': 14,
        'stock': 110,
        'unit': '1 Kg Pack',
        'crop_type': 'Tomato, Chilli, Cotton, Wheat, Citrus, Banana',
        'dosage': '5-7 gm per Litre water during pre-flowering and fruit set',
        'application_method': 'Foliar Spray & Drip',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'Nitrogen-free formulation with 52% Phosphorus and 34% Potash. Prevents unwanted vegetative drop, increases fruit size, enhances grain weight, and promotes natural crop disease resistance.',
        'img_args': ('mahadhan_0052.jpg', 'Mahadhan 00-52-34', 'Mahadhan', 'BLOOM & GRAIN SWELL', '#fef2f2', '#fee2e2', '#dc2626')
    },
    {
        'category': cat_fert,
        'name': 'Coromandel Gromor 14-35-14 NPK Complex',
        'hindi_name': 'कोरोमंडल ग्रोमोर 14-35-14',
        'brand': 'Coromandel International',
        'price': 1450,
        'discount': 6,
        'stock': 40,
        'unit': '50 Kg Bag',
        'crop_type': 'Sugarcane, Groundnut, Soybean, Wheat, Maize',
        'dosage': '50 kg to 100 kg per Acre as basal application during sowing',
        'application_method': 'Soil Broadcasting',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': False,
        'description': 'High-analysis complex fertilizer rich in ammoniacal nitrogen, water-soluble phosphate, and potassium. Specifically balanced for Indian soils requiring high phosphorus kick-start for oilseeds and cash crops.',
        'img_args': ('coromandel_1435.jpg', 'Coromandel 14-35-14', 'Gromor', 'BASAL FERTILIZER', '#f0fdfa', '#ccfbf1', '#0d9488')
    },
    {
        'category': cat_fert,
        'name': 'Aries Chelamin Zinc EDTA 12%',
        'hindi_name': 'एरीज़ चेलामिन जिंक 12%',
        'brand': 'Aries Agro',
        'price': 380,
        'discount': 15,
        'stock': 75,
        'unit': '500 gm Pack',
        'crop_type': 'Paddy (Khaira Disease), Wheat, Maize, Citrus',
        'dosage': '1 gm to 1.5 gm per Litre water (Foliar spray)',
        'application_method': 'Foliar Spray',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': False,
        'description': 'Pure chelated Zinc EDTA overcomes zinc deficiency and prevents yellowing and stunted internodes in paddy and maize. Chelated form ensures 100% systemic availability without getting locked in alkaline soils.',
        'img_args': ('zinc_edta.jpg', 'Aries Zinc EDTA 12%', 'Aries Agro', 'CHELATED MICRONUTRIENT', '#f8fafc', '#e2e8f0', '#475569')
    },
    {
        'category': cat_fert,
        'name': 'Utkarsh Humic Acid 98% Potassium Humate',
        'hindi_name': 'ह्यूमिक एसिड 98% पोटेशियम ह्यूमेट',
        'brand': 'Utkarsh Agrochem',
        'price': 420,
        'discount': 20,
        'stock': 130,
        'unit': '1 Kg Shiny Flakes',
        'crop_type': 'All Vegetable Crops, Cotton, Groundnut, Spices',
        'dosage': '1-2 gm per Litre water or 1 kg per Acre with flood/drip irrigation',
        'application_method': 'Soil Drench & Spray',
        'is_organic': True,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'Premium 98% water-soluble Potassium Humate flakes extracted from natural Leonardite. Multiplies white root rhizosphere, enhances soil aeration, unbinds locked soil minerals, and boosts organic carbon.',
        'img_args': ('humic_acid.jpg', 'Humic Acid 98% Flakes', 'Utkarsh', 'WHITE ROOT BOOSTER', '#fff7ed', '#ffedd5', '#ea580c')
    },
    {
        'category': cat_fert,
        'name': 'Multiplex Kranti Complete Micronutrient Mixture',
        'hindi_name': 'मल्टीप्लेक्स क्रांति सूक्ष्म पोषक तत्व',
        'brand': 'Multiplex Group',
        'price': 520,
        'discount': 12,
        'stock': 65,
        'unit': '1 Litre Liquid',
        'crop_type': 'Cotton, Chilli, Tomato, Grapes, Soybean, Vegetables',
        'dosage': '2.5 ml per Litre water (Spray at vegetative and pre-flowering)',
        'application_method': 'Foliar Spray',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': True,
        'description': 'Balanced cocktail of Zinc, Iron, Manganese, Copper, Boron, and Molybdenum approved by State Agriculture Departments. Eliminates hidden multi-nutrient hunger and gives rich lush dark-green crop foliage.',
        'img_args': ('multiplex_kranti.jpg', 'Multiplex Kranti', 'Multiplex', 'MULTI-MICRONUTRIENT', '#f0fdf4', '#dcfce7', '#15803d')
    },
    {
        'category': cat_fert,
        'name': 'Boron 20% (Disodium Octaborate Tetrahydrate)',
        'hindi_name': 'घुलनशील बोरॉन 20%',
        'brand': 'Agro Star Lab',
        'price': 340,
        'discount': 18,
        'stock': 90,
        'unit': '500 gm Powder',
        'crop_type': 'Mustard, Sunflower, Pomegranate, Cauliflower, Tomato',
        'dosage': '1 gm to 1.5 gm per Litre water at flower initiation',
        'application_method': 'Foliar Spray',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': False,
        'description': 'Pure 100% soluble Boron prevents blossom drop, hollow heart disease in cauliflower, and fruit cracking in pomegranate and tomato. Essential for pollen tube germination and maximum fruit seed setting.',
        'img_args': ('boron_20.jpg', 'Boron 20% Soluble', 'Agro Star', 'FLOWER SETTING AID', '#fefce8', '#fef08a', '#a16207')
    },
    {
        'category': cat_fert,
        'name': 'Magnesium Sulphate (Epsom Salt Agriculture Grade)',
        'hindi_name': 'मैग्नीशियम सल्फेट (एप्सम साल्ट)',
        'brand': 'IFFCO-MC',
        'price': 650,
        'discount': 10,
        'stock': 50,
        'unit': '25 Kg Bag',
        'crop_type': 'Sugarcane, Banana, Cotton, Turmeric, Ginger',
        'dosage': '25 kg per Acre as soil basal or top-dressing',
        'application_method': 'Soil Application',
        'is_organic': True,
        'is_featured': False,
        'is_best_seller': False,
        'description': 'High-purity crystalline Magnesium (9.6%) and Sulphur (12%). Crucial central molecule of plant chlorophyll. Cures chlorosis between leaf veins and accelerates cane elongation and starch accumulation.',
        'img_args': ('magnesium_sulphate.jpg', 'Magnesium Sulphate 25kg', 'IFFCO-MC', 'CHLOROPHYLL BUILDER', '#f1f5f9', '#e2e8f0', '#334155')
    },

    # --- 10 CROP PROTECTION & PESTICIDES ---
    {
        'category': cat_pest,
        'name': 'Bayer Confidor Imidacloprid 17.8% SL',
        'hindi_name': 'बायर कॉन्फिडोर इमिडाक्लोप्रिड',
        'brand': 'Bayer CropScience',
        'price': 420,
        'discount': 10,
        'stock': 140,
        'unit': '100 ml Bottle',
        'crop_type': 'Cotton, Chilli, Tomato, Paddy, Okra, Mango',
        'dosage': '0.5 ml to 0.75 ml per Litre water (or 50-70 ml per Acre)',
        'application_method': 'Foliar Spray',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'World-standard systemic insecticide for long-lasting control of sucking insect pests including aphids, jassids, thrips, and whiteflies. Rapid translaminar action protects untreated new leaf flushes.',
        'img_args': ('confidor.jpg', 'Bayer Confidor 17.8% SL', 'Bayer', 'SUCKING PEST SHIELD', '#ecfdf5', '#a7f3d0', '#047857')
    },
    {
        'category': cat_pest,
        'name': 'Syngenta Ampligo (Chlorantraniliprole + Lambda Cyhalothrin)',
        'hindi_name': 'सिंजेंटा एम्प्लीगो कीटनाशक',
        'brand': 'Syngenta India',
        'price': 780,
        'discount': 12,
        'stock': 80,
        'unit': '100 ml Pack',
        'crop_type': 'Cotton (Bollworm), Maize (Fall Armyworm), Pulses, Tomato',
        'dosage': '80 ml to 100 ml per Acre in 150-200 Litres of water',
        'application_method': 'Foliar Spray',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'Dual-action contact and systemic insecticide powered by ZEOS technology. Delivers instant knockdown plus persistent residual protection against tough caterpillars, stem borers, and lepidopteran pests.',
        'img_args': ('ampligo.jpg', 'Syngenta Ampligo', 'Syngenta', 'BOLLWORM & CATERPILLAR', '#eff6ff', '#bfdbfe', '#1d4ed8')
    },
    {
        'category': cat_pest,
        'name': 'UPL Saaf Fungicide (Carbendazim 12% + Mancozeb 63% WP)',
        'hindi_name': 'यूपीएल साफ फफूंदनाशक',
        'brand': 'UPL Limited',
        'price': 340,
        'discount': 15,
        'stock': 160,
        'unit': '500 gm Pack',
        'crop_type': 'Groundnut, Chilli, Potato (Late Blight), Grapes, Paddy',
        'dosage': '2 gm per Litre water for foliar spray; 2.5 gm per kg seed',
        'application_method': 'Seed Treatment & Spray',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'India’s most trusted dual systemic and contact broad-spectrum fungicide. Effectively prevents tikka leaf spot, blast, anthracnose, damping off, and early/late blights with manganese and zinc bonus.',
        'img_args': ('upl_saaf.jpg', 'UPL Saaf Fungicide', 'UPL', 'DUAL-ACTION FUNGICIDE', '#fef2f2', '#fecaca', '#b91c1c')
    },
    {
        'category': cat_pest,
        'name': 'Tata Rallis Contaf Plus (Hexaconazole 5% SC)',
        'hindi_name': 'टाटा रैलीस कोंटाफ प्लस',
        'brand': 'Tata Rallis India',
        'price': 490,
        'discount': 10,
        'stock': 70,
        'unit': '500 ml Bottle',
        'crop_type': 'Paddy (Sheath Blight), Apple, Groundnut, Mango (Powdery Mildew)',
        'dosage': '2 ml per Litre water (or 400 ml per Acre)',
        'application_method': 'Foliar Spray',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': True,
        'description': 'Advanced triazole systemic suspension fungicide with protective, curative, and eradicative properties. Imparts distinct crop greening effect while curing powdery mildew, rusts, and sheath blight.',
        'img_args': ('contaf_plus.jpg', 'Tata Contaf Plus 5% SC', 'Tata Rallis', 'SHEATH BLIGHT CURE', '#f0fdf4', '#bbf7d0', '#166534')
    },
    {
        'category': cat_pest,
        'name': 'Bayer Nativo Fungicide (Tebuconazole 50% + Trifloxystrobin 25% WG)',
        'hindi_name': 'बायर नेटिवो फफूंदनाशक',
        'brand': 'Bayer CropScience',
        'price': 1180,
        'discount': 8,
        'stock': 45,
        'unit': '100 gm Pack',
        'crop_type': 'Paddy (Neck Blast & False Smut), Tomato, Mango, Chilli',
        'dosage': '0.8 gm per Litre water (or 120 gm to 160 gm per Acre)',
        'application_method': 'Foliar Spray',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': False,
        'description': 'Premium mesostemic and systemic combination fungicide. Guarantees clean panicles, spotless golden grains, and highest head rice recovery by eliminating dirty panicle disease and false smut in paddy.',
        'img_args': ('nativo.jpg', 'Bayer Nativo WG', 'Bayer', 'PREMIUM BLAST CONTROL', '#fefce8', '#fef08a', '#854d0e')
    },
    {
        'category': cat_pest,
        'name': 'PI Industries Osheen (Dinotefuran 20% SG)',
        'hindi_name': 'पीआई ओशीन (डिनोटेफ्यूरॉन)',
        'brand': 'PI Industries',
        'price': 620,
        'discount': 12,
        'stock': 85,
        'unit': '100 gm Pack',
        'crop_type': 'Paddy (Brown Plant Hopper - BPH), Cotton (Whitefly)',
        'dosage': '80 gm to 100 gm per Acre in 150-200 Litres water',
        'application_method': 'Foliar Spray at Base',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': '3rd Generation neonicotinoid from Mitsui Japan offering fast anti-feedant action against notorious Brown Plant Hopper (BPH/Maho) in paddy. Directly reaches the stem base to stop hopper burn.',
        'img_args': ('osheen.jpg', 'PI Industries Osheen', 'PI Industries', 'BPH HOPPER SPECIALIST', '#f5f3ff', '#ddd6fe', '#6d28d9')
    },
    {
        'category': cat_pest,
        'name': 'Dhanuka EM-1 (Emamectin Benzoate 5% SG)',
        'hindi_name': 'धनुका ईएम-1 कीटनाशक',
        'brand': 'Dhanuka Agritech',
        'price': 480,
        'discount': 15,
        'stock': 125,
        'unit': '100 gm Granules',
        'crop_type': 'Brinjal (Shoot Borer), Tomato (Fruit Borer), Cotton, Gram (Pod Borer)',
        'dosage': '0.5 gm per Litre water (or 80-100 gm per Acre)',
        'application_method': 'Foliar Spray',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': True,
        'description': 'Bio-rational modern water-soluble granular insecticide derived from actinomycetes soil bacteria. Highly active against all larval instars of Helicoverpa, Spodoptera, and fruit and shoot borers.',
        'img_args': ('dhanuka_em1.jpg', 'Dhanuka EM-1 5% SG', 'Dhanuka', 'LARVAL BORER SHIELD', '#fff1f2', '#fecdd3', '#be123c')
    },
    {
        'category': cat_pest,
        'name': 'Bayer Regent SC (Fipronil 5% SC)',
        'hindi_name': 'बायर रीजेंट कीटनाशक',
        'brand': 'Bayer CropScience',
        'price': 690,
        'discount': 10,
        'stock': 90,
        'unit': '250 ml Bottle',
        'crop_type': 'Paddy (Stem Borer, Leaf Folder), Sugarcane, Chilli, Cabbage',
        'dosage': '1.5 ml to 2 ml per Litre water',
        'application_method': 'Foliar Spray',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': True,
        'description': 'Broad-spectrum phenylpyrazole insecticide providing Plant Growth Enhancement (PGE) effect with vigorous greening and tillering while eradicating yellow stem borer, leaf folders, and thrips.',
        'img_args': ('regent_sc.jpg', 'Bayer Regent 5% SC', 'Bayer', 'STEM BORER & GREENING', '#ecfdf5', '#a7f3d0', '#065f46')
    },
    {
        'category': cat_pest,
        'name': 'UPL Ulala (Flonicamid 50% WG)',
        'hindi_name': 'यूपीएल उलाला कीटनाशक',
        'brand': 'UPL Limited',
        'price': 790,
        'discount': 14,
        'stock': 60,
        'unit': '60 gm Pack',
        'crop_type': 'Cotton (Whitefly, Jassids), Paddy (BPH)',
        'dosage': '60 gm to 80 gm per Acre in 150-200 Litres water',
        'application_method': 'Foliar Spray',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': False,
        'description': 'Selective novel sucking pest killer. Stops feeding within 30 minutes of contact. Safe on beneficial pollinator honeybees and ladybird predatory beetles while annihilating resistant whiteflies.',
        'img_args': ('upl_ulala.jpg', 'UPL Ulala 50% WG', 'UPL', 'WHITEFLY SPECIALIST', '#f0fdfa', '#99f6e4', '#0f766e')
    },
    {
        'category': cat_pest,
        'name': 'Dhanuka Conika (Kasugamycin 5% + Copper Oxychloride 45% WP)',
        'hindi_name': 'धनुका कोनिका कवकनाशी',
        'brand': 'Dhanuka Agritech',
        'price': 580,
        'discount': 12,
        'stock': 70,
        'unit': '300 gm Pack',
        'crop_type': 'Paddy (Bacterial Leaf Blight - BLB), Tomato, Chilli, Grapes',
        'dosage': '2 gm per Litre water',
        'application_method': 'Foliar Spray',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': False,
        'description': 'Unique antibacterial and antifungal combination. Eradicates devastating Bacterial Leaf Blight (BLB) in paddy and bacterial canker and black rot in horticultural vegetables and fruit trees.',
        'img_args': ('dhanuka_conika.jpg', 'Dhanuka Conika WP', 'Dhanuka', 'BACTERIAL BLIGHT CURE', '#fefce8', '#fef08a', '#713f12')
    },

    # --- 10 CERTIFIED SEEDS ---
    {
        'category': cat_seeds,
        'name': 'Shriram Super 303 Certified Wheat Seeds',
        'hindi_name': 'श्रीराम सुपर 303 गेहूं बीज',
        'brand': 'Shriram Bioseed',
        'price': 1350,
        'discount': 10,
        'stock': 80,
        'unit': '40 Kg Bag',
        'crop_type': 'Wheat (Rabi Season)',
        'dosage': '40 kg per Acre seed rate',
        'application_method': 'Seed Drill / Broadcasting',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'North India’s highest yielding research wheat variety. Strong thick culm prevents lodging during rain and western disturbances. Long bold earheads with 65-75 grains per ear yielding 28-32 Quintals/Acre.',
        'img_args': ('shriram_303.jpg', 'Shriram Super 303 Wheat', 'Shriram Bioseed', 'HIGH YIELD 30 Q/ACRE', '#fefce8', '#fef08a', '#ca8a04')
    },
    {
        'category': cat_seeds,
        'name': 'Bayer Arize 6444 Gold Hybrid Paddy Seeds',
        'hindi_name': 'बायर एराइज 6444 गोल्ड धान',
        'brand': 'Bayer CropScience',
        'price': 980,
        'discount': 8,
        'stock': 95,
        'unit': '3 Kg Pack',
        'crop_type': 'Paddy (Kharif Season)',
        'dosage': '6 kg per Acre for nursery transplanting',
        'application_method': 'Nursery Bed & Transplanting',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'India’s most celebrated hybrid paddy with BLB (Bacterial Leaf Blight) genetic tolerance. Maturity 135-140 days. Exceptional heavy tillering with 25-30 fertile tillers per hill yielding over 32 Quintals/Acre.',
        'img_args': ('arize_6444.jpg', 'Arize 6444 Gold Paddy', 'Bayer', 'BLB GENETIC SHIELD', '#ecfdf5', '#a7f3d0', '#059669')
    },
    {
        'category': cat_seeds,
        'name': 'Mahyco Bollgard-II Bt Cotton Hybrid Seeds',
        'hindi_name': 'माहिको बीटी कपास बीज बीजी-II',
        'brand': 'Mahyco Seeds',
        'price': 864,
        'discount': 5,
        'stock': 120,
        'unit': '450 gm Pack (+ Refugia)',
        'crop_type': 'Cotton (Kharif Cash Crop)',
        'dosage': '2 packets per Acre with 4x1.5 ft spacing',
        'application_method': 'Dibbling Method',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'Government approved Bollgard-II hybrid cotton. Delivers heavy boll retention (80-100 bolls/plant), large boll weight (5.5 gm), long staple fiber length, and in-built resistance against American bollworm.',
        'img_args': ('mahyco_cotton.jpg', 'Mahyco Bt Cotton BG-II', 'Mahyco', 'HEAVY BOLL RETENTION', '#f0fdf4', '#dcfce7', '#15803d')
    },
    {
        'category': cat_seeds,
        'name': 'Pioneer 3396 Hybrid Maize Corn Seeds',
        'hindi_name': 'पायनियर 3396 हाइब्रिड मक्का',
        'brand': 'Corteva Pioneer',
        'price': 1050,
        'discount': 10,
        'stock': 70,
        'unit': '4 Kg Pack',
        'crop_type': 'Maize / Corn (Kharif & Rabi)',
        'dosage': '7-8 kg per Acre seed rate',
        'application_method': 'Line Sowing with Planter',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': True,
        'description': 'Orange-flint bold grains with excellent cob tip-filling right to the apex. Heat and drought tolerance with stay-green fodder quality even at harvest time. Consistent record yielder for grain & silage.',
        'img_args': ('pioneer_3396.jpg', 'Pioneer 3396 Corn', 'Corteva Pioneer', 'TIP TO TIP COB FILLING', '#fffbeb', '#fde68a', '#d97706')
    },
    {
        'category': cat_seeds,
        'name': 'Advanta 414 Hybrid Mustard Seeds',
        'hindi_name': 'एडवांटा 414 हाइब्रिड सरसों',
        'brand': 'Advanta Seeds UPL',
        'price': 720,
        'discount': 12,
        'stock': 110,
        'unit': '1 Kg Pack',
        'crop_type': 'Mustard / Rapeseed (Rabi)',
        'dosage': '1.5 kg per Acre',
        'application_method': 'Line Sowing with Sower',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'High oil content (41-42%) research hybrid mustard. Multi-branching from ground level, dense long pods with 16-18 seeds per pod. Maturity 125-130 days with resistance to Alternaria blight and white rust.',
        'img_args': ('advanta_mustard.jpg', 'Advanta 414 Mustard', 'Advanta UPL', '42% HIGH OIL CONTENT', '#fefce8', '#fef08a', '#eab308')
    },
    {
        'category': cat_seeds,
        'name': 'Syngenta Abhinav F1 Hybrid Tomato Seeds',
        'hindi_name': 'सिंजेंटा अभिनव हाइब्रिड टमाटर',
        'brand': 'Syngenta Seeds',
        'price': 650,
        'discount': 15,
        'stock': 90,
        'unit': '10 gm Pack (approx 3500 seeds)',
        'crop_type': 'Tomato (All Seasons)',
        'dosage': '50-60 gm per Acre for seedling nursery',
        'application_method': 'Nursery Raising & Staking',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'India’s most celebrated market leader tomato hybrid. Deep square-round glossy red firm fruits (80-90 gm). Thick skin enables long distance transport without bursting. Resistant to TYLCV virus.',
        'img_args': ('syngenta_abhinav.jpg', 'Syngenta Abhinav Tomato', 'Syngenta Seeds', 'TYLCV VIRUS RESISTANT', '#fff1f2', '#fecdd3', '#e11d48')
    },
    {
        'category': cat_seeds,
        'name': 'Nunhems US-705 Hot Pepper Chilli Seeds',
        'hindi_name': 'नुनहेम्स US-705 तीखी हरी मिर्च',
        'brand': 'Nunhems BASF',
        'price': 890,
        'discount': 10,
        'stock': 65,
        'unit': '10 gm Pack',
        'crop_type': 'Chilli / Hot Pepper',
        'dosage': '60-80 gm per Acre',
        'application_method': 'Transplanting on Raised Beds',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': True,
        'description': 'Dark green pungent 10-12 cm long chillies turning deep glossy red upon ripening. High tolerance to thrips and leaf curl virus (LCV). Delivers over 10 to 12 pickings over a prolonged 7-month crop cycle.',
        'img_args': ('nunhems_chilli.jpg', 'Nunhems US-705 Chilli', 'BASF Nunhems', 'HIGH PUNGENCY & YIELD', '#f0fdf4', '#bbf7d0', '#15803d')
    },
    {
        'category': cat_seeds,
        'name': 'Namdhari NS-53 Hybrid Onion Seeds',
        'hindi_name': 'नामधारी NS-53 प्याज बीज',
        'brand': 'Namdhari Seeds',
        'price': 1480,
        'discount': 12,
        'stock': 55,
        'unit': '500 gm Pack',
        'crop_type': 'Onion (Kharif & Late Kharif)',
        'dosage': '3-4 kg per Acre nursery',
        'application_method': 'Nursery Bed & Transplanting',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': False,
        'description': 'Flat globe attractive dark red bulbs with tight neck preventing rotting. High pungency, excellent shelf-life storage capacity of 4-5 months, and uniform maturity in 90-100 days after transplanting.',
        'img_args': ('namdhari_onion.jpg', 'Namdhari NS-53 Onion', 'Namdhari', 'EXCELLENT 5-MO STORAGE', '#fff7ed', '#ffedd5', '#c2410c')
    },
    {
        'category': cat_seeds,
        'name': 'Mahyco No. 10 Hybrid Okra Bhindi Seeds',
        'hindi_name': 'माहिको 10 हाइब्रिड भिंडी बीज',
        'brand': 'Mahyco Seeds',
        'price': 440,
        'discount': 15,
        'stock': 100,
        'unit': '250 gm Pack',
        'crop_type': 'Okra / Bhindi (Summer & Rainy)',
        'dosage': '3-4 kg per Acre',
        'application_method': 'Direct Line Sowing',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': True,
        'description': 'Dark green 5-ridged smooth tender fruits without spines. Short internodal distance ensures heavy bearing. Strong field resistance to Yellow Vein Mosaic Virus (YVMV) and enation leaf curl virus.',
        'img_args': ('mahyco_okra.jpg', 'Mahyco No.10 Okra', 'Mahyco Seeds', 'YVMV VIRUS TOLERANT', '#ecfdf5', '#a7f3d0', '#047857')
    },
    {
        'category': cat_seeds,
        'name': 'Kaveri Chintu 222+ Hybrid Pearl Millet Bajra',
        'hindi_name': 'कावेरी चिंटू 222+ हाइब्रिड बाजरा',
        'brand': 'Kaveri Seed Company',
        'price': 580,
        'discount': 8,
        'stock': 75,
        'unit': '1.5 Kg Pack',
        'crop_type': 'Bajra / Pearl Millet (Kharif & Summer)',
        'dosage': '1.5 kg per Acre',
        'application_method': 'Line Sowing with Sower',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': False,
        'description': 'Heavy tillering compact earhead bajra hybrid with bristled spikes protecting grains from bird damage. Tolerant to downy mildew. Bold pearl gray grains with sweet nutritious cattle green fodder.',
        'img_args': ('kaveri_bajra.jpg', 'Kaveri Chintu Bajra', 'Kaveri Seeds', 'BIRD-PROOF BRISTLES', '#fefce8', '#fef08a', '#854d0e')
    },

    # --- 6 FARMING TOOLS & SPRAYERS ---
    {
        'category': cat_tools,
        'name': 'KisanKraft 16-Litre 12V/12Ah Dual-Motor Battery Sprayer',
        'hindi_name': 'किसानक्राफ्ट 16 लीटर बैटरी स्प्रेयर',
        'brand': 'KisanKraft',
        'price': 3450,
        'discount': 22,
        'stock': 35,
        'unit': '1 Complete Unit with Charger & Lances',
        'crop_type': 'All Agricultural & Horticultural Crops',
        'dosage': 'Generates 100 PSI pressure; covers 25-30 tanks on single charge',
        'application_method': 'Continuous High-Pressure Mist Spray',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'Heavy-duty 16-litre tank made of virgin UV-resistant polypropylene. Dual motor system allows switching between single motor for fine mist and dual motor for high tree canopy blast spraying. Telescopic SS lance with 4 nozzle attachments.',
        'img_args': ('kisankraft_sprayer.jpg', 'KisanKraft 16L Sprayer', 'KisanKraft', '12V DUAL MOTOR 100 PSI', '#eff6ff', '#bfdbfe', '#1d4ed8')
    },
    {
        'category': cat_tools,
        'name': 'Neptune 2-Stroke Portable Power Sprayer Pump',
        'hindi_name': 'नेपच्यून 2-स्ट्रोक पोर्टेबल पावर स्प्रेयर',
        'brand': 'Neptune Farming Tools',
        'price': 5890,
        'discount': 25,
        'stock': 20,
        'unit': '1 Set with 50-Meter High-Pressure Hose',
        'crop_type': 'Paddy, Sugarcane, Cotton, Mango Orchards, Tea Gardens',
        'dosage': 'Discharges 8 Litres/minute with 50 meter long delivery hose',
        'application_method': 'Orchard & Field High-Reach Spray',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': False,
        'description': 'Portable 26cc 2-stroke petrol powered brass pump. Draw water from farm pond, barrel, or canal to spray tall trees and distant field patches without carrying heavy water on farmer’s back.',
        'img_args': ('neptune_sprayer.jpg', 'Neptune Power Sprayer', 'Neptune Tools', '50M HIGH REACH HOSE', '#fef2f2', '#fecaca', '#dc2626')
    },
    {
        'category': cat_tools,
        'name': 'Automatic Drip Irrigation Kit 100 Plants',
        'hindi_name': 'ऑटोमैटिक ड्रिप सिंचाई किट 100 पौधे',
        'brand': 'Jain Agri Drip',
        'price': 1650,
        'discount': 30,
        'stock': 45,
        'unit': 'Complete Kit (Main Line + Drippers + Connectors)',
        'crop_type': 'Vegetable Polyhouse, Kitchen Gardens, Orchards, Nursery',
        'dosage': 'Adjustable drippers (0 - 70 Litres/hour)',
        'application_method': 'Root-Zone Micro Irrigation',
        'is_organic': True,
        'is_featured': False,
        'is_best_seller': True,
        'description': 'Saves up to 70% irrigation water and electricity. Complete DIY kit with 50m 16mm main pipe, 100 adjustable pressure-compensating drippers, T-joints, end-caps, tap adapter, and punch tool.',
        'img_args': ('drip_kit.jpg', 'Jain Drip Kit 100 Plants', 'Jain Agri Drip', 'SAVES 70% FARM WATER', '#ecfdf5', '#a7f3d0', '#047857')
    },
    {
        'category': cat_tools,
        'name': 'Falcon Heavy Duty Professional Bypass Pruning Secateur',
        'hindi_name': 'फाल्कन हैवी ड्यूटी प्रूनिंग कटर',
        'brand': 'Falcon Garden Tools',
        'price': 680,
        'discount': 18,
        'stock': 85,
        'unit': '1 Unit (SK-5 Japanese Carbon Steel)',
        'crop_type': 'Pomegranate, Grapes, Citrus, Apple, Rose, General Orchards',
        'dosage': 'Cuts branches up to 20 mm clean without bark bruising',
        'application_method': 'Manual Pruning & Training',
        'is_organic': False,
        'is_featured': False,
        'is_best_seller': True,
        'description': 'High-grade Japanese SK-5 tempered carbon steel blade with non-stick Teflon coating. Ergonomic non-slip rubber handles with safety locking latch. Clean cutting prevents fungal rot at pruned stem edges.',
        'img_args': ('falcon_secateur.jpg', 'Falcon Pruning Secateur', 'Falcon Tools', 'JAPANESE SK-5 STEEL', '#fff7ed', '#ffedd5', '#ea580c')
    },
    {
        'category': cat_tools,
        'name': '4-in-1 Digital Soil pH, Moisture, Sunlight & Fertility Meter',
        'hindi_name': 'डिजिटल मृदा परीक्षण यंत्र (pH व नमी मीटर)',
        'brand': 'Kisan Tech Labs',
        'price': 1250,
        'discount': 35,
        'stock': 60,
        'unit': '1 Digital Sensor Probe with LCD Screen',
        'crop_type': 'All Soils & Greenhouse Substrates',
        'dosage': 'Instant reading on probe insertion into moist soil',
        'application_method': 'Soil Testing Diagnostic',
        'is_organic': False,
        'is_featured': True,
        'is_best_seller': False,
        'description': 'Empowers farmers to self-test soil acidity (pH 3.5 to 9.0), root moisture %, sunlight lux, and ambient temperature without waiting for laboratory delays. Backlit LCD screen for night field checks.',
        'img_args': ('soil_meter.jpg', '4-in-1 Soil pH Meter', 'Kisan Tech', 'INSTANT SOIL DIAGNOSTIC', '#f0fdf4', '#dcfce7', '#16a34a')
    },
    {
        'category': cat_tools,
        'name': 'Solar LED Automatic Insect Pest Trap (फसल कीट ट्रैप)',
        'hindi_name': 'सोलर एलईडी स्वचालित कीट ट्रैप',
        'brand': 'SunAgri Tech',
        'price': 1890,
        'discount': 20,
        'stock': 40,
        'unit': '1 Solar Unit with Catch Bucket',
        'crop_type': 'Paddy, Cotton, Sugarcane, Vegetables, Orchards',
        'dosage': '1 unit covers 1 to 1.5 Acres of farm land',
        'application_method': 'Eco-Friendly Pest Mass Trapping',
        'is_organic': True,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'Rechargeable solar-powered UV light automatically turns ON at dusk and OFF at dawn. Attracts and traps nocturnal moth pests, borers, and hoppers without using hazardous chemical sprays. 100% organic.',
        'img_args': ('solar_trap.jpg', 'Solar Insect Pest Trap', 'SunAgri Tech', 'SOLAR ECO PEST CONTROL', '#fefce8', '#fef08a', '#ca8a04')
    },

    # --- 4 ORGANIC & BIO-PRODUCTS ---
    {
        'category': cat_organic,
        'name': 'Multiplex Bio-Jodi (Trichoderma Viride + Pseudomonas Fluorescens)',
        'hindi_name': 'मल्टीप्लेक्स बायो-जोड़ी (ट्राइकोडर्मा)',
        'brand': 'Multiplex Bio-Tech',
        'price': 390,
        'discount': 15,
        'stock': 120,
        'unit': '1 Kg + 1 Kg Twin Pack',
        'crop_type': 'Chickpea (Wilt), Ginger (Rhizome Rot), Tomato, Cotton, Chilli',
        'dosage': 'Seed treatment: 10 gm/kg; Soil: 2 kg mixed with 100 kg FYM/Acre',
        'application_method': 'Seed Treatment & Soil Drench',
        'is_organic': True,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'Synergistic combination of beneficial bio-fungicide (Trichoderma) and plant-growth promoting rhizobacteria (Pseudomonas). Naturally destroys soil-borne pathogenic Fusarium, Pythium, and Rhizoctonia root rots.',
        'img_args': ('bio_jodi.jpg', 'Multiplex Bio-Jodi 2kg', 'Multiplex Bio', 'BIO-FUNGICIDE TRICHODERMA', '#f0fdf4', '#dcfce7', '#166534')
    },
    {
        'category': cat_organic,
        'name': 'Utkarsh VAM (Vesicular Arbuscular Mycorrhiza Bio-Fertilizer)',
        'hindi_name': 'उत्कर्ष वैम (माइकोराइजा बायो-उर्वरक)',
        'brand': 'Utkarsh Agrochem',
        'price': 480,
        'discount': 18,
        'stock': 90,
        'unit': '1 Kg Granular Formulation (100 IP/gm)',
        'crop_type': 'All Field Crops, Spices, Fruit Trees, Vegetables',
        'dosage': '4 kg per Acre mixed with organic manure at planting',
        'application_method': 'Root Zone Soil Application',
        'is_organic': True,
        'is_featured': True,
        'is_best_seller': True,
        'description': 'Symbiotic mycorrhizal fungus that expands plant root absorptive surface area by 1000%. Mobilizes locked soil phosphorus, improves drought survival, and reduces chemical fertilizer requirement by 25%.',
        'img_args': ('vam_mycorrhiza.jpg', 'Utkarsh VAM Mycorrhiza', 'Utkarsh', 'EXPANDS ROOTS 10X', '#ecfdf5', '#a7f3d0', '#059669')
    },
    {
        'category': cat_organic,
        'name': 'Dr. Soil Health Biological Micro-Nutrient & Humus Booster',
        'hindi_name': 'डॉ. सॉइल हेल्थ जैविक पोषण',
        'brand': 'Microbax Organics',
        'price': 1250,
        'discount': 20,
        'stock': 50,
        'unit': '5 Litre Can',
        'crop_type': 'Paddy, Banana, Sugarcane, Arecanut, Vegetables',
        'dosage': '5 Litres per Acre with drip or flood irrigation',
        'application_method': 'Drip Fertigation & Flood',
        'is_organic': True,
        'is_featured': False,
        'is_best_seller': True,
        'description': 'Fermented plant extract enriched with natural sea-kelp, amino acids, fulvic minerals, and beneficial microflora. Restores hard degraded soil fertility, earthworm count, and water holding capacity.',
        'img_args': ('dr_soil.jpg', 'Dr. Soil Health 5 Litre', 'Microbax', 'ORGANIC SOIL RESTORER', '#fefce8', '#fef08a', '#854d0e')
    },
    {
        'category': cat_organic,
        'name': 'Pure Cold-Pressed Karanja (Pongamia) Oil 10,000 PPM',
        'hindi_name': 'शुद्ध करंज तेल कीटनाशक (10,000 PPM)',
        'brand': 'Organic India Agro',
        'price': 520,
        'discount': 15,
        'stock': 70,
        'unit': '1 Litre Emulsifiable Concentrate',
        'crop_type': 'Vegetables, Pulses, Mustard, Floriculture, Tea',
        'dosage': '3-4 ml per Litre water (Foliar spray)',
        'application_method': 'Foliar Spray',
        'is_organic': True,
        'is_featured': False,
        'is_best_seller': False,
        'description': 'Rich in natural Pongamol and Karanjin alkaloids. Functions as an organic repellent, ovicide, and anti-feedant against mites, scales, thrips, and nematodes without leaving any toxic chemical residue.',
        'img_args': ('karanja_oil.jpg', 'Pure Karanja Oil 1L', 'Organic India', 'ZERO CHEMICAL RESIDUE', '#fff7ed', '#ffedd5', '#ea580c')
    }
]

# Verified Farmer Review Templates
review_samples = [
    ("Excellent results in my fields! Within 5-7 days after application, the crop showed deep green color and vigorous tillering.", 5),
    ("Very fast doorstep delivery by FarmKart in our village. Packaging was tamper-proof and genuine product.", 5),
    ("Used this during critical flowering stage. Significantly prevented flower drop and increased overall harvest weight.", 5),
    ("Authentic quality product. Checked the batch number and QR code, 100% genuine.", 4),
    ("Great value for money. Saved at least 20% compared to local Mandi dealer prices.", 5)
]

added_count = 0
for idx, data in enumerate(products_data):
    # Check if product already exists to avoid duplication
    existing = Product.objects.filter(name=data['name']).first()
    if existing:
        print(f"Skipping existing: {data['name']}")
        continue

    # Generate Image
    img_name, title, sub, badge, c1, c2, c3 = data['img_args']
    img_rel_path = generate_image(img_name, title, sub, badge, c1, c2, c3)

    product = Product.objects.create(
        category=data['category'],
        name=data['name'],
        hindi_name=data['hindi_name'],
        brand=data['brand'],
        price=Decimal(str(data['price'])),
        discount=Decimal(str(data['discount'])),
        stock=data['stock'],
        unit=data['unit'],
        crop_type=data['crop_type'],
        dosage=data['dosage'],
        application_method=data['application_method'],
        description=data['description'],
        is_organic=data['is_organic'],
        is_featured=data['is_featured'],
        is_best_seller=data['is_best_seller'],
        image=img_rel_path,
        rating=Decimal('4.8'),
        review_count=15 + (idx % 18)
    )

    # Attach a couple of verified farmer reviews
    rev_text, rev_stars = review_samples[idx % len(review_samples)]
    user_reviewer = users[idx % len(users)]
    Review.objects.create(
        product=product,
        user=user_reviewer,
        rating=rev_stars,
        comment=rev_text,
        crop_used_on=data['crop_type'].split(',')[0],
        is_verified_farmer=True
    )

    added_count += 1
    print(f"[{added_count}/40] Added: {product.name} (Category: {product.category.name})")

print(f"\nSuccessfully added {added_count} brand-new agricultural products to the database!")
print(f"Total Products in FarmKart database now: {Product.objects.count()}")
