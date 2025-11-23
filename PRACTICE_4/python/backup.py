import os
import time

def backup_v01(sources, target_dir):
    """Cria um backup usando a versão simples baseada em concatenação."""
    
    hoje = time.strftime('%Y%m%d%H%M%S')
    zipname = os.path.join(target_dir, hoje + '.zip')

    command = "zip -r {0} {1}".format(zipname, " ".join(sources))
    print("\n[backup_v01] Comando gerado:")
    print(command)

def backup_v02(sources, target_dir):
    """Cria backup com organização automática em pastas por dia."""

    dia = time.strftime('%Y%m%d')
    destino_dia = os.path.join(target_dir, dia)

    if not os.path.exists(destino_dia):
        os.makedirs(destino_dia)
    
    hora = time.strftime('%H%M%S')
    zipname = os.path.join(destino_dia, hora + '.zip')

    command = "zip -r {0} {1}".format(zipname, " ".join(sources))
    print("\n[backup_v02] Comando gerado:")
    print(command)

def backup_v03(sources, target_dir, comentario=""):
    """Permite adicionar comentário ao nome do ZIP."""

    dia = time.strftime('%Y%m%d')
    destino_dia = os.path.join(target_dir, dia)

    if not os.path.exists(destino_dia):
        os.makedirs(destino_dia)

    hora = time.strftime('%H%M%S')

    comentario = comentario.replace(" ", "_")
    zipname = os.path.join(destino_dia, f"{hora}_{comentario}.zip")

    command = "zip -r {0} {1}".format(zipname, " ".join(sources))
    print("\n[backup_v03] Comando gerado:")
    print(command)

if __name__ == "__main__":
    sources = ["./a01_aFunction.py", "./a02_anotherBehavior.py"]
    target = "./backups"

    backup_v01(sources, target)
    backup_v02(sources, target)
    backup_v03(sources, target, comentario="primeiro_backup")
