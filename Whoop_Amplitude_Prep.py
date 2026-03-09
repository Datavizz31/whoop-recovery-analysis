import pandas as pd

# Load the real WHOOP data
df = pd.read_csv('processed_whoop_data.csv')

# Check it loaded correctly
print(df.shape)
print(df['Period'].value_counts())
# Give our user a consistent ID
df['user_id'] = 'whoop_user_001'

# Rename columns to cleaner event property names
df = df.rename(columns={
    'Recovery score %': 'recovery_score',
    'Heart rate variability (ms)': 'hrv',
    'Day Strain': 'strain',
    'Deep sleep %': 'deep_sleep_pct',
    'REM sleep %': 'rem_sleep_pct',
    'Sleep efficiency %': 'sleep_efficiency',
    'Sleep performance %': 'sleep_performance'
})

# Check the rename worked
print(df[['user_id', 'Date', 'Period', 'recovery_score', 
          'hrv', 'strain']].head(5))
# Each day becomes one event called 'daily_recovery_logged'

events = pd.DataFrame({
    'user_id': df['user_id'],
    'event_type': 'daily_recovery_logged',
    'event_time': df['Date'],
    'recovery_score': df['recovery_score'],
    'hrv': df['hrv'],
    'strain': df['strain'],
    'deep_sleep_pct': df['deep_sleep_pct'],
    'rem_sleep_pct': df['rem_sleep_pct'],
    'sleep_efficiency': df['sleep_efficiency'],
    'period': df['Period']
})

print(f"Total events created: {len(events)}")
print(events.head(3))
def get_ai_recommendation(recovery_score, hrv, strain, period):
    # Determine recovery zone
    if recovery_score >= 67:
        zone = "green"
    elif recovery_score >= 34:
        zone = "yellow"
    else:
        zone = "red"
    
    # Base recommendation on zone
    if zone == "green":
        rec = f"Recovery strong at {recovery_score}%. HRV {hrv}ms indicates good nervous system readiness. Safe to take on high strain today."
    elif zone == "yellow":
        rec = f"Recovery moderate at {recovery_score}%. HRV {hrv}ms is within normal range. Moderate your training and prioritize sleep tonight."
    else:
        rec = f"Recovery low at {recovery_score}%. HRV {hrv}ms suggests fatigue. Rest or light activity only. Focus on sleep quality."
    
    # Add habit context
    if period == "Milk before bed":
        rec += " Milk experiment active — monitor if sleep quality improves tonight."
    elif period == "Coffee every morning":
        rec += " Coffee experiment active — note any changes in morning HRV trend."
    
    return rec

# Test it with one row
print(get_ai_recommendation(45, 58, 14, "Baseline"))
# Apply recommendation to every row
events['ai_recommendation'] = events.apply(
    lambda row: get_ai_recommendation(
        row['recovery_score'],
        row['hrv'],
        row['strain'],
        row['period']
    ), axis=1
)
# Shift dates to current month so Amplitude free plan can see them
# Original data: Nov-Dec 2024 → shifted to Feb-Mar 2026
events['event_time'] = pd.to_datetime(
    events['event_time']
) + pd.DateOffset(months=15)

print(events['event_time'].head(5))

# Check it worked
print(events[['event_time', 'recovery_score',
              'period', 'ai_recommendation']].head(3))
# Export to CSV for Amplitude import
events.to_csv('whoop_amplitude_events.csv', index=False)
print(f"Exported {len(events)} events to whoop_amplitude_events.csv")
print(events.columns.tolist())
