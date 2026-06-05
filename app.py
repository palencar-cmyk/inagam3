import streamlit as st
import streamlit.components.v1 as components
import os
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Ina Bros Game", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container {padding-top: 1rem;}
    body {background-color: #111;}
    </style>
""", unsafe_allow_html=True)

def carregar_imagem_base64(nome_arquivo):
    if os.path.exists(nome_arquivo):
        try:
            img = Image.open(nome_arquivo)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return "data:image/png;base64," + img_str
        except Exception:
            return ""
    return ""

img_capa = carregar_imagem_base64("Capa.png")
img_cenario = carregar_imagem_base64("Cenário 1.png")
img_player = carregar_imagem_base64("Personagem.png")
img_inimigo = carregar_imagem_base64("Inimigo.png")
img_boss = carregar_imagem_base64("Boss SF.png")

partes_html = [
    "<!DOCTYPE html><html lang='pt-br'><head><meta charset='UTF-8'>",
    "<link rel='preconnect' href='https://fonts.googleapis.com'>",
    "<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>",
    "<link href='https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=MedievalSharp&display=swap' rel='stylesheet'>",
    "<style>",
    "body { margin: 0; padding: 0; background-color: #111; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; font-family: 'MedievalSharp', cursive; user-select: none; }",
    "#game-container { width: 800px; height: 600px; background-color: #0d0d0d; position: relative; border: 4px solid #3a0000; box-shadow: 0 0 30px rgba(139, 0, 0, 0.5); border-radius: 10px; overflow: hidden; }",
    ".screen { width: 100%; height: 100%; position: absolute; top: 0; left: 0; display: none; background-size: cover; background-position: center; background-repeat: no-repeat; }",
    ".active { display: block; }",
    "#menu-screen { background-image: url('", img_capa, "'); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px; }",
    ".menu-panel { background: rgba(0, 0, 0, 0.65); padding: 30px 50px; border-radius: 12px; border: 3px solid #8b0000; text-align: center; box-shadow: 0 0 20px rgba(0, 0, 0, 0.8); z-index: 10; }",
    ".game-title { font-family: 'Cinzel Decorative', serif; font-size: 52px; color: #ff1a1a; text-shadow: 3px 3px 0px #000, 0 0 25px rgba(255, 0, 0, 0.8); margin: 0 0 30px 0; letter-spacing: 4px; }",
    "#start-btn { padding: 15px 50px; font-family: 'MedievalSharp', cursive; font-size: 26px; font-weight: bold; cursor: pointer; color: #fff; background: linear-gradient(135deg, #4a0000 0%, #1a0000 100%); border: 2px solid #8b0000; border-radius: 4px; box-shadow: 0 0 15px rgba(139, 0, 0, 0.6); text-shadow: 2px 2px 4px #000; transition: all 0.3s; }",
    "#start-btn:hover { background: linear-gradient(135deg, #8b0000 0%, #4a0000 100%); border-color: #ff1a1a; box-shadow: 0 0 25px rgba(255, 26, 26, 0.8); transform: scale(1.05); }",
    "#game-screen { background-image: url('", img_cenario, "'); }",
    "#player { width: 65px; height: 95px; background-image: url('", img_player, "'); background-size: contain; background-repeat: no-repeat; background-position: bottom; position: absolute; bottom: 55px; left: 100px; z-index: 10; transition: filter 0.1s; }",
    ".enemy { width: 60px; height: 90px; background-image: url('", img_inimigo, "'); background-size: contain; background-repeat: no-repeat; background-position: bottom; position: absolute; bottom: 55px; z-index: 5; }",
    "#boss-sf { width: 140px; height: 190px; background-image: url('", img_boss, "'); background-size: contain; background-repeat: no-repeat; background-position: bottom; position: absolute; bottom: 55px; right: 50px; display: none; z-index: 6; filter: drop-shadow(0 0 15px rgba(255, 0, 0, 0.5)); }",
    "#floor { width: 100%; height: 55px; background: transparent; position: absolute; bottom: 0; left: 0; }",
    ".controls-container { position: absolute; top: 20px; left: 20px; display: flex; gap: 10px; background: rgba(10, 10, 10, 0.85); padding: 10px; border-radius: 6px; border: 2px solid #3a0000; z-index: 100; }",
    ".control-btn { padding: 10px 18px; font-family: 'MedievalSharp', cursive; font-size: 14px; font-weight: bold; color: #ccc; background: #1f1f1f; border: 1px solid #444; cursor: pointer; border-radius: 4px; transition: all 0.2s; }",
    ".control-btn:hover { color: #fff; background: #2d2d2d; border-color: #8b0000; box-shadow: 0 0 8px rgba(139, 0, 0, 0.6); }",
    ".attack-btn { background: linear-gradient(to bottom, #8b0000, #4a0000); color: #fff; border: 1px solid #ff1a1a; }",
    ".attack-btn:hover { background: linear-gradient(to bottom, #ff1a1a, #8b0000); box-shadow: 0 0 12px rgba(255, 26, 26, 0.8); }",
    "#stage-indicator { position: absolute; top: 20px; right: 20px; background: rgba(10, 10, 10, 0.85); padding: 10px 20px; border-radius: 6px; border: 2px solid #3a0000; color: #ff1a1a; font-size: 18px; font-weight: bold; letter-spacing: 2px; z-index: 100; }",
    "</style></head><body>",
    "<div id='game-container'>",
    "<div id='menu-screen' class='screen active'><div class='menu-panel'><h1 class='game-title'>INA BROS</h1><button id='start-btn' onclick='startGame()'>INICIAR JOGO</button></div></div>",
    "<div id='game-screen' class='screen'><div class='controls-container'><button class='control-btn' onclick='movePlayer(-30)'>⬅️ A / ESQ</button><button class='control-btn' onclick='jumpPlayer()'>⬆️ W / PULAR</button><button class='control-btn' onclick='movePlayer(30)'>DIR / D ➡️</button><button class='control-btn attack-btn' onclick='attackPlayer()'>⚔️ ESPAÇO / GOLPE</button></div>",
    "<div id='stage-indicator'>FASE: 1</div><div id='player'></div><div id='enemies-container'></div><div id='boss-sf'></div><div id='floor'></div></div></div>",
    "<script>",
    "let playerX = 100; let playerY = 55; let isJumping = false; let isAttacking = false; let currentStage = 1; const totalStages = 3;",
    "const player = document.getElementById('player'); const enemiesContainer = document.getElementById('enemies-container'); const bossSf = document.getElementById('boss-sf'); const stageIndicator = document.getElementById('stage-indicator');",
    "let enemiesList = []; let gameLoopInterval;",
    "function startGame() { document.getElementById('menu-screen').classList.remove('active'); document.getElementById('game-screen').classList.add('active'); initStage(); if(gameLoopInterval) clearInterval(gameLoopInterval); gameLoopInterval = setInterval(updateGame, 30); }",
    "function initStage() { enemiesContainer.innerHTML = ''; enemiesList = []; stageIndicator.innerText = 'FASE: ' + currentStage;",
    "if (currentStage < totalStages) { bossSf.style.display = 'none'; createEnemy(450, 2); createEnemy(680, -2); } else { stageIndicator.innerText = 'CENÁRIO FINAL: BOSS SF'; bossSf.style.display = 'block'; } }",
    "function createEnemy(startX, speed) { const enemyEl = document.createElement('div'); enemyEl.className = 'enemy'; enemyEl.style.left = startX + 'px'; enemiesContainer.appendChild(enemyEl); enemiesList.push({ element: enemyEl, x: startX, speed: speed, minX: startX - 130, maxX: startX + 130 }); }",
    "function updateGame() { enemiesList.forEach(enemy => { enemy.x += enemy.speed; if (enemy.x > enemy.maxX || enemy.x < enemy.minX || enemy.x > 730 || enemy.x < 0) { enemy.speed *= -1; } enemy.element.style.left = enemy.x + 'px';",
    "if (Math.abs(playerX - enemy.x) < 45 && playerY < 120) { if (isAttacking) { enemy.element.remove(); enemiesList = enemiesList.filter(e => e !== enemy); } else if (!isJumping) { playerX = 50; player.style.left = playerX + 'px'; } } });",
    "if (playerX >= 730) { if (currentStage < totalStages) { currentStage++; playerX = 50; player.style.left = playerX + 'px'; initStage(); } else { playerX = 730; player.style.left = playerX + 'px'; } } }",
    "function movePlayer(offset) { if (isAttacking) return; playerX += offset; if (playerX < 0) playerX = 0; if (playerX > 730) playerX = 730; player.style.left = playerX + 'px'; }",
    "function jumpPlayer() { if (isJumping) return; isJumping = true; let baseFloor = playerY; let targetHeight = baseFloor + 140;",
    "let upInterval = setInterval(() => { playerY += 8; player.style.bottom = playerY + 'px'; if (playerY >= targetHeight) { clearInterval(upInterval);",
    "let downInterval = setInterval(() => { playerY -= 8; player.style.bottom = playerY + 'px'; if (playerY <= 55) { clearInterval(downInterval); playerY = 55; player.style.bottom = playerY + 'px'; isJumping = false; } }, 15); } }, 15); }",
    "function attackPlayer() { if (isAttacking) return; isAttacking = true; player.style.filter = 'drop-shadow(0 0 15px #ff1a1a) brightness(1.4)';",
    "if (currentStage === totalStages && playerX >= 520) { bossSf.style.filter = 'hue-rotate(90deg) brightness(2)'; setTimeout(() => { bossSf.style.display = 'none'; alert('Vitória! Você derrotou a Boss SF!'); currentStage = 1; playerX = 100; player.style.left = playerX + 'px'; document.getElementById('game-screen').classList.remove('active'); document.getElementById('menu-screen').classList.add('active'); }, 300); }",
    "setTimeout(() => { player.style.filter = 'none'; isAttacking = false; }, 150); }",
    "window.addEventListener('keydown', function(event) { if(['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.code)) { event.preventDefault(); }",
    "if (!document.getElementById('game-screen').classList.contains('active')) { if (event.code === 'Enter' || event.code === 'Space') { startGame(); } return; }",
    "switch(event.code) { case 'KeyA': case 'ArrowLeft': movePlayer(-25); break; case 'KeyD': case 'ArrowRight': movePlayer(25); break; case 'KeyW': case 'ArrowUp': jumpPlayer(); break; case 'Space': attackPlayer(); break; } });",
    "</script></body></html>"
]

game_html = "".join(partes_html)
components.html(game_html, width=800, height=600)
