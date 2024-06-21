#!/bin/bash

if [ ! -f keys/*.json ]; then
    echo "Key file does not exist."
    echo "Please make sure the key file is in the keys directory, and named key.json"
    exit 1
fi

key_files=$(ls keys/*.json)

if [ $(echo $key_files | wc -w) -gt 1 ]; then
    echo "Multiple key files found in keys/ directory."

    while true; do
        echo "Please enter the name of the key file you would like to use, or press enter to use the first key file in the list."
        echo "Files found:"
        echo $key_files
        read key_file

        if [ -z $key_file ]; then
            key_file=$(echo $key_files | cut -d ' ' -f 1)
            break
        else 
            key_file="keys/$key_file"
            if [ -f $key_file ]; then
                break
            else
                echo "File does not exist. Please try again."
            fi
        fi
    done

else
    key_file="$key_files"
fi

echo "Encrypting key file..."

if [ ! -d encrypted_mnt/keys ]; then
    mkdir -p encrypted_mnt/keys
fi

if [ -z $GPG_PASSPHRASE ]; then
    echo "Please set the GPG_PASSPHRASE environment variable to the passphrase for the GPG key."
    exit 1
fi

gpg --quiet --batch --yes --passphrase="${GPG_PASSPHRASE}" --output=encrypted_mnt/keys/key.json.gpg -c $key_file
echo "Encrypted key file is stored in encrypted_mnt/keys/key.json"
echo "Delete it if you are done with mounting the encrypted_mnt/keys directory."
exit 0