"""
crop_data.py
Rich botanical, agronomic, and benchmark data for the 22 supported crops.
Includes presets, detailed agronomic guidelines, and test cases.
"""

CROP_DETAILS = {
    "apple": {
        "botanical_name": "Malus domestica",
        "category": "Fruit / Temperate",
        "growth_period_days": "150-180 days (Harvest in Autumn)",
        "water_requirement": "Moderate (600-1000 mm annually)",
        "soil_preference": "Well-drained, deep loam rich in organic matter",
        "market_profile": "High economic value, export potential, cold-storage friendly",
        "advisory": {
            "soil_prep": "Maintain slightly acidic soil (pH 5.5-6.5). Avoid waterlogging.",
            "fertilizer": "Requires balanced potassium and phosphorus for fruit firming.",
            "water": "Regular drip irrigation during fruit development; reduce near harvest.",
            "tips": "Requires chilling hours in winter for optimal bud break and flowering."
        },
        "icon": "🍎"
    },
    "banana": {
        "botanical_name": "Musa acuminata",
        "category": "Fruit / Tropical",
        "growth_period_days": "300-365 days (10-12 months)",
        "water_requirement": "High (1200-2000 mm annually)",
        "soil_preference": "Rich, deep clay loam with excellent drainage",
        "market_profile": "High daily market demand, continuous harvesting cycles",
        "advisory": {
            "soil_prep": "Needs high organic compost and neutral to slightly acidic pH (6.0-7.5).",
            "fertilizer": "Heavy feeder of Potassium (K) and Nitrogen (N). Split into 4-5 applications.",
            "water": "Provide frequent irrigation; never allow soil to dry out completely.",
            "tips": "Protect pseudostems with windbreaks to prevent lodging in storms."
        },
        "icon": "🍌"
    },
    "blackgram": {
        "botanical_name": "Vigna mungo (Urad)",
        "category": "Pulse / Legume",
        "growth_period_days": "70-90 days",
        "water_requirement": "Low to Moderate (400-600 mm)",
        "soil_preference": "Loamy to heavy clay with good drainage",
        "market_profile": "Essential staple pulse, high protein demand in South Asia",
        "advisory": {
            "soil_prep": "Can tolerate slightly alkaline soils (pH 6.5-7.5). Fixes atmospheric nitrogen.",
            "fertilizer": "Low nitrogen requirement. Requires starter phosphorus for root nodulation.",
            "water": "Drought-hardy. Avoid waterlogging at flowering and pod filling.",
            "tips": "Excellent crop for intercropping and green manuring."
        },
        "icon": "🌱"
    },
    "chickpea": {
        "botanical_name": "Cicer arietinum (Gram)",
        "category": "Pulse / Legume",
        "growth_period_days": "90-120 days (Rabi Season)",
        "water_requirement": "Low (200-400 mm)",
        "soil_preference": "Deep, well-drained sandy loam or black cotton soil",
        "market_profile": "Major staple pulse, steady domestic demand and export market",
        "advisory": {
            "soil_prep": "Prefers neutral to slightly alkaline soil (pH 6.0-8.0).",
            "fertilizer": "Inoculate seeds with Rhizobium culture. Apply single superphosphate (SSP).",
            "water": "Requires only 1-2 protective irrigations (branching & pod formation).",
            "tips": "Extremely susceptible to excess moisture; avoid fields with poor drainage."
        },
        "icon": "🌰"
    },
    "coconut": {
        "botanical_name": "Cocos nucifera",
        "category": "Plantation / Perennial",
        "growth_period_days": "Perennial (First bearing 5-7 years, productive for 60+ yrs)",
        "water_requirement": "High (1500-2500 mm annually)",
        "soil_preference": "Coastal alluvium, sandy loam, or red sandy loam",
        "market_profile": "Multi-utility cash crop (oil, copra, coir, water, tender nut)",
        "advisory": {
            "soil_prep": "Tolerates salinity and sandy textures with adequate ground moisture.",
            "fertilizer": "Demands high potassium, magnesium, and chlorine for palm vigor.",
            "water": "Basin irrigation or drip system; critical during dry summer spells.",
            "tips": "Maintain circular mulch around palm base to conserve root moisture."
        },
        "icon": "🥥"
    },
    "coffee": {
        "botanical_name": "Coffea arabica / canephora",
        "category": "Plantation / Cash Crop",
        "growth_period_days": "Perennial (Harvest Nov-Feb)",
        "water_requirement": "High (1500-2000 mm with dry spell before blossom)",
        "soil_preference": "Rich volcanic or humus-rich hill loams, slightly acidic",
        "market_profile": "Premium global commodity, lucrative export revenues",
        "advisory": {
            "soil_prep": "Soil must have pH 5.5-6.5 and rich organic mulch.",
            "fertilizer": "Apply balanced NPK with magnesium and zinc micro-nutrients.",
            "water": "Blossom showers (25-40 mm) in March are vital for flower setting.",
            "tips": "Requires two-tier shade trees (silver oak, dadap) to buffer thermal stress."
        },
        "icon": "☕"
    },
    "cotton": {
        "botanical_name": "Gossypium hirsutum",
        "category": "Cash Crop / Fiber",
        "growth_period_days": "150-180 days",
        "water_requirement": "Moderate (600-800 mm)",
        "soil_preference": "Deep black vertisols or heavy alluvial soils",
        "market_profile": "Primary raw material for textile industries worldwide",
        "advisory": {
            "soil_prep": "Black soils with high moisture retention capacity are ideal.",
            "fertilizer": "Split nitrogen doses; adequate potassium prevents premature boll opening.",
            "water": "Irrigate at squaring, flowering, and boll development stages.",
            "tips": "Monitor for pink bollworm and sucking pests with pheromone traps."
        },
        "icon": "☁️"
    },
    "grapes": {
        "botanical_name": "Vitis vinifera",
        "category": "Fruit / Horticulture",
        "growth_period_days": "Perennial (110-130 days from pruning to harvest)",
        "water_requirement": "Moderate (500-700 mm)",
        "soil_preference": "Well-drained sandy loam or gravelly loam with neutral pH",
        "market_profile": "High revenue per acre, table grapes, raisins, and wine production",
        "advisory": {
            "soil_prep": "Ensure excellent subsurface drainage to prevent root rot.",
            "fertilizer": "High requirement of potassium for sugar accumulation and berry size.",
            "water": "Controlled drip irrigation; cease water 10-15 days prior to harvest.",
            "tips": "Maintain proper trellis canopy and practice seasonal shoot thinning."
        },
        "icon": "🍇"
    },
    "jute": {
        "botanical_name": "Corchorus capsularis",
        "category": "Fiber / Cash Crop",
        "growth_period_days": "120-150 days",
        "water_requirement": "High (1200-1500 mm, humid monsoon conditions)",
        "soil_preference": "New alluvial soils, silt loams near river basins",
        "market_profile": "Eco-friendly golden fiber, packaging, hessian, and geotextiles",
        "advisory": {
            "soil_prep": "Fine tilth soil with pH 6.0-7.5. Flooding tolerant in later stages.",
            "fertilizer": "Needs modest nitrogen and phosphorus for rapid vegetative stem growth.",
            "water": "Thrives in high atmospheric humidity (>75%) and standing rain showers.",
            "tips": "Harvest at 50% flowering stage for maximum fiber tensile strength."
        },
        "icon": "🌾"
    },
    "kidneybeans": {
        "botanical_name": "Phaseolus vulgaris (Rajma)",
        "category": "Pulse / Legume",
        "growth_period_days": "90-110 days",
        "water_requirement": "Moderate (450-600 mm)",
        "soil_preference": "Deep, fertile loam with pH 5.5-6.5",
        "market_profile": "Popular culinary pulse with steady high wholesale rates",
        "advisory": {
            "soil_prep": "Needs light, non-crusting soil with good aeration.",
            "fertilizer": "Unlike some legumes, Rajma lacks native nodulation; requires basal nitrogen.",
            "water": "Sensitive to water stagnation. 3-4 light irrigations recommended.",
            "tips": "Avoid high temperatures (>30°C) during flowering to prevent flower drop."
        },
        "icon": "🫘"
    },
    "lentil": {
        "botanical_name": "Lens culinaris (Masoor)",
        "category": "Pulse / Legume",
        "growth_period_days": "100-120 days",
        "water_requirement": "Low (250-350 mm)",
        "soil_preference": "Light loams to clay loams with neutral pH",
        "market_profile": "Nutrient-rich staple, high demand in domestic cooking",
        "advisory": {
            "soil_prep": "Tolerates moderate soil salinity and alkalinity.",
            "fertilizer": "Basal application of DAP (Di-ammonium Phosphate) and sulfur.",
            "water": "Very low water user. One irrigation at pod formation is sufficient.",
            "tips": "Sow in moisture-retaining residual soil following rice harvest."
        },
        "icon": "🍲"
    },
    "maize": {
        "botanical_name": "Zea mays (Corn)",
        "category": "Cereal / Coarse Grain",
        "growth_period_days": "90-115 days",
        "water_requirement": "Moderate (500-750 mm)",
        "soil_preference": "Fertile, deep loamy soils rich in organic matter",
        "market_profile": "Industrial fodder, poultry feed, starch, ethanol, and food",
        "advisory": {
            "soil_prep": "Well-aerated soil with pH 5.8-7.2. Sensitive to water stagnation.",
            "fertilizer": "Heavy feeder of Nitrogen (N). Apply in 3 splits (knee-high, tasseling, grain).",
            "water": "Critical moisture stages: silking and grain filling.",
            "tips": "Maintain plant population of ~65,000 plants per hectare for peak yield."
        },
        "icon": "🌽"
    },
    "mango": {
        "botanical_name": "Mangifera indica",
        "category": "Fruit / Perennial",
        "growth_period_days": "Perennial (Bearing begins 3-4 years, harvest March-July)",
        "water_requirement": "Moderate (750-1000 mm with dry winter period)",
        "soil_preference": "Deep alluvial, red loam, or laterite with 2m+ soil depth",
        "market_profile": "King of fruits, major domestic and international export market",
        "advisory": {
            "soil_prep": "Slightly acidic to neutral pH (5.5-7.5). Avoid hard pans in subsoil.",
            "fertilizer": "Apply farmyard manure and balanced NPK after harvest in monsoon.",
            "water": "Withhold water 2 months prior to flowering to stimulate flower buds.",
            "tips": "Protect panicles from powdery mildew and hopper pests during bloom."
        },
        "icon": "🥭"
    },
    "mothbeans": {
        "botanical_name": "Vigna aconitifolia (Matki)",
        "category": "Pulse / Legume",
        "growth_period_days": "60-75 days (Ultra-short duration)",
        "water_requirement": "Very Low (200-350 mm)",
        "soil_preference": "Sandy to light sandy loam soils",
        "market_profile": "Key ingredient in savory snacks (namkeen, bhujia) and sprouts",
        "advisory": {
            "soil_prep": "Ideal for arid and desert zones. Tolerates heat up to 45°C.",
            "fertilizer": "Minimal nutrient input required. Responds to basal phosphate.",
            "water": "Extreme drought tolerance. Rainfed cultivation usually succeeds.",
            "tips": "Forms a dense green carpet that prevents wind erosion in drylands."
        },
        "icon": "🌱"
    },
    "mungbean": {
        "botanical_name": "Vigna radiata (Moong)",
        "category": "Pulse / Legume",
        "growth_period_days": "60-70 days",
        "water_requirement": "Low (300-450 mm)",
        "soil_preference": "Well-drained loam or sandy loam with neutral pH",
        "market_profile": "High retail prices, ubiquitous consumption, fast rotation crop",
        "advisory": {
            "soil_prep": "Prefers well-pulverized seedbed with pH 6.2-7.2.",
            "fertilizer": "Seed treatment with Rhizobium and PSB culture enhances root nodules.",
            "water": "Avoid waterlogging; irrigate once at flowering if dry.",
            "tips": "Ideal catch crop between wheat harvest and rice transplantation."
        },
        "icon": "🟢"
    },
    "muskmelon": {
        "botanical_name": "Cucumis melo",
        "category": "Fruit / Cucurbit",
        "growth_period_days": "75-90 days",
        "water_requirement": "Low to Moderate (400-500 mm)",
        "soil_preference": "Sandy river beds or light sandy loam with good drainage",
        "market_profile": "High seasonal demand during warm summer months",
        "advisory": {
            "soil_prep": "Warm soil temperature (>22°C) is mandatory for seed germination.",
            "fertilizer": "Balanced NPK; excess nitrogen can lead to vine growth over fruiting.",
            "water": "Drip irrigation; stop water a week before harvest to sweeten fruits.",
            "tips": "Turn developing melons gently to ensure uniform color and netting."
        },
        "icon": "🍈"
    },
    "orange": {
        "botanical_name": "Citrus sinensis / reticulata",
        "category": "Fruit / Citrus",
        "growth_period_days": "Perennial (240-270 days from flowering to maturity)",
        "water_requirement": "Moderate (800-1100 mm)",
        "soil_preference": "Well-drained light loams, avoids heavy clay",
        "market_profile": "High beverage and fresh fruit demand, high Vitamin C market",
        "advisory": {
            "soil_prep": "Needs neutral to slightly acidic pH (6.0-7.0) with no salinity.",
            "fertilizer": "Requires zinc, iron, and boron micronutrients along with NPK.",
            "water": "Micro-sprinkler or drip. Sensitive to waterlogging around trunk collar.",
            "tips": "Perform light post-harvest pruning to eliminate dead twigs and scale insects."
        },
        "icon": "🍊"
    },
    "papaya": {
        "botanical_name": "Carica papaya",
        "category": "Fruit / Horticulture",
        "growth_period_days": "270-300 days (Fruit ready in 9-10 months)",
        "water_requirement": "Moderate to High (1000-1400 mm)",
        "soil_preference": "Rich, porous alluvial or volcanic soil with rapid drainage",
        "market_profile": "Fast return on investment, year-round harvest potential",
        "advisory": {
            "soil_prep": "Extremely sensitive to standing water. Plant on raised mounds.",
            "fertilizer": "Monthly small doses of nitrogen and potassium keep trees bearing.",
            "water": "Keep root zone moist but never soaked; stem rot occurs readily in swamps.",
            "tips": "Select gynodioecious varieties (like Red Lady) for 100% productive trees."
        },
        "icon": "🥭"
    },
    "pigeonpeas": {
        "botanical_name": "Cajanus cajan (Arhar / Toor)",
        "category": "Pulse / Legume",
        "growth_period_days": "150-180 days (Medium-long duration)",
        "water_requirement": "Low to Moderate (500-650 mm)",
        "soil_preference": "Deep, well-drained loamy to black soils",
        "market_profile": "Prime protein pulse in Indian diets, commanding premium prices",
        "advisory": {
            "soil_prep": "Deep taproot system opens up hard soil horizons. pH 6.0-7.5.",
            "fertilizer": "Requires starter phosphorus; fixes copious nitrogen into the soil.",
            "water": "Tolerates extensive dry spells; critical water needed at pod development.",
            "tips": "Ideal for intercropping with cotton, soybean, or sorghum."
        },
        "icon": "🫛"
    },
    "pomegranate": {
        "botanical_name": "Punica granatum",
        "category": "Fruit / Horticulture",
        "growth_period_days": "Perennial (140-160 days from bloom to harvest)",
        "water_requirement": "Low to Moderate (500-700 mm)",
        "soil_preference": "Light loamy to deep sandy soils, tolerates moderate alkalinity",
        "market_profile": "Premium antioxidant fruit with high export price stability",
        "advisory": {
            "soil_prep": "Soil must have excellent drainage. pH range 6.0-7.8.",
            "fertilizer": "Adequate calcium and boron prevent fruit cracking during maturation.",
            "water": "Regulated deficit drip irrigation; maintain uniform moisture.",
            "tips": "Bagging fruits protects from fruit borer and bacterial blight (telya)."
        },
        "icon": "🫐"
    },
    "rice": {
        "botanical_name": "Oryza sativa (Paddy)",
        "category": "Cereal / Staple",
        "growth_period_days": "110-140 days (Kharif / Monsoon)",
        "water_requirement": "Very High (1200-2000 mm, standing water preferred)",
        "soil_preference": "Heavy clay or clay loams with low water permeability",
        "market_profile": "World's most critical staple grain, guaranteed government MSP & market",
        "advisory": {
            "soil_prep": "Puddle soil to create an impermeable layer that holds surface water.",
            "fertilizer": "Apply Nitrogen in 3 splits (transplanting, tillering, panicle initiation).",
            "water": "Maintain 2-5 cm standing water until 10 days before harvest.",
            "tips": "Incorporate green manure (dhaincha) prior to transplanting to enrich soil."
        },
        "icon": "🌾"
    },
    "watermelon": {
        "botanical_name": "Citrullus lanatus",
        "category": "Fruit / Cucurbit",
        "growth_period_days": "80-100 days",
        "water_requirement": "Moderate (400-600 mm)",
        "soil_preference": "Sandy loam, alluvial riverbeds with high organic matter",
        "market_profile": "High volume summer cash crop with rapid turnover",
        "advisory": {
            "soil_prep": "Well-drained soil that warms up quickly in spring (pH 6.0-7.0).",
            "fertilizer": "Needs high potassium for high Brix sugar levels and crisp rind.",
            "water": "Drip irrigation beneath mulch film; reduce watering as harvest nears.",
            "tips": "Mulching with silver-black plastic controls weeds and boosts early growth."
        },
        "icon": "🍉"
    }
}

