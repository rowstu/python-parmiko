import paramiko

# Define a list of server details (hostname without domain, username, and private key file path)
server_list = [
    {"hostname": "server1", "username": "your_username", "private_key_file": "/path/to/private_key"},
    {"hostname": "server2", "username": "your_username", "private_key_file": "/path/to/private_key"},
    # Add more servers as needed
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

        # Load the private key for authentication
        private_key = paramiko.RSAKey(filename=private_key_file)

        # Connect to the server using the private key
        ssh.connect(hostname, username=username, pkey=private_key)

        # Execute the command
        command = "cat /etc/hosts"
        stdin, stdout, stderr = ssh.exec_command(command)

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
