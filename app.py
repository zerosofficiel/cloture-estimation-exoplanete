import streamlit as st
from urllib.parse import quote

# -----------------------------
# CONFIGURATION DE LA PAGE
# -----------------------------
st.set_page_config(
    page_title="Architect Pro | Estimation Clôture",
    page_icon="🏗️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# CSS SIMPLE
# -----------------------------
st.markdown("""
<style>
    .progress-container {
        display: flex;
        justify-content: space-between;
        margin: 30px auto 40px auto;
        position: relative;
        max-width: 600px;
    }
    
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        z-index: 2;
        position: relative;
        flex: 1;
    }
    
    .step-circle {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #f0f0f0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 500;
        color: #666;
        margin-bottom: 8px;
        border: 2px solid #ddd;
        font-size: 14px;
    }
    
    .step-circle.active {
        background: #1a73e8;
        color: white;
        border-color: #1a73e8;
    }
    
    .step-label {
        font-size: 12px;
        color: #666;
        font-weight: 500;
        text-align: center;
    }
    
    .step-label.active {
        color: #1a73e8;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DONNÉES
# -----------------------------
PRIX_BASE_ML = 51107

COEFF_LOCALITE = {"Cotonou": 1.05}
COEFF_HAUTEUR = {
    "1.8m": 0.95,
    "2.0m (standard)": 1.00,
    "2.5m": 1.15,
    "3.0m": 1.35
}

TYPES_PARCELLE = {
    "Angle": 1.10,
    "Entre 3 parcelles": 1.15
}

# -----------------------------
# FONCTIONS
# -----------------------------
def update_step(step):
    st.session_state.etape = step
    # Scroll en haut
    st.markdown("<div id='top'></div>", unsafe_allow_html=True)

def show_progress():
    steps = ["Votre projet", "Simulation", "Contact", "Confirmation"]
    icons = ["🎯", "🧮", "📋", "✅"]
    
    html = '<div class="progress-container">'
    
    for i in range(len(steps)):
        active = "active" if (i + 1) == st.session_state.etape else ""
        display_icon = icons[i] if (i + 1) == st.session_state.etape else str(i + 1)
        html += f'<div class="step"><div class="step-circle {active}">{display_icon}</div><div class="step-label {active}">{steps[i]}</div></div>'
    
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# -----------------------------
# INITIALISATION
# -----------------------------
if 'etape' not in st.session_state:
    st.session_state.etape = 1

defaults = {
    'parcelle': None,
    'topo': None,
    'budget': None,
    'localite': "Abomey-Calavi",
    'type_parcelle': "Angle",
    'longueur': 20,
    'largeur': 15,
    'hauteur': "2.0m (standard)",
    'estimation': 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# ÉTAPE 1: QUALIFICATION
# -----------------------------
if st.session_state.etape == 1:
    st.markdown("<h1 style='text-align: center; color: #1a73e8;'>Estimation de clôture</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; margin-bottom: 30px;'>3 questions pour votre estimation</p>", unsafe_allow_html=True)
    
    show_progress()
    
    st.subheader("1. Votre situation")
    
    cols = st.columns(3)
    options = [
        ("Terrain disponible", "Je possède le terrain", "possede"),
        ("En recherche", "Je cherche un terrain", "recherche"),
        ("Projet futur", "Planification à venir", "futur")
    ]
    
    for i, (title, desc, value) in enumerate(options):
        with cols[i]:
            if st.button(f"**{title}**\n\n{desc}", key=f"parcelle_{i}", use_container_width=True):
                st.session_state.parcelle = value
                st.rerun()
    
    if st.session_state.parcelle == "possede":
        st.subheader("2. Levé topographique")
        
        cols = st.columns(3)
        options = [
            ("Disponible", "J'ai le document", "oui"),
            ("À réaliser", "Je peux le faire", "a_faire"),
            ("Non", "Je n'ai pas", "non")
        ]
        
        for i, (title, desc, value) in enumerate(options):
            with cols[i]:
                if st.button(f"**{title}**\n\n{desc}", key=f"topo_{i}", use_container_width=True):
                    st.session_state.topo = value
                    st.rerun()
    
    if st.session_state.parcelle and (st.session_state.topo or st.session_state.parcelle != "possede"):
        st.subheader("3. Budget approximatif")
        
        budgets = ["500k - 1M", "1M - 3M", "3M - 5M", "5M - 10M", "10M +"]
        cols = st.columns(5)
        
        for i, budget in enumerate(budgets):
            with cols[i]:
                if st.button(budget, key=f"budget_{i}", use_container_width=True):
                    st.session_state.budget = budget
                    st.rerun()
    
    if st.session_state.parcelle:
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            parcelle_text = {"possede": "Terrain", "recherche": "En recherche", "futur": "Projet"}.get(st.session_state.parcelle, "-")
            st.metric("Parcelle", parcelle_text)
        
        with col2:
            if st.session_state.topo:
                topo_text = {"oui": "Levé OK", "a_faire": "À faire", "non": "Pas de levé"}.get(st.session_state.topo, "-")
                st.metric("Levé topo", topo_text)
        
        with col3:
            if st.session_state.budget:
                st.metric("Budget", st.session_state.budget)
    
    if st.session_state.parcelle and (st.session_state.topo or st.session_state.parcelle != "possede") and st.session_state.budget:
        st.divider()
        if st.button("**Continuer →**", type="primary", use_container_width=True):
            update_step(2)
            st.rerun()
    elif st.session_state.parcelle:
        st.info("Répondez à toutes les questions")

# -----------------------------
# ÉTAPE 2: SIMULATION
# -----------------------------
elif st.session_state.etape == 2:
    st.markdown("<h1 style='text-align: center; color: #1a73e8;'>Configuration</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; margin-bottom: 30px;'>Détails de votre projet</p>", unsafe_allow_html=True)
    
    show_progress()
    
    if st.button("← Retour"):
        update_step(1)
        st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        localites = ["Abomey-Calavi", "Cotonou", "Dassa-Zoumè", "Sèmè-Podji", "Ouidah", "Allada", "Porto-Novo", "Parakou", "Bohicon", "Abomey"]
        st.session_state.localite = st.selectbox("Localité", localites, index=0)
        
        st.session_state.type_parcelle = st.selectbox("Type de parcelle", list(TYPES_PARCELLE.keys()), index=0)
    
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.longueur = st.number_input("Longueur (m)", min_value=5, value=20, step=1)
        with col_b:
            st.session_state.largeur = st.number_input("Largeur (m)", min_value=5, value=15, step=1)
        
        perimetre = (st.session_state.longueur + st.session_state.largeur) * 2
        st.info(f"**Périmètre :** {perimetre} ml")
        
        st.session_state.hauteur = st.select_slider("Hauteur", options=list(COEFF_HAUTEUR.keys()), value="2.0m (standard)")
    
    # CALCUL SIMPLE
    coeff_localite = COEFF_LOCALITE.get(st.session_state.localite, 1.0)
    coeff_hauteur = COEFF_HAUTEUR.get(st.session_state.hauteur, 1.0)
    coeff_type = TYPES_PARCELLE.get(st.session_state.type_parcelle, 1.0)
    
    st.session_state.estimation = PRIX_BASE_ML * perimetre * coeff_localite * coeff_hauteur * coeff_type
    
    # AFFICHAGE
    st.divider()
    st.markdown(f"""
    <div style='background: #f8f9fa; border-radius: 12px; padding: 25px; margin: 20px 0; border: 1px solid #e0e0e0; text-align: center;'>
        <h2 style='color: #666; margin: 0; font-weight: 500;'>Estimation</h2>
        <h1 style='color: #1a73e8; margin: 10px 0; font-size: 2.2rem; font-weight: 700;'>{st.session_state.estimation:,.0f} FCFA</h1>
        <p style='color: #666; margin: 5px 0;'>Pour {perimetre} ml • Clé en main</p>
    </div>
    """, unsafe_allow_html=True)
    
    # MESSAGE COURT POUR DÉTAILS
    st.warning("""
    **📋 Devis détaillé disponible (payant)**
    
    Pour un devis avec quantités exactes de matériaux (ciment, fer, sable, gravier) 
    et planning détaillé, contactez-nous après cette estimation.
    """)
    
    st.info("""
    **⚠️ Terrain complexe ?** (pente, forme irrégulière, accès difficile)
    Contactez-nous directement pour une étude personnalisée.
    """)
    
    # NAVIGATION
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Retour", use_container_width=True):
            update_step(1)
            st.rerun()
    
    with col2:
        if st.button("**Obtenir estimation →**", type="primary", use_container_width=True):
            update_step(3)
            st.rerun()

# -----------------------------
# ÉTAPE 3: CONTACT
# -----------------------------
elif st.session_state.etape == 3:
    st.markdown("<h1 style='text-align: center; color: #1a73e8;'>Votre estimation</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; margin-bottom: 30px;'>Recevez votre estimation par WhatsApp</p>", unsafe_allow_html=True)
    
    show_progress()
    
    if st.button("← Retour"):
        update_step(2)
        st.rerun()
    
    perimetre = (st.session_state.longueur + st.session_state.largeur) * 2
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Localité", st.session_state.localite)
        st.metric("Type parcelle", st.session_state.type_parcelle)
    with col2:
        st.metric("Hauteur", st.session_state.hauteur)
        st.metric("Estimation", f"{st.session_state.estimation:,.0f} FCFA")
    
    # MESSAGE COURT
    st.warning("""
    **💎 Devis détaillé payant**
    
    Cette estimation est gratuite. Pour un devis avec :
    - Quantités exactes de tous les matériaux
    - Planning jour par jour
    - Budget détaillé par poste
    
    Contactez-nous après réception.
    """)
    
    # FORMULAIRE
    st.divider()
    st.subheader("📝 Coordonnées")
    
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom*", placeholder="Votre nom")
    with col2:
        telephone = st.text_input("WhatsApp*", placeholder="Votre numéro")
    
    email = st.text_input("Email (facultatif)", placeholder="email@exemple.com")
    
    projet = st.selectbox(
        "Projet futur ?",
        ["Maison", "Immeuble", "Commerce", "Autre", "Pas de projet"]
    )
    
    # WHATSAPP
    if nom and telephone:
        st.success("✅ Prêt à envoyer")
        
        message = f"""*ESTIMATION CLÔTURE*

Client : {nom}
Téléphone : {telephone}
Email : {email if email else 'Non fourni'}

Localité : {st.session_state.localite}
Périmètre : {perimetre} ml
Type : {st.session_state.type_parcelle}
Hauteur : {st.session_state.hauteur}
Estimation : {st.session_state.estimation:,.0f} FCFA

Projet futur : {projet}

Demande : Estimation gratuite
Devis détaillé : Disponible en option payante"""

        whatsapp_url = "https://wa.me/2290167655962?text=" + quote(message)
        
        st.markdown(f"""
        <div style='text-align: center; margin: 30px 0;'>
            <a href='{whatsapp_url}' target='_blank'>
                <button style='
                    background: #25D366;
                    color: white;
                    padding: 15px 40px;
                    font-size: 16px;
                    font-weight: 600;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                '>
                    📲 Recevoir sur WhatsApp
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("**Voir confirmation →**", type="secondary", use_container_width=True):
            update_step(4)
            st.rerun()
    else:
        st.warning("Remplissez nom et téléphone")

# -----------------------------
# ÉTAPE 4: CONFIRMATION
# -----------------------------
elif st.session_state.etape == 4:
    st.markdown("<h1 style='text-align: center; color: #1a73e8;'>✅ Envoyé</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; margin-bottom: 30px;'>Votre demande est transmise</p>", unsafe_allow_html=True)
    
    show_progress()
    
    st.markdown("<div style='text-align: center; font-size: 60px; color: #1a73e8; margin: 20px 0;'>✓</div>", unsafe_allow_html=True)
    
    st.subheader("Prochaines étapes")
    
    st.markdown("""
    1. **Réception WhatsApp** - Sous 24h
    2. **Échange avec expert** - Discussion de votre projet
    3. **Option devis détaillé** - Si besoin (payant)
    4. **Suivi personnalisé** - Pour votre projet
    """)
    
    st.info("**📞 Contact :** 01 67 65 59 62")
    
    st.warning("""
    **Rappel :** L'estimation est gratuite.
    Pour un devis détaillé avec quantités exactes de matériaux,
    discutez-en avec notre expert (service payant).
    """)
    
    if st.button("🏠 Nouvelle simulation", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()