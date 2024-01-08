import streamlit as st
import matplotlib.pyplot as plt
import numpy as np



#################STROŠKI#####################
@st.cache_data
def stroški_čiščenja(št_dni, pričakovano_št_dni_v_najemu_na_leto, pogostost_čiščenja, cena_čiščenja, št_hiš=12):
    št_mesecev = št_dni / 30.5
    št_let = št_mesecev / 12

    faktor_zasedenosti = pričakovano_št_dni_v_najemu_na_leto / 365
    št_čiščenj = št_hiš * št_dni * faktor_zasedenosti / pogostost_čiščenja
    stroški = št_čiščenj * cena_čiščenja 

    return stroški

@st.cache_data
def stroški_amortizacije_po_času(št_dni, začetna_inv, amortizacijska_stopnja):
    amortizacija = začetna_inv * amortizacijska_stopnja ** (št_dni/365)
    return amortizacija


def stroški_po_času(št_dni, začetna_inv, amortizacijska_stopnja, pogostost_čiščenja, cena_čiščenja, pričakovano_št_dni_v_najemu_na_leto, p_dnevni_najem, provizija, letni_stroški_vzdrževanja_okolice, letni_ostali_stroški):
    """predpostavlja ničelno om"""
    št_mesecev = št_dni / 30.5

    amortizacija = stroški_amortizacije_po_času(št_dni, začetna_inv, amortizacijska_stopnja)
    čiščenje = stroški_čiščenja(št_dni, pričakovano_št_dni_v_najemu_na_leto, pogostost_čiščenja, cena_čiščenja, št_hiš=12)
    prihodki = prihodki_po_času(št_dni, p_dnevni_najem)
    stroški_provizij = prihodki * provizija

    stroški = amortizacija + čiščenje + stroški_provizij
    return stroški



####################################################

def začetna_investicija(p_zemlja, p_hiša, delež_nepredvidljivih_stroškov_na_hiško, št_hiš=12):
    vložek = p_zemlja + št_hiš * p_hiša * delež_nepredvidljivih_stroškov_na_hiško
    return vložek

@st.cache_data
def prihodki_po_času(št_dni, pričakovano_št_dni_v_najemu_na_leto, p_dnevni_najem, št_hiš=12):
    """predpostavlja ničelno om"""
    št_mesecev = št_dni / 30.5
    št_let = št_mesecev / 12

    faktor_zasedenosti = pričakovano_št_dni_v_najemu_na_leto / 365

    prihodki = št_hiš * p_dnevni_najem * št_dni * faktor_zasedenosti

    return prihodki

def stroški_provizije(prihodki, provizija):
    return prihodki * provizija

def vrednost_investicije(p_hiša, p_zemlja, št_hiš, amortizacijski_faktor, rast_vr_zemlje, št_dni):
    #vrednost
    št_mesecev = št_dni / 30.5
    št_let = št_mesecev / 12
    vrednost_hiške = p_hiša * amortizacijski_faktor ** št_let
    vrednost_zemlje = p_zemlja * (1+rast_vr_zemlje)**št_let

    vrednost = št_hiš * vrednost_hiške + vrednost_zemlje

    return vrednost

@st.cache_data
def dobiček_po_času(stroški, prihodki, delez_davka_na_dobicek):
    dobiček = (prihodki - stroški) * (1 - delez_davka_na_dobicek)

    return dobiček




