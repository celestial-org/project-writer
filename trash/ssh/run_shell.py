import paramiko
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from database import SSH


def run_cmd(hostname: str, username: str, password: str, ssh_port: int, cmd: str):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, ssh_port, username, password)
        stdin, stdout, stderr = ssh.exec_command(cmd)

        output = stdout.read().decode("utf-8")
        errors = stderr.read().decode("utf-8")

        exit_status = stdout.channel.recv_exit_status()
        ssh.close()

        if exit_status == 0:
            return output
        else:
            raise Exception(f"Command execution failed with error: {errors}")

    except Exception as e:
        raise Exception(f"Error: {e}")


def _shell(_, __, m):
    return m.text and m.text.startswith(".") and m.text.replace(".", "") is not None


@Client.on_message(filters.create(_shell))
def run_shell_command(c, m):
    ssh = SSH(m.from_user.id)
    m.reply_chat_action(ChatAction.TYPING)
    try:
        if not m.text.replace(".", "").replace(" ", ""):
            raise Exception(
                "Thiếu lệnh và tên máy.\nHãy thực hiện theo mẫu: `.machine0 echo Hello, World`"
            )
        machine = m.text.split(" ")[0].replace(".", "")
        shell_cmd = m.text.split(" ", 1)[1]
        host, sshuser, passwd, port = ssh.get(machine)
        result = run_cmd(host, sshuser, passwd, port, shell_cmd)
        max_length = 4000
        if len(result) > max_length:
            parts = [
                result[i : i + max_length] for i in range(0, len(result), max_length)
            ]
            for i, part in enumerate(parts, start=1):
                m.reply(f"{i}```bash\n{part}\n```", quote=True)
        else:
            m.reply(f"```bash\n{result}\n```", quote=True)
    except Exception as e:
        m.reply(f"```bash\n{e}\n```", quote=True)
