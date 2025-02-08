import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from django.shortcuts import render, redirect
from .forms import UploadFileForm
import matplotlib.ticker as ticker

# Temporary storage location csv file
CLEANED_FILE_PATH = "media/uploads/dataset_cleaned.csv"

def upload_file(request):
    """Handle file upload and store cleaned data in session."""
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            df = pd.read_csv(file)

            # Data Cleaning
            cleaned_df = clean_data(df)

            # Save dataset to session in json format
            request.session["cleaned_df"] = df.to_json(orient="records")
            request.session.modified = True

            return redirect("dashboard")  # Redirect to dashboard page
    else:
        form = UploadFileForm()

    return render(request, "home.html", {"form": form})

def clean_data(df):

    #Handling Missing Value
    #Calculate the percentage of missing value per column
    missing_percentage = df.isnull().mean() * 100
    #Iteration of each column and handling according to the conditions
    for col in df.columns:
        if missing_percentage[col] == 0:
            continue  #If 0%, don't do anything
        elif missing_percentage[col] < 5:
            df = df.dropna(subset=[col])  #If <5%, delete lines that have missing values
        else:
            df[col] = df[col].fillna(df[col].mean())  #If ≥5%, fill with the mean column

    return df   

def save_plot_to_base64():
    """Save a Matplotlib figure to a Base64 image."""
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close()
    return image_base64

def generate_dashboard(df):
    """Generate dashboard visualizations and return Base64-encoded images."""
    charts = {}

    # Make sure the 'Invoice_date' column is a data type DATETIME
    df['invoice_date'] = pd.to_datetime(df['invoice_date'])
    # Group by date (Month) dan sum total sales
    sales_over_time = df.groupby(df['invoice_date'].dt.to_period('M'))['total_sales'].sum()
    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(sales_over_time.index.astype(str), sales_over_time.values, marker='o', linestyle='-', color='b')
    # Format axis Y
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: format_sales(x)))
    # Title and label
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Sales', fontsize=12)
    # Grid dan rotation label
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    charts["sales_over_time"] = save_plot_to_base64()

    # Plot
    plt.figure(figsize=(8, 6))
    ax = sns.scatterplot(x=df['quantity'], y=df['total_sales'], alpha=0.6, color='blue')
    plt.xlabel('Quantity')
    plt.ylabel('Total Sales')
    plt.grid(True)
    plt.tight_layout()
    charts["quantity_vs_total_sales"] = save_plot_to_base64()

    # Group data based on product_category and total sales
    sales_by_category = df.groupby('product_category')['total_sales'].sum().reset_index()
    # Plot
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='product_category', y='total_sales', data=sales_by_category, palette='viridis')
    # Format axis Y
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: format_sales(x)))
    # X-axis label rotation for better readability
    plt.xticks(rotation=45)
    plt.xlabel('Product Category')
    plt.ylabel('Total Sales')
    # Display the above value of each bar
    for p in ax.patches:
        formatted_value = format_sales(p.get_height())
        ax.annotate(formatted_value, (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                    textcoords='offset points')
    charts["sales_by_category"] = save_plot_to_base64()

    # Top 10 Customers
    top_customers = df.groupby("customer_id")["total_sales"].sum().nlargest(10).reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x="customer_id", y="total_sales", data=top_customers, palette="magma")
    plt.title("Top 10 Customers with Highest Sales")
    plt.xlabel("Customer ID")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    charts["top_customers"] = save_plot_to_base64()

    # Age Distribution
    age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
    age_labels = ['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '65+']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)
    age_distribution = df['age_group'].value_counts().sort_index()
    # Plot
    fig, ax = plt.subplots(figsize=(10, 7))  # Only one subplot
    sns.barplot(x=age_distribution.index, y=age_distribution.values, ax=ax, palette='pastel')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Total Customers')
    # Add the above value of each bar (age)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.0f}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                    textcoords='offset points')
    plt.tight_layout()
    charts["age_distribution"] = save_plot_to_base64()


   # Total sales
    total_sales = df["total_sales"].sum()
    charts["total_sales"] = format_sales(total_sales)

    # Total quantity
    total_quantity = df['quantity'].sum()
    charts['total_quantity'] = format_sales(total_quantity)

    return charts

def dashboard(request):
    """Load cleaned dataset from session and generate visualizations."""
    cleaned_json = request.session.get("cleaned_df", None)

    if cleaned_json is None:
        return render(request, "error.html", {"error": "No data available. Please upload a file first."})

    df = pd.read_json(cleaned_json)

    if df.empty:
        return render(request, "error.html", {"error": "Dataset is empty after loading from session."})

    charts = generate_dashboard(df)
    return render(request, "dashboard.html", {"charts": charts})

def format_sales(total_sales):
    """Format total sales into a more readable format (e.g., 20K+, 1.5M)."""
    if total_sales >= 1_000_000:
        return f"{total_sales / 1_000_000:.1f}M+"
    elif total_sales >= 1_000:
        return f"{total_sales / 1_000:.0f}K+"
    else:
        return f"{total_sales:.0f}"
