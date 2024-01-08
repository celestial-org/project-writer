import paramiko
import time

def install_endpoint(hostname, username, password, ssh_port, http_port):
  try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, ssh_port, username, password)
    docker_command = f'docker run -d -p {http_port}:8080 mymaking/test-endpoint:main'
    stdin, stdout, stderr = ssh.exec_command(docker_command)
    result = stdout.read().decode('utf-8')
    while not stdout.channel.exit_status_ready():
        time.sleep(1)
        ssh.close()
        return f"Docker đã chạy thành công với mã: {stdout.channel.recv_exit_status()}```shell\n{result}\n```"
        
  except Exception as e:
    raise Exception(str(e))
    
def run_cmd(hostname, username, password, ssh_port, cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, ssh_port, username, password)
        stdin, stdout, stderr = ssh.exec_command(cmd)

        output = stdout.read().decode('utf-8')
        errors = stderr.read().decode('utf-8')

        exit_status = stdout.channel.recv_exit_status()
        ssh.close()

        if exit_status == 0:
            return output
        else:
            raise Exception(f"Command execution failed with error: {errors}")

    except Exception as e:
        raise Exception(f"Error: {e}")