import streamlit as st

st.set_page_config(
    page_title="Calculadora Financeira",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Calculadora Financeira")
st.write("Simule investimentos, juros, financiamentos e rentabilidade.")
st.divider()


def moeda(valor):
    """Formata um número no padrão brasileiro."""
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def calcular_juros_simples(capital, taxa, tempo):
    juros = capital * (taxa / 100) * tempo
    return juros, capital + juros


def calcular_juros_compostos(capital, taxa, tempo):
    montante = capital * (1 + taxa / 100) ** tempo
    return montante, montante - capital


def calcular_parcela_price(valor, taxa, meses):
    taxa_mensal = taxa / 100

    if meses <= 0:
        raise ValueError("O prazo deve ser maior que zero.")

    if taxa_mensal == 0:
        return valor / meses

    return valor * (
        taxa_mensal * (1 + taxa_mensal) ** meses
    ) / (
        (1 + taxa_mensal) ** meses - 1
    )


def calcular_investimento(capital, aporte, taxa, meses):
    saldo = capital
    taxa_mensal = taxa / 100

    for _ in range(meses):
        saldo = saldo * (1 + taxa_mensal) + aporte

    total_investido = capital + aporte * meses
    rendimento = saldo - total_investido

    return saldo, total_investido, rendimento


operacao = st.selectbox(
    "Escolha uma operação financeira",
    [
        "Juros simples",
        "Juros compostos",
        "Simulador de investimentos",
        "Financiamento - Tabela Price",
        "Calculadora de rentabilidade"
    ]
)

st.divider()

if operacao == "Juros simples":
    st.subheader("📊 Cálculo de juros simples")

    capital = st.number_input(
        "Capital inicial (R$)", min_value=0.0, value=1000.0
    )
    taxa = st.number_input(
        "Taxa de juros por período (%)",
        min_value=0.0, value=2.0
    )
    tempo = st.number_input(
        "Quantidade de períodos",
        min_value=0, value=12
    )

    if st.button("Calcular juros"):
        juros, montante = calcular_juros_simples(
            capital, taxa, tempo
        )
        st.metric("Juros acumulados", moeda(juros))
        st.metric("Montante final", moeda(montante))

elif operacao == "Juros compostos":
    st.subheader("📈 Cálculo de juros compostos")

    capital = st.number_input(
        "Capital inicial (R$)", min_value=0.0, value=1000.0
    )
    taxa = st.number_input(
        "Taxa de juros por período (%)",
        min_value=0.0, value=1.0
    )
    tempo = st.number_input(
        "Quantidade de períodos",
        min_value=0, value=12
    )

    if st.button("Calcular montante"):
        montante, rendimento = calcular_juros_compostos(
            capital, taxa, tempo
        )
        st.metric("Valor final", moeda(montante))
        st.metric("Rendimento", moeda(rendimento))

elif operacao == "Simulador de investimentos":
    st.subheader("💹 Simulador de investimentos")

    capital = st.number_input(
        "Investimento inicial (R$)",
        min_value=0.0, value=1000.0
    )
    aporte = st.number_input(
        "Aporte mensal (R$)",
        min_value=0.0, value=200.0
    )
    taxa = st.number_input(
        "Rentabilidade mensal (%)",
        min_value=0.0, value=0.8
    )
    meses = st.number_input(
        "Prazo em meses",
        min_value=1, value=12
    )

    if st.button("Simular investimento"):
        saldo, investido, rendimento = calcular_investimento(
            capital, aporte, taxa, int(meses)
        )

        st.metric("Patrimônio acumulado", moeda(saldo))
        st.metric("Total investido", moeda(investido))
        st.metric("Rendimento estimado", moeda(rendimento))

elif operacao == "Financiamento - Tabela Price":
    st.subheader("🏠 Simulador de financiamento")

    valor = st.number_input(
        "Valor financiado (R$)",
        min_value=0.0, value=10000.0
    )
    taxa = st.number_input(
        "Taxa de juros mensal (%)",
        min_value=0.0, value=1.5
    )
    meses = st.number_input(
        "Prazo em meses",
        min_value=1, value=24
    )

    if st.button("Calcular financiamento"):
        parcela = calcular_parcela_price(
            valor, taxa, int(meses)
        )
        total = parcela * meses
        juros_total = total - valor

        st.metric("Parcela mensal estimada", moeda(parcela))
        st.metric("Total a pagar", moeda(total))
        st.metric("Total de juros", moeda(juros_total))

elif operacao == "Calculadora de rentabilidade":
    st.subheader("💵 Calcule o retorno financeiro")

    investimento = st.number_input(
        "Valor investido (R$)",
        min_value=0.01, value=1000.0
    )
    valor_final = st.number_input(
        "Valor final recebido (R$)",
        min_value=0.0, value=1250.0
    )

    if st.button("Calcular rentabilidade"):
        lucro = valor_final - investimento
        rentabilidade = (lucro / investimento) * 100

        st.metric("Lucro ou prejuízo", moeda(lucro))
        st.metric("Rentabilidade", f"{rentabilidade:.2f}%")

st.divider()
st.caption(
    "Calculadora para fins educativos. "
    "Os resultados são estimativas e não incluem automaticamente "
    "impostos, tarifas, inflação ou outros custos."
)
