import pandas as pd
import pulp as pp

def transformar_tabela(tabela: dict) -> pd.DataFrame:
    """
    Transforma um dicionário de tabela em um DataFrame do pandas.
    
    :param tabela: Dicionário contendo os dados da tabela com produtos, preços, mínimo e máximo.
    :return: DataFrame com os dados da tabela.
    """
    df = pd.DataFrame(tabela, columns=['Produto', 'Preço', 'Quant. Min.', 'Quant. Max.'])
    
    colunas_necessarias = ['Produto', 'Preço', 'Quant. Min.', 'Quant. Max.']
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            raise ValueError(f"A coluna '{coluna}' é necessária na tabela.")
    
    return df


def processar_tabela(tabela: dict, restricao: dict, modo: bool):
    """
    Processa a tabela e a restrição para otimização de ingredientes.
    
    :param tabela: Dicionário contendo os dados da tabela com produtos, preços, mínimo e máximo.
    :param restricao: Dicionário com as restrições dos atributos da tabela.
    :return: Resultado da otimização.
    """
    tabela_normal = transformar_tabela(tabela)
    
    modo = 'modo' if modo else 'min'
    
    resultado = resolver_problema(tabela_normal, modo, restricao)
    
    return resultado


def processar_restricao(prob, df, variaveis, restricao):
    for r in restricao:
        campo = r.get('campo')
        operador = r.get('operador')
        valor = r.get('valor')
        
        operador = '<=' if operador == '<' else '>='

        if campo in ['Preço', 'Quant. Min.', 'Quant. Max.', 'Quantidade', 'Quantidade Total', 'Preço Total']:
            try:
                valor = float(valor)
            except ValueError:
                raise ValueError(f"Valor inválido para o campo '{campo}': {valor}")
            
        if campo == 'Quantidade Total':
            expressao = pp.lpSum(variaveis.values())
        elif campo == 'Preço Total':
            expressao = pp.lpSum(variaveis[nome] * float(df.loc[df['Produto'] == nome, 'Preço'].values[0]) for nome in variaveis)
        elif campo in ['Preço', 'Quant. Min.', 'Quant. Max.', 'Quantidade']:
            for nome in variaveis:

                if campo == 'Quantidade':
                    valor_expr = variaveis[nome]
                else:
                    coef = float(df.loc[df['Produto'] == nome, campo].values[0])
                    valor_expr = coef * variaveis[nome]  # expressão matemática válida
                
                if operador not in {'==', '>=', '<=', '>', '<'}:
                    raise ValueError(f"Operador inválido: {operador}")

                if valor is None:
                    raise ValueError(f"Valor ausente para o campo '{campo}'")

                restr_expr = {
                    '==': valor_expr == valor,
                    '>=': valor_expr >= valor,
                    '<=': valor_expr <= valor
                }[operador]

                prob += restr_expr, f"Restricao_{campo}_{nome}"
            return

        else:
            raise ValueError(f"Campo de restrição inválido: {campo}")

        if campo in ['Quantidade Total', 'Preço Total']:
            restr_expr = {
                '==': expressao == valor,
                '>=': expressao >= valor,
                '<=': expressao <= valor,
            }[operador]
            prob += restr_expr, f"Restricao_{campo.replace(' ', '_')}"
      
        
def resolver_problema(df: pd.DataFrame, modo: str, restricao) -> dict:
    # Validação e sanitização dos dados
    for coluna in ['Preço', 'Quant. Min.', 'Quant. Max.']:
        if coluna not in df.columns:
            raise ValueError(f"Coluna obrigatória '{coluna}' não encontrada no DataFrame.")
        df[coluna] = pd.to_numeric(df[coluna], errors='raise')

    if not restricao:
        restricao = []
    elif isinstance(restricao, dict):
        restricao = [restricao]

    # Definição do objetivo
    objetivo = pp.LpMinimize if modo == 'min' else pp.LpMaximize
    prob = pp.LpProblem("Problema_Otimizacao", objetivo)

    # Criação das variáveis de decisão
    variaveis = {}
    for _, row in df.iterrows():
        nome = row['Produto']
        quant_min = float(row['Quant. Min.'])
        quant_max = float(row['Quant. Max.'])
        variaveis[nome] = pp.LpVariable(
            nome,
            lowBound=quant_min,
            upBound=quant_max,
            cat='Continuous'
        )

    # Definição da função objetivo (minimizar ou maximizar custo total)
    prob += pp.lpSum(
        variaveis[nome] * df.loc[df['Produto'] == nome, 'Preço'].values[0]
        for nome in variaveis
    )

    # Aplicação das restrições
    processar_restricao(prob, df, variaveis, restricao)

    # Resolver o problema
    prob.solve()

    # Montagem do resultado
    resultado_df = df.copy()
    resultado_df['Quantidade'] = resultado_df['Produto'].map(lambda nome: variaveis[nome].varValue)
    resultado_df['Preço Total'] = resultado_df['Quantidade'] * resultado_df['Preço']

    return {
        'Status': pp.LpStatus[prob.status],
        'Objetivo': pp.value(prob.objective),
        'Ingredientes': {nome: variaveis[nome].varValue for nome in variaveis},
        'Resultado': resultado_df
    }