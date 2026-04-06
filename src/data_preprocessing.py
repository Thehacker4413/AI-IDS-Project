import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_data():
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

    train_df = pd.read_csv(os.path.join(BASE_DIR, 'dataset', 'raw', 'KDDTrain+.txt'), names=columns)
    test_df = pd.read_csv(os.path.join(BASE_DIR, 'dataset', 'raw', 'KDDTest+.txt'), names=columns)
    
    # Drop difficulty_level as it's not a real feature for classification
    train_df.drop('difficulty_level', axis=1, inplace=True)
    test_df.drop('difficulty_level', axis=1, inplace=True)
    
    return train_df, test_df

def map_attack_types(df):
    dos_attacks = ['apache2','back','land','neptune','mailbomb','pod','processtable','smurf','teardrop','udpstorm','worm']
    probe_attacks = ['ipsweep','mscan','nmap','portsweep','saint','satan']
    u2r_attacks = ['buffer_overflow','loadmodule','perl','ps','rootkit','sqlattack','xterm']
    r2l_attacks = ['ftp_write','guess_passwd','httptunnel','imap','multihop','named','phf','sendmail','snmpgetattack','snmpguess','spy','warezclient','warezmaster','xlock','xsnoop']
    
    def map_attack(attack):
        if attack in dos_attacks: return 'DoS'
        if attack in probe_attacks: return 'Probe'
        if attack in u2r_attacks: return 'U2R'
        if attack in r2l_attacks: return 'R2L'
        if attack == 'normal': return 'Normal'
        return 'Unknown'
        
    df['attack_category'] = df['attack_type'].apply(map_attack)
    df.drop('attack_type', axis=1, inplace=True)
    return df

def preprocess():
    print("--- PHASE 3: DATA PREPROCESSING ---")
    train_df, test_df = load_data()
    print(f"Initial Train shape: {train_df.shape}")
    print(f"Initial Test shape: {test_df.shape}")
    
    # Drop duplicates
    train_df.drop_duplicates(inplace=True)
    test_df.drop_duplicates(inplace=True)
    print(f"After dropping duplicates - Train: {train_df.shape}, Test: {test_df.shape}")
    
    # Map attacks to 5 main categories
    train_df = map_attack_types(train_df)
    test_df = map_attack_types(test_df)
    
    # Remove any rows with 'Unknown' attack category if they exist
    train_df = train_df[train_df['attack_category'] != 'Unknown']
    test_df = test_df[test_df['attack_category'] != 'Unknown']
    
    # Categorical encoding
    cat_columns = ['protocol_type', 'service', 'flag']
    encoders = {}
    
    for col in cat_columns:
        le = LabelEncoder()
        # Fit on combined data to ensure all possible categories in test are covered
        combined = pd.concat([train_df[col], test_df[col]], axis=0)
        le.fit(combined)
        train_df[col] = le.transform(train_df[col])
        test_df[col] = le.transform(test_df[col])
        encoders[col] = le
        
    # Scale numerical features using StandardScaler
    num_columns = [col for col in train_df.columns if col not in cat_columns and col != 'attack_category']
    scaler = StandardScaler()
    
    train_df[num_columns] = scaler.fit_transform(train_df[num_columns])
    test_df[num_columns] = scaler.transform(test_df[num_columns])
    
    # Label encode the target variable (attack_category)
    target_le = LabelEncoder()
    train_df['attack_category'] = target_le.fit_transform(train_df['attack_category'])
    test_df['attack_category'] = target_le.transform(test_df['attack_category'])
    encoders['target'] = target_le
    
    print("\nAttack classes encoded as:", dict(zip(target_le.classes_, target_le.transform(target_le.classes_))))
    
    # Save encoders and scaler for inference pipeline
    os.makedirs(os.path.join(BASE_DIR, 'models'), exist_ok=True)
    joblib.dump(scaler, os.path.join(BASE_DIR, 'models', 'scaler.pkl'))
    joblib.dump(encoders, os.path.join(BASE_DIR, 'models', 'encoders.pkl'))
    print("Scaler and Encoders saved to models/ directory.")
    
    # Save preprocessed datasets
    os.makedirs(os.path.join(BASE_DIR, 'dataset', 'processed'), exist_ok=True)
    train_df.to_csv(os.path.join(BASE_DIR, 'dataset', 'processed', 'train.csv'), index=False)
    test_df.to_csv(os.path.join(BASE_DIR, 'dataset', 'processed', 'test.csv'), index=False)
    print("Preprocessed Data saved to dataset/processed/train.csv and test.csv.")
    
if __name__ == '__main__':
    preprocess()
