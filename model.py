import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


p_zemlja = 100
p_hisa = 90

mesecni_stroski = 1.5
p_dnevni_najem = 0.25

št_hiš = 8

rast_vr_zemlje = 0.03
amortizacijski_faktor = 0.9

delez_davka_na_dobicek = 0.35
delež_nepredvidljivih_stroškov_na_hiško = 1.1

pričakovano_št_dni_v_najemu_na_leto = 100

prič_om = 0.02


def stroški_čiščenja(št_dni, št_hiš, pričakovano_št_dni_v_najemu_na_leto):
    št_mesecev = št_dni / 30.5
    št_let = št_mesecev / 12

    faktor_zasedenosti = pričakovano_št_dni_v_najemu_na_leto / 365

    stroški = št_hiš * št_dni * faktor_zasedenosti * 0.05

    return stroški


def odhodki_po_času(št_dni, p_zemlja, p_hiša, št_hiš, mesecni_stroski, delež_nepredvidljivih_stroškov_na_hiško):
    """predpostavlja ničelno om"""
    št_mesecev = št_dni / 30.5
    št_let = št_mesecev / 12
    
    vložek = p_zemlja + št_hiš * p_hiša * delež_nepredvidljivih_stroškov_na_hiško + mesecni_stroski * št_mesecev 

    return vložek



def prihodki_po_času(št_dni, št_hiš, p_dnevni_najem):
    """predpostavlja ničelno om"""
    št_mesecev = št_dni / 30.5
    št_let = št_mesecev / 12

    faktor_zasedenosti = pričakovano_št_dni_v_najemu_na_leto / 365

    prihodki = št_hiš * p_dnevni_najem * št_dni * faktor_zasedenosti * (1 - delez_davka_na_dobicek)

    return prihodki


def vrednost_investicije(p_hiša, p_zemlja, št_hiš, amortizacijski_faktor, rast_vr_zemlje, št_dni):
    #vrednost
    št_mesecev = št_dni / 30.5
    št_let = št_mesecev / 12
    vrednost_hiške = p_hiša * amortizacijski_faktor ** št_let
    vrednost_zemlje = p_zemlja * (1+rast_vr_zemlje)**št_let

    vrednost = št_hiš * vrednost_hiške + vrednost_zemlje

    return vrednost


def dobiček_po_času(št_dni, p_zemlja, p_hiša, št_hiš, mesecni_stroski, p_dnevni_najem, amortizacijski_faktor, rast_vr_zemlje, delež_nepredvidljivih_stroškov_na_hiško, delez_davka_na_dobicek):
    št_mesecev = št_dni / 30.5
    št_let = št_mesecev / 12

    vložek = odhodki_po_času(št_dni, p_zemlja, p_hiša, št_hiš, mesecni_stroski, delež_nepredvidljivih_stroškov_na_hiško)
    vrednost = vrednost_investicije(p_hiša, p_zemlja, št_hiš, amortizacijski_faktor, rast_vr_zemlje, št_dni)
    prihodki = prihodki_po_času(št_dni, št_hiš, p_dnevni_najem)

    dobiček = (prihodki - vložek + vrednost) * (1 - delez_davka_na_dobicek)

    return dobiček


#print(odhodki_po_času(0, p_zemlja, p_hisa, št_hiš, mesecni_stroski, delež_nepredvidljivih_stroškov_na_hiško))

#print(prihodki_po_času(0, št_hiš, p_dnevni_najem))




# Vaše funkcije (odhodki_po_času, prihodki_po_času, etc.) tukaj


