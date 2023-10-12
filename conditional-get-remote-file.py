import paramiko

# Define a list of server details (hostname, username, and private key file path)
server_list = [
    {"hostname": "server1", "username": "your_username", "private_key_file": "/path/to/private_key"},
    {"hostname": "server2", "username": "your_username", "private_key_file": "/path/to/private_key"},
    # Add other servers as needed
]

# Append the domain for each server
for server_info in server_list:
    server_info["hostname"] = f"{server_info['hostname']}.domain.name"

# Iterate over the server list and perform the SSH operation on each server
for server_info in server_list:
    hostname = server_info["hostname"]
    username = server_info["username"]
    private_key_file = server_info["private_key_file"]

    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Attempt to connect on port 22
            ssh.connect(hostname, username=username, pkey=private_key, port=22)
        except:
            # If port 22 fails, attempt to connect on port 2022
            ssh.connect(hostname, username=username, pkey=private_key, port=2022)


        # Check the Red Hat version
        command = "if [ -f /etc/redhat-release ]; then cat /etc/redhat-release; fi"
        stdin, stdout, stderr = ssh.exec_command(command)
        redhat_release = stdout.read().decode('utf-8').strip()

        # Depending on the Red Hat version, execute the appropriate command
        if "Red Hat Enterprise Linux Server 7" in redhat_release:
            cat_command = "cat /etc/hosts"
        elif "Red Hat Enterprise Linux Server 8" in redhat_release or "Red Hat Enterprise Linux Server 9" in redhat_release:
            cat_command = "cat /etc/hosts2"
        else:
            print(f"Unsupported Red Hat version on '{hostname}': {redhat_release}")
            continue

        # Execute the appropriate 'cat' command
        stdin, stdout, stderr = ssh.exec_command(cat_command)

        # Read the output
        output = stdout.read().decode('utf-8')

        # Save the output to a file named after the hostname
        filename = f"{hostname}_hosts.txt"
        with open(filename, "w") as file:
            file.write(output)

        # Close the SSH connection
        ssh.close()

        print(f"Host '{hostname}' output saved to '{filename}'")

    except Exception as e:
        print(f"Error on host '{hostname}': {str(e)}")
        continue
