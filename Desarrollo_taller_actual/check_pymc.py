import pymc as pm
import arviz as az
import pandas as pd
import numpy as np

df = pd.read_excel('../Taller actual/BaseUBER.xlsx')
df['total_matches_thousands'] = df['total_matches'] / 1000
df['Intercept'] = 1
X = df[['Intercept', 'treat', 'commute', 'total_matches_thousands']].values.astype(float)
y = df['total_driver_payout'].values.astype(float)

with pm.Model() as m:
    beta = pm.Normal('beta', mu=0, sigma=100_000, shape=4)
    sigma = pm.HalfNormal('sigma', sigma=100_000)
    mu = pm.math.dot(X, beta)
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
    trace = pm.sample(2000, random_seed=42, progressbar=False)

print(az.summary(trace))
