import matplotlib.pyplot as plt
import networkx as nx
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# -----------------------------
# 1. Build the Bayesian Network
# -----------------------------
bn = DiscreteBayesianNetwork([
    ('TechFail', 'SQLi'),
    ('DefFail',  'SQLi'),
    ('SQLi',     'DataLeak')
])

# Prior: Technical Failures (e.g. unsafe input)
cpd_tech = TabularCPD(variable='TechFail', variable_card=2, values=[[0.65], [0.35]])
# Prior: Defense Failures (e.g. missing WAF)
cpd_def  = TabularCPD(variable='DefFail', variable_card=2, values=[[0.55], [0.45]])

# SQLi Conditional Probability Table (TechFail & DefFail)
cpd_sqli = TabularCPD(
    variable='SQLi', variable_card=2,
    values=[
        [0.99, 0.60, 0.50, 0.10],  # SQLi = False
        [0.01, 0.40, 0.50, 0.90]   # SQLi = True
    ],
    evidence=['TechFail', 'DefFail'],
    evidence_card=[2, 2]
)

# DataLeak conditional on SQLi
cpd_leak = TabularCPD(
    variable='DataLeak', variable_card=2,
    values=[
        [0.95, 0.20],  # No leak
        [0.05, 0.80]   # Leak
    ],
    evidence=['SQLi'],
    evidence_card=[2]
)

# Add all CPDs
bn.add_cpds(cpd_tech, cpd_def, cpd_sqli, cpd_leak)
assert bn.check_model()

# -----------------------------
# 2. Inference Examples
# -----------------------------
infer = VariableElimination(bn)

p_leak = infer.query(['DataLeak']).values[1]
p_leak_given_def_safe = infer.query(['DataLeak'], evidence={'DefFail': 0}).values[1]

print("P(DataLeak) =", round(p_leak, 4))
print("P(DataLeak | DefFail=F) =", round(p_leak_given_def_safe, 4))

# -----------------------------
# 3. Draw Bayesian Network Structure
# -----------------------------
def draw_bn_structure(model, filename="bayesian_network_structure.png"):
    import networkx as nx
    import matplotlib.pyplot as plt

    # Manually create a directed graph from edges
    g = nx.DiGraph()
    g.add_edges_from(model.edges())

    pos = nx.spring_layout(g, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(
        g, pos, with_labels=True,
        node_size=2500, node_color='lightblue',
        font_size=12, font_weight='bold',
        arrowsize=20
    )
    plt.title("Bayesian Network Structure", fontsize=14)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

draw_bn_structure(bn)
