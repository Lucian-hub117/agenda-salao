import streamlit as st
import json
import os
from datetime import date, datetime, timedelta

st.set_page_config(page_title="Agenda do Salão", page_icon="💅", layout="centered")

DADOS_ARQUIVO = "agendamentos.json"


def carregar_agendamentos():
    if os.path.exists(DADOS_ARQUIVO):
        with open(DADOS_ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_agendamentos(agendamentos):
    with open(DADOS_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(agendamentos, f, ensure_ascii=False, indent=2)


if "agendamentos" not in st.session_state:
    st.session_state.agendamentos = carregar_agendamentos()

st.title("💅 Agenda do Salão")

dia_selecionado = st.date_input("Escolha o dia", value=date.today(), format="DD/MM/YYYY")
dia_str = dia_selecionado.strftime("%Y-%m-%d")

st.markdown("---")

st.subheader("➕ Novo horário")

with st.form("novo_agendamento", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        horario = st.time_input("Horário", value=datetime.strptime("09:00", "%H:%M").time())
    with col2:
        servico = st.selectbox("Serviço", ["Unhas", "Sobrancelha", "Unhas + Sobrancelha", "Outro"])

    cliente = st.text_input("Nome da cliente")
    telefone = st.text_input("Telefone (opcional)")
    observacao = st.text_input("Observação (opcional)")

    enviado = st.form_submit_button("Salvar horário", type="primary", use_container_width=True)

    if enviado:
        if cliente.strip() == "":
            st.error("Digite o nome da cliente.")
        else:
            novo = {
                "data": dia_str,
                "horario": horario.strftime("%H:%M"),
                "cliente": cliente.strip(),
                "servico": servico,
                "telefone": telefone.strip(),
                "observacao": observacao.strip(),
            }
            st.session_state.agendamentos.append(novo)
            salvar_agendamentos(st.session_state.agendamentos)
            st.success(f"Horário das {novo['horario']} salvo para {novo['cliente']}!")
            st.rerun()

st.markdown("---")

st.subheader(f"📅 Horários de {dia_selecionado.strftime('%d/%m/%Y')}")

agendamentos_do_dia = [a for a in st.session_state.agendamentos if a["data"] == dia_str]
agendamentos_do_dia.sort(key=lambda a: a["horario"])

if not agendamentos_do_dia:
    st.info("Nenhum horário marcado para este dia ainda.")
else:
    for i, ag in enumerate(agendamentos_do_dia):
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**🕐 {ag['horario']} — {ag['cliente']}**")
                st.caption(f"{ag['servico']}" + (f" · 📞 {ag['telefone']}" if ag["telefone"] else ""))
                if ag["observacao"]:
                    st.caption(f"📝 {ag['observacao']}")
            with col2:
                if st.button("🗑️", key=f"del_{dia_str}_{i}_{ag['horario']}", help="Excluir"):
                    st.session_state.agendamentos.remove(ag)
                    salvar_agendamentos(st.session_state.agendamentos)
                    st.rerun()

st.markdown("---")
st.caption("💡 Dica: adicione este app à tela inicial do celular para acessar rapidinho.")
