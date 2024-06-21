#!/bin/bash

# Ask user for the key file to encrypt
while true; do
    echo "Please enter the path to the key file you would like to encrypt"
    read key_file

    if [ ! -f "$key_file" ]; then
        echo "Key file does not exist."
    else
        echo "Confirm the key file at $key_file? (y/n)"
        read confirm
        if [ $confirm = "y" ]; then
            break
        fi
    fi
done

# Encrypt the key file

while true; do

    echo "Enter your own encryption key"
    read -s user_key
    echo "Enter your own encryption key again"
    read -s user_key2

    if [ $user_key = $user_key2 ]; then
        break
    fi

    echo "The encryption keys do not match. Please try again."
done

echo "Encrypting key file..."

if [ $(pwd | awk -F'/' '{print $NF}') = "src" ]; then
    output_filepath="../mnt/encrypted_keys/key.json.gpg"
else
    if [ ! -d mnt/encrypted_keys ]; then
        mkdir -p mnt/encrypted_keys
    fi
    output_filepath="mnt/encrypted_keys/key.json.gpg"
fi

gpg --quiet --batch --yes --passphrase="${user_key}" --output=$output_filepath -c $key_file
echo "Encrypted key file is stored in $output_filepath."
echo "Delete it if you are done with mounting the the directory."
exit 0