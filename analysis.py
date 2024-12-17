import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages

# Load data from CSV
filename = "data/serial_data_2024-12-18_00-06-09.csv"  # Ensure path is correct
df = pd.read_csv(filename)

# Parse the timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')

# Calculate statistics for numerical columns
stats = {}
for col in df.columns:
    if df[col].dtype in ['float64', 'int64']:  # Only calculate for numerical columns
        col_mean = df[col].mean()
        col_median = df[col].median()
        col_mode = df[col].mode().iloc[0] if not df[col].mode().empty else None
        col_std = df[col].std()
        col_cv = (col_std / col_mean * 100) if col_mean != 0 else 0
        stats[col] = {
            'Mean': col_mean,
            'Median': col_median,
            'Mode': col_mode,
            'Std Dev': col_std,
            'CV%': col_cv
        }

# Convert stats to a DataFrame for better formatting
stats_df = pd.DataFrame(stats).T
stats_df.reset_index(inplace=True)
stats_df.columns = ['Column', 'Mean', 'Median', 'Mode', 'Std Dev', 'CV%']

# Calculate total duration
start_time = df['timestamp'].iloc[0]
end_time = df['timestamp'].iloc[-1]
duration = end_time - start_time
duration_str = str(duration)

# Generate Plots
fig, axs = plt.subplots(2, 1, figsize=(10, 12))

# Subplot 1: fire_intesity vs Time
axs[0].plot(df['timestamp'], df['fire_intesity'], marker='o', color='red', label='Fire Intensity')
axs[0].set_title(f'Fire Intensity vs Time\n(Duration: {duration_str})')
axs[0].set_xlabel('Time (HH:MM:SS)')
axs[0].set_ylabel('Fire Intensity')
axs[0].legend()
axs[0].grid(True)
axs[0].tick_params(axis='x', rotation=45)

# Subplot 2: fire_detection vs Time
axs[1].plot(df['timestamp'], df['fire_detection'], marker='x', color='blue', label='Fire Detection')
axs[1].set_title(f'Fire Detection vs Time\n(Duration: {duration_str})')
axs[1].set_xlabel('Time (HH:MM:SS)')
axs[1].set_ylabel('Fire Detection')
axs[1].legend()
axs[1].grid(True)
axs[1].tick_params(axis='x', rotation=45)

plt.tight_layout()

# Save plots and stats to a PDF
# Windows-compatible file naming
base = os.path.basename(filename).split(".csv")[0].replace("serial_data_", "")
pdf_filename = os.path.join("reports", f"report_{base}.pdf")

# Create the reports folder if it doesn't exist
if not os.path.exists("reports"):
    os.makedirs("reports")

with PdfPages(pdf_filename) as pdf:
    # Add a new page with the stats table
    fig2, ax = plt.subplots(figsize=(8, 6))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=stats_df.values, colLabels=stats_df.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(stats_df.columns))))
    pdf.savefig(fig2)
    plt.close(fig2)
    
    # Save the plot figure
    pdf.savefig(fig)
    plt.close(fig)

print(f"[INFO] Report saved as {pdf_filename}")
