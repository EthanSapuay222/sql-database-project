import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from model import Location, ReportCategory, ReportSeverity, Species, EnvironmentalReport
from database import db
from datetime import date, timedelta
import random


# SECTION 1: LOCATIONS DATA

# 34 locations covering Batangas: 5 cities + 29 municipalities
# Fields: city_name, location_type (city/municipality), latitude, longitude, severity_level

SAMPLE_LOCATIONS = [
    # CITIES
    {'city_name': 'Batangas City', 'latitude': 13.7565, 'location_type': 'city', 'longitude': 121.0583, 'severity_level': 'Critical'},
    {'city_name': 'Calaca', 'latitude': 13.9167, 'location_type': 'city', 'longitude': 120.8167, 'severity_level': 'Low'},
    {'city_name': 'Lipa City', 'latitude': 13.9411, 'location_type': 'city', 'longitude': 121.1622, 'severity_level': 'High'},
    {'city_name': 'Santo Tomas', 'latitude': 14.1078, 'location_type': 'city', 'longitude': 121.1414, 'severity_level': 'Medium'},
    {'city_name': 'Tanauan City', 'latitude': 14.0858, 'location_type': 'city', 'longitude': 121.1500, 'severity_level': 'Critical'},

    # MUNICIPALITIES
    {'city_name': 'Agoncillo', 'latitude': 13.9333, 'location_type': 'municipality', 'longitude': 120.9333, 'severity_level': 'Low'},
    {'city_name': 'Alitagtag', 'latitude': 13.8667, 'location_type': 'municipality', 'longitude': 121.0000, 'severity_level': 'Low'},
    {'city_name': 'Balayan', 'latitude': 13.9389, 'location_type': 'municipality', 'longitude': 120.7333, 'severity_level': 'Medium'},
    {'city_name': 'Balete', 'latitude': 13.9833, 'location_type': 'municipality', 'longitude': 121.1000, 'severity_level': 'Low'},
    {'city_name': 'Bauan', 'latitude': 13.7917, 'location_type': 'municipality', 'longitude': 121.0089, 'severity_level': 'High'},
    {'city_name': 'Calatagan', 'latitude': 13.8319, 'location_type': 'municipality', 'longitude': 120.6322, 'severity_level': 'Low'},
    {'city_name': 'Cuenca', 'latitude': 13.9072, 'location_type': 'municipality', 'longitude': 121.0497, 'severity_level': 'Medium'},
    {'city_name': 'Ibaan', 'latitude': 13.8167, 'location_type': 'municipality', 'longitude': 121.1333, 'severity_level': 'Low'},
    {'city_name': 'Laurel', 'latitude': 14.0500, 'location_type': 'municipality', 'longitude': 120.9167, 'severity_level': 'Medium'},
    {'city_name': 'Lemery', 'latitude': 13.9167, 'location_type': 'municipality', 'longitude': 120.8833, 'severity_level': 'Medium'},
    {'city_name': 'Lian', 'latitude': 14.0333, 'location_type': 'municipality', 'longitude': 120.6500, 'severity_level': 'Low'},
    {'city_name': 'Lobo', 'latitude': 13.6500, 'location_type': 'municipality', 'longitude': 121.2333, 'severity_level': 'High'},
    {'city_name': 'Mabini', 'latitude': 13.7233, 'location_type': 'municipality', 'longitude': 120.8961, 'severity_level': 'Critical'},
    {'city_name': 'Malvar', 'latitude': 14.0444, 'location_type': 'municipality', 'longitude': 121.1550, 'severity_level': 'Low'},
    {'city_name': 'Mataasnakahoy', 'latitude': 13.9667, 'location_type': 'municipality', 'longitude': 121.1000, 'severity_level': 'Medium'},
    {'city_name': 'Nasugbu', 'latitude': 14.0689, 'location_type': 'municipality', 'longitude': 120.6317, 'severity_level': 'High'},
    {'city_name': 'Padre Garcia', 'latitude': 13.8833, 'location_type': 'municipality', 'longitude': 121.2167, 'severity_level': 'Low'},
    {'city_name': 'Rosario', 'latitude': 13.8472, 'location_type': 'municipality', 'longitude': 121.2056, 'severity_level': 'Medium'},
    {'city_name': 'San Jose', 'latitude': 13.8806, 'location_type': 'municipality', 'longitude': 121.0931, 'severity_level': 'Low'},
    {'city_name': 'San Juan', 'latitude': 13.8333, 'location_type': 'municipality', 'longitude': 121.4000, 'severity_level': 'Critical'},
    {'city_name': 'San Luis', 'latitude': 13.8500, 'location_type': 'municipality', 'longitude': 120.9500, 'severity_level': 'Medium'},
    {'city_name': 'San Nicolas', 'latitude': 13.9167, 'location_type': 'municipality', 'longitude': 120.9667, 'severity_level': 'High'},
    {'city_name': 'San Pascual', 'latitude': 13.8083, 'location_type': 'municipality', 'longitude': 121.0275, 'severity_level': 'Medium'},
    {'city_name': 'Santa Teresita', 'latitude': 13.8333, 'location_type': 'municipality', 'longitude': 121.0000, 'severity_level': 'Low'},
    {'city_name': 'Taal', 'latitude': 13.8833, 'location_type': 'municipality', 'longitude': 120.9333, 'severity_level': 'High'},
    {'city_name': 'Talisay', 'latitude': 14.1000, 'location_type': 'municipality', 'longitude': 121.0167, 'severity_level': 'Low'},
    {'city_name': 'Taysan', 'latitude': 13.7667, 'location_type': 'municipality', 'longitude': 121.2167, 'severity_level': 'Medium'},
    {'city_name': 'Tingloy', 'latitude': 13.6667, 'location_type': 'municipality', 'longitude': 120.8833, 'severity_level': 'Low'},
    {'city_name': 'Tuy', 'latitude': 14.0167, 'location_type': 'municipality', 'longitude': 120.7333, 'severity_level': 'Low'},
]


