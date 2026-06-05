import streamlit as st
import streamlit.components.v1 as components
import os
import base64

# Configuração da página para o jogo
st.set_page_config(page_title="Ina Bros Game", layout="centered")

# Ocultar elementos do Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

# Função para converter imagens locais para Base64 (resolve o fundo preto)
def carregar_imagem_base64(nome_arquivo):
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "rb") as f:
            dados = f.read()
            return "data:image/png;base64," + base64.b64encode(dados).decode()
    return ""

# Lendo suas imagens do repositório
img_capa = carregar_imagem_base64("Capa.png")
img_cenario = carregar_imagem_base64("Cenário 1.png")

# Construção do HTML do Jogo de Plataforma (Estilo Mario)
game_html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0; padding: 0; background-color: #222;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden; font-family: Arial, sans-serif;
        }
        #game-container {
            width: 800px; height: 600px; background-color: #5c94fc;
            position: relative; border: 4px solid #fff; overflow: hidden;
        }
        .screen {
            width: 100%; height: 100%; position: absolute;
            top: 0; left: 0; display: none; background-size: 100% 100%;
        }
        .active { display: block; }
        
        /* Menu */
        #menu-screen {
            background-image: url('""" + img_capa + """');
            background-color: #000;
        }
        #start-btn {
            position: absolute; bottom: 60px; left: 50%;
            transform: translateX(-50%); padding: 15px 40px;
            font-size: 22px; font-weight: bold; cursor: pointer;
            background-color: #e52521; color: white;
            border: 3px solid #fff; border-radius: 8px;
        }

        /* Tela do Jogo */
        #game-screen {
            background-image: url('""" + img_cenario + """');
        }
        #player {
            width: 40px; height: 60px; background-color: #e52521;
            border: 2px solid #000; position: absolute;
            bottom: 60px; left: 100px; border-radius: 4px;
        }
        #floor {
            width: 100%; height: 60px; background-color: #73c740;
            border-top: 4px solid #4da22b; position: absolute; bottom: 0; left: 0;
        }
        .platform {
            width: 150px; height: 30px; background-color: #fcb443;
            border: 3px solid #6b4000; position: absolute;
            bottom: 220px; left: 350px; text-align: center;
            line-height: 30px; font-weight: bold; color: #6b4000;
        }

        /* Controles */
        .controls-container {
            position: absolute; top: 20px; left: 20px;
            display: flex; gap: 15px; background: rgba(0, 0, 0, 0.6);
            padding: 10px; border-radius: 8px;
        }
        .control-btn {
            padding: 10px 20px; font-size: 16px; font-weight: bold;
            background: #fff; border: 2px solid #000; cursor: pointer; border-radius: 5px;
        }
    </style>
</head>
<body>

    <div id="game-container">
        <div id="menu-screen" class="screen active">
            <button id="start-btn" onclick="startGame()">JOGAR</button>
        </div>

        <div id="game-screen" class="screen">
            <div class="controls-container">
                <button class="control-btn" onclick="movePlayer(-30)">⬅️ ESQ</button>
                <button class="control-btn" onclick="jumpPlayer()">⬆️ PULAR</button>
                <button class="control-btn" onclick="movePlayer(30)">DIR ➡️</button>
            </div>
            <div id="player"></div>
            <div class="platform">TIJOLO</div>
            <div id="floor"></div>
        </div>
    </div>

    <script>
        let playerX = 100;
        let playerY = 60;
        let isJumping = false;
        const player = document.getElementById('player');

        function startGame() {
            document.getElementById('menu-screen').classList.remove('active');
            document.getElementById('game-screen').classList.add('active');
        }

        function movePlayer(offset) {
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

components.html(game_html, width=800, height=600)
