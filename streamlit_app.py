import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# ---------------- CONFIGURATION ----------------
st.set_page_config(page_title="AdamCV", layout="centered")

os.makedirs("generated", exist_ok=True)

st.title("AdamCV")
st.markdown("Voici mon générateur de CV")

# ---------------- CLASSE PDF ----------------
class PDF(FPDF):
    def header(self):
        self.set_left_margin(15)
        self.set_right_margin(15)
        self.set_auto_page_break(auto=True, margin=20)

        # Nom
        self.set_xy(40, 12)
        self.set_font("Arial", "B", 16)
        self.cell(0, 8, getattr(self, "nom", "").upper(), ln=True)

        # Contact
        self.set_font("Arial", "", 11)
        self.set_x(40)
        self.cell(0, 6, f"{getattr(self, 'email', '')} | {getattr(self, 'telephone', '')}", ln=True)

        self.ln(10)

    def section(self, titre):
        self.set_font("Arial", "B", 13)
        self.set_x(20)
        self.cell(0, 7, titre.upper(), ln=True)
        self.set_x(20)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(4)

    def texte(self, txt):
        self.set_font("Arial", "", 11)
        self.set_x(20)
        self.multi_cell(0, 6, txt)
        self.ln(4)

# ---------------- CV ADMINISTRATIF ----------------
def cv_administratif(pdf, d):
    pdf.section("État civil")
    pdf.texte(
        f"Nom : {d['Nom']}\n"
        f"Date de naissance : {d['Date naissance']}\n"
        f"Nationalité : {d['Nationalité']}\n"
        f"Téléphone : {d['Téléphone']}\n"
        f"Email : {d['Email']}"
        f"Adresse : {d['Adresse']}"
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
    nationalite = st.text_input("Nationalité")
    email = st.text_input("Email")
    telephone = st.text_input("Téléphone")
    adress = st.text_input("Adresse")

    date_naissance_str = st.text_input("Date de naissance")

    profil = st.text_area("Profil")
    diplomes = st.text_area("Diplômes / Formations")
    experiences = st.text_area("Expériences professionnelles")
    competences = st.text_area("Compétences")
    langues = st.text_area("Langues")

    valider = st.form_submit_button("Creer le CV")

# ---------------- GÉNÉRATION PDF ----------------
if valider:
    pdf = PDF(format="A4")
    pdf.nom = nom or ""
    pdf.email = email or ""
    pdf.telephone = telephone or ""

    pdf.add_page()

    # Gestion de la date arbitraire
    if date_naissance_str:
        try:
            date_naissance = datetime.strptime(date_naissance_str, "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            date_naissance = "Format invalide"
    else:
        date_naissance = "Non renseignée"

    # Données
    donnees = {
        "Nom": nom or "",
        "Date naissance": date_naissance,
        "Nationalité": nationalite or "",
        "Email": email or "",
        "Téléphone": telephone or "",
        "Profil": profil or "",
        "Diplômes": diplomes or "",
        "Expériences": experiences or "",
        "Compétences": competences or "",
        "Langues": langues or ""
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

    st.success("CV généré avec succès")
