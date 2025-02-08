import pandas as pd
from io import StringIO
from datetime import datetime

def clean_sales_data(csv_data):
    """ Membersihkan dataset sebelum disimpan ke database """
    
    # Load CSV ke DataFrame
    df = pd.read_csv(StringIO(csv_data))
 
    # Pastikan kolom yang diperlukan ada
    required_columns = ["customer_id", "gender", "age", "product_category", "quantity", "invoice_date", "unit_price", "total_sales"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError("customer_id", "gender", "age", "product_category", "quantity", "invoice_date", "unit_price")

    # Hapus duplikasi
    df = df.drop_duplicates()

    # Hitung persentase missing value per kolom
    missing_percentage = df.isnull().mean() * 100

    # Iterasi setiap kolom dan lakukan handling sesuai kondisi
    for col in df.columns:
        if missing_percentage[col] == 0:
            continue  # Jika 0%, tidak lakukan apa-apa
        elif missing_percentage[col] < 5:   
            df = df.dropna(subset=[col])  # Jika <5%, hapus baris yang memiliki missing values
        else:
            df[col] = df[col].fillna(df[col].mean())  # Jika ≥5%, isi dengan mean kolom

    # Konversi tipe data
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    #df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    #df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce")

    # Hapus baris dengan tanggal tidak valid
    #df = df.dropna(subset=["date"])

    return df
