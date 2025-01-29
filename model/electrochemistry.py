"""
electrochemistry.py
Implements Butler-Volmer equation for current density:
  i = i0 * [ exp(alpha_a * F * eta / (R*T)) - exp(-alpha_c * F * eta / (R*T)) ]
"""

import math

def butler_volmer_current(i0, alpha_a, alpha_c, F, R, T, overpotential):
    """
    i0          : exchange current density (A/m^2)
    alpha_a     : anodic transfer coefficient
    alpha_c     : cathodic transfer coefficient
    F           : Faraday constant (~96485 C/mol)
    R           : gas constant (~8.314 J/(mol K))
    T           : absolute temperature (K)
    overpotential : (V), potential difference from equilibrium
    """
    term1 = math.exp((alpha_a * F * overpotential) / (R*T))
    term2 = math.exp((-alpha_c * F * overpotential) / (R*T))
    current = i0 * (term1 - term2)
    return current