# ============================================================================
# SECTION 2: REPORT CATEGORIES DATA
# ============================================================================
# 5 categories for environmental reports
# Used in submission form dropdown and dashboard filtering
#
# ⚠️ IMPORTANT: Category names are converted to enum values in the database!
# Conversion: name.lower().replace(' ', '_')
# Example: "Waste Dumping" → "waste_dumping"
#
# If you change these categories, you MUST also update:
# 1. model.py → EnvironmentalReport.report_type Enum values
# 2. forms.py → EnvironmentalReportForm.report_type choices
# 3. All SAMPLE_REPORTS below that reference these categories
#
# Current enum values: pollution, deforestation, waste_dumping, wildlife_incident, other

SAMPLE_CATEGORIES = [
    {'name': 'Pollution', 'description': 'Air, water, soil, or noise pollution'},
    {'name': 'Deforestation', 'description': 'Illegal or unauthorized forest clearing'},
    {'name': 'Waste Dumping', 'description': 'Illegal waste disposal'},
    {'name': 'Wildlife Incident', 'description': 'Wildlife injury, trafficking, or habitat issues'},
    {'name': 'Other', 'description': 'Other environmental concerns'},
]


# ============================================================================
# SECTION 3: REPORT SEVERITY LEVELS DATA
# ============================================================================
# 4 severity levels for environmental reports
# Used in submission form dropdown and dashboard stats
#
# ⚠️ IMPORTANT: Severity levels are case-sensitive in the database!
# Enum values: Critical, High, Medium, Low (capitalized)
#
# If you change these levels, you MUST also update:
# 1. model.py → EnvironmentalReport.severity Enum values
# 2. model.py → Location.severity_level Enum values
# 3. forms.py → EnvironmentalReportForm.severity choices
# 4. All SAMPLE_REPORTS and SAMPLE_LOCATIONS that reference severity

SAMPLE_SEVERITY = [
    {'level': 'Low', 'description': 'Minor environmental impact, non-urgent'},
    {'level': 'Medium', 'description': 'Moderate impact, should be addressed soon'},
    {'level': 'High', 'description': 'Significant impact, requires prompt action'},
    {'level': 'Critical', 'description': 'Severe impact, immediate action required'},
]


