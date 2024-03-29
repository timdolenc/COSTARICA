import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sys

class Model:
    def __init__(self, št_let, skupna_vrednost_investicije, vložek_investitorja, delež_investitorja, amortizacijska_stopnja, pogostost_čiščenja, cena_čiščenja, pričakovano_št_dni_v_najemu_na_leto, p_dnevni_najem, provizija, letni_stroški_vzdrževanja_okolice, letni_ostali_stroški, delez_davka_na_dobicek):
        self.št_let = št_let
        self.št_dni = št_let * 365
        self.dnevi = np.arange(1, self.št_dni + 1)
        self.delež_investitorja = delež_investitorja
        
        self.skupna_vrednost_investicije = skupna_vrednost_investicije
        self.vložek_investitorja = self.skupna_vrednost_investicije * self.delež_investitorja
        self.št_hiš = 12

        self.amortizacijska_stopnja = amortizacijska_stopnja
        self.pogostost_čiščenja = pogostost_čiščenja
        self.cena_čiščenja = cena_čiščenja
        self.pričakovano_št_dni_v_najemu_na_leto = pričakovano_št_dni_v_najemu_na_leto
        self.p_dnevni_najem = p_dnevni_najem
        self.provizija = provizija
        self.letni_stroški_vzdrževanja_okolice = letni_stroški_vzdrževanja_okolice
        self.letni_ostali_stroški = letni_ostali_stroški
        self.delez_davka_na_dobicek = delez_davka_na_dobicek


    ######################STROŠKI##############################
    def stroški_čiščenja(self):
        faktor_zasedenosti = self.pričakovano_št_dni_v_najemu_na_leto / 365
        št_čiščenj = self.št_hiš * self.dnevi * faktor_zasedenosti / self.pogostost_čiščenja
        stroški = št_čiščenj * self.cena_čiščenja
        return stroški 

    #@st.cache_data
    def stroški_amortizacije_po_času(self):
        amortizacija = self.skupna_vrednost_investicije * self.amortizacijska_stopnja * (self.dnevi / 365)
        return amortizacija
    



    def stroški_po_času(self):
        amortizacija = self.stroški_amortizacije_po_času()
        čiščenje = self.stroški_čiščenja()
        prihodki = self.prihodki_po_času() / self.delež_investitorja
        
        stroški_provizij = self.provizija * prihodki
        okolica = self.letni_stroški_vzdrževanja_okolice * self.dnevi / 365
        ostali_stroški = self.letni_ostali_stroški * self.dnevi / 365

        stroški = amortizacija + čiščenje + stroški_provizij + okolica + ostali_stroški
        return stroški * self.delež_investitorja

    #######################################################################
    #@st.cache_data
    def prihodki_po_času(self):
        faktor_zasedenosti = self.pričakovano_št_dni_v_najemu_na_leto / 365
        prihodki = self.št_hiš * self.p_dnevni_najem * self.dnevi * faktor_zasedenosti
        return prihodki * self.delež_investitorja


    def dobiček_po_času(self):
        stroški = self.stroški_po_času()
        prihodki = self.prihodki_po_času()
        dobiček = (prihodki - stroški) * (1 - self.delez_davka_na_dobicek)
        return dobiček

    ##########################LETNE ZADEVE#############################################
    def letni_prihodki(self):
        return self.prihodki_po_času()[365]

    def letni_stroški(self):
        return self.stroški_po_času()[365]

    def letni_dobiček_pred_davki(self):
        return self.letni_prihodki() - self.letni_stroški()

    def letni_dobiček_po_davkih(self):
        return self.letni_dobiček_pred_davki() * (1 - self.delez_davka_na_dobicek)

    #######################################################################
    def plot_data(self):
        stroški = self.stroški_po_času()
        prihodki = self.prihodki_po_času()
        dobiček = self.dobiček_po_času()

        # Create a figure and axes object
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plotting using day numbers
        ax.plot(self.dnevi, self.vložek_investitorja * np.ones_like(self.dnevi), label='Investment')
        #ax.plot(self.dnevi, stroški, label='Costs')
        #ax.plot(self.dnevi, prihodki, label='Revenues')
        ax.plot(self.dnevi, dobiček, label='Profit') # (after taxes)

        # Set labels and title
        ax.set_xlabel('Years')
        ax.set_ylabel('1000$')
        ax.set_title('Investment Chart Over Time')
        ax.legend()

        # Adjust x-axis to show years
        year_ticks = np.arange(365, self.št_dni + 1, 365)
        ax.set_xticks(year_ticks)
        ax.set_xticklabels(range(1, self.št_dni // 365 + 1))
        ax.grid(True)

        # Column setup for results display
        col_widths = [3, 3, 3, 3]  # Adjust the values as needed

        col1, col2, col3, col4 = st.columns(col_widths)
        with col1:
            st.metric("Annual Revenues", f"{self.letni_prihodki():,.3f}".replace(',', '.') + " $")
        with col2:
            st.metric("Annual Costs", f"{self.letni_stroški():,.3f}".replace(',', '.') + " $")
        with col3:
            st.metric("Annual Profit before taxes", f"{self.letni_dobiček_pred_davki():,.3f}".replace(',', '.') + " $") # Before Taxes
        #    st.metric("Annual Profit After Taxes", f"{self.letni_dobiček_po_davkih():,.3f}".replace(',', '.') + " $")

        # Calculation for intersection points
        payback_period_without_tax = np.argmin(np.abs(dobiček / (1 - self.delez_davka_na_dobicek) - self.vložek_investitorja)) / 365
        payback_period_with_tax = np.argmin(np.abs(dobiček - self.vložek_investitorja)) / 365
        annual_yield = self.letni_dobiček_po_davkih() / self.vložek_investitorja
        
        st.markdown(f"**Payback Period (Gross):** {payback_period_without_tax:.1f} years")
        st.markdown(f"**Payback Period (Net):** {payback_period_with_tax:.1f} years")
        st.markdown(f"**Annual Yield:** {100 * annual_yield:.2f} %")
        
        # Display the plot
        st.pyplot(fig)




if __name__ == '__main__':
    št_let = 15

    import streamlit as st

# Custom CSS to inject into Streamlit's HTML
    st.markdown("""
        <style>
            /* Remove padding and margin from the main block */
            .css-18e3th9 {
                padding: 0 !important;
                margin: 0 !important;
            }
            /* Additional selectors for more specific adjustments might be necessary */
        </style>
    """, unsafe_allow_html=True)

    # Your Streamlit app code here


    #skupni_vložek = st.sidebar.slider('Total Investment (in $1000)', min_value=0, max_value=5000, value=2750)

    skupni_vložek = 3200
    delež_investitorja = st.sidebar.slider('Investor Share (%)', min_value=0, max_value=100, value=12) / 100
    vložek_investitorja = skupni_vložek * delež_investitorja
    pričakovano_št_dni_v_najemu_na_leto = st.sidebar.slider('Expected Number of Days Rented per Year', min_value=0, max_value=365, value=200)
    p_dnevni_najem = st.sidebar.slider('Expected Daily Rent Price ($)', min_value=0, max_value=500, value=250) / 1000

    amortizacijska_stopnja = st.sidebar.slider('Amortization Rate (%)', min_value=0, max_value=30, value=5) / 100
    delez_davka_na_dobicek = st.sidebar.slider('Tax Rate on Profit (%)', min_value=0, max_value=100, value=20) / 100
    pogostost_čiščenja = st.sidebar.slider('Days between cleaning (rented)', min_value=1, max_value=30, value=5)
    cena_čiščenja = st.sidebar.slider('Price per Cleaning ($)', min_value=0, max_value=20, value=15) / 1000
    provizija = st.sidebar.slider('Commission on revenues and taxes (VAT) (%)', min_value=0, max_value=100, value=10) / 100
    letni_stroški_vzdrževanja_okolice = st.sidebar.slider('Annual Maintenance Costs ($)', min_value=0, max_value=10000, value=3500) / 1000
    ostali_stroški = st.sidebar.slider('Other Annual Costs (electricity, taxes, etc.) ($)', min_value=0, max_value=50000, value=10000) / 1000

    

    model = Model(št_let, skupna_vrednost_investicije=skupni_vložek, vložek_investitorja=vložek_investitorja, delež_investitorja=delež_investitorja, amortizacijska_stopnja=amortizacijska_stopnja, pogostost_čiščenja=pogostost_čiščenja, cena_čiščenja=cena_čiščenja, pričakovano_št_dni_v_najemu_na_leto=pričakovano_št_dni_v_najemu_na_leto, p_dnevni_najem=p_dnevni_najem, provizija=provizija, letni_stroški_vzdrževanja_okolice=letni_stroški_vzdrževanja_okolice, letni_ostali_stroški=ostali_stroški, delez_davka_na_dobicek=delez_davka_na_dobicek)
    
    

    st.title('INVESTMENT CALCULATOR')
    model.plot_data()
        
        

    