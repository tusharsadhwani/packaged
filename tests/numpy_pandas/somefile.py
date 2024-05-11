import numpy as np
import pandas as pd

data = np.linspace(-5, 5, 10)
df = pd.DataFrame(data)
print(df[1:5].mean())
