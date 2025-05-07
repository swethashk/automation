import subprocess
import os

def get_modulus(file_path, file_type):
    """
    Extracts the modulus value of a certificate or private key using OpenSSL.

    Args:
        file_path (str): Path to the certificate or private key file.
        file_type (str): Type of the file ('certificate' or 'private_key').

    Returns:
        str: Modulus value as a string, or None if an error occurs.
    """
    try:
        if file_type == 'certificate':
            command = ["openssl", "x509", "-noout", "-modulus", "-in", file_path]
        elif file_type == 'private_key':
            command = ["openssl", "rsa", "-noout", "-modulus", "-in", file_path]
        else:
            raise ValueError("Invalid file type specified.")
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # Extract the modulus part after "Modulus="
        return result.stdout.strip().split('=')[-1]
    except subprocess.CalledProcessError as e:
        print(f"Error: OpenSSL command failed for {file_path}: {e.stderr}")
    except Exception as e:
        print(f"Error: {e}")
    return None

def main():
    print("Certificate and Private Key Modulus Checker")
    cert_path = input("Enter the path to the certificate (.pem) file: ").strip()
    key_path = input("Enter the path to the private key file: ").strip()

    if not os.path.exists(cert_path) or not os.path.exists(key_path):
        print("Error: One or both file paths do not exist.")
        return

    cert_modulus = get_modulus(cert_path, "certificate")
    key_modulus = get_modulus(key_path, "private_key")

    if cert_modulus and key_modulus:
        if cert_modulus == key_modulus:
            print("Success: The certificate and private key match (modulus values are identical).")
        else:
            print("Error: The certificate and private key do not match (modulus values differ).")
    else:
        print("Error: Could not retrieve modulus values for one or both files.")

if __name__ == "__main__":
    main()
