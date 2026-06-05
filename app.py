import streamlit as st
import streamlit.components.v1 as components
import os
import base64

# Configuração da página para o jogo
st.set_page_config(page_title="Ina Bros Game", layout="centered")

# Ocultar menus padrões do Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container {padding-top: 1rem;}
    body {background-color: #111;}
    </style>
""", unsafe_allow_html=True)

# Função para converter imagens locais para Base64
def carregar_imagem_base64(nome_arquivo):
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "rb") as f:
            dados = f.read()
            return "data:image/png;base64," + base64.b64encode(dados).decode()
    return ""

# Lendo suas imagens do repositório
img_capa = carregar_imagem_base64("Capa.png")
img_cenario = carregar_imagem_base64("Cenário 1.png")

# Construção do HTML com design Gótico e botões estilizados
game_html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Almendra+Display&family=Cinzel+Decorative:wght@700&family=MedievalSharp&display=swap" rel="stylesheet">
    
    <style>
        body {{
            margin: 0; padding: 0; background-color: #111;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden;
            font-family: 'MedievalSharp', cursive;
        }}
        #game-container {{
            width: 800px; height: 600px; background-color: #0d0d0d;
            position: relative; border: 4px solid #3a0000; 
            box-shadow: 0 0 30px rgba(139, 0, 0, 0.5);
            border-radius: 10px;
            overflow: hidden;
        }}
        .screen {{
            width: 100%; height: 100%; position: absolute;
            top: 0; left: 0; display: none; background-size: 100% 100%;
        }}
        .active {{ display: block; }}
        
        /* --- DESIGN DA TELA DE MENU --- */
        #menu-screen {{
            background-image: url('{img_capa}');
            background-color: #000;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        /* Título Gótico em cima da capa */
        .game-title {{
            font-family: 'Cinzel Decorative', serif;
            font-size: 56px;
            color: #ff1a1a;
            text-align: center;
            text-shadow: 3px 3px 0px #000, 0 0 20px rgba(255, 0, 0, 0.8);
            margin-top: -80px;
            margin-bottom: 40px;
            letter-spacing: 4px;
        }}
        
        /* Botão JOGAR Estilizado */
        #start-btn {{
            padding: 15px 50px;
            font-family: 'MedievalSharp', cursive;
            font-size: 26px; font-weight: bold; cursor: pointer;
            color: #fff; background: linear-gradient(135deg, #4a0000 0%, #1a0000 100%);
            border: 2px solid #8b0000; border-radius: 4px;
            box-shadow: 0 0 15px rgba(139, 0, 0, 0.6), inset 0 0 10px rgba(0,0,0,0.5);
            text-shadow: 2px 2px 4px #000;
            transition: all 0.3s ease;
        }}
        #start-btn:hover {{
            background: linear
