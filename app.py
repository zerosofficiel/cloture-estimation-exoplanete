import streamlit as st
from urllib.parse import quote

# -----------------------------
# CONFIGURATION DE LA PAGE
# -----------------------------
st.set_page_config(
    page_title="Exo Planete Groupe | Estimation Clôture",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# CSS SIMPLIFIÉ ET CORRIGÉ - BARRE DE PROGRESSION SUPPRIMÉE
# -----------------------------
st.markdown("""
<style>
    /* Reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* CONTENT SECTIONS */
    .content-section {
        padding: 25px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 30px;
        border-left: 4px solid #1a73e8;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from { 
            opacity: 0;
            transform: translateY(20px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* RESPONSIVE */
    @media (max-width: 768px) {
        .main-container {
            padding: 10px;
        }
        
        .content-section {
            padding: 20px 15px;
            margin-bottom: 20px;
        }
        
        h1 {
            font-size: 1.7rem !important;
        }
        
        h2 {
            font-size: 1.4rem !important;
        }
    }
    
    /* MESSAGES - CORRIGÉ (texte lisible) */
    .message-box {
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid;
    }
    
    .message-info {
        background: #e8f4fd !important;
        border-left-color: #1a73e8 !important;
        color: #1a446b !important;
    }
    
    .message-warning {
        background: #fff3cd !important;
        border-left-color: #ffc107 !important;
        color: #856404 !important;
    }
    
    .message-success {
        background: #d4edda !important;
        border-left-color: #28a745 !important;
        color: #155724 !important;
    }
    
    /* Force le texte en noir dans les messages */
    .message-box strong {
        color: #000 !important;
    }
    
    .message-box p, .message-box div {
        color: #000 !important;
    }
    
    /* BOUTONS */
    .btn-primary {
        background: #1a73e8;
        color: white;
        border: none;
        padding: 14px 28px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        margin-top: 20px;
    }
    
    .btn-primary:hover {
        background: #0d5bb5;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
    }
    
    .btn-secondary {
        background: #f5f5f5;
        color: #333;
        border: 1px solid #ddd;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 15px;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
    }
    
    .btn-secondary:hover {
        background: #e0e0e0;
    }
    
    /* ESTIMATION BOX */
    .estimation-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 30px;
        margin: 30px 0;
        border: 2px solid #1a73e8;
        text-align: center;
    }
    
    /* WHATSAPP BUTTON */
    .btn-whatsapp {
        background: #25D366;
        color: white;
        padding: 18px 40px;
        font-size: 18px;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        max-width: 400px;
        display: block;
        margin: 30px auto;
        text-align: center;
        text-decoration: none;
    }
    
    .btn-whatsapp:hover {
        background: #1da851;
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4);
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
# FONCTIONS - SUPPRIMÉ show_progress_bar()
# -----------------------------
def calculate_estimation():
    """Calcule l'estimation du coût"""
    coeff_localite = COEFF_LOCALITE.get(st.session_state.localite, 1.0)
    coeff_hauteur = COEFF_HAUTEUR.get(st.session_state.hauteur, 1.0)
    coeff_type = TYPES_PARCELLE.get(st.session_state.type_parcelle, 1.0)
    
    return PRIX_BASE_ML * st.session_state.perimetre * coeff_localite * coeff_hauteur * coeff_type

# -----------------------------
# INITIALISATION
# -----------------------------
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

# Initialiser les valeurs
defaults = {
    'parcelle': None,
    'topo': None,
    'localite': "Abomey-Calavi",
    'type_parcelle': "Angle",
    'perimetre': 70,
    'hauteur': "2.0m (standard)",
    'nom': "",
    'telephone': "",
    'email': "",
    'projet': "Maison individuelle"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# APPLICATION PRINCIPALE
# -----------------------------
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# Titre principal
st.markdown("<h1 style='text-align: center; color: #1a73e8; margin-bottom: 10px;'>Estimation de Clôture</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; margin-bottom: 30px;'>Obtenez une estimation précise en 3 étapes simples</p>", unsafe_allow_html=True)

# -----------------------------
# ÉTAPE 1: VOTRE PROJET
# -----------------------------
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.markdown("<h2 style='color: #1a73e8; margin-bottom: 20px;'>🎯 Étape 1: Votre projet</h2>", unsafe_allow_html=True)

st.markdown("<h3 style='margin-bottom: 15px;'>1. Votre situation</h3>", unsafe_allow_html=True)
cols = st.columns(3)
options_parcelle = [
    ("Terrain disponible", "Je possède le terrain", "possede"),
    ("En recherche", "Je cherche un terrain", "recherche"),
    ("Projet futur", "Planification à venir", "futur")
]

for i, (title, desc, value) in enumerate(options_parcelle):
    with cols[i]:
        is_selected = st.session_state.parcelle == value
        if st.button(f"**{title}**\n\n{desc}", 
                    key=f"parcelle_{i}",
                    type="primary" if is_selected else "secondary",
                    use_container_width=True):
            st.session_state.parcelle = value
            st.rerun()

if st.session_state.parcelle:
    st.markdown("<h3 style='margin-top: 25px; margin-bottom: 15px;'>2. Levé topographique</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    options_topo = [
        ("Disponible", "J'ai le document", "oui"),
        ("À réaliser", "Je souhaite le faire", "a_faire"),
        ("Non", "Je n'ai pas", "non")
    ]
    
    for i, (title, desc, value) in enumerate(options_topo):
        with cols[i]:
            is_selected = st.session_state.topo == value
            if st.button(f"**{title}**\n\n{desc}", 
                        key=f"topo_{i}",
                        type="primary" if is_selected else "secondary",
                        use_container_width=True):
                st.session_state.topo = value
                st.rerun()

if st.session_state.parcelle and (st.session_state.topo or st.session_state.parcelle != "possede"):
    st.divider()
    
    # Récapitulatif étape 1
    col1, col2 = st.columns(2)
    with col1:
        parcelle_text = {"possede": "Terrain disponible", "recherche": "En recherche", "futur": "Projet futur"}.get(st.session_state.parcelle, "-")
        st.metric("📌 Parcelle", parcelle_text)
    
    with col2:
        if st.session_state.topo:
            topo_text = {"oui": "Levé disponible", "a_faire": "À réaliser", "non": "Non disponible"}.get(st.session_state.topo, "-")
            st.metric("📐 Levé topo", topo_text)
    
    # Bouton pour passer à l'étape 2
    if st.button("**Continuer vers la simulation →**", 
                 type="primary", 
                 use_container_width=True,
                 key="btn_step1_continue"):
        st.session_state.current_step = 2
        st.rerun()

elif st.session_state.parcelle:
    st.markdown("<div class='message-box message-info'><strong>Veuillez répondre à la deuxième question pour continuer</strong></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# ÉTAPE 2: SIMULATION
# -----------------------------
if st.session_state.current_step >= 2:
    st.markdown("<div class='content-section'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #1a73e8; margin-bottom: 20px;'>🧮 Étape 2: Simulation</h2>", unsafe_allow_html=True)
    
    # Bouton pour revenir à l'étape 1
    if st.button("← Retour à l'étape 1", 
                 key="btn_back_to_step1",
                 use_container_width=True,
                 type="secondary"):
        st.session_state.current_step = 1
        st.rerun()
    
    cols = st.columns(2)
    
    with cols[0]:
        st.markdown("<h3 style='margin-bottom: 10px;'>Localisation</h3>", unsafe_allow_html=True)
        localites = ["Abomey-Calavi", "Cotonou", "Dassa-Zoumè", "Sèmè-Podji", "Ouidah", "Allada", "Porto-Novo", "Parakou", "Bohicon", "Abomey"]
        st.session_state.localite = st.selectbox(
            "Sélectionnez votre ville",
            localites,
            index=0,
            key="localite_select",
            label_visibility="collapsed"
        )
        
        st.markdown("<h3 style='margin-top: 25px; margin-bottom: 10px;'>Type de parcelle</h3>", unsafe_allow_html=True)
        st.session_state.type_parcelle = st.selectbox(
            "Forme de votre terrain",
            list(TYPES_PARCELLE.keys()),
            index=0,
            key="type_parcelle_select",
            label_visibility="collapsed"
        )
    
    with cols[1]:
        st.markdown("<h3 style='margin-bottom: 10px;'>Périmètre de la parcelle (ml)</h3>", unsafe_allow_html=True)
        
        # SEULEMENT le widget natif Streamlit
        st.session_state.perimetre = st.number_input(
            "Périmètre",
            min_value=10,
            max_value=500,
            value=st.session_state.perimetre,
            step=1,
            key="perimetre_input",
            label_visibility="collapsed"
        )
        
        st.markdown(f"<p style='text-align: center; color: #666; margin-top: 10px;'><strong>Périmètre sélectionné :</strong> {st.session_state.perimetre} ml</p>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='margin-top: 25px; margin-bottom: 10px;'>Hauteur de clôture</h3>", unsafe_allow_html=True)
        
        # Widget pour la hauteur
        hauteur_options = list(COEFF_HAUTEUR.keys())
        current_index = hauteur_options.index(st.session_state.hauteur) if st.session_state.hauteur in hauteur_options else 1
        
        col_h_minus, col_h_middle, col_h_plus = st.columns([1, 2, 1])
        
        with col_h_minus:
            if st.button("⬅️", key="hauteur_minus", use_container_width=True):
                if current_index > 0:
                    st.session_state.hauteur = hauteur_options[current_index - 1]
                st.rerun()
        
        with col_h_middle:
            st.markdown(f"""
            <div style='
                background: white;
                border: 2px solid #1a73e8;
                border-radius: 8px;
                padding: 12px;
                text-align: center;
                font-size: 16px;
                font-weight: bold;
                color: #1a73e8;
                margin: 0 auto;
            '>
                {st.session_state.hauteur}
            </div>
            """, unsafe_allow_html=True)
        
        with col_h_plus:
            if st.button("➡️", key="hauteur_plus", use_container_width=True):
                if current_index < len(hauteur_options) - 1:
                    st.session_state.hauteur = hauteur_options[current_index + 1]
                st.rerun()
    
    # CALCUL ET AFFICHAGE DE L'ESTIMATION
    st.session_state.estimation = calculate_estimation()
    
    st.divider()
    st.markdown(f"""
    <div class='estimation-card'>
        <h2 style='color: #666; margin: 0;'>Estimation du coût</h2>
        <h1 style='color: #1a73e8; margin: 15px 0; font-size: 2.8rem;'>{st.session_state.estimation:,.0f} FCFA</h1>
        <p style='color: #666; margin: 5px 0;'>Pour {st.session_state.perimetre} ml • {st.session_state.hauteur} • {st.session_state.localite}</p>
        <p style='color: #888; font-size: 0.9rem; margin-top: 10px;'>Inclut fondations, murs, chaînage, enduit • TTC</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Messages informatifs - CORRIGÉS (texte noir lisible)
    st.markdown("""
    <div class='message-box message-warning'>
        <strong>📋 Devis détaillé disponible (service payant)</strong><br><br>
        Pour un devis avec quantités exactes de tous les matériaux (ciment, fer, sable, briques, etc.),<br>
        contactez-nous après cette estimation.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='message-box message-info'>
        <strong>⚠️ Terrain complexe ?</strong><br><br>
        Si votre terrain est en pente ou de forme irrégulière,<br>
        contactez-nous directement pour une étude personnalisée.
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton pour passer à l'étape 3
    if st.button("**Obtenir mon estimation détaillée →**", 
                 type="primary", 
                 use_container_width=True,
                 key="btn_step2_continue"):
        st.session_state.current_step = 3
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# ÉTAPE 3: CONTACT
# -----------------------------
if st.session_state.current_step == 3:
    st.markdown("<div class='content-section'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #1a73e8; margin-bottom: 20px;'>📋 Étape 3: Contact</h2>", unsafe_allow_html=True)
    
    # Bouton pour revenir à l'étape 2
    if st.button("← Retour à la simulation", 
                 key="btn_back_to_step2",
                 use_container_width=True,
                 type="secondary"):
        st.session_state.current_step = 2
        st.rerun()
    
    # RÉCAPITULATIF COMPLET
    st.markdown("<h3 style='margin-bottom: 20px;'>Récapitulatif de votre projet</h3>", unsafe_allow_html=True)
    
    parcelle_text = {
        "possede": "Terrain disponible",
        "recherche": "En recherche de terrain", 
        "futur": "Projet futur"
    }.get(st.session_state.parcelle, "Non spécifié")
    
    topo_text = {
        "oui": "Levé disponible",
        "a_faire": "À réaliser",
        "non": "Non disponible"
    }.get(st.session_state.topo, "Non spécifié")
    
    # Métriques
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📌 Parcelle", parcelle_text)
        st.metric("📐 Levé topo", topo_text)
    
    with col2:
        st.metric("📍 Localité", st.session_state.localite)
        st.metric("🔺 Type parcelle", st.session_state.type_parcelle)
    
    with col3:
        st.metric("📏 Périmètre", f"{st.session_state.perimetre} ml")
        st.metric("📐 Hauteur", st.session_state.hauteur)
    
    # ESTIMATION FINALE
    st.markdown(f"""
    <div style='background: #f0f7ff; border-radius: 12px; padding: 25px; margin: 30px 0; border: 2px solid #1a73e8; text-align: center;'>
        <h2 style='color: #1a73e8; margin: 0;'>ESTIMATION FINALE</h2>
        <h1 style='color: #1a73e8; margin: 15px 0; font-size: 3rem;'>{st.session_state.estimation:,.0f} FCFA</h1>
        <p style='color: #666; margin: 5px 0;'>Basé sur DQE validé • Estimation envoyée sous 24h</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FORMULAIRE DE CONTACT
    st.markdown("<h3 style='margin-bottom: 20px;'>Vos coordonnées</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; margin-bottom: 20px;'>Remplissez vos informations pour recevoir l'estimation détaillée sur WhatsApp</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.nom = st.text_input(
            "Votre nom complet *",
            value=st.session_state.nom,
            placeholder="Ex: Jean Dupont",
            key="nom_input"
        )
    
    with col2:
        st.session_state.telephone = st.text_input(
            "Votre numéro WhatsApp *",
            value=st.session_state.telephone,
            placeholder="Ex: 01 23 45 67 89",
            key="telephone_input"
        )
    
    st.session_state.email = st.text_input(
        "Votre email (facultatif)",
        value=st.session_state.email,
        placeholder="email@exemple.com",
        key="email_input"
    )
    
    st.session_state.projet = st.selectbox(
        "Avez-vous un projet de construction ?",
        ["Maison individuelle", "Immeuble", "Commerce", "Autre projet", "Pas de projet immédiat"],
        index=0,
        key="projet_select"
    )
    
    # Validation et bouton WhatsApp
    if st.session_state.nom and st.session_state.telephone:
        st.markdown("<div class='message-box message-success'><strong>✅ Toutes les informations sont complètes. Cliquez ci-dessous pour recevoir votre estimation.</strong></div>", unsafe_allow_html=True)
        
        # Préparation du message WhatsApp
        message = f"""*ESTIMATION CLÔTURE - EXO PLANETE GROUPE*

*Informations client*
Nom : {st.session_state.nom}
Téléphone : {st.session_state.telephone}
Email : {st.session_state.email if st.session_state.email else 'Non fourni'}

*Critères du projet*
Parcelle : {parcelle_text}
Levé topo : {topo_text}
Localité : {st.session_state.localite}
Type parcelle : {st.session_state.type_parcelle}
Périmètre : {st.session_state.perimetre} ml
Hauteur : {st.session_state.hauteur}
Projet futur : {st.session_state.projet}

*Estimation*
Coût estimé : {st.session_state.estimation:,.0f} FCFA

*Demande*
{'Intéressé par devis détaillé des matériaux' if st.session_state.projet != 'Pas de projet immédiat' else 'Information seulement'}

--- 
Envoyé via l'outil d'estimation en ligne"""

        whatsapp_url = "https://wa.me/2290166815278?text=" + quote(message)
        
        # Bouton WhatsApp
        st.markdown(f"""
        <a href='{whatsapp_url}' target='_blank' class='btn-whatsapp'>
            📲 RECEVOIR MON ESTIMATION SUR WHATSAPP
        </a>
        <p style='text-align: center; color: #666; margin-top: 10px; font-size: 0.9rem;'>
        Vous serez redirigé vers WhatsApp. Réponse sous 24h.
        </p>
        """, unsafe_allow_html=True)
        
        # Bouton pour recommencer
        st.divider()
        if st.button("🔄 Faire une nouvelle estimation", 
                     use_container_width=True,
                     type="secondary",
                     key="btn_restart"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    else:
        st.markdown("<div class='message-box message-warning'><strong>Veuillez remplir votre nom et numéro de téléphone pour recevoir votre estimation.</strong></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # Fermer main-container

# -----------------------------
# SCRIPT POUR SCROLL AUTOMATIQUE
# -----------------------------
st.markdown("""
<script>
// Fonction pour scroller vers le bas de la page
function scrollToBottom() {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
}

// Fonction pour scroller vers le contenu actif
function scrollToActiveContent() {
    const activeSections = document.querySelectorAll('.content-section');
    if (activeSections.length > 0) {
        const lastSection = activeSections[activeSections.length - 1];
        lastSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Observer les changements du DOM
const observer = new MutationObserver(function(mutations) {
    for (let mutation of mutations) {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            // Attendre un peu que Streamlit termine le rendu
            setTimeout(scrollToActiveContent, 500);
            break;
        }
    }
});

// Démarrer l'observation
observer.observe(document.body, {
    childList: true,
    subtree: true
});

// Scroll initial
setTimeout(scrollToActiveContent, 1000);
</script>

""", unsafe_allow_html=True)
