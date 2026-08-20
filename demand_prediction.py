import pandas as pd
from sklearn.linear_model import LinearRegression
from database import get_connection


connection = get_connection()

query = """
SELECT quantity_sold
FROM sales
ORDER BY sale_id
"""

df = pd.read_sql(query, connection)

connection.close()


X = [[i] for i in range(len(df))]
y = df["quantity_sold"]

model = LinearRegression()
model.fit(X, y)

next_sale = [[len(df)]]

prediction = model.predict(next_sale)

print("Predicted Demand:", round(prediction[0]))