import pandas as pd
import pulp as pp


def preencher_tabela():
    macarrao = pd.DataFrame(columns=['Nome', 'Preço', 'Mínimo', 'Máximo'])

    while True:
        r = input("Deseja adicionar um ingrediente? (s/n): ").strip().lower()
        
        if r == 's':
            nome = input("Digite o nome do ingrediente: ").strip()

            while True:
                try:
                    preco = float(input("Digite o preço (ou lucro) por unidade do ingrediente: "))
                    break
                except ValueError:
                    print("Valor inválido. Digite um número (ex: 4.50).")

            while True:
                try:
                    minimo = float(input("Informe a quantidade mínima do ingrediente: "))
                    break
                except ValueError:
                    print("Valor inválido. Digite um número.")

            while True:
                try:
                    maximo = float(input("Informe a quantidade máxima do ingrediente: "))
                    if maximo < minimo:
                        print("O valor máximo não pode ser menor que o mínimo. Digite novamente.")
                        continue
                    break
                except ValueError:
                    print("Valor inválido. Digite um número.")

            macarrao.loc[len(macarrao)] = [nome, preco, minimo, maximo]

        elif r == 'n':
            print("\nPreenchimento finalizado.")
            break

        else:
            print("Resposta inválida. Responda apenas com 's' para SIM e 'n' para NÃO.")
    
    return macarrao


def resolver_problema(df, total_min, total_max, modo):
    if modo == 'min':
        prob = pp.LpProblem("Minimizar_Custo", pp.LpMinimize)
    else:
        prob = pp.LpProblem("Maximizar_Lucro", pp.LpMaximize)

    variaveis = {
        row['Nome']: pp.LpVariable(row['Nome'], lowBound=row['Mínimo'], upBound=row['Máximo'], cat='Continuous')
        for _, row in df.iterrows()
    }

    if modo == 'min':
        prob += pp.lpSum(variaveis[nome] * df.loc[df['Nome'] == nome, 'Preço'].values[0] for nome in variaveis)
    else:
        prob += pp.lpSum(variaveis[nome] * df.loc[df['Nome'] == nome, 'Preço'].values[0] for nome in variaveis)

    prob += pp.lpSum(variaveis.values()) >= total_min, "Quantidade_Minima_Total"
    prob += pp.lpSum(variaveis.values()) <= total_max, "Quantidade_Maxima_Total"

    prob.solve()

    resultado = {
        'Status': pp.LpStatus[prob.status],
        'Objetivo': pp.value(prob.objective),
        'Ingredientes': {nome: variaveis[nome].varValue for nome in variaveis}
    }

    return resultado


def main():
    df = preencher_tabela()
    print("\nTabela Final:")
    print(df)

    while True:
        try:
            total_min = float(input("\nInforme a quantidade total MÍNIMA do produto final: "))
            total_max = float(input("Informe a quantidade total MÁXIMA do produto final: "))
            if total_max < total_min:
                print("O valor máximo não pode ser menor que o mínimo.")
                continue
            break
        except ValueError:
            print("Valor inválido. Digite números válidos.")

    while True:
        modo = input("\nDeseja minimizar custo ou maximizar lucro? (Digite 'min' ou 'max'): ").strip().lower()
        if modo in ['min', 'max']:
            break
        else:
            print("Opção inválida. Digite apenas 'min' ou 'max'.")

    resultado = resolver_problema(df, total_min, total_max, modo)

    print("\nResultado da Otimização:")
    print(f"Status: {resultado['Status']}")
    objetivo_txt = "Custo Total" if modo == 'min' else "Lucro Total"
    print(f"{objetivo_txt}: R$ {resultado['Objetivo']:.2f}")
    print("Distribuição dos Ingredientes:")
    for nome, valor in resultado['Ingredientes'].items():
        print(f" - {nome}: {valor:.2f} unidades")


if __name__ == "__main__":
    main()
