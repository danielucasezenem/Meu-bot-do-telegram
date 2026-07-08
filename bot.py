from pathlib import Path
import importlib.util
import os

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

BASE_DIR = Path(__file__).parent

load_dotenv(BASE_DIR / "Infos" / "token.env")

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("O token não foi encontrado em Infos/token.env")

application = Application.builder().token(TOKEN).build()

comandos_pasta = BASE_DIR / "Comandos"

for comando in comandos_pasta.rglob("*.py"):

    if comando.name.startswith("_"):
        continue

    nome = comando.stem

    try:
        spec = importlib.util.spec_from_file_location(nome, comando)

        if spec is None or spec.loader is None:
            print(f"⚠️ Não foi possível carregar {comando}")
            continue

        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)

        if hasattr(modulo, "executar"):
            application.add_handler(
                CommandHandler(nome, modulo.executar)
            )

            print(
                f"✅ Comando /{nome} carregado "
                f"({comando.relative_to(BASE_DIR)})"
            )

        else:
            print(
                f"⚠️ {comando.relative_to(BASE_DIR)} "
                "não possui a função executar()."
            )

    except Exception as erro:
        print(f"❌ Erro ao carregar {comando}: {erro}")

print("🤖 Bot iniciado!")
application.run_polling()