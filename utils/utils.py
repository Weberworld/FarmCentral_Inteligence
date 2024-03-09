import random


def generate_random_string():
    s = [str(_) for _ in range(random.randint(6, 15))]
    random.shuffle(s)
    random_str = "".join(s)
    return random_str


nigeria_states = [
    "Abia", "Adamawa", "AkwaIbom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "CrossRiver",
    "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano",
    "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo",
    "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara",
]


def parse_search_key(key):
    """
    Determines the type of the search key suggestions
    """
    try:
        int(key)
        return "phone"
    except ValueError:
        # Check if the key matches a state
        for state in nigeria_states:
            if state.lower().startswith(key) or key.lower() in state.lower():
                return "state"
        return "crop_type"