# ============================================================================
# SECTION 4: SPECIES DATA
# ============================================================================
# 20 species: 12 land animals, 8 water animals
# Used in Life on Land and Water page and animal sighting submissions

LAND_SPECIES = [
    # Birds
    {
        'common_name': 'Philippine Duck',
        'scientific_name': 'Anas luzonica',
        'category': 'land',
        'species_type': 'bird',
        'conservation_status': 'Least Concern',
        'status_trend': 'stable',
        'total_sightings_estimate': '15,000-30,000',
        'description': 'Sporting brown plumage and a distinctive blue-grey bill, this species charms with its subtle beauty and surprises with its adaptability.',
        'habitat_info': 'Freshwater lakes, marshes, rice paddies, and wetlands throughout the Philippines. Prefers shallow waters with vegetation.',
        'diet_info': 'Seeds, aquatic plants, small invertebrates, and grain. Dabbles and tips-up to feed on submerged vegetation.'
    },
    {
        'common_name': 'White-breasted Waterhen',
        'scientific_name': 'Amaurornis phoenicurus',
        'category': 'land',
        'species_type': 'bird',
        'conservation_status': 'Least Concern',
        'status_trend': 'stable',
        'total_sightings_estimate': '10,000-100,000',
        'description': 'Adult White-breasted waterhens have mainly dark grey upperparts and flanks, and a white face, neck, and breast. The lower belly and undertail are cinnamon or white colored.',
        'habitat_info': 'Wetlands, marshes, ricefields, and water margins. Often found in areas with dense vegetation and reeds.',
        'diet_info': 'Aquatic invertebrates, small fish, seeds, and plant material. Forages by picking from water surface or ground.'
    },
    {
        'common_name': 'Garden Sunbird',
        'scientific_name': 'Cinnyris jugularis',
        'category': 'land',
        'species_type': 'bird',
        'conservation_status': 'Least Concern',
        'status_trend': 'stable',
        'total_sightings_estimate': '15,000-25,000',
        'description': 'A beautifully colored passerine bird from Southeast Asia. It has a long downward-curved bill which it uses to take nectar and capture insects.',
        'habitat_info': 'Gardens, scrubland, forest edges, and cultivated areas with flowering plants. Found in lowlands and hills up to 2000m.',
        'diet_info': 'Primarily nectar from flowering plants, also small insects and spiders caught while feeding on flowers.'
    },
    {
        'common_name': 'Collared Kingfisher',
        'scientific_name': 'Todiramphus chloris',
        'category': 'land',
        'species_type': 'bird',
        'conservation_status': 'Least Concern',
        'status_trend': 'stable',
        'total_sightings_estimate': 'Unknown',
        'description': 'It hunts insects, crabs and small fish by perching and quickly diving its prey. This species is widespread and easily spotted due to its loud calls.',
        'habitat_info': 'Open habitats near water including mangroves, coastal areas, ricefields, and forest edges. Often seen perched prominently.',
        'diet_info': 'Small fish, crustaceans, and large insects. Hunts by perching and diving quickly to catch prey in water.'
    },
    
    # Mammals
    {
        'common_name': 'Greater Musky Fruit Bat',
        'scientific_name': 'Ptenochirus jagori',
        'category': 'land',
        'species_type': 'mammal',
        'conservation_status': 'Least Concern',
        'status_trend': 'stable',
        'total_sightings_estimate': 'Not specified yet',
        'description': 'A captivating creature of the night, found gracefully navigating the tropical forests of Southeast Asia. These fascinating bats play a vital role in their ecosystems.',
        'habitat_info': 'Tropical forests, secondary forests, and forest gardens. Roosts in caves, tree hollows, and human structures.',
        'diet_info': 'Fruits and nectar from various tree species. Plays important role in seed dispersal and pollination.'
    },
    {
        'common_name': 'Luzon Giant Cloud Rat',
        'scientific_name': 'Phloeomys pallidus',
        'category': 'land',
        'species_type': 'mammal',
        'conservation_status': 'Concerned',
        'status_trend': 'stable',
        'total_sightings_estimate': 'Unknown',
        'description': 'This rodent has a relatively long pelage, which also covers the tail. The color is highly variable, but it is usually pale brown-grey or white with some dark brown or black patches.',
        'habitat_info': 'Cloud forests and mossy montane forests of northern Luzon at high elevations (1500-2500m). Nocturnal and arboreal.',
        'diet_info': 'Leaves, bark, and vegetation found in forest canopy. Primarily herbivorous, adapted for arboreal life.'
    },
    {
        'common_name': 'Lion',
        'scientific_name': 'Panthera leo',
        'category': 'land',
        'species_type': 'mammal',
        'conservation_status': 'Vulnerable',
        'status_trend': 'decreasing',
        'total_sightings_estimate': '23,000-39,000',
        'description': 'The lion is a big wild cat with short, tawny-colored fur and white underparts. The long tail ends with a black tuft.',
        'habitat_info': 'Savannas, grasslands, and open woodlands in Africa and small population in Gir Forest, India. Social cats living in prides.',
        'diet_info': 'Large herbivores including zebras, antelope, and buffalo. Apex predators hunted cooperatively in groups.'
    },
    {
        'common_name': 'Philippine Warty Pig',
        'scientific_name': 'Sus philippensis',
        'category': 'land',
        'species_type': 'mammal',
        'conservation_status': 'Vulnerable',
        'status_trend': 'decreasing',
        'total_sightings_estimate': 'Unknown',
        'description': 'A wild pig species with a distinctive "mane" and warty face. Important for nutrient cycling in forests.',
        'habitat_info': 'Tropical forests and forest edges throughout the Philippines. Nocturnal and solitary, uses forest for shelter and food.',
        'diet_info': 'Roots, tubers, insects, small animals, and fallen fruit. Forages on forest floor and helps maintain soil health.'
    },
    {
        'common_name': 'Philippine Long-Tailed Macaque',
        'scientific_name': 'Macaca fascicularis philippensis',
        'category': 'land',
        'species_type': 'mammal',
        'conservation_status': 'Least Concern',
        'status_trend': 'decreasing',
        'total_sightings_estimate': 'Unknown',
        'description': 'Lives in group and eat fruits, leaves, and small animals, making it very adaptable. However, its population is decreasing due to habitat loss and trapping.',
        'habitat_info': 'Tropical forests, mangroves, and agricultural areas throughout Philippines. Highly adaptable to different habitats. Social species living in troops.',
        'diet_info': 'Fruits, leaves, seeds, insects, and small vertebrates. Opportunistic feeders adaptable to various food sources.'
    },
    
    # Reptiles
    {
        'common_name': 'Tokay Gecko',
        'scientific_name': 'Gekko gecko',
        'category': 'land',
        'species_type': 'reptile',
        'conservation_status': 'Least Concern',
        'status_trend': 'stable',
        'total_sightings_estimate': 'Unknown',
        'description': 'The skin of Tokay geckos is soft to the touch and is generally gray with red speckles. However, Tokay geckos can change the color of their skin to blend into the environment.',
        'habitat_info': 'Tropical forests, caves, human structures, and rocky areas. Nocturnal, often heard by distinctive loud calls at night.',
        'diet_info': 'Insects, spiders, small vertebrates, and other small animals. Active hunters that wait for prey on surfaces.'
    },
    {
        'common_name': 'Reticulated Python',
        'scientific_name': 'Malayopython reticulatus',
        'category': 'land',
        'species_type': 'reptile',
        'conservation_status': 'Least Concern',
        'status_trend': 'stable',
        'total_sightings_estimate': 'Unknown',
        'description': 'Is a non-venomous snake native to South and Southeast Asia. It is the world\'s longest snake and is among the three heaviest snakes.',
        'habitat_info': 'Tropical rainforests, swamps, and cultivated areas throughout Southeast Asia. Semi-aquatic, often found near water.',
        'diet_info': 'Mammals and large birds. Constrictor that swallows prey whole. Can consume large animals.'
    },
    {
        'common_name': 'Common House Gecko',
        'scientific_name': 'Hemidactylus frenatus',
        'category': 'land',
        'species_type': 'reptile',
        'conservation_status': 'Least Concern',
        'status_trend': 'stable',
        'total_sightings_estimate': 'Unknown',
        'description': 'A small lizard native to Southeast Asia. They are named so because they are often seen climbing walls of houses and other buildings in search of insects.',
        'habitat_info': 'Human settlements, houses, buildings, and trees. Commensal species highly adapted to living with humans.',
        'diet_info': 'Small insects, spiders, and invertebrates. Nocturnal hunters attracted to artificial lights around buildings.'
    },
]