def plot_data(št_let, skupna_inv, začetna_inv, vrednost_inv, delež_v_podjetju, p_dnevni_najem, delez_davka_na_dobicek, pričakovano_št_dni_v_najemu_na_leto, amortizacijska_stopnja, ):
    št_dni = št_let * 365
    dni = np.arange(1, št_dni + 1)

    vrednost_inv_sez = [vrednost_inv * delež_v_podjetju for dan in dni]
    začetna_inv_sez = [vložek_investitorja for dan in dni]

    # Izračuni za vsak dan
    #začetna_inv0 = začetna_investicija(p_zemlja, p_hiša, št_hiš, delež_nepredvidljivih_stroškov_na_hiško)
    
    stroški = [stroški_po_času(dan, začetna_inv, mesecni_stroski, amortizacijska_stopnja) for dan in dni]
    prihodki = [prihodki_po_času(dan, pričakovano_št_dni_v_najemu_na_leto, p_dnevni_najem) for dan in dni]
    #vrednost = [vrednost_investicije(p_hiša, p_zemlja, št_hiš, amortizacijski_faktor, rast_vr_zemlje, dan) for dan in dni]
    dobiček = [(prihodki[dan-1] - stroški[dan-1] - začetna_inv) * (1 - delez_davka_na_dobicek) for dan in dni]

    # Create a figure and axes object
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting using day numbers
    ax.plot(dni, začetna_inv, label='Začetna investicija')
    ax.plot(dni, stroški, label='Stroški')
    ax.plot(dni, prihodki, label='Prihodki')
    #ax.plot(dni, vrednost, label='Vrednost')
    ax.plot(dni, dobiček, label='Dobiček (po davkih))')

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
#p_zemlja = st.sidebar.slider('Cena zemlje', min_value=50.0, max_value=200.0, value=100.0)
#p_hiša = st.sidebar.slider('Cena hiše', min_value=50.0, max_value=200.0, value=90.0)

skupni_vložek = st.sidebar.slider('Vložek', min_value=0, max_value=3000, value=2100)
vložek_investitorja = st.sidebar.slider('Vložek investitorja', min_value=0, max_value=3000, value=2100)
delež_investitorja = st.sidebar.slider('Delež investitorja', min_value=0.0, max_value=1.0, value=0.12)


#mesecni_stroski = st.sidebar.slider('Mesečni stroški', min_value=0.0, max_value=10.0, value=1.5)
#p_dnevni_najem = st.sidebar.slider('Dnevni najem', min_value=0.1, max_value=1.0, value=0.25)
#št_hiš = st.sidebar.slider('Število hiš', min_value=1, max_value=20, value=12)
#rast_vr_zemlje = st.sidebar.slider('Rast vrednosti zemlje', min_value=0.0, max_value=0.1, value=0.03)
#amortizacijski_faktor = st.sidebar.slider('Amortizacijski faktor', min_value=0.0, max_value=1.0, value=0.9)
amortizacijska_stopnja = st.sidebar.slider('Amortizacijska stopnja', min_value=0.0, max_value=1.0, value=0.05)
delez_davka_na_dobicek = st.sidebar.slider('Delež davka na dobiček', min_value=0.0, max_value=0.5, value=0.30)
#delež_nepredvidljivih_stroškov_na_hiško = st.sidebar.slider('Delež nepredvidljivih stroškov na hiško', min_value=1.0, max_value=2.0, value=1.1)
pričakovano_št_dni_v_najemu_na_leto = st.sidebar.slider('Pričakovano število dni v najemu na leto', min_value=0, max_value=365, value=100)


#if st.button('Izračunaj dobiček'):
#    dobiček = dobiček_po_času(št_let, p_zemlja, p_hiša, št_hiš, mesecni_stroski, p_dnevni_najem, amortizacijski_faktor, rast_vr_zemlje, delež_nepredvidljivih_stroškov_na_hiško, delez_davka_na_dobicek, pričakovano_št_dni_v_najemu_na_leto)
#    st.write(f'Dobiček po {št_let} letih: {dobiček}')

# Klic funkcije plot_data ob spremembi kateregakoli drsnika
plot_data(št_let, p_zemlja, p_hiša, št_hiš, mesecni_stroski, p_dnevni_najem, amortizacijski_faktor, rast_vr_zemlje, delež_nepredvidljivih_stroškov_na_hiško, delez_davka_na_dobicek, pričakovano_št_dni_v_najemu_na_leto, amortizacijska_stopnja)


