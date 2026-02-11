import runpy

def executar_calibracao():
    runpy.run_module("src.calibrar", run_name="__main__")


def executar_reconhecimento():
    runpy.run_module("src.libra", run_name="__main__")


if __name__ == "__main__":
    print("Escolha uma opção:")
    print("1. Calibrar (Adicionar/Atualizar letras)")
    print("2. Iniciar reconhecimento")
    print("3. Sair")
    escolha = input("Digite 1, 2 ou 3: ").strip()

    if escolha == "1":
        executar_calibracao()
    elif escolha == "2":
        executar_reconhecimento()
    elif escolha =="3":
        exit()
    else:
        print("Opção inválida. Encerrando.")