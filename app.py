import streamlit as st
import streamlit.components.v1 as components
import os
import base64
from PIL import Image
from io import BytesIO

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

# Função robusta para converter imagens locais para Base64 usando PIL
def carregar_imagem_base64(nome_arquivo):
    if os.path.exists(nome_arquivo):
        try:
            img = Image.open(nome_arquivo)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return f"data:image/png;base64,{img_str}"
        except Exception:
            return ""
    return ""

# Lendo as imagens de cenário direto do seu repositório
img_capa = carregar_imagem_base64("Capa.png")
img_cenario = carregar_imagem_base64("Cenário 1.png")

# HTML do jogo estruturado de forma limpa
html_puro = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=MedievalSharp&display=swap" rel="stylesheet">
    
    <style>
        body {
            margin: 0; padding: 0; background-color: #111;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden;
            font-family: 'MedievalSharp', cursive;
        }
        #game-container {
            width: 800px; height: 600px; background-color: #0d0d0d;
            position: relative; border: 4px solid #3a0000; 
            box-shadow: 0 0 30px rgba(139, 0, 0, 0.5);
            border-radius: 10px; overflow: hidden;
        }
        .screen {
            width: 100%; height: 100%; position: absolute;
            top: 0; left: 0; display: none; 
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        .active { display: block; }
        
        /* TELA DE MENU */
        #menu-screen {
            background-image: url('URL_DA_CAPA');
            background-color: #000;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .game-title {
            font-family: 'Cinzel Decorative', serif;
            font-size: 56px;
            color: #ff1a1a;
            text-align: center;
            text-shadow: 3px 3px 0px #000, 0 0 25px rgba(255, 0, 0, 0.9);
            margin-top: -60px;
            margin-bottom: 40px;
            letter-spacing: 4px;
        }
        #start-btn {
            padding: 15px 50px; font-family: 'MedievalSharp', cursive;
            font-size: 26px; font-weight: bold; cursor: pointer;
            color: #fff; background: linear-gradient(135deg, #4a0000 0%, #1a0000 100%);
            border: 2px solid #8b0000; border-radius: 4px;
            box-shadow: 0 0 15px rgba(139, 0, 0, 0.6);
            text-shadow: 2px 2px 4px #000; transition: all 0.3s;
        }
        #start-btn:hover {
            background: linear-gradient(135deg, #8b0000 0%, #4a0000 100%);
            border-color: #ff1a1a; box-shadow: 0 0 25px rgba(255, 26, 26, 0.8);
            transform: scale(1.05);
        }

        /* TELA DE JOGO */
        #game-screen {
            background-image: url('URL_DO_CENARIO');
        }
        #player {
            width: 40px; height: 60px; 
            background: linear-gradient(to bottom, #ff1a1a, #8b0000);
            border: 2px solid #3a0000; position: absolute;
            bottom: 60px; left: 100px; border-radius: 6px;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
            transition: background 0.1s ease;
        }
        #floor {
            width: 100%; height: 60px; 
            background: linear-gradient(to bottom, #15250c, #0a1206);
            border-top: 4px solid #3a0000; position: absolute; bottom: 0; left: 0;
        }
        .platform {
            width: 150px; height: 30px; 
            background: linear-gradient(to bottom, #2b2b2b, #141414);
            border: 2px solid #555; position: absolute;
            bottom: 220px; left: 350px; text-align: center;
            line-height: 30px; font-weight: bold; color: #8b0000;
            font-size: 14px; letter-spacing: 2px; border-radius: 4px;
        }

        /* PAINEL DE CONTROLES GÓTICO */
        .controls-container {
            position: absolute; top: 20px; left: 20px;
            display: flex; gap: 10px; background: rgba(10, 10, 10, 0.85);
            padding: 10px; border-radius: 6px; border: 2px solid #3a0000;
        }
        .control-btn {
            padding: 10px 18px; font-family: 'MedievalSharp', cursive;
            font-size: 14px; font-weight: bold; color: #ccc; background: #1f1f1f;
            border: 1px solid #444; cursor: pointer; border-radius: 4px; transition: all 0.2s;
        }
        .control-btn:hover {
            color: #fff; background: #2d2d2d; border-color: #8b0000;
            box-shadow: 0 0 8px rgba(139, 0, 0, 0.6);
        }
        .attack-btn {
            background: linear-gradient(to bottom, #8b0000, #4a0000);
            color: #fff; border: 1px solid #ff1a1a;
        }
        .attack-btn:hover {
            background: linear-gradient(to bottom, #ff1a1a, #8b0000);
            box-shadow: 0 0 12px rgba(255, 26, 26, 0.8);
        }
    </style>
</head>
<body>

    <div id="game-container">
        <div id="menu-screen" class="screen active">
            <div class="game-title">INA BROS</div>
            <button id="start-btn" onclick="startGame()">INICIAR</button>
        </div>

        <div id="game-screen" class="screen">
            <div class="controls-container">
                <button class="control-btn" onclick="movePlayer(-30)">⬅️ ESQ</button>
                <button class="control-btn" onclick="jumpPlayer()">⬆️ PULAR</button>
                <button class="control-btn" onclick="movePlayer(30)">DIR ➡️</button>
                <button class="control-btn attack-btn" onclick="attackPlayer()">⚔️ GOLPE</button>
            </div>
            <div id="player"></div>
            <div class="platform">PLATAFORMA</div>
            <div id="floor"></div>
        </div>
    </div>

    <script>
        let playerX = 100;
        let playerY = 60;
        let isJumping = false;
        let isAttacking = false;
        const player = document.getElementById('player');

        function startGame() {
            document.getElementById('menu-screen').classList.remove('active');
            document.getElementById('game-screen').classList.add('active');
        }

        function movePlayer(offset) {
            if (isAttacking) return;
            playerX += offset;
            if (playerX < 0) playerX = 0;
            if (playerX > 760) playerX = 760;
            player.style.left = playerX + 'px';
            checkPlatform();
        }

        function jumpPlayer() {
            if (isJumping) return;
            isJumping = true;
            let baseFloor = playerY;
            let targetHeight = baseFloor + 160;

            let upInterval = setInterval(() => {
                playerY += 8;
                player.style.bottom = playerY + 'px';
                if (playerY >= targetHeight) {
                    clearInterval(upInterval);
                    let downInterval = setInterval(() => {
                        playerY -= 8;
                        player.style.bottom = playerY + 'px';
                        
                        if (playerX >= 310 && playerX <= 480 && playerY <= 250 && playerY >= 240) {
                            clearInterval(downInterval);
                            playerY = 250;
                            player.style.bottom = playerY + 'px';
                            isJumping = false;
                        } else if (playerY <= 60) {
                            clearInterval(downInterval);
                            playerY = 60;
                            player.style.bottom = playerY + 'px';
                            isJumping = false;
                        }
                    }, 15);
                }
            }, 15);
        }

        function attackPlayer() {
            if (isAttacking) return;
            isAttacking = true;
            player.style.background = '#ff1a1a'; 
            player.style.boxShadow = '0 0 25px #ff1a1a, 0 0 10px #fff';

            setTimeout(() => {
                player.style.background = 'linear-gradient(to bottom, #ff1a1a, #8b0000)';
                player.style.boxShadow = '0 0 10px rgba(255, 0, 0, 0.5)';
                isAttacking = false;
            }, 150);
        }

        function checkPlatform() {
            if (playerY === 250 && (playerX < 310 || playerX > 480)) {
                let fallInterval = setInterval(() => {
                    playerY -= 8;
                    player.style.bottom = playerY + 'px';
                    if (playerY <= 60) {
                        clearInterval(fallInterval);
                        playerY = 60;
                        player.style.bottom = playerY + 'px';
                    }
                }, 15);
            }
        }
    </script>
</body>
</html>
"""

# Substituição direta injetando as imagens transformadas em dados embutidos
game_html = html_puro.replace("URL_DA_CAPA", img_capa).replace("URL_DO_CENARIO", img_cenario)

# Renderiza o contêiner final
components.html(game_html, width=800, height=600)
