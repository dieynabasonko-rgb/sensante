# notebooks/test_groq.py
# Test de l'API Groq avec Llama 3

import os
from dotenv import load_dotenv
from groq import Groq

# Charger la cle depuis .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERREUR : GROQ_API_KEY non trouvee dans .env")
    exit()

# Creer le client Groq
client = Groq(api_key=api_key)

# --- Test 1 : question simple ---
print("=== Test 1 : Question simple ===")
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": "Tu es un assistant medical senegalais. "
                       "Reponds en francais simple. "
                       "Maximum 3 phrases."
        },
        {
            "role": "user",
            "content": "Quels sont les symptomes du paludisme ?"
        }
    ],
    max_tokens=200,
    temperature=0.3
)
print(response.choices[0].message.content)
print(f"\nTokens utilises : {response.usage.total_tokens}")

# --- Test 2 : format SénSanté ---
print("\n=== Test 2 : Explication SenSante ===")
response2 = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": """Tu es un assistant medical senegalais.
Tu recois un diagnostic et des donnees patient.
Explique le resultat en francais simple,
comme un medecin parlerait a son patient.
Sois rassurant mais recommande une consultation.
Maximum 3 phrases.
Ne fais JAMAIS de diagnostic toi-meme."""
        },
        {
            "role": "user",
            "content": """Patient : Femme, 28 ans, region Dakar
Symptomes : temperature 39.5, toux, fatigue, maux de tete
Diagnostic du modele : paludisme (probabilite 72%)
Explique ce resultat au patient."""
        }
    ],
    max_tokens=200,
    temperature=0.3
)
print(response2.choices[0].message.content)

# --- Test 3 : format SénSanté complet (etape 3.3) ---
print("\n=== Test 3 : Diagnostic SenSante complet ===")
response3 = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": """Tu es un assistant medical senegalais.
Tu recois un diagnostic et des donnees patient.
Explique le resultat en francais simple,
comme un medecin parlerait a son patient.
Sois rassurant mais recommande toujours une consultation medicale.
Maximum 3 phrases.
Ne fais JAMAIS de diagnostic toi-meme.
Tu expliques uniquement le diagnostic fourni."""
        },
        {
            "role": "user",
            "content": """Patient : Femme, 28 ans, region Dakar
Symptomes : temperature 39.5, toux, fatigue, maux de tete
Diagnostic du modele : paludisme (probabilite 72%)
Explique ce resultat au patient."""
        }
    ],
    max_tokens=200,
    temperature=0.3
)
print(response3.choices[0].message.content)

print("\n=== Exercice 2 : Test des temperatures ===")

for temp in [0.0, 0.5, 1.0]:
    response_temp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """Tu es un assistant medical senegalais.
Explique le resultat en francais simple.
Maximum 3 phrases.
Ne fais JAMAIS de diagnostic toi-meme."""
            },
            {
                "role": "user",
                "content": """Patient : Homme, 35 ans, region Dakar
Temperature : 39.5 C
Diagnostic du modele : paludisme (probabilite 72%)
Explique ce resultat au patient."""
            }
        ],
        max_tokens=200,
        temperature=temp
    )
    print(f"\n--- temperature={temp} ---")
    print(response_temp.choices[0].message.content)