def plot_data(št_let, p_zemlja, p_hiša, št_hiš, mesecni_stroski, p_dnevni_najem, amortizacijski_faktor, rast_vr_zemlje, delež_nepredvidljivih_stroškov_na_hiško, delez_davka_na_dobicek, pričakovano_št_dni_v_najemu_na_leto):
    št_dni = št_let * 365
    dni = np.arange(1, št_dni + 1)

    # Izračuni za vsak dan
    vložek = [odhodki_po_času(dan, p_zemlja, p_hiša, št_hiš, mesecni_stroski, delež_nepredvidljivih_stroškov_na_hiško) for dan in dni]
    prihodki = [prihodki_po_času(dan, št_hiš, p_dnevni_najem) for dan in dni]
    vrednost = [vrednost_investicije(p_hiša, p_zemlja, št_hiš, amortizacijski_faktor, rast_vr_zemlje, dan) for dan in dni]
    dobiček = [dobiček_po_času(dan, p_zemlja, p_hiša, št_hiš, mesecni_stroski, p_dnevni_najem, amortizacijski_faktor, rast_vr_zemlje, delež_nepredvidljivih_stroškov_na_hiško, delez_davka_na_dobicek) for dan in dni]

    # Create a figure and axes object
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting using day numbers
    ax.plot(dni, vložek, label='Vložek')
    ax.plot(dni, prihodki, label='Prihodki')
    ax.plot(dni, vrednost, label='Vrednost')
    ax.plot(dni, dobiček, label='Dobiček')

    # Set labels and title
    ax.set_xlabel('Leto')
    ax.set_ylabel('Vrednosti')
    ax.set_title('Graf investicije skozi čas')
    ax.legend()

    # Adjust x-axis to show years
    year_ticks = np.arange(365, št_dni + 1, 365)
    ax.set_xticks(year_ticks)
    ax.set_xticklabels(range(1, št_let + 1))
    ax.grid(True)

    # Pass the figure to st.pyplot()
    st.pyplot(fig)


st.title('Investicijski model')

# Drsnik za število dni
#št_dni = st.sidebar.slider('Število dni', min_value=1, max_value=365*30, value=365*10)
št_let = st.sidebar.slider('Število let', min_value=1, max_value=30, value=10)
p_zemlja = st.sidebar.slider('Cena zemlje', min_value=50.0, max_value=200.0, value=100.0)
p_hiša = st.sidebar.slider('Cena hiše', min_value=50.0, max_value=200.0, value=90.0)
mesecni_stroski = st.sidebar.slider('Mesečni stroški', min_value=0.0, max_value=10.0, value=1.5)
p_dnevni_najem = st.sidebar.slider('Dnevni najem', min_value=0.1, max_value=1.0, value=0.25)
št_hiš = st.sidebar.slider('Število hiš', min_value=1, max_value=20, value=8)
rast_vr_zemlje = st.sidebar.slider('Rast vrednosti zemlje', min_value=0.0, max_value=0.1, value=0.03)
amortizacijski_faktor = st.sidebar.slider('Amortizacijski faktor', min_value=0.0, max_value=1.0, value=0.9)
delez_davka_na_dobicek = st.sidebar.slider('Delež davka na dobiček', min_value=0.0, max_value=0.5, value=0.35)
delež_nepredvidljivih_stroškov_na_hiško = st.sidebar.slider('Delež nepredvidljivih stroškov na hiško', min_value=1.0, max_value=2.0, value=1.1)
pričakovano_št_dni_v_najemu_na_leto = st.sidebar.slider('Pričakovano število dni v najemu na leto', min_value=0, max_value=365, value=100)


#if st.button('Izračunaj dobiček'):
#    dobiček = dobiček_po_času(št_let, p_zemlja, p_hiša, št_hiš, mesecni_stroski, p_dnevni_najem, amortizacijski_faktor, rast_vr_zemlje, delež_nepredvidljivih_stroškov_na_hiško, delez_davka_na_dobicek, pričakovano_št_dni_v_najemu_na_leto)
#    st.write(f'Dobiček po {št_let} letih: {dobiček}')

# Klic funkcije plot_data ob spremembi kateregakoli drsnika
plot_data(št_let, p_zemlja, p_hiša, št_hiš, mesecni_stroski, p_dnevni_najem, amortizacijski_faktor, rast_vr_zemlje, delež_nepredvidljivih_stroškov_na_hiško, delez_davka_na_dobicek, pričakovano_št_dni_v_najemu_na_leto)


