import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    # Define columns for NSL-KDD based on its documentation
    columns = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
        'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins',
        'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
        'num_root', 'num_file_creations', 'num_shells', 'num_access_files',
        'num_outbound_cmds', 'is_host_login', 'is_guest_login', 'count',
        'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate',
        'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
        'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
        'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
        'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
        'dst_host_serror_rate', 'dst_host_srv_serror_rate',
        'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'attack_type', 'difficulty_level'
    ]

    print("--- PHASE 2: DATA UNDERSTANDING ---")
    print("Loading datasets...")
    # Load the dataset
    train_df = pd.read_csv(os.path.join(BASE_DIR, 'dataset', 'raw', 'KDDTrain+.txt'), names=columns)
    test_df = pd.read_csv(os.path.join(BASE_DIR, 'dataset', 'raw', 'KDDTest+.txt'), names=columns)
    
    print("\n1. Data Shape:")
    print(f"Training dataset shape: {train_df.shape}")
    print(f"Testing dataset shape: {test_df.shape}")
    
    print("\n2. Data Types (First 10 features):")
    print(train_df.dtypes.head(10))
    
    print("\n3. Unique Attack Types in Training Data:")
    unique_attacks = train_df['attack_type'].unique()
    print(f"Total Unique Attacks: {len(unique_attacks)}")
    print(unique_attacks)
    
    print("\n4. Class Distribution (Top 10 attack types):")
    print(train_df['attack_type'].value_counts().head(10))
    
    print("\n5. Feature Explanations (Sample):")
    feature_explanation = """
    - duration: length (number of seconds) of the connection
    - protocol_type: type of the protocol, e.g. tcp, udp, etc.
    - service: network service on the destination, e.g., http, telnet, etc.
    - flag: normal or error status of the connection
    - src_bytes: number of data bytes from source to destination
    - dst_bytes: number of data bytes from destination to source
    - attack_type: The label indicating if connection is normal or a specific attack
    - difficulty_level: assigned score for difficulty of predicting the connection
    """
    print(feature_explanation)
    
    # Save output to a report file
    os.makedirs(os.path.join(BASE_DIR, 'reports'), exist_ok=True)
    with open(os.path.join(BASE_DIR, 'reports', 'data_understanding_report.txt'), 'w') as f:
        f.write("--- DATA UNDERSTANDING REPORT ---\n")
        f.write(f"Training Shape: {train_df.shape}\n")
        f.write(f"Testing Shape: {test_df.shape}\n\n")
        f.write("Attack Types Distribution (Train):\n")
        f.write(train_df['attack_type'].value_counts().to_string())
        
    print("\nReport saved to reports/data_understanding_report.txt")

if __name__ == "__main__":
    main()
