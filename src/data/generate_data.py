import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_dirty_telemetry(days=14, interval_minutes=5):
    """
    Generates a realistic, dirty time-series telemetry dataset with missing fields,
    malformed rows, unparsed data types, and deliberate format corruptions.
    """
    print(f"Generating dirty production telemetry for {days} days...")
    
    # Calculate absolute baseline timestamps
    start_time = datetime(2026, 7, 10, 0, 0, 0)
    total_intervals = int(days * 24 * 60 / interval_minutes)
    
    # 1. Structural Component Vectors
    services = ['auth-api', 'payment-service', 'inventory-db', 'frontend-web']
    regions = ['us-east', 'us-west', 'eu-central', 'ap-southeast']
    versions = ['v1.2.4', 'v1.2.5', 'v1.3.0-rc1']
    
    data_list = []
    
    for i in range(total_intervals):
        current_time = start_time + timedelta(minutes=i * interval_minutes)
        
        # Pick dimensional context
        service = np.random.choice(services)
        region = np.random.choice(regions)
        version = np.random.choice(versions)
        
        # Dynamic baseline behaviors (Cyclical components)
        hour_val = current_time.hour
        day_name = current_time.strftime('%A')
        time_factor = np.sin(2 * np.pi * hour_val / 24.0)
        
        # Default normal metric distributions
        users = int(400 + 200 * time_factor + np.random.normal(0, 30))
        users = max(10, users)
        
        req_count = int(users * np.random.uniform(2.0, 3.5))
        cpu = 45.0 + 15.0 * time_factor + np.random.normal(0, 4)
        memory = 55.0 + 5.0 * time_factor + np.random.normal(0, 2)
        disk = 70.0 + (i / total_intervals) * 12.0 + np.random.normal(0, 0.5) # Creeping disk fill
        disk_io = 50.0 + 30.0 * time_factor + np.random.normal(0, 10)
        net_in = 20.0 + 15.0 * time_factor + np.random.normal(0, 3)
        net_out = 15.0 + 12.0 * time_factor + np.random.normal(0, 2)
        resp_time = 120.0 + 40.0 * time_factor + np.random.normal(0, 15)
        error = np.random.exponential(0.01)
        
        anomaly_type = "none"
        is_anomaly = 0
        
        # 2. Inject Anomaly Signatures
        # CPU Spike incident (around 20% into dataset)
        if int(total_intervals * 0.20) <= i <= int(total_intervals * 0.22):
            cpu += np.random.uniform(35.0, 45.0)
            resp_time += np.random.uniform(100.0, 250.0)
            anomaly_type = "cpu_spike"
            is_anomaly = 1
            
        # Memory Leak incident (around 50% into dataset)
        elif int(total_intervals * 0.50) <= i <= int(total_intervals * 0.55):
            leak_progression = (i - int(total_intervals * 0.50)) / (total_intervals * 0.05)
            memory += leak_progression * 35.0
            anomaly_type = "memory_leak"
            is_anomaly = 1
            
        # Downstream Network Link Surge (around 80% into dataset)
        elif int(total_intervals * 0.80) <= i <= int(total_intervals * 0.82):
            resp_time += np.random.uniform(600.0, 1200.0)
            error += np.random.uniform(0.15, 0.40)
            net_out += np.random.uniform(80.0, 150.0)
            anomaly_type = "latency_surge"
            is_anomaly = 1

        # 3. Inject Dirty Data Corruptions (Real-world structural noise)
        rand_draw = np.random.random()
        
        # Format Timestamp string variations (Unparsed string pollution)
        if rand_draw < 0.02:
            ts_str = current_time.strftime('%Y/%m/%d %H:%M:%S')  # Bad delimiter switch
        elif rand_draw < 0.04:
            ts_str = current_time.strftime('%d-%m-%Y %H:%M:%S')  # Day-First inversion
        else:
            ts_str = current_time.strftime('%Y-%m-%d %H:%M:%S')  # Target regular standard
            
        # Inject Out-Of-Bounds Sensor Failures (NaN and extreme value drops)
        if rand_draw > 0.98:
            cpu = np.nan          # Missing metrics
        if 0.96 < rand_draw <= 0.98:
            memory = 999.9        # Impossible telemetry hardware error spike
        if 0.95 < rand_draw <= 0.96:
            error = -1.0          # Broken software log status value
            
        # Introduce categorical nulls and casing inconsistencies
        if rand_draw < 0.01:
            service = None
        if 0.01 <= rand_draw < 0.02:
            region = region.upper() # Inconsistent casing string values (e.g. US-EAST)

        # Assemble individual dictionary records
        record = {
            "timestamp": ts_str,
            "cpu_usage": np.round(cpu, 1) if not np.isnan(cpu) else np.nan,
            "memory_usage": np.round(memory, 1),
            "disk_usage": np.round(disk, 1),
            "disk_io": np.round(disk_io, 1),
            "network_in": np.round(net_in, 1),
            "network_out": np.round(net_out, 1),
            "response_time": int(resp_time),
            "request_count": int(req_count),
            "error_rate": np.round(error, 3),
            "active_users": int(users),
            "service_name": service,
            "region": region,
            "deployment_version": version,
            "day_of_week": day_name,
            "hour": int(hour_val),
            "anomaly_type": anomaly_type,
            "is_anomaly": is_anomaly
        }
        data_list.append(record)
        
        # Inject Duplicate Timestamps (Simulated pipeline retries / Race conditions)
        if 0.35 < rand_draw <= 0.36:
            duplicate_record = record.copy()
            # Slightly change metric to simulate near-simultaneous scraping logs
            duplicate_record["cpu_usage"] = np.round(cpu * 1.02, 1) if not np.isnan(cpu) else np.nan
            data_list.append(duplicate_record)

    df = pd.DataFrame(data_list)
    return df

if __name__ == "__main__":
    output_dir = os.path.join("data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    
    dirty_df = generate_dirty_telemetry()
    output_path = os.path.join(output_dir, "metrics.csv")
    dirty_df.to_csv(output_path, index=False)
    
    print(f"\nDirty data generation complete. Saved {len(dirty_df)} rows to: {output_path}")
    print("\nVisual preview of raw output:")
    print(dirty_df.iloc[50:56][["timestamp", "cpu_usage", "memory_usage", "service_name", "region"]])
