import streamlit as st
from fpdf import FPDF
import os
from datetime import date

# ---------------- CONFIGURATION ----------------
st.set_page_config(page_title="AdamCV", layout="centered")

os.makedirs("generated", exist_ok=True)
os.makedirs("logos", exist_ok=True)

st.title("AdamCV")
st.markdown("Générateur de CV administratif sénégalais – format officiel")

# ---------------- CLASSE PDF ----------------
class PDF(FPDF):
    def header(self):
        self.set_auto_page_break(auto=True, margin=20)

        # Logo discret
        if self.logo:
            self.image(self.logo, 10, 10, 18)

        # Nom
        self.set_xy(35, 12)
        self.set_font("Arial", "B", 15)
        self.cell(0, 8, self.nom.upper(), ln=True)

        # Contact
        self.set_font("Arial", "", 11)
        self.cell(0, 6, f"{self.email} | {self.telephone}", ln=True)

        # Marque AdamCV
        #self.set_font("Arial", "B", 9)
        #self.set_xy(150, 12)
        #self.cell(40, 6, "ADAMCV", align="R")

        self.ln(8)

    def section(self, titre):
        self.set_font("Arial", "B", 12)
        self.cell(0, 7, titre.upper(), ln=True)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)

    def texte(self, txt):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 6, txt)
        self.ln(1)

# ---------------- CV ADMINISTRATIF ----------------
def cv_administratif(pdf, d):
    pdf.section("Etat civil")
    pdf.texte(
        f"Nom : {d['Nom']}\n"
        f"Date de naissance : {d['Date naissance']}\n"
        f"Nationalité : {d['Nationalité']}\n"
        f"Téléphone : {d['Téléphone']}\n"
        f"Email : {d['Email']}"
    )

    pdf.section("Profil")
    pdf.texte(d["Profil"])

    pdf.section("Diplômes et formations")
    pdf.texte(d["Diplômes"])

    pdf.section("Expériences professionnelles")
    pdf.texte(d["Expériences"])

    pdf.section("Compétences")
    pdf.texte(d["Compétences"])

    pdf.section("Langues")
    pdf.texte(d["Langues"])

# ---------------- INTERFACE ----------------
with st.form("form_cv"):
    nom = st.text_input("Nom complet")

    # Date de naissance réaliste
    date_naissance = st.date_input(
        "Date de naissance",
        min_value=date(1950, 1, 1),
        max_value=date.today()
    )

    nationalite = st.text_input("Nationalité")
    email = st.text_input("Email")
    telephone = st.text_input("Téléphone")

    profil = st.text_area("Profil")
    diplomes = st.text_area("Diplômes / Formations")
    experiences = st.text_area("Expériences professionnelles")
    competences = st.text_area("Compétences")
    langues = st.text_area("Langues")

    logo = st.file_uploader("Logo (optionnel)", type=["png", "jpg"])

    valider = st.form_submit_button("Générer le CV officiel")

# ---------------- GÉNÉRATION PDF ----------------
if valider:
    pdf = PDF(format="A4")
    pdf.nom = nom
    pdf.email = email
    pdf.telephone = telephone
    pdf.logo = None

    if logo:
        logo_path = f"logos/{logo.name}"
        with open(logo_path, "wb") as f:
            f.write(logo.getbuffer())
        pdf.logo = logo_path

    pdf.add_page()

    # Données
    donnees = {
        "Nom": nom,
        "Date naissance": date_naissance.strftime("%d/%m/%Y"),
        "Nationalité": nationalite,
        "Email": email,
        "Téléphone": telephone,
        "Profil": profil,
        "Diplômes": diplomes,
        "Expériences": experiences,
        "Compétences": competences,
        "Langues": langues
    }

    # Générer le CV
    cv_administratif(pdf, donnees)

    # ---------------- Enregistrer PDF ----------------
    fichier = f"generated/{nom.replace(' ', '_')}_CV.pdf"
    pdf.output(fichier)

    # Bouton téléchargement
    with open(fichier, "rb") as f:
        st.download_button(
            "Télécharger le CV",
            f,
            file_name=fichier
        )

    st.success("CV administratif généré avec succès")