PRESETS = [
    {
        "id": "monsoon-rice",
        "name": "Indo-Gangetic Alluvial (Rice Paddy)",
        "description": "High rainfall, tropical humidity, nutrient-rich alluvial clay loam.",
        "icon": "🌾",
        "values": {
            "N": 90,
            "P": 42,
            "K": 43,
            "temperature": 23.5,
            "humidity": 82.0,
            "ph": 6.8,
            "rainfall": 230.0
        },
        "expected_crop": "rice"
    },
    {
        "id": "deccan-cotton",
        "name": "Deccan Vertisol (Cotton Black Soil)",
        "description": "Warm climate, moderate rainfall, balanced nitrogen and potash in deep black soil.",
        "icon": "☁️",
        "values": {
            "N": 115,
            "P": 45,
            "K": 20,
            "temperature": 24.0,
            "humidity": 80.0,
            "ph": 6.9,
            "rainfall": 80.0
        },
        "expected_crop": "cotton"
    },
    {
        "id": "himalayan-apple",
        "name": "Himalayan Valley (Apple Orchard)",
        "description": "Cool temperate temperature, very high phosphorus and potassium requirements.",
        "icon": "🍎",
        "values": {
            "N": 20,
            "P": 135,
            "K": 200,
            "temperature": 22.0,
            "humidity": 92.0,
            "ph": 6.0,
            "rainfall": 110.0
        },
        "expected_crop": "apple"
    },
    {
        "id": "ghats-coffee",
        "name": "Western Ghats (Coffee Plantation)",
        "description": "High altitude, tropical humid showers, slightly acidic rich organic soil.",
        "icon": "☕",
        "values": {
            "N": 100,
            "P": 30,
            "K": 30,
            "temperature": 25.5,
            "humidity": 65.0,
            "ph": 6.7,
            "rainfall": 160.0
        },
        "expected_crop": "coffee"
    },
    {
        "id": "coastal-coconut",
        "name": "Coastal Sandy Loam (Coconut Palm)",
        "description": "Tropical coastal warmth, humid sea breeze, high rainfall and potassium.",
        "icon": "🥥",
        "values": {
            "N": 20,
            "P": 15,
            "K": 30,
            "temperature": 27.0,
            "humidity": 95.0,
            "ph": 6.0,
            "rainfall": 175.0
        },
        "expected_crop": "coconut"
    },
    {
        "id": "riverine-watermelon",
        "name": "Riverine Sandy Bed (Watermelon)",
        "description": "Warm sunny days, moderate humidity, light soil with moderate rainfall.",
        "icon": "🍉",
        "values": {
            "N": 100,
            "P": 18,
            "K": 50,
            "temperature": 26.0,
            "humidity": 85.0,
            "ph": 6.5,
            "rainfall": 50.0
        },
        "expected_crop": "watermelon"
    },
    {
        "id": "dryland-chickpea",
        "name": "Semi-Arid Dryland (Chickpea / Gram)",
        "description": "Cool dry winter rabi conditions, low rainfall, moderate phosphate.",
        "icon": "🌰",
        "values": {
            "N": 40,
            "P": 68,
            "K": 80,
            "temperature": 18.5,
            "humidity": 17.0,
            "ph": 7.3,
            "rainfall": 75.0
        },
        "expected_crop": "chickpea"
    },
    {
        "id": "tropical-banana",
        "name": "Tropical River Basin (Banana)",
        "description": "High warmth, high moisture, heavy nitrogen and potassium feeder.",
        "icon": "🍌",
        "values": {
            "N": 105,
            "P": 75,
            "K": 50,
            "temperature": 27.5,
            "humidity": 80.0,
            "ph": 6.2,
            "rainfall": 105.0
        },
        "expected_crop": "banana"
    }
]