WATER_SPECIES = [
    # Sea Turtles
    {
        'common_name': 'Olive Ridley Turtle',
        'scientific_name': 'Lepidochelys olivacea',
        'category': 'water',
        'species_type': 'reptile',
        'conservation_status': 'Vulnerable',
        'status_trend': 'unknown',
        'total_sightings_estimate': 'Unknown',
        'description': 'A small to medium sea turtle known for its olive colored shell. They are famous for nesting events called "arribadas". They feed on jellyfish, small fish, crustaceans.',
        'habitat_info': 'Tropical and subtropical oceans worldwide. Highly migratory, travels long distances between feeding and nesting grounds.',
        'diet_info': 'Jellyfish, small fish, crustaceans, and marine plants. Also consumes floating debris which can be fatal.'
    },
    {
        'common_name': 'Green Turtle',
        'scientific_name': 'Chelonia mydas',
        'category': 'water',
        'species_type': 'reptile',
        'conservation_status': 'Endangered',
        'status_trend': 'unknown',
        'total_sightings_estimate': 'Unknown',
        'description': 'Large herbivorous sea turtle often found near coral reefs and seagrass beds. Adults eat sea grass, helping maintain healthy marine ecosystems.',
        'habitat_info': 'Tropical and subtropical oceans, coastal reefs, and seagrass beds. Females return to natal beaches to nest.',
        'diet_info': 'Juveniles are omnivorous eating jellyfish and invertebrates. Adults are herbivorous, feeding on seagrass and algae.'
    },
    {
        'common_name': 'Hawksbill Turtle',
        'scientific_name': 'Eretmochelys imbricata',
        'category': 'water',
        'species_type': 'reptile',
        'conservation_status': 'Critically Endangered',
        'status_trend': 'unknown',
        'total_sightings_estimate': 'Unknown',
        'description': 'Critically endangered turtle known for its beautifully patterned shell. They help control sponge populations on coral reefs.',
        'habitat_info': 'Tropical coral reefs and rocky areas throughout world oceans. Highly migratory and solitary species.',
        'diet_info': 'Primarily sponges living on coral reefs. Also eats tunicates, corals, and other invertebrates. Helps maintain reef health.'
    },
    
    # Fish/Sharks
    {
        'common_name': 'Whale Shark',
        'scientific_name': 'Rhincodon typus',
        'category': 'water',
        'species_type': 'fish',
        'conservation_status': 'Endangered',
        'status_trend': 'decreasing',
        'total_sightings_estimate': 'Unknown',
        'description': 'The world\'s largest fish. A gentle filter feeder eating plankton and small fish. Important to ocean plankton balance.',
        'habitat_info': 'Tropical and subtropical oceans between 21-30°C. Migratory, seasonally moves to areas with plankton blooms.',
        'diet_info': 'Filter feeder eating plankton, fish eggs, and small fish. Processes large volumes of water daily.'
    },
    {
        'common_name': 'Blacktip Reef Shark',
        'scientific_name': 'Carcharhinus melanopterus',
        'category': 'water',
        'species_type': 'fish',
        'conservation_status': 'Near Threatened',
        'status_trend': 'unknown',
        'total_sightings_estimate': 'Unknown',
        'description': 'A small reef shark with black-tipped fins. Lives in shallow water and coral reefs. Plays a role in keeping fish populations balanced.',
        'habitat_info': 'Shallow coastal waters, coral reefs, and lagoons in Indo-Pacific region. Found at depths less than 60m.',
        'diet_info': 'Small fish, rays, and crustaceans. Important predator maintaining balance in reef ecosystems.'
    },
    
    # Rays
    {
        'common_name': 'Manta Rays',
        'scientific_name': 'Mobula alfredi, Mobula birostris',
        'category': 'water',
        'species_type': 'fish',
        'conservation_status': 'Vulnerable',
        'status_trend': 'unknown',
        'total_sightings_estimate': 'Unknown',
        'description': 'Large, gentle rays called "sea butterflies". Filter feeding on plankton. Highly intelligent and long lived.',
        'habitat_info': 'Tropical and subtropical oceans. Highly migratory, seasonally congregates in areas with plankton abundance.',
        'diet_info': 'Filter feeders eating plankton and small fish. Can consume up to 1% of body weight daily in plankton.'
    },
    
    # Marine Mammals
    {
        'common_name': 'Spinner Dolphin',
        'scientific_name': 'Stenella longirostris',
        'category': 'water',
        'species_type': 'mammal',
        'conservation_status': 'Vulnerable',
        'status_trend': 'unknown',
        'total_sightings_estimate': 'Unknown',
        'description': 'Small, active dolphins known for spinning jumps. Feed on small fish and squid. Important part of marine food chain.',
        'habitat_info': 'Tropical and subtropical oceans worldwide. Often found in groups, daylight hours in deeper offshore waters.',
        'diet_info': 'Small fish and squid caught during night feeding dives. Uses echolocation to hunt in deep waters.'
    },
    {
        'common_name': 'Dwarf Sperm Whale',
        'scientific_name': 'Kogia sima',
        'category': 'water',
        'species_type': 'mammal',
        'conservation_status': 'Data Deficient',
        'status_trend': 'unknown',
        'total_sightings_estimate': 'Unknown',
        'description': 'A small, shy whale species rarely seen alive. Known for releasing a cloud of ink-like fluid to escape predators.',
        'habitat_info': 'Deep offshore waters of tropical and subtropical oceans. Elusive and rarely observed in wild.',
        'diet_info': 'Deep-sea squid and fish. Dives to depths of 300-900m to hunt in deep water.'
    },
]


