#!/bin/bash

while true; do
    base_path=$(pwd | awk -F'/' '{print $NF}')
    if [ $base_path = "src" ] || [ $base_path = "app" ]; then
        if [ -d ../mnt/encrypted_keys ]; then
            default_key_file=$(find ../mnt/encrypted_keys -type f -name "*.json" | head -n 1)
            key_base_dir="../mnt/encrypted_keys"
        fi
    else
        if [ -d mnt/encrypted_keys ]; then
            default_key_file=$(find mnt/encrypted_keys -type f -name "*.json" | head -n 1)
            key_base_dir="mnt/encrypted_keys"
        fi
    fi
    
    if [ -f "$default_key_file" ]; then
        echo "The mounted key file is detected at $default_key_file. Do you want to use this key file? (y/n)"
        read use_default_key_file
        if [ $use_default_key_file = "y" ]; then
            key_file="$default_key_file"
        fi
    else
        echo "Current path: $(pwd)"
        echo "Please enter the path to the key file you would like to encrypt."
        read key_file
    fi

    if [ ! -f "$key_file" ]; then
        echo "Key file does not exist."
    else
        echo "Confirm the key file: $key_file (y/n)"
        read confirm
        if [ $confirm = "y" ]; then
            break
        fi
    fi
done

echo "We will encrypt the key file to protect your data. Make sure to use the same encryption key that you passed/or will pass to the program to decrypt."

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

if [ $key_file = $default_key_file ]; then
    output_filepath="$key_base_dir/key.json.gpg"
else
    if [ ! -d mnt/encrypted_keys ]; then
        mkdir -p mnt/encrypted_keys
    fi
    output_filepath="mnt/encrypted_keys/key.json.gpg"
fi

gpg --quiet --batch --yes --passphrase="${user_key}" --output=$output_filepath -c $key_file
echo "Encrypted key file is stored in $output_filepath. (You can delete it when you want the program to stop using the key file.)"
echo ""
echo "The program will no longer use the original key file. Do you want to delete the original key file "$key_file"? (y/n)"
read delete_key_file

if [ $delete_key_file = "y" ]; then
    rm $key_file
    echo "Key file deleted."
else 
    if [ $key_file = $default_key_file ]; then
    echo "It seems like you mounted the key file. We recommend deleting it for security reasons."
    echo "Do you want to delete the original key file "$key_file"? (y/n)"
    read delete_key_file
        if [ $delete_key_file = "y" ]; then
            rm $key_file
            echo "Key file deleted."
        else
            echo "Key file is not deleted."
            echo "You can delete it manually by running 'rm $key_file' or from the file explorer."
        fi
    fi
fi

exit 0