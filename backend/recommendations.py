RECOMMENDATIONS = {
    "aphid": "Apply neem oil spray or insecticidal soap.",
    "whitefly": "Use yellow sticky traps and neem oil.",
    "pink_bollworm": "Apply Bt spray (Bacillus thuringiensis).",
    "bollworm": "Apply Bt spray (Bacillus thuringiensis).",
    "default": "Consult your local agricultural extension officer for specific treatment."
}

def get_recommendation(pest_class: str) -> str:
    return RECOMMENDATIONS.get(pest_class.lower(), RECOMMENDATIONS["default"])