# ============================================================================
# SECTION 5: SAMPLE REPORTS DATA
# ============================================================================
# 10 sample environmental reports for testing dashboard and map

SAMPLE_REPORTS = [
    {
        'title': 'Illegal Waste Dumping at Batangas City Port',
        'description': 'Large amounts of industrial waste found dumped near the port area. Immediate cleanup required.',
        'report_type': 'pollution',
        'severity': 'Critical',
        'reporter_name': 'Juan Dela Cruz',
        'reporter_contact': 'juan@email.com',
        'status': 'pending'
    },
    {
        'title': 'Deforestation in Taal Watershed',
        'description': 'Unauthorized tree cutting observed in the protected watershed area.',
        'report_type': 'deforestation',
        'severity': 'High',
        'reporter_name': 'Maria Santos',
        'reporter_contact': 'maria@email.com',
        'status': 'in_progress'
    },
    {
        'title': 'Plastic Pollution at Nasugbu Beach',
        'description': 'Excessive plastic waste accumulating along the shoreline, affecting marine life.',
        'report_type': 'pollution',
        'severity': 'High',
        'reporter_name': 'Pedro Reyes',
        'reporter_contact': '09123456789',
        'status': 'pending'
    },
    {
        'title': 'Wildlife Trafficking Suspected',
        'description': 'Reports of illegal bird trading in the local market area.',
        'report_type': 'wildlife_incident',
        'severity': 'Critical',
        'reporter_name': 'Ana Garcia',
        'reporter_contact': 'ana.garcia@email.com',
        'status': 'in_progress'
    },
    {
        'title': 'Water Pollution in Tanauan River',
        'description': 'Factory discharge causing water discoloration and fish kill.',
        'report_type': 'pollution',
        'severity': 'High',
        'reporter_name': 'Carlos Manuel',
        'reporter_contact': '09187654321',
        'status': 'pending'
    },
    {
        'title': 'Illegal Fishing Activity',
        'description': 'Use of dynamite fishing reported in coastal areas of Mabini.',
        'report_type': 'waste_dumping',
        'severity': 'Critical',
        'reporter_name': 'Rosa Mendoza',
        'reporter_contact': 'rosa.m@email.com',
        'status': 'completed'
    },
    {
        'title': 'Air Quality Concerns in Lipa City',
        'description': 'Increased smoke emissions from industrial area affecting residents.',
        'report_type': 'pollution',
        'severity': 'Medium',
        'reporter_name': 'Jose Villanueva',
        'reporter_contact': 'jose.v@email.com',
        'status': 'in_progress'
    },
    {
        'title': 'Coral Reef Damage',
        'description': 'Boat anchors damaging coral formations in Tingloy marine sanctuary.',
        'report_type': 'deforestation',
        'severity': 'High',
        'reporter_name': 'Lisa Fernandez',
        'reporter_contact': '09162345678',
        'status': 'pending'
    },
    {
        'title': 'Noise Pollution from Construction',
        'description': 'Excessive noise during late hours affecting wildlife in Santo Tomas.',
        'report_type': 'other',
        'severity': 'Low',
        'reporter_name': 'Roberto Cruz',
        'reporter_contact': 'roberto@email.com',
        'status': 'completed'
    },
    {
        'title': 'Mangrove Clearing in Balayan',
        'description': 'Illegal clearing of mangrove forest for construction purposes.',
        'report_type': 'deforestation',
        'severity': 'Critical',
        'reporter_name': 'Elena Torres',
        'reporter_contact': 'elena.t@email.com',
        'status': 'in_progress'
    }
]


