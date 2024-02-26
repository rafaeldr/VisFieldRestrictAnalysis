import numpy as np
import pandas as pd
import itertools
from typing import List

def outlier_iqr(data : pd.Series) -> List[int]:
	
	# Calculate os quartiles and IQR (Interquartile Range)
	q1 = np.percentile(data, 25)
	q3 = np.percentile(data, 75)
	iqr = q3 - q1

	lower_bound = q1 - 1.5 * iqr
	upper_bound = q3 + 1.5 * iqr

	filtered_data = [x for x in data if lower_bound <= x <= upper_bound]
	
	outliers = [x for x in data if x not in filtered_data]
	outliers_idx = list(itertools.chain.from_iterable([data[data==x].index.to_list() for x in outliers]))

	return outliers_idx