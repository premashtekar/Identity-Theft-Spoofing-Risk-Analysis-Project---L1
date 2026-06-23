import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
from haversine import haversine

fake = Faker()

# City database (included in the generation script)
CITIES = {
    'New York': {'lat': 40.7128, 'lon': -74.0060, 'country': 'USA'},
    'Los Angeles': {'lat': 34.0522, 'lon': -118.2437, 'country': 'USA'},
    'London': {'lat': 51.5074, 'lon': -0.1278, 'country': 'UK'},
    'Mumbai': {'lat': 19.0760, 'lon': 72.8777, 'country': 'India'},
    'Tokyo': {'lat': 35.6762, 'lon': 139.6503, 'country': 'Japan'},
    'Sydney': {'lat': -33.8688, 'lon': 151.2093, 'country': 'Australia'},
    'Paris': {'lat': 48.8566, 'lon': 2.3522, 'country': 'France'},
    'Singapore': {'lat': 1.3521, 'lon': 103.8198, 'country': 'Singapore'},
    'Dubai': {'lat': 25.2048, 'lon': 55.2708, 'country': 'UAE'},
    'Toronto': {'lat': 43.6532, 'lon': -79.3832, 'country': 'Canada'}
}

DEVICES = ['iPhone', 'Android Phone', 'Windows Laptop', 'MacBook', 'iPad', 'Android Tablet']
BROWSERS = ['Chrome', 'Firefox', 'Safari', 'Edge']

def generate_master_dataset(num_users=100, days=30, suspicious_percentage=15):
    """
    Generate ONE master dataset with all information
    """
    
    records = []
    
    for user_id in range(1, num_users + 1):
        # --- USER PROFILE INFORMATION ---
        home_city = random.choice(list(CITIES.keys()))
        
        # Each user has 2-3 trusted devices
        num_trusted_devices = random.randint(2, 3)
        trusted_devices = random.sample(DEVICES, num_trusted_devices)
        trusted_devices_str = ",".join(trusted_devices)
        
        # Each user has 1-2 trusted browsers
        num_trusted_browsers = random.randint(1, 2)
        trusted_browsers = random.sample(BROWSERS, num_trusted_browsers)
        trusted_browsers_str = ",".join(trusted_browsers)
        
        # --- LOGIN HISTORY ---
        num_logins = random.randint(20, 100)
        user_logins = []
        
        for _ in range(num_logins):
            # Random login time over 'days' period
            login_time = datetime.now() - timedelta(days=random.randint(0, days))
            login_time = login_time.replace(
                hour=random.randint(6, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
            
            # Determine login location
            # 70% from home city, 30% from random city
            if random.random() < 0.7:
                city = home_city
            else:
                city = random.choice(list(CITIES.keys()))
            
            lat, lon = CITIES[city]['lat'], CITIES[city]['lon']
            
            # Random device (sometimes suspicious!)
            if random.random() < 0.1:  # 10% chance of unusual device
                device = random.choice([d for d in DEVICES if d not in trusted_devices])
            else:
                device = random.choice(trusted_devices)
            
            # Random browser
            if random.random() < 0.1:  # 10% chance of unusual browser
                browser = random.choice([b for b in BROWSERS if b not in trusted_browsers])
            else:
                browser = random.choice(trusted_browsers)
            
            user_logins.append({
                'login_time': login_time,
                'city': city,
                'latitude': lat,
                'longitude': lon,
                'device': device,
                'browser': browser,
                'ip_address': fake.ipv4()
            })
        
        # --- INJECT SUSPICIOUS EVENTS ---
        # For suspicious_percentage of users, inject anomalies
        if user_id <= num_users * suspicious_percentage / 100 and len(user_logins) >= 3:
            
            # 1. IMPOSSIBLE TRAVEL (30 mins between far cities)
            if len(user_logins) >= 2:
                idx = random.randint(0, len(user_logins) - 2)
                far_city = random.choice([c for c in CITIES.keys() if c != user_logins[idx]['city']])
                user_logins[idx+1]['city'] = far_city
                user_logins[idx+1]['latitude'] = CITIES[far_city]['lat']
                user_logins[idx+1]['longitude'] = CITIES[far_city]['lon']
                user_logins[idx+1]['login_time'] = user_logins[idx]['login_time'] + timedelta(minutes=30)
                # Use unusual device for this login
                user_logins[idx+1]['device'] = random.choice([d for d in DEVICES if d not in trusted_devices])
            
            # 2. DEVICE SPOOFING (2 mins between different devices)
            if len(user_logins) >= 2:
                idx = random.randint(0, len(user_logins) - 2)
                user_logins[idx+1]['device'] = random.choice([d for d in DEVICES if d != user_logins[idx]['device']])
                user_logins[idx+1]['login_time'] = user_logins[idx]['login_time'] + timedelta(minutes=2)
            
            # 3. ODD HOUR LOGIN (3 AM)
            if len(user_logins) >= 1:
                idx = random.randint(0, len(user_logins) - 1)
                user_logins[idx]['login_time'] = user_logins[idx]['login_time'].replace(hour=3, minute=random.randint(0, 59))
        
        # --- Add user profile info to each login ---
        for login in user_logins:
            records.append({
                'user_id': f'USER_{user_id:04d}',
                'home_city': home_city,
                'trusted_devices': trusted_devices_str,
                'trusted_browsers': trusted_browsers_str,
                'login_time': login['login_time'],
                'city': login['city'],
                'latitude': login['latitude'],
                'longitude': login['longitude'],
                'device': login['device'],
                'browser': login['browser'],
                'ip_address': login['ip_address']
            })
    
    df = pd.DataFrame(records)
    df = df.sort_values(['user_id', 'login_time'])
    
    # Add flag for suspicious events (to be filled later)
    df['is_suspicious'] = 0
    
    return df

# Generate the master dataset
print("Generating master login dataset...")
df = generate_master_dataset(
    num_users=100,      # 100 users
    days=90,            # 90 days history
    suspicious_percentage=15  # 15% users with suspicious activity
)

# Save to single CSV
df.to_csv('master_login_data.csv', index=False)
print(f"✅ Generated {len(df)} login records")
print(f"📊 File size: {df.memory_usage(deep=True).sum() / 1_000_000:.2f} MB")

# Display summary
print("\n📈 Dataset Summary:")
print(f"  - Users: {df['user_id'].nunique()}")
print(f"  - Total logins: {len(df)}")
print(f"  - Unique cities: {df['city'].nunique()}")
print(f"  - Unique devices: {df['device'].nunique()}")
print(f"  - Date range: {df['login_time'].min()} to {df['login_time'].max()}")

print("\n👤 Sample Data:")
print(df.head())
