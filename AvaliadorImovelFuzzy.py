#pip install scikit-fuzzy
#pip install matplotlib
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

### DADOS NECESSARIOS PARA FUZZIFICACAO
tamanho = ctrl.Antecedent(np.arange(20, 351, 1), 'tamanho') #metros quadrados do ap
qualidade = ctrl.Antecedent(np.arange(0, 11, 1), 'qualidade') #qualidade do ap
valor = ctrl.Consequent(np.arange(50, 1001, 1), 'valor') #valor estimado

qualidade.automf(3) #(3, 5, or 7) classes equidistantes
# Funcoes customizadas
tamanho["kitnet"] = fuzz.trapmf(tamanho.universe, [20, 20, 35, 45])
tamanho['small'] = fuzz.trapmf(tamanho.universe, [35, 45, 75, 85]) 
tamanho['average'] = fuzz.trapmf(tamanho.universe, [75, 85, 140, 150])
tamanho['big'] = fuzz.trapmf(tamanho.universe, [140, 150, 350, 350])
                                                # k unidades | aluguel equivalente 0,4% do valor do imovel
valor['low_price'] = fuzz.trapmf(valor.universe, [50, 50, 105 ,125])
valor['low_medium_price'] = fuzz.trapmf(valor.universe, [105, 125, 157.5, 177.5])
valor['medium_price'] = fuzz.trapmf(valor.universe, [157.5, 177.5 , 317.5, 337.5])
valor['high_price'] = fuzz.trapmf(valor.universe, [317.5, 337.5, 600, 675])
valor['very_high_price'] = fuzz.trapmf(valor.universe, [500, 900, 1000, 1000])


### REGRAS UTILIZADAS PARA INFERENCIA
rule1 = ctrl.Rule(tamanho['kitnet'] & qualidade['poor'], valor['low_price'])
rule2 = ctrl.Rule(tamanho['small'] & qualidade['poor'], valor['low_medium_price'])
rule3 = ctrl.Rule(tamanho['average'] & qualidade['poor'], valor['medium_price'])
rule4 = ctrl.Rule(tamanho['big'] & qualidade['poor'], valor['high_price'])

rule5 = ctrl.Rule(tamanho['kitnet'] & qualidade['average'], valor['low_price'])
rule6 = ctrl.Rule(tamanho['small'] & qualidade['average'], valor['low_medium_price'])
rule7 = ctrl.Rule(tamanho['average'] & qualidade['average'], valor['medium_price'])
rule8 = ctrl.Rule(tamanho['big'] & qualidade['average'], valor['high_price'])

rule9 = ctrl.Rule(tamanho['kitnet'] & qualidade['good'], valor['low_medium_price'])
rule10 = ctrl.Rule(tamanho['small'] & qualidade['good'], valor['medium_price'])
rule11 = ctrl.Rule(tamanho['average'] & qualidade['good'], valor['high_price'])
rule12 = ctrl.Rule(tamanho['big'] & qualidade['good'], valor['very_high_price'])

tipping_ctrl = ctrl.ControlSystem(eval("rule" + str(x)) for x in range(1,13))
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)


### ENTRADA DOS DADOS
tipping.input['tamanho'] = float(input("Tamanho do imovel em m² [20-350]: "))
tipping.input['qualidade'] = float(input("Qualidade [0-10]: "))
### COMPUTA OS RESULTADOS E DEFUZZIFICA POR CENTROIDE
tipping.compute()


### PRINTS E RESULTADOS
from decimal import Decimal
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR')
resultado = Decimal(str(tipping.output['valor'] * 1000))
print("\nValor estimado: ", locale.currency(resultado, grouping=True))
print("Aluguel estimado: ", locale.currency(resultado/250, grouping=True))

tamanho.view()
qualidade.view()
valor.view(sim=tipping)
plt.show()