# ============================================================================
# SEEDING FUNCTIONS
# ============================================================================

def seed_locations():
    """Seed locations table with upsert logic (insert or update)"""
    inserted = 0
    updated = 0

    for loc in SAMPLE_LOCATIONS:
        existing = Location.query.filter_by(city_name=loc['city_name']).first()
        if existing:
            # Update fields if they've changed
            changed = False
            if existing.location_type != loc['location_type']:
                existing.location_type = loc['location_type']
                changed = True
            if existing.latitude != loc['latitude']:
                existing.latitude = loc['latitude']
                changed = True
            if existing.longitude != loc['longitude']:
                existing.longitude = loc['longitude']
                changed = True
            if existing.severity_level != loc['severity_level']:
                existing.severity_level = loc['severity_level']
                changed = True

            if changed:
                updated += 1
        else:
            new_loc = Location(
                city_name=loc['city_name'],
                location_type=loc['location_type'],
                latitude=loc['latitude'],
                longitude=loc['longitude'],
                severity_level=loc['severity_level'],
                total_reports=0,
            )
            db.session.add(new_loc)
            inserted += 1

    if inserted or updated:
        db.session.commit()

    return inserted, updated


def seed_categories():
    """Seed report categories table with upsert logic"""
    inserted = 0
    updated = 0

    for cat_data in SAMPLE_CATEGORIES:
        existing = ReportCategory.query.filter_by(name=cat_data['name']).first()
        if existing:
            # Update description if changed
            if existing.description != cat_data.get('description'):
                existing.description = cat_data.get('description')
                updated += 1
        else:
            new_cat = ReportCategory(
                name=cat_data['name'],
                description=cat_data.get('description')
            )
            db.session.add(new_cat)
            inserted += 1

    if inserted or updated:
        db.session.commit()

    return inserted, updated