BENCHMARK_TESTS = [
    {
        "id": "T1",
        "name": "Baseline Valid Soil & Weather Input",
        "description": "Standard balanced agronomic input. Verifies baseline model inference.",
        "input": {"N": 90, "P": 42, "K": 43, "temperature": 20.8, "humidity": 82.0, "ph": 6.5, "rainfall": 202.9},
        "expected_crop": "rice"
    },
    {
        "id": "T2",
        "name": "Temperature Sensitivity Check",
        "description": "Tests response to cool temperate climate (22°C) with high K and P.",
        "input": {"N": 20, "P": 134, "K": 200, "temperature": 22.0, "humidity": 92.0, "ph": 6.0, "rainfall": 112.0},
        "expected_crop": "apple"
    },
    {
        "id": "T3",
        "name": "Low Humidity / Arid Condition",
        "description": "Tests extremely dry atmospheric humidity (~17%) typical of winter pulses.",
        "input": {"N": 40, "P": 65, "K": 80, "temperature": 19.0, "humidity": 16.5, "ph": 7.3, "rainfall": 75.0},
        "expected_crop": "chickpea"
    },
    {
        "id": "T4",
        "name": "Soil pH Sensitivity Check",
        "description": "Tests acidic soil profile (pH ~5.5-6.0) suitable for highland plantation.",
        "input": {"N": 100, "P": 30, "K": 30, "temperature": 25.0, "humidity": 65.0, "ph": 6.5, "rainfall": 160.0},
        "expected_crop": "coffee"
    },
    {
        "id": "T5",
        "name": "High Rainfall Monsoon Condition",
        "description": "Tests heavy precipitation (>200 mm) with high moisture.",
        "input": {"N": 80, "P": 45, "K": 40, "temperature": 24.0, "humidity": 85.0, "ph": 6.8, "rainfall": 250.0},
        "expected_crop": "rice"
    },
    {
        "id": "T6",
        "name": "High Nitrogen Demand Crop",
        "description": "Tests heavy nitrogen enrichment (>100) and high moisture.",
        "input": {"N": 115, "P": 45, "K": 20, "temperature": 24.0, "humidity": 80.0, "ph": 6.9, "rainfall": 80.0},
        "expected_crop": "cotton"
    },
    {
        "id": "T7",
        "name": "High Phosphorus Requirement",
        "description": "Tests extreme phosphorus (>120) and potash (>190) fingerprint.",
        "input": {"N": 30, "P": 130, "K": 200, "temperature": 23.0, "humidity": 93.0, "ph": 6.1, "rainfall": 110.0},
        "expected_crop": "apple"
    },
    {
        "id": "T8",
        "name": "High Potassium & Coastal Humidity",
        "description": "Tests high humidity (>90%) with coastal sandy loam profile.",
        "input": {"N": 20, "P": 15, "K": 30, "temperature": 27.0, "humidity": 95.0, "ph": 6.0, "rainfall": 175.0},
        "expected_crop": "coconut"
    },
    {
        "id": "T9",
        "name": "Out-of-Range Boundary Rejection",
        "description": "Tests boundary validation (e.g. negative N or pH > 14) returning safe validation error.",
        "input": {"N": -10, "P": 50, "K": 50, "temperature": 25.0, "humidity": 70.0, "ph": 15.5, "rainfall": 100.0},
        "expected_status": "rejected"
    },
    {
        "id": "T10",
        "name": "Dataset Integrity & Zero-Corrupt Checks",
        "description": "Verifies that dataset has 2,200 clean rows, 0 nulls, and 22 balanced classes.",
        "expected_status": "verified"
    }
]
