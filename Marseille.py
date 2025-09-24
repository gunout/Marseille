import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class MarseilleArrondissementImmobilierAnalyzer:
    def __init__(self, arrondissement_name):
        self.arrondissement = arrondissement_name
        self.colors = ['#003366', '#FF6B6B', '#4ECDC4', '#45B7D1', '#F9A602', 
                      '#6A0572', '#AB83A1', '#8B0000', '#228B22', '#FFD700']
        
        self.start_year = 2002
        self.end_year = 2025
        
        # Configuration spécifique à chaque arrondissement marseillais
        self.config = self._get_arrondissement_config()
        
    def _get_arrondissement_config(self):
        """Retourne la configuration spécifique pour chaque arrondissement marseillais"""
        configs = {
            "1er": {
                "population_base": 40000,
                "budget_base": 80,
                "type": "centre_ville",
                "specialites": ["vieux_port", "commerce", "administration", "tourisme"],
                "prix_m2_base": 4500,
                "segment_immobilier": "haut_de_gamme"
            },
            "2e": {
                "population_base": 25000,
                "budget_base": 60,
                "type": "portuaire",
                "specialites": ["vieux_port", "panier", "culture", "tourisme"],
                "prix_m2_base": 5000,
                "segment_immobilier": "premium"
            },
            "3e": {
                "population_base": 45000,
                "budget_base": 85,
                "type": "populaire",
                "specialites": ["commerces", "residentiel", "diversite", "proximite_centre"],
                "prix_m2_base": 3200,
                "segment_immobilier": "mixte"
            },
            "4e": {
                "population_base": 50000,
                "budget_base": 90,
                "type": "historique",
                "specialites": ["le_panier", "historique", "artistique", "tourisme"],
                "prix_m2_base": 4800,
                "segment_immobilier": "haut_de_gamme"
            },
            "5e": {
                "population_base": 42000,
                "budget_base": 75,
                "type": "residentiel",
                "specialites": ["collines", "calme", "vues_mer", "residentiel"],
                "prix_m2_base": 3800,
                "segment_immobilier": "residentiel"
            },
            "6e": {
                "population_base": 40000,
                "budget_base": 120,
                "type": "bourgeois",
                "specialites": ["prestige", "bord_mer", "luxe", "calme"],
                "prix_m2_base": 6500,
                "segment_immobilier": "luxe"
            },
            "7e": {
                "population_base": 35000,
                "budget_base": 100,
                "type": "cotier",
                "specialites": ["corniche", "plages", "tourisme", "prestige"],
                "prix_m2_base": 6000,
                "segment_immobilier": "luxe"
            },
            "8e": {
                "population_base": 80000,
                "budget_base": 150,
                "type": "diversifie",
                "specialites": ["plages", "periere", "commerce", "residentiel"],
                "prix_m2_base": 4200,
                "segment_immobilier": "mixte"
            },
            "9e": {
                "population_base": 75000,
                "budget_base": 110,
                "type": "residentiel",
                "specialites": ["mazargues", "calanques", "nature", "residentiel"],
                "prix_m2_base": 3500,
                "segment_immobilier": "residentiel"
            },
            "10e": {
                "population_base": 60000,
                "budget_base": 95,
                "type": "populaire",
                "specialites": ["estaque", "industriel", "portuaire", "diversite"],
                "prix_m2_base": 2800,
                "segment_immobilier": "abordable"
            },
            "11e": {
                "population_base": 60000,
                "budget_base": 90,
                "type": "populaire",
                "specialites": ["marseille_est", "commerces", "jeunes", "dynamique"],
                "prix_m2_base": 2700,
                "segment_immobilier": "abordable"
            },
            "12e": {
                "population_base": 65000,
                "budget_base": 100,
                "type": "residentiel",
                "specialites": ["olympiques", "stades", "parcs", "familial"],
                "prix_m2_base": 3000,
                "segment_immobilier": "mixte"
            },
            "13e": {
                "population_base": 90000,
                "budget_base": 130,
                "type": "universitaire",
                "specialites": ["universite", "hopitaux", "commerce", "diversite"],
                "prix_m2_base": 2900,
                "segment_immobilier": "universitaire"
            },
            "14e": {
                "population_base": 65000,
                "budget_base": 85,
                "type": "populaire",
                "specialites": ["sainte_marthe", "commerces", "populaire", "proximite_centre"],
                "prix_m2_base": 2600,
                "segment_immobilier": "abordable"
            },
            "15e": {
                "population_base": 85000,
                "budget_base": 120,
                "type": "populaire",
                "specialites": ["littoral", "industriel", "portuaire", "diversite"],
                "prix_m2_base": 2500,
                "segment_immobilier": "abordable"
            },
            "16e": {
                "population_base": 20000,
                "budget_base": 45,
                "type": "cotier",
                "specialites": ["l'esteve", "calanques", "nature", "calme"],
                "prix_m2_base": 3200,
                "segment_immobilier": "residentiel"
            },
            # Configuration par défaut
            "default": {
                "population_base": 50000,
                "budget_base": 80,
                "type": "residentiel",
                "specialites": ["residentiel", "commerce_local", "services"],
                "prix_m2_base": 3500,
                "segment_immobilier": "mixte"
            }
        }
        
        return configs.get(self.arrondissement, configs["default"])
    
    def generate_financial_data(self):
        """Génère des données financières et immobilières pour l'arrondissement marseillais"""
        print(f"🏛️ Génération des données financières et immobilières pour le {self.arrondissement}e arrondissement de Marseille...")
        
        # Créer une base de données annuelle
        dates = pd.date_range(start=f'{self.start_year}-01-01', 
                             end=f'{self.end_year}-12-31', freq='Y')
        
        data = {'Annee': [date.year for date in dates]}
        
        # Données démographiques
        data['Population'] = self._simulate_population(dates)
        data['Menages'] = self._simulate_households(dates)
        
        # Recettes communales
        data['Recettes_Totales'] = self._simulate_total_revenue(dates)
        data['Impots_Locaux'] = self._simulate_tax_revenue(dates)
        data['Dotations_Etat'] = self._simulate_state_grants(dates)
        data['Autres_Recettes'] = self._simulate_other_revenue(dates)
        
        # Dépenses communales
        data['Depenses_Totales'] = self._simulate_total_expenses(dates)
        data['Fonctionnement'] = self._simulate_operating_expenses(dates)
        data['Investissement'] = self._simulate_investment_expenses(dates)
        data['Charge_Dette'] = self._simulate_debt_charges(dates)
        data['Personnel'] = self._simulate_staff_costs(dates)
        
        # Indicateurs financiers
        data['Epargne_Brute'] = self._simulate_gross_savings(dates)
        data['Dette_Totale'] = self._simulate_total_debt(dates)
        data['Taux_Endettement'] = self._simulate_debt_ratio(dates)
        data['Taux_Fiscalite'] = self._simulate_tax_rate(dates)
        
        # Données immobilières (spécifiques à Marseille)
        data['Prix_m2_Moyen'] = self._simulate_avg_price_per_sqm(dates)
        data['Transactions_Immobilieres'] = self._simulate_real_estate_transactions(dates)
        data['Nouveaux_Logements'] = self._simulate_new_housing(dates)
        data['Taxe_Fonciere'] = self._simulate_property_tax(dates)
        data['Taxe_Habitation'] = self._simulate_residence_tax(dates)
        
        # Investissements spécifiques adaptés à Marseille
        data['Investissement_Immobilier'] = self._simulate_real_estate_investment(dates)
        data['Investissement_Transport'] = self._simulate_transport_investment(dates)
        data['Investissement_Portuaire'] = self._simulate_port_investment(dates)
        data['Investissement_Tourisme'] = self._simulate_tourism_investment(dates)
        data['Investissement_Culture'] = self._simulate_culture_investment(dates)
        data['Investissement_Education'] = self._simulate_education_investment(dates)
        
        df = pd.DataFrame(data)
        
        # Ajouter des tendances spécifiques au marché immobilier marseillais
        self._add_marseille_trends(df)
        
        return df
    
    def _simulate_population(self, dates):
        """Simule la population de l'arrondissement (croissance marseillaise modérée)"""
        base_population = self.config["population_base"]
        
        population = []
        for i, date in enumerate(dates):
            # Croissance démographique marseillaise
            if self.config["type"] == "centre_ville":
                growth_rate = 0.005  # Croissance modérée dans le centre
            elif self.config["type"] == "luxe":
                growth_rate = 0.003  # Croissance faible dans les quartiers aisés
            elif self.config["type"] == "populaire":
                growth_rate = 0.008  # Croissance plus forte dans les quartiers populaires
            else:
                growth_rate = 0.006  # Croissance moyenne
                
            growth = 1 + growth_rate * i
            population.append(base_population * growth)
        
        return population
    
    def _simulate_households(self, dates):
        """Simule le nombre de ménages"""
        base_households = self.config["population_base"] / 2.1  # Taille des ménages plus petite à Marseille
        
        households = []
        for i, date in enumerate(dates):
            growth = 1 + 0.007 * i  # Croissance modérée
            households.append(base_households * growth)
        
        return households
    
    def _simulate_total_revenue(self, dates):
        """Simule les recettes totales de l'arrondissement"""
        base_revenue = self.config["budget_base"]
        
        revenue = []
        for i, date in enumerate(dates):
            # Croissance économique marseillaise
            if self.config["type"] == "luxe":
                growth_rate = 0.025  # Croissance forte dans les quartiers aisés
            elif self.config["type"] == "populaire":
                growth_rate = 0.020  # Croissance modérée
            else:
                growth_rate = 0.022  # Croissance moyenne
                
            growth = 1 + growth_rate * i
            noise = np.random.normal(1, 0.07)
            revenue.append(base_revenue * growth * noise)
        
        return revenue
    
    def _simulate_tax_revenue(self, dates):
        """Simule les recettes fiscales"""
        base_tax = self.config["budget_base"] * 0.35
        
        tax_revenue = []
        for i, date in enumerate(dates):
            growth = 1 + 0.018 * i
            noise = np.random.normal(1, 0.08)
            tax_revenue.append(base_tax * growth * noise)
        
        return tax_revenue
    
    def _simulate_state_grants(self, dates):
        """Simule les dotations de l'État"""
        base_grants = self.config["budget_base"] * 0.40  # Plus de dotations à Marseille
        
        grants = []
        for i, date in enumerate(dates):
            year = date.year
            if year >= 2010:
                increase = 1 + 0.006 * (year - 2010)
            else:
                increase = 1
            
            noise = np.random.normal(1, 0.06)
            grants.append(base_grants * increase * noise)
        
        return grants
    
    def _simulate_other_revenue(self, dates):
        """Simule les autres recettes"""
        base_other = self.config["budget_base"] * 0.25
        
        other_revenue = []
        for i, date in enumerate(dates):
            growth = 1 + 0.020 * i
            noise = np.random.normal(1, 0.09)
            other_revenue.append(base_other * growth * noise)
        
        return other_revenue
    
    def _simulate_total_expenses(self, dates):
        """Simule les dépenses totales"""
        base_expenses = self.config["budget_base"] * 0.98  # Dépenses plus élevées à Marseille
        
        expenses = []
        for i, date in enumerate(dates):
            growth = 1 + 0.025 * i
            noise = np.random.normal(1, 0.06)
            expenses.append(base_expenses * growth * noise)
        
        return expenses
    
    def _simulate_operating_expenses(self, dates):
        """Simule les dépenses de fonctionnement"""
        base_operating = self.config["budget_base"] * 0.65  # Plus de fonctionnement à Marseille
        
        operating = []
        for i, date in enumerate(dates):
            growth = 1 + 0.022 * i
            noise = np.random.normal(1, 0.05)
            operating.append(base_operating * growth * noise)
        
        return operating
    
    def _simulate_investment_expenses(self, dates):
        """Simule les dépenses d'investissement"""
        base_investment = self.config["budget_base"] * 0.33
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2007, 2013, 2019, 2024]:
                multiplier = 1.5
            elif year in [2009, 2015, 2021]:
                multiplier = 0.8
            else:
                multiplier = 1.0
            
            growth = 1 + 0.020 * i
            noise = np.random.normal(1, 0.16)
            investment.append(base_investment * growth * multiplier * noise)
        
        return investment
    
    def _simulate_debt_charges(self, dates):
        """Simule les charges de la dette"""
        base_debt_charge = self.config["budget_base"] * 0.08  # Dette plus élevée à Marseille
        
        debt_charges = []
        for i, date in enumerate(dates):
            year = date.year
            if year >= 2005:
                increase = 1 + 0.008 * (year - 2005)
            else:
                increase = 1
            
            noise = np.random.normal(1, 0.09)
            debt_charges.append(base_debt_charge * increase * noise)
        
        return debt_charges
    
    def _simulate_staff_costs(self, dates):
        """Simule les dépenses de personnel"""
        base_staff = self.config["budget_base"] * 0.45  # Plus de personnel à Marseille
        
        staff_costs = []
        for i, date in enumerate(dates):
            growth = 1 + 0.021 * i
            noise = np.random.normal(1, 0.04)
            staff_costs.append(base_staff * growth * noise)
        
        return staff_costs
    
    def _simulate_gross_savings(self, dates):
        """Simule l'épargne brute"""
        savings = []
        for i, date in enumerate(dates):
            base_saving = self.config["budget_base"] * 0.02  # Épargne plus faible à Marseille
            
            year = date.year
            if year >= 2010:
                improvement = 1 + 0.007 * (year - 2010)
            else:
                improvement = 1
            
            noise = np.random.normal(1, 0.13)
            savings.append(base_saving * improvement * noise)
        
        return savings
    
    def _simulate_total_debt(self, dates):
        """Simule la dette totale"""
        base_debt = self.config["budget_base"] * 0.90  # Dette plus élevée
        
        debt = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2007, 2013, 2019, 2024]:
                change = 1.20
            elif year in [2009, 2015, 2021]:
                change = 0.92
            else:
                change = 1.0
            
            noise = np.random.normal(1, 0.08)
            debt.append(base_debt * change * noise)
        
        return debt
    
    def _simulate_debt_ratio(self, dates):
        """Simule le taux d'endettement"""
        ratios = []
        for i, date in enumerate(dates):
            base_ratio = 0.85  # Endettement plus élevé à Marseille
            
            year = date.year
            if year >= 2010:
                improvement = 1 - 0.008 * (year - 2010)
            else:
                improvement = 1
            
            noise = np.random.normal(1, 0.06)
            ratios.append(base_ratio * improvement * noise)
        
        return ratios
    
    def _simulate_tax_rate(self, dates):
        """Simule le taux de fiscalité (plus élevé à Marseille)"""
        rates = []
        for i, date in enumerate(dates):
            base_rate = 1.05  # Fiscalité plus élevée
            
            year = date.year
            if year >= 2010:
                increase = 1 + 0.005 * (year - 2010)
            else:
                increase = 1
            
            noise = np.random.normal(1, 0.04)
            rates.append(base_rate * increase * noise)
        
        return rates
    
    def _simulate_avg_price_per_sqm(self, dates):
        """Simule le prix moyen au m² (spécifique à Marseille)"""
        base_price = self.config["prix_m2_base"]
        
        prices = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Croissance du marché immobilier marseillais
            if self.config["segment_immobilier"] == "luxe":
                growth_rate = 0.040  # Croissance forte pour le luxe
            elif self.config["segment_immobilier"] == "premium":
                growth_rate = 0.038  # Croissance pour le premium
            elif self.config["segment_immobilier"] == "haut_de_gamme":
                growth_rate = 0.035  # Croissance pour le haut de gamme
            else:
                growth_rate = 0.030  # Croissance moyenne
            
            # Ajustements annuels basés sur des événements réels
            if 2002 <= year <= 2007:
                # Période de croissance modérée
                multiplier = 1 + 0.04 * (year - 2002)
            elif 2008 <= year <= 2009:
                # Impact de la crise financière
                multiplier = 0.92
            elif 2010 <= year <= 2013:
                # Effet Capitale Européenne de la Culture
                multiplier = 1 + 0.06 * (year - 2010)
            elif 2014 <= year <= 2019:
                # Croissance soutenue
                multiplier = 1 + 0.04 * (year - 2014)
            elif 2020 <= year <= 2021:
                # Résilience pendant le COVID
                multiplier = 1.01
            else:
                # Reprise post-COVID
                multiplier = 1 + 0.035 * (year - 2022)
            
            growth = 1 + growth_rate * i
            noise = np.random.normal(1, 0.10)
            prices.append(base_price * growth * multiplier * noise)
        
        return prices
    
    def _simulate_real_estate_transactions(self, dates):
        """Simule le nombre de transactions immobilières"""
        base_transactions = self.config["population_base"] / 120  # Base proportionnelle à la population
        
        transactions = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Variations selon la conjoncture
            if 2002 <= year <= 2007:
                multiplier = 1 + 0.06 * (year - 2002)  # Croissance modérée
            elif 2008 <= year <= 2009:
                multiplier = 0.70  # Forte baisse pendant la crise
            elif 2010 <= year <= 2013:
                multiplier = 1 + 0.08 * (year - 2010)  # Effet Capitale de la Culture
            elif 2014 <= year <= 2019:
                multiplier = 1 + 0.05 * (year - 2014)  # Croissance régulière
            elif 2020 <= year <= 2021:
                multiplier = 0.78  # Fort ralentissement COVID
            else:
                multiplier = 1 + 0.06 * (year - 2022)  # Reprise post-COVID
            
            growth = 1 + 0.012 * i
            noise = np.random.normal(1, 0.14)
            transactions.append(base_transactions * growth * multiplier * noise)
        
        return transactions
    
    def _simulate_new_housing(self, dates):
        """Simule le nombre de nouveaux logements construits"""
        base_housing = self.config["population_base"] / 600  # Base proportionnelle
        
        housing = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Pics de construction selon les programmes
            if year in [2005, 2010, 2015, 2020]:
                multiplier = 1.8  # Années de grands programmes
            elif year in [2008, 2014, 2021]:
                multiplier = 0.6  # Ralentissements
            else:
                multiplier = 1.0
            
            growth = 1 + 0.015 * i
            noise = np.random.normal(1, 0.22)
            housing.append(base_housing * growth * multiplier * noise)
        
        return housing
    
    def _simulate_property_tax(self, dates):
        """Simule la taxe foncière"""
        base_tax = self.config["budget_base"] * 0.18  # Plus élevée à Marseille
        
        tax = []
        for i, date in enumerate(dates):
            year = date.year
            if year >= 2010:
                increase = 1 + 0.014 * (year - 2010)
            else:
                increase = 1
            
            noise = np.random.normal(1, 0.07)
            tax.append(base_tax * increase * noise)
        
        return tax
    
    def _simulate_residence_tax(self, dates):
        """Simule la taxe d'habitation (en diminution)"""
        base_tax = self.config["budget_base"] * 0.15  # Plus élevée à Marseille
        
        tax = []
        for i, date in enumerate(dates):
            year = date.year
            if year >= 2018:
                # Réduction progressive de la taxe d'habitation
                reduction = 1 - 0.15 * min(4, year - 2018)  # Suppression progressive
            else:
                reduction = 1
            
            noise = np.random.normal(1, 0.06)
            tax.append(base_tax * reduction * noise)
        
        return tax
    
    def _simulate_real_estate_investment(self, dates):
        """Simule l'investissement immobilier"""
        base_investment = self.config["budget_base"] * 0.07
        
        # Ajustement selon les spécialités
        multiplier = 1.4 if "residentiel" in self.config["specialites"] else 0.9
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2006, 2012, 2018, 2023]:
                year_multiplier = 1.6
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.028 * i
            noise = np.random.normal(1, 0.17)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_transport_investment(self, dates):
        """Simule l'investissement en transport (métro, tramway, etc.)"""
        base_investment = self.config["budget_base"] * 0.05
        
        # Ajustement selon les spécialités
        multiplier = 1.5 if "transport" in self.config["specialites"] else 1.0
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            # Pics d'investissement liés aux extensions de métro/tramway
            if year in [2003, 2007, 2010, 2019]:
                year_multiplier = 2.0
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.025 * i
            noise = np.random.normal(1, 0.19)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_port_investment(self, dates):
        """Simule l'investissement portuaire (spécifique à Marseille)"""
        base_investment = self.config["budget_base"] * 0.04
        
        # Ajustement selon les spécialités
        multiplier = 2.2 if "portuaire" in self.config["specialites"] else 0.4
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2005, 2010, 2015, 2020]:
                year_multiplier = 1.8
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.030 * i
            noise = np.random.normal(1, 0.23)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_tourism_investment(self, dates):
        """Simule l'investissement touristique"""
        base_investment = self.config["budget_base"] * 0.06
        
        # Ajustement selon les spécialités
        multiplier = 1.8 if "tourisme" in self.config["specialites"] else 0.7
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2007, 2013, 2019, 2024]:
                year_multiplier = 1.7
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.026 * i
            noise = np.random.normal(1, 0.18)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_culture_investment(self, dates):
        """Simule l'investissement culturel"""
        base_investment = self.config["budget_base"] * 0.04
        
        # Ajustement selon les spécialités
        multiplier = 1.7 if "culture" in self.config["specialites"] else 0.7
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2010, 2013, 2016, 2022]:
                year_multiplier = 2.0  # Effet Capitale de la Culture 2013
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.022 * i
            noise = np.random.normal(1, 0.16)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_education_investment(self, dates):
        """Simule l'investissement éducatif"""
        base_investment = self.config["budget_base"] * 0.06
        
        # Ajustement selon les spécialités
        multiplier = 1.7 if "universite" in self.config["specialites"] else 0.9
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2008, 2014, 2020]:
                year_multiplier = 1.6
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.025 * i
            noise = np.random.normal(1, 0.15)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _add_marseille_trends(self, df):
        """Ajoute des tendances réalistes adaptées au marché marseillais"""
        for i, row in df.iterrows():
            year = row['Annee']
            
            # Capitale Européenne de la Culture 2013
            if year == 2013:
                df.loc[i, 'Investissement_Culture'] *= 3.0
                df.loc[i, 'Investissement_Tourisme'] *= 1.8
                df.loc[i, 'Prix_m2_Moyen'] *= 1.08
            
            # Développement du tramway (phases successives)
            if year in [2007, 2008]:
                df.loc[i, 'Investissement_Transport'] *= 2.2  # Lancement tramway
            if year in [2010, 2011]:
                df.loc[i, 'Investissement_Transport'] *= 1.8  # Extensions
            if year in [2019, 2020]:
                df.loc[i, 'Investissement_Transport'] *= 1.6  # Nouvelles extensions
            
            # Euroméditerranée (grand projet d'aménagement)
            if 2005 <= year <= 2015:
                df.loc[i, 'Investissement_Immobilier'] *= 1.4
                df.loc[i, 'Nouveaux_Logements'] *= 1.3
            
            # Impact COVID-19 (2020-2021) - marché résilient mais impacté
            if 2020 <= year <= 2021:
                if year == 2020:
                    df.loc[i, 'Transactions_Immobilieres'] *= 0.75
                    df.loc[i, 'Prix_m2_Moyen'] *= 0.98
                else:
                    df.loc[i, 'Prix_m2_Moyen'] *= 1.02  # Reprise modérée
                    df.loc[i, 'Transactions_Immobilieres'] *= 1.08
            
            # Plan de relance marseillais (2022-2025)
            if year >= 2022:
                df.loc[i, 'Investissement_Transport'] *= 1.12
                df.loc[i, 'Investissement_Immobilier'] *= 1.15
                df.loc[i, 'Nouveaux_Logements'] *= 1.20
    
    def create_financial_analysis(self, df):
        """Crée une analyse complète des finances et de l'immobilier"""
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 28))
        
        # 1. Évolution des recettes et dépenses
        ax1 = plt.subplot(5, 2, 1)
        self._plot_revenue_expenses(df, ax1)
        
        # 2. Structure des recettes
        ax2 = plt.subplot(5, 2, 2)
        self._plot_revenue_structure(df, ax2)
        
        # 3. Évolution des prix immobiliers
        ax3 = plt.subplot(5, 2, 3)
        self._plot_real_estate_prices(df, ax3)
        
        # 4. Activité immobilière
        ax4 = plt.subplot(5, 2, 4)
        self._plot_real_estate_activity(df, ax4)
        
        # 5. Structure des dépenses
        ax5 = plt.subplot(5, 2, 5)
        self._plot_expenses_structure(df, ax5)
        
        # 6. Investissements communaux
        ax6 = plt.subplot(5, 2, 6)
        self._plot_investments(df, ax6)
        
        # 7. Dette et endettement
        ax7 = plt.subplot(5, 2, 7)
        self._plot_debt(df, ax7)
        
        # 8. Indicateurs de performance
        ax8 = plt.subplot(5, 2, 8)
        self._plot_performance_indicators(df, ax8)
        
        # 9. Démographie
        ax9 = plt.subplot(5, 2, 9)
        self._plot_demography(df, ax9)
        
        # 10. Investissements sectoriels
        ax10 = plt.subplot(5, 2, 10)
        self._plot_sectorial_investments(df, ax10)
        
        plt.suptitle(f'Analyse des Comptes Communaux et Immobiliers du {self.arrondissement}e Arrondissement de Marseille ({self.start_year}-{self.end_year})', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.arrondissement}e_arrondissement_marseille_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Générer les insights
        self._generate_financial_insights(df)
    
    def _plot_revenue_expenses(self, df, ax):
        """Plot de l'évolution des recettes et dépenses"""
        ax.plot(df['Annee'], df['Recettes_Totales'], label='Recettes Totales', 
               linewidth=2, color='#003366', alpha=0.8)
        ax.plot(df['Annee'], df['Depenses_Totales'], label='Dépenses Totales', 
               linewidth=2, color='#FF6B6B', alpha=0.8)
        
        ax.set_title('Évolution des Recettes et Dépenses (M€)', 
                    fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_revenue_structure(self, df, ax):
        """Plot de la structure des recettes"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Impots_Locaux', 'Dotations_Etat', 'Autres_Recettes']
        colors = ['#003366', '#FF6B6B', '#4ECDC4']
        labels = ['Impôts Locaux', 'Dotations État', 'Autres Recettes']
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title('Structure des Recettes (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_real_estate_prices(self, df, ax):
        """Plot de l'évolution des prix immobiliers"""
        ax.plot(df['Annee'], df['Prix_m2_Moyen'], label='Prix moyen au m²', 
               linewidth=3, color='#003366', alpha=0.8)
        
        ax.set_title('Évolution des Prix Immobiliers (€/m²)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Prix (€/m²)')
        ax.grid(True, alpha=0.3)
        
        # Ajouter des annotations pour les événements marquants
        ax.annotate('Capitale Culture 2013', xy=(2013, df.loc[df['Annee'] == 2013, 'Prix_m2_Moyen'].values[0]), 
                   xytext=(2013, df.loc[df['Annee'] == 2013, 'Prix_m2_Moyen'].values[0] * 0.9),
                   arrowprops=dict(arrowstyle='->', color='red'))
        
        ax.annotate('Euroméditerranée', xy=(2010, df.loc[df['Annee'] == 2010, 'Prix_m2_Moyen'].values[0]), 
                   xytext=(2010, df.loc[df['Annee'] == 2010, 'Prix_m2_Moyen'].values[0] * 1.1),
                   arrowprops=dict(arrowstyle='->', color='green'))
    
    def _plot_real_estate_activity(self, df, ax):
        """Plot de l'activité immobilière"""
        # Transactions immobilières
        ax.bar(df['Annee'], df['Transactions_Immobilieres'], label='Transactions', 
              color='#003366', alpha=0.7)
        
        ax.set_title('Activité Immobilière', fontsize=12, fontweight='bold')
        ax.set_ylabel('Transactions immobilières', color='#003366')
        ax.tick_params(axis='y', labelcolor='#003366')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Nouveaux logements en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Nouveaux_Logements'], label='Nouveaux logements', 
                linewidth=2, color='#FF6B6B')
        ax2.set_ylabel('Nouveaux logements', color='#FF6B6B')
        ax2.tick_params(axis='y', labelcolor='#FF6B6B')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_expenses_structure(self, df, ax):
        """Plot de la structure des dépenses"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Fonctionnement', 'Investissement', 'Charge_Dette', 'Personnel']
        colors = ['#003366', '#FF6B6B', '#4ECDC4', '#45B7D1']
        labels = ['Fonctionnement', 'Investissement', 'Charge Dette', 'Personnel']
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title('Structure des Dépenses (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_investments(self, df, ax):
        """Plot des investissements communaux"""
        ax.plot(df['Annee'], df['Investissement_Immobilier'], label='Immobilier', 
               linewidth=2, color='#003366', alpha=0.8)
        ax.plot(df['Annee'], df['Investissement_Transport'], label='Transport', 
               linewidth=2, color='#FF6B6B', alpha=0.8)
        ax.plot(df['Annee'], df['Investissement_Portuaire'], label='Portuaire', 
               linewidth=2, color='#4ECDC4', alpha=0.8)
        ax.plot(df['Annee'], df['Investissement_Tourisme'], label='Tourisme', 
               linewidth=2, color='#45B7D1', alpha=0.8)
        ax.plot(df['Annee'], df['Investissement_Education'], label='Éducation', 
               linewidth=2, color='#F9A602', alpha=0.8)
        
        ax.set_title('Répartition des Investissements (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_debt(self, df, ax):
        """Plot de la dette et du taux d'endettement"""
        # Dette totale
        ax.bar(df['Annee'], df['Dette_Totale'], label='Dette Totale (M€)', 
              color='#003366', alpha=0.7)
        
        ax.set_title('Dette Communale et Taux d\'Endettement', fontsize=12, fontweight='bold')
        ax.set_ylabel('Dette (M€)', color='#003366')
        ax.tick_params(axis='y', labelcolor='#003366')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Taux d'endettement en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Taux_Endettement'], label='Taux d\'Endettement', 
                linewidth=3, color='#FF6B6B')
        ax2.set_ylabel('Taux d\'Endettement', color='#FF6B6B')
        ax2.tick_params(axis='y', labelcolor='#FF6B6B')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_performance_indicators(self, df, ax):
        """Plot des indicateurs de performance"""
        # Épargne brute
        ax.bar(df['Annee'], df['Epargne_Brute'], label='Épargne Brute (M€)', 
              color='#4ECDC4', alpha=0.7)
        
        ax.set_title('Indicateurs de Performance', fontsize=12, fontweight='bold')
        ax.set_ylabel('Épargne Brute (M€)', color='#4ECDC4')
        ax.tick_params(axis='y', labelcolor='#4ECDC4')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Taux de fiscalité en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Taux_Fiscalite'], label='Taux de Fiscalité', 
                linewidth=3, color='#FF6B6B')
        ax2.set_ylabel('Taux de Fiscalité', color='#FF6B6B')
        ax2.tick_params(axis='y', labelcolor='#FF6B6B')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_demography(self, df, ax):
        """Plot de l'évolution démographique"""
        ax.plot(df['Annee'], df['Population'], label='Population', 
               linewidth=2, color='#003366', alpha=0.8)
        
        ax.set_title('Évolution Démographique', fontsize=12, fontweight='bold')
        ax.set_ylabel('Population', color='#003366')
        ax.tick_params(axis='y', labelcolor='#003366')
        ax.grid(True, alpha=0.3)
        
        # Nombre de ménages en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Menages'], label='Ménages', 
                linewidth=2, color='#FF6B6B', alpha=0.8)
        ax2.set_ylabel('Ménages', color='#FF6B6B')
        ax2.tick_params(axis='y', labelcolor='#FF6B6B')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_sectorial_investments(self, df, ax):
        """Plot des investissements sectoriels"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Investissement_Immobilier', 'Investissement_Transport', 
                     'Investissement_Portuaire', 'Investissement_Tourisme', 
                     'Investissement_Education']
        
        colors = ['#003366', '#FF6B6B', '#4ECDC4', '#45B7D1', '#F9A602']
        labels = ['Immobilier', 'Transport', 'Portuaire', 'Tourisme', 'Éducation']
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title('Répartition Sectorielle des Investissements (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _generate_financial_insights(self, df):
        """Génère des insights analytiques adaptés au marché marseillais"""
        print(f"🏛️ INSIGHTS ANALYTIQUES - {self.arrondissement}e Arrondissement de Marseille")
        print("=" * 70)
        
        # 1. Statistiques de base
        print("\n1. 📈 STATISTIQUES GÉNÉRALES:")
        avg_revenue = df['Recettes_Totales'].mean()
        avg_expenses = df['Depenses_Totales'].mean()
        avg_price = df['Prix_m2_Moyen'].mean()
        avg_transactions = df['Transactions_Immobilieres'].mean()
        
        print(f"Recettes moyennes annuelles: {avg_revenue:.2f} M€")
        print(f"Dépenses moyennes annuelles: {avg_expenses:.2f} M€")
        print(f"Prix moyen au m²: {avg_price:.0f} €")
        print(f"Transactions immobilières moyennes: {avg_transactions:.0f}")
        
        # 2. Croissance immobilière
        print("\n2. 📊 CROISSANCE IMMOBILIÈRE:")
        price_growth = ((df['Prix_m2_Moyen'].iloc[-1] / 
                        df['Prix_m2_Moyen'].iloc[0]) - 1) * 100
        population_growth = ((df['Population'].iloc[-1] / 
                             df['Population'].iloc[0]) - 1) * 100
        
        print(f"Croissance des prix au m² ({self.start_year}-{self.end_year}): {price_growth:.1f}%")
        print(f"Croissance de la population ({self.start_year}-{self.end_year}): {population_growth:.1f}%")
        
        # 3. Structure financière
        print("\n3. 📋 STRUCTURE FINANCIÈRE:")
        tax_share = (df['Impots_Locaux'].mean() / df['Recettes_Totales'].mean()) * 100
        state_share = (df['Dotations_Etat'].mean() / df['Recettes_Totales'].mean()) * 100
        property_tax_share = (df['Taxe_Fonciere'].mean() / df['Recettes_Totales'].mean()) * 100
        
        print(f"Part des impôts locaux dans les recettes: {tax_share:.1f}%")
        print(f"Part des dotations de l'État dans les recettes: {state_share:.1f}%")
        print(f"Part de la taxe foncière dans les recettes: {property_tax_share:.1f}%")
        
        # 4. Marché immobilier
        print("\n4. 🏠 MARCHÉ IMMOBILIER:")
        last_price = df['Prix_m2_Moyen'].iloc[-1]
        price_2020 = df.loc[df['Annee'] == 2020, 'Prix_m2_Moyen'].values[0]
        covid_impact = ((last_price / price_2020) - 1) * 100
        
        print(f"Prix actuel au m²: {last_price:.0f} €")
        print(f"Impact COVID-19 sur les prix (2020-{self.end_year}): +{covid_impact:.1f}%")
        print(f"Segment immobilier: {self.config['segment_immobilier']}")
        
        # 5. Spécificités de l'arrondissement marseillais
        print(f"\n5. 🌟 SPÉCIFICITÉS DU {self.arrondissement}E ARRONDISSEMENT:")
        print(f"Type d'arrondissement: {self.config['type']}")
        print(f"Spécialités: {', '.join(self.config['specialites'])}")
        print(f"Prix de référence au m²: {self.config['prix_m2_base']} €")
        
        # 6. Événements marquants du marché marseillais
        print("\n6. 📅 ÉVÉNEMENTS MARQUANTS MARSEILLE:")
        print("• 2005-2015: Projet Euroméditerranée et transformation urbaine")
        print("• 2007-2010: Développement du tramway marseillais")
        print("• 2013: Marseille Capitale Européenne de la Culture")
        print("• 2014-2019: Poursuite des investissements structurants")
        print("• 2020-2021: Impact significatif de la crise COVID-19")
        print("• 2022-2025: Plan de relance et nouvelles extensions métro")
        
        # 7. Recommandations stratégiques
        print("\n7. 💡 RECOMMANDATIONS STRATÉGIQUES:")
        if "portuaire" in self.config["specialites"]:
            print("• Développer l'économie bleue et les activités portuaires")
            print("• Valoriser le front de mer et les connexions port-ville")
        if "tourisme" in self.config["specialites"]:
            print("• Renforcer l'offre touristique et l'accueil international")
            print("• Développer le tourisme de croisière et balnéaire")
        if "culture" in self.config["specialites"]:
            print("• Capitaliser sur l'héritage Capitale de la Culture")
            print("• Développer les industries créatives et artistiques")
        if "universite" in self.config["specialites"]:
            print("• Renforcer le pôle universitaire et de recherche")
            print("• Développer l'immobilier étudiant et chercheurs")
        print("• Poursuivre les investissements en transports en commun")
        print("• Améliorer la qualité de vie et les espaces publics")
        print("• Lutter contre la spéculation immobilière")
        print("• Développer l'offre de logements sociaux et abordables")

def main():
    """Fonction principale pour Marseille"""
    # Liste des arrondissements de Marseille
    arrondissements = [str(i) for i in range(1, 17)]
    
    print("🏛️ ANALYSE DES COMPTES COMMUNAUX ET IMMOBILIERS - MARSEILLE ARRONDISSEMENTS (2002-2025)")
    print("=" * 75)
    
    # Demander à l'utilisateur de choisir un arrondissement
    print("Liste des arrondissements disponibles:")
    for i, arr in enumerate(arrondissements, 1):
        print(f"{i}. {arr}e arrondissement")
    
    try:
        choix = int(input("\nChoisissez le numéro de l'arrondissement à analyser: "))
        if choix < 1 or choix > len(arrondissements):
            raise ValueError
        arrondissement_selectionne = arrondissements[choix-1]
    except (ValueError, IndexError):
        print("Choix invalide. Sélection du 1er arrondissement par défaut.")
        arrondissement_selectionne = "1"
    
    # Initialiser l'analyseur
    analyzer = MarseilleArrondissementImmobilierAnalyzer(arrondissement_selectionne)
    
    # Générer les données
    financial_data = analyzer.generate_financial_data()
    
    # Sauvegarder les données
    output_file = f'{arrondissement_selectionne}e_arrondissement_marseille_data_2002_2025.csv'
    financial_data.to_csv(output_file, index=False)
    print(f"💾 Données sauvegardées: {output_file}")
    
    # Aperçu des données
    print("\n👀 Aperçu des données:")
    print(financial_data[['Annee', 'Population', 'Prix_m2_Moyen', 'Transactions_Immobilieres', 'Recettes_Totales']].head())
    
    # Créer l'analyse
    print("\n📈 Création de l'analyse financière et immobilière...")
    analyzer.create_financial_analysis(financial_data)
    
    print(f"\n✅ Analyse du {arrondissement_selectionne}e arrondissement de Marseille terminée!")
    print(f"📊 Période: {analyzer.start_year}-{analyzer.end_year}")
    print("🏠 Données: Démographie, finances, marché immobilier, investissements")

if __name__ == "__main__":
    main()