def seed_severity():
    """Seed report severity levels table with upsert logic"""
    inserted = 0
    updated = 0

    for sev_data in SAMPLE_SEVERITY:
        existing = ReportSeverity.query.filter_by(level=sev_data['level']).first()
        if existing:
            # Update description if changed
            if existing.description != sev_data.get('description'):
                existing.description = sev_data.get('description')
                updated += 1
        else:
            new_sev = ReportSeverity(
                level=sev_data['level'],
                description=sev_data.get('description')
            )
            db.session.add(new_sev)
            inserted += 1

    if inserted or updated:
        db.session.commit()

    return inserted, updated


def seed_species():
    """Seed species table with land and water species"""
    inserted = 0
    updated = 0

    # Seed Land Species
    for species_data in LAND_SPECIES:
        existing = Species.query.filter_by(common_name=species_data['common_name']).first()
        if existing:
            # Update if changed
            changed = False
            for key, value in species_data.items():
                if getattr(existing, key) != value:
                    setattr(existing, key, value)
                    changed = True
            if changed:
                updated += 1
        else:
            new_species = Species(**species_data)
            db.session.add(new_species)
            inserted += 1

    # Seed Water Species
    for species_data in WATER_SPECIES:
        existing = Species.query.filter_by(common_name=species_data['common_name']).first()
        if existing:
            # Update if changed
            changed = False
            for key, value in species_data.items():
                if getattr(existing, key) != value:
                    setattr(existing, key, value)
                    changed = True
            if changed:
                updated += 1
        else:
            new_species = Species(**species_data)
            db.session.add(new_species)
            inserted += 1

    if inserted or updated:
        db.session.commit()

    return inserted, updated


