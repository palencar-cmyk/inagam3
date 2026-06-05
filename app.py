import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Ina@game",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Remover margens e elementos padrões do Streamlit
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0rem;}
        iframe {display: block; margin: auto;}
    </style>
""", unsafe_allow_html=True)

# Função para codificar as imagens em Base64
def carregar_imagem_base64(nome_arquivo, extensao="png"):
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            mime = "jpeg" if extensao.lower() in ["jpg", "jpeg"] else "png"
            return f"data:image/{mime};base64,{encoded_string}"
    return ""

# Convertendo as imagens locais
capa_uri = carregar_imagem_base64("Capa.png")
cenario1_uri = carregar_imagem_base64("Cenário 1.png")
cenario2_uri = carregar_imagem_base64("Cenário 2.png")
cenario3_uri = carregar_imagem_base64("Cenário 3.png")
cenario4_uri = carregar_imagem_base64("Cenário 4.png")
personagens_uri = carregar_imagem_base64("Personagens.png")
knife_uri = carregar_imagem_base64("knife.jpg", "jpg")
skel1_uri = carregar_imagem_base64("skeleton.jpg", "jpg")
skel2_uri = carregar_imagem_base64("skeleton2.jpg", "jpg")
weed_uri = carregar_imagem_base64("weed.jpg", "jpg")
vinho_svg = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23722F37"><path d="M12 2v4c.55 0 1 .45 1 1v2.59l4 4V22H7v-8.41l4-4V7c0-.55.45-1 1-1V2h2zm2 14H10v4h4v-4z"/></svg>'

game_html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Ina@game</title>
    <style>
        * {{
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
            margin: 0;
            padding: 0;
        }}
        body, html {{
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #0d0d0d;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #e0e0e0;
        }}
        #game-container {{
            position: relative;
            width: 100vw;
            height: 100vh;
            max-width: 854px;
            max-height: 480px;
            margin: auto;
            overflow: hidden;
            background-color: #1a1a1a;
        }}
        .screen {{
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            display: none;
            background-size: 100% 100%;
            background-position: center;
            z-index: 10;
        }}
        #screen-start {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-image: url('{capa_uri}');
            background-color: #0a0a0a;
        }}
        #screen-start h1 {{
            font-size: 3rem;
            color: #8b0000;
            text-shadow: 0 0 10px #000, 2px 2px 4px #000;
            margin-bottom: 30px;
            letter-spacing: 4px;
        }}
        .btn {{
            padding: 12px 35px;
            font-size: 1.2rem;
            background: linear-gradient(135deg, #4a0000, #1a0000);
            color: #fff;
            border: 2px solid #8b0000;
            border-radius: 5px;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 2px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        }}
        #screen-game {{ background-image: url('{cenario1_uri}'); }}
        #hud {{
            position: absolute;
            top: 10px;
            left: 10px;
            right: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 100;
        }}
        #hearts {{ display: flex; gap: 5px; }}
        .heart {{ font-size: 24px; color: #ff0033; text-shadow: 0 0 5px #000; }}
        #score-board {{
            background: rgba(0, 0, 0, 0.7);
            padding: 5px 15px;
            border-radius: 15px;
            border: 1px solid #444;
            font-size: 1rem;
            font-weight: bold;
        }}
        #boss-hud {{
            display: none;
            position: absolute;
            top: 50px;
            left: 50%;
            transform: translateX(-50%);
            width: 60%;
            background: rgba(0,0,0,0.8);
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #ff0000;
            z-index: 100;
            text-align: center;
        }}
        #boss-hearts {{ display: flex; justify-content: center; gap: 5px; }}
        .boss-heart {{ font-size: 18px; color: #00ff66; }}
        #game-world {{ position: relative; width: 100%; height: 100%; }}
        .character-group {{
            position: absolute;
            bottom: 60px;
            left: 50px;
            height: 100px;
            display: flex;
            align-items: flex-end;
            gap: 12px;
        }}
        .char-sprite {{
            width: 60px;
            height: 85px;
            background-image: url('{personagens_uri}');
            background-size: 300% 100%;
            background-repeat: no-repeat;
        }}
        #inara {{ background-position: 0% center; }}
        #queen {{ display: none; background-position: 50% center; }}
        #herr {{ display: none; background-position: 100% center; }}
        .enemy {{
            position: absolute;
            bottom: 60px;
            width: 60px;
            height: 85px;
            background-size: contain;
            background-repeat: no-repeat;
            background-position: bottom;
        }}
        .boss {{
            position: absolute;
            bottom: 60px;
            right: 40px;
            width: 110px;
            height: 130px;
            background-image: url('{personagens_uri}');
            background-position: 0% center;
            filter: hue-rotate(140deg) brightness(0.6);
            background-size: 300% 100%;
            background-repeat: no-repeat;
            display: none;
        }}
        .projectile {{
            position: absolute;
            width: 30px;
            height: 30px;
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
        }}
        .boss-projectile {{
            position: absolute;
            font-family: 'Comic Sans MS', 'Comic Sans', sans-serif;
            color: #00ff33;
            font-weight: bold;
            white-space: nowrap;
            font-size: 18px;
            text-shadow: 1px 1px 2px #000;
        }}
        #controls {{
            position: absolute;
            bottom: 15px;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 30px;
            z-index: 150;
        }}
        .control-btn {{
            width: 75px;
            height: 75px;
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid #8b0000;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #fff;
            font-size: 2rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.7);
        }}
        .control-btn:active {{ background: rgba(139, 0, 0, 0.8); }}
        #screen-end {{
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: #000;
            z-index: 200;
        }}
        #end-title {{ font-size: 4rem; color: #00ff66; margin-bottom: 20px; }}
    </style>
</head>
<body>

    <div id="game-container">
        <div id="screen-start" class="screen" style="display: flex;">
            <h1>Ina@game</h1>
            <button class="btn" id="btn-start">Iniciar</button>
        </div>

        <div id="screen-game" class="screen">
            <div id="hud">
                <div id="hearts"></div>
                <div id="score-board">Inimigos: <span id="score-val">