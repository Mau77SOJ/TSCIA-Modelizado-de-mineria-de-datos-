import pandas as pd 

# Simulated Dataset
data = {
        "Cliente_ID": range(1, 21), 
        "Genero": ["F", "M"] * 10, 
        "Edad": [23, 34, 45, 29, 31, 38, 27, 50, 40, 36, 25, 33, 46, 28, 39, 42, 30, 48, 35, 37], 
        "Recibio_Promo": ["Sí", "No", "Sí", "Sí", "No", "Sí", "No", "Sí", "No", "Sí", "No", "Sí", "Sí", "No", "No", "Sí", "No", "Sí", "No", "Sí"], 
        "Monto_Promocion": [500, 0, 700, 300, 0, 600, 0, 800, 0, 450, 0, 620, 710, 0, 0, 480, 0, 750, 0, 520], 
        "Recompra": ["Sí", "No", "Sí", "No", "No", "Sí", "No", "Sí", "No", "Sí", "No", "No", "Sí", "No", "No", "Sí", "No", "Sí", "No", "Sí"], 
        "Total_Compras": [2, 1, 3, 1, 1, 4, 1, 5, 1, 3, 1, 2, 4, 1, 1, 3, 1, 5, 1, 3], 
        "Ingreso_Mensual": [30000, 45000, 40000, 28000, 32000, 50000, 31000, 60000, 29000, 37000, 31000, 34000, 47000, 30000, 29000, 43000, 33000, 55000, 30000, 41000] 
        }

df = pd.DataFrame(data)

# Save to Excel
df.to_excel("Mini_Proyecto_Clientes_Promociones.xlsx", index=False)
print("Excel file generated with success.")