def seed_sample_reports():
    """Seed sample environmental reports for testing"""
    inserted = 0
    
    # Get all locations
    locations = Location.query.all()
    if not locations:
        print("      ⚠️  No locations found! Skipping sample reports.")
        return 0
    
    # Clear existing reports
    EnvironmentalReport.query.delete()
    
    # Add sample reports
    for report_data in SAMPLE_REPORTS:
        # Randomly assign location
        location = random.choice(locations)
        
        # Create report with dates in the past few days
        days_ago = random.randint(0, 14)
        report_date = date.today() - timedelta(days=days_ago)
        
        new_report = EnvironmentalReport(
            location_id=location.location_id,
            title=report_data['title'],
            description=report_data['description'],
            report_type=report_data['report_type'],
            severity=report_data['severity'],
            status=report_data['status'],
            reporter_name=report_data['reporter_name'],
            reporter_contact=report_data['reporter_contact'],
            report_date=report_date
        )
        
        db.session.add(new_report)
        inserted += 1
    
    if inserted:
        db.session.commit()
    
    return inserted


def main():
    """Run all seeding operations"""
    with app.app_context():
        print("=" * 70)
        print("🌱 MASTER SEED - EcoTrack Database Initialization")
        print("=" * 70)

        # Seed Locations
        print("\n[1/5] Seeding Locations (34 Batangas cities & municipalities)...")
        loc_inserted, loc_updated = seed_locations()
        print(f"      ✅ Locations - Inserted: {loc_inserted}, Updated: {loc_updated}")

        # Seed Categories
        print("\n[2/5] Seeding Report Categories (5 types)...")
        cat_inserted, cat_updated = seed_categories()
        print(f"      ✅ Categories - Inserted: {cat_inserted}, Updated: {cat_updated}")

        # Seed Severity
        print("\n[3/5] Seeding Report Severity Levels (4 levels)...")
        sev_inserted, sev_updated = seed_severity()
        print(f"      ✅ Severity Levels - Inserted: {sev_inserted}, Updated: {sev_updated}")

        # Seed Species
        print("\n[4/5] Seeding Species (20 land and water animals)...")
        spec_inserted, spec_updated = seed_species()
        print(f"      ✅ Species - Inserted: {spec_inserted}, Updated: {spec_updated}")

        # Seed Sample Reports
        print("\n[5/5] Seeding Sample Environmental Reports (10 test reports)...")
        rep_inserted = seed_sample_reports()
        print(f"      ✅ Sample Reports - Inserted: {rep_inserted}")

        print("\n" + "=" * 70)
        print("✅ SEEDING COMPLETE!")
        print("=" * 70)
        print(f"\nTotal Summary:")
        print(f"  - Locations:       {loc_inserted} inserted, {loc_updated} updated")
        print(f"  - Categories:      {cat_inserted} inserted, {cat_updated} updated")
        print(f"  - Severity:        {sev_inserted} inserted, {sev_updated} updated")
        print(f"  - Species:         {spec_inserted} inserted, {spec_updated} updated")
        print(f"  - Sample Reports:  {rep_inserted} inserted")
        print("\n")


if __name__ == '__main__':
    main()
