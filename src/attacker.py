import random
import pandas as pd

def generate_traffic(num_samples=200):
    data = []

    for _ in range(num_samples):
        attack_type = random.choice(["normal", "port_scan", "brute_force"])

        if attack_type == "normal":
            packet_size = random.randint(40, 1500)
            duration = random.uniform(0.1, 1.0)
            failed_logins = 0

        elif attack_type == "port_scan":
            packet_size = random.randint(40, 100)
            duration = random.uniform(0.01, 0.1)
            failed_logins = random.randint(0, 2)

        else:  # brute force
            packet_size = random.randint(200, 500)
            duration = random.uniform(0.5, 2.0)
            failed_logins = random.randint(5, 20)

        data.append([packet_size, duration, failed_logins, attack_type])

    df = pd.DataFrame(data, columns=["packet_size", "duration", "failed_logins", "label"])
    df.to_csv("traffic.csv", index=False)

    print("Traffic generated!")

if __name__ == "__main__":
    generate_traffic()

#Simulates AI attacker → generates fake network traffic → saves it → used for training defense model

#This module simulates different types of network traffic including normal behavior, port scanning, and brute-force attacks. 
# It generates realistic feature patterns such as packet size, duration, and failed login attempts, 
# which are then used to train our intrusion detection system. 
# These features were chosen because they are commonly used 
# indicators in network security — for example, high failed login attempts
#  indicate brute-force attacks, while very short connection
#  durations indicate port scanning.