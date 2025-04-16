import datetime
from collections import defaultdict

# Constants
ARRIVAL_DATE = "2024-03-26"
SEASON_TO_DATE = {
    "spring": "-03-21",
    "summer": "-06-21",
    "fall": "-09-21",
    "autumn": "-09-21",  # in case "autumn" is used
    "winter": "-12-21"
}

# Load names from animalNames.txt
def load_names(filename):
    with open(filename, "r") as file:
        return [name.strip() for name in file.readlines()]

# Generate birth date
def gen_birth_date(description):
    tokens = description.lower().split(",")[0].split()
    try:
        age_index = tokens.index("year")
        age = int(tokens[age_index - 1])
    except ValueError:
        age = int(tokens[0])  # fallback if "year" is missing

    # Check if season is mentioned
    birth_season = None
    for season in SEASON_TO_DATE.keys():
        if season in description.lower():
            birth_season = season
            break

    current_year = datetime.date.today().year
    birth_year = current_year - age

    if birth_season:
        return f"{birth_year}{SEASON_TO_DATE[birth_season]}"
    else:
        # default to June 1st if no season provided
        return f"{birth_year}-06-01"

# Generate unique ID
def gen_unique_id(species, counter_dict):
    code = species[:2].capitalize()
    counter_dict[code] += 1
    return f"{code}{counter_dict[code]:02d}"

# Main function to process zoo data
def process_zoo(arriving_file, names_file, output_file):
    names = load_names(names_file)
    with open(arriving_file, "r") as file:
        animal_lines = [line.strip() for line in file.readlines()]

    habitat_dict = defaultdict(list)
    id_counters = defaultdict(int)
    name_index = 0

    for desc in animal_lines:
        tokens = desc.split(",")
        primary = tokens[0].strip().split()
        age = int(primary[0])
        sex = primary[3]
        species = primary[4].lower()
        color = tokens[1].strip().split()[0]
        weight = tokens[2].strip().split()[0]
        origin = ", ".join([t.strip() for t in tokens[3:]])

        birth_date = gen_birth_date(desc)
        animal_id = gen_unique_id(species, id_counters)
        animal_name = names[name_index] if name_index < len(names) else f"Unnamed{animal_id}"
        name_index += 1

        # Build formatted line
        animal_info = (
            f"{animal_id}; {animal_name}; birth date: {birth_date}; "
            f"{color} color; {sex}; {weight} pounds; from {origin}; arrived {ARRIVAL_DATE}"
        )
        habitat_dict[species.capitalize() + " Habitat"].append(animal_
