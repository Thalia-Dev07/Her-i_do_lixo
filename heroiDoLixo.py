import pygame
import random
import os

# Inicializar o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Ecodefensor: Combatendo Pragas e Infecções.")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)

# Diretório base do jogo
DIRETORIO_BASE = r"C:\Users\jossylyn.campos\Desktop\Jogo-Ecodenfensor"
# Função para carregar imagens com fallback
def carregar_imagem(nome_arquivo, tamanho=None):
    caminho = os.path.join(DIRETORIO_BASE, nome_arquivo)
    if os.path.exists(caminho):
        imagem = pygame.image.load(caminho)
        if tamanho:
            imagem = pygame.transform.scale(imagem, tamanho)
        return imagem
    else:
        print(f"Erro: Imagem '{nome_arquivo}' não encontrada!")
        return pygame.Surface((50, 50))

# Carregar imagens
fundo = carregar_imagem("fundo.jpg", (LARGURA, ALTURA))
leo_img = carregar_imagem("leo.png", (50, 50))
barata_img = carregar_imagem("barata.png", (30, 30))
aranha_img = carregar_imagem("aranha.png", (35, 35))
rato_img = carregar_imagem("rato.png", (35, 35))
lixo_img = carregar_imagem("lixo.png", (30, 30))
chefao_img = carregar_imagem("chafao.png", (100, 100))

# Criar personagem
leo = pygame.Rect(100, 500, 50, 50)
velocidade = 5

# Sons
pygame.mixer.init()
try:
    som_ataque = pygame.mixer.Sound(os.path.join(DIRETORIO_BASE, "ataque.mp3"))
    som_fundo = pygame.mixer.Sound(os.path.join(DIRETORIO_BASE, "coleta.mp3"))
except pygame.error:
    print("Erro: Um ou mais arquivos de som não foram encontrados!")

# Variáveis do jogo
vidas = 3
pontuacao = 0
fase = 1
ataques = []
ataque_velocidade = 7
clock = pygame.time.Clock()

# Função para gerar inimigos e lixos
def gerar_inimigos_e_lixos(quantidade_inimigos, quantidade_lixos):
    inimigos = []
    velocidades = []
    tipos = []
    lixos = []
    
    for _ in range(quantidade_inimigos):
        x = random.randint(0, LARGURA - 35)
        y = random.randint(0, ALTURA - 35)
        tipo = random.choice(["barata", "aranha", "rato"])
        inimigos.append(pygame.Rect(x, y, 35, 35))
        velocidades.append(random.choice([-2, 2]))
        tipos.append(tipo)
    
    for _ in range(quantidade_lixos):
        lixos.append(pygame.Rect(random.randint(0, LARGURA - 30), random.randint(0, ALTURA - 30), 30, 30))
    
    return inimigos, velocidades, tipos, lixos

def tela_fase_concluida():
    fonte = pygame.font.SysFont(None, 72)
    texto = fonte.render("Fase Concluída!", True, VERDE)
    TELA.blit(fundo, (0, 0))
    TELA.blit(texto, ((LARGURA - texto.get_width()) // 2, ALTURA // 2 - 50))
    pygame.display.update()
    pygame.time.delay(2000)  # Espera 2 segundos antes de continuar

# Função para exibir a tela inicial
def tela_inicial():
    TELA.blit(fundo, (0, 0))  # Cenário de fundo com nuvem
    fonte_titulo = pygame.font.SysFont(None, 72)
    fonte_botao = pygame.font.SysFont(None, 48)
    
    # Desenhar título com quebra de linha
    titulo1 = fonte_titulo.render("Ecodefensor:", True, PRETO)
    titulo2 = fonte_titulo.render("Combatendo Pragas e Infecções", True, PRETO)

# Centralizar na tela
    x_centro = (LARGURA - titulo1.get_width()) // 2
    y_inicial = (ALTURA // 2) - 100  # Ajuste conforme necessário

# Desenhar na tela
    TELA.blit(titulo1, (x_centro, y_inicial))
    TELA.blit(titulo2, ((LARGURA - titulo2.get_width()) // 2, y_inicial + 50))  # 50px abaixo

    
    # Desenhar botão "Play"
    botao_play = pygame.Rect(LARGURA // 2 - 50, ALTURA // 2, 120, 50)
    pygame.draw.rect(TELA, VERDE, botao_play)
    texto_play = fonte_botao.render("Play", True, PRETO)
    TELA.blit(texto_play, (botao_play.x + 25, botao_play.y + 10))
    
    pygame.display.update()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_play.collidepoint(evento.pos):
                    esperando = False
    return True

# Função para exibir tela de "Game Over"
def tela_game_over():
    TELA.blit(fundo, (0, 0))  # Cenário de fundo com nuvem
    fonte_titulo = pygame.font.SysFont(None, 72)
    fonte_botao = pygame.font.SysFont(None, 48)
    
   # Desenhar título centralizado
    titulo = fonte_titulo.render("Game Over", True, PRETO)
    titulo_x = (LARGURA - titulo.get_width()) // 2
    titulo_y = (ALTURA // 2) - 130
    TELA.blit(titulo, (titulo_x, titulo_y))

    # Definir tamanho do botão "Jogar Novamente"
    botao_largura, botao_altura = 330, 50
    botao_x = (LARGURA - botao_largura) // 2
    botao_y = ALTURA // 2

    # Criar e desenhar o botão centralizado
    botao_play = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)
    pygame.draw.rect(TELA, VERDE, botao_play)

    # Renderizar e centralizar o texto dentro do botão
    texto_play = fonte_botao.render("Jogar Novamente", True, PRETO)
    texto_x = botao_x + (botao_largura - texto_play.get_width()) // 2
    texto_y = botao_y + (botao_altura - texto_play.get_height()) // 2
    TELA.blit(texto_play, (texto_x, texto_y))

    
    pygame.display.update()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_play.collidepoint(evento.pos):
                    esperando = False
                    return True
    return False

# Gerar inimigos e lixos
inimigos, velocidades_inimigos, tipos_inimigos, lixos = gerar_inimigos_e_lixos(10, 15)

# Exibir tela inicial
if not tela_inicial():
    pygame.quit()
    exit()

# Iniciar a música de fundo após o clique em "Play"
som_fundo.play(-1)  # Tocar o som de fundo em loop

# Variável para controlar a música de coleta
som_coleta_tocando = False

# Loop principal do jogo
rodando = True
while rodando:
    clock.tick(30)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            ataques.append(pygame.Rect(leo.x + 20, leo.y, 10, 20))
            som_ataque.play()
  
    # Movimento do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: leo.x = max(0, leo.x - velocidade)
    if teclas[pygame.K_RIGHT]: leo.x = min(LARGURA - leo.width, leo.x + velocidade)
    if teclas[pygame.K_UP]: leo.y = max(0, leo.y - velocidade)
    if teclas[pygame.K_DOWN]: leo.y = min(ALTURA - leo.height, leo.y + velocidade)

    # Movimento dos inimigos
    for i, inimigo in enumerate(inimigos):
        inimigo.x += velocidades_inimigos[i]
        if inimigo.x <= 0 or inimigo.x >= LARGURA - 35:
            velocidades_inimigos[i] *= -1

    # Movimentação dos ataques
    for ataque in ataques:
        ataque.y -= ataque_velocidade
    ataques = [ataque for ataque in ataques if ataque.y > 0]

    # Verificar colisões entre Léo e inimigos
    for inimigo in inimigos[:]:
        if leo.colliderect(inimigo):
            vidas -= 1
            inimigos.remove(inimigo)
            if vidas == 0:
                if tela_game_over():  # Exibe tela de game over e reinicia
                    # Reiniciar variáveis do jogo
                    vidas = 3
                    pontuacao = 0
                    inimigos, velocidades_inimigos, tipos_inimigos, lixos = gerar_inimigos_e_lixos(10, 7)
                    som_fundo.play(-1)
                else:
                    rodando = False

    # Verificar colisões entre Léo e lixos
    for lixo in lixos[:]:
        if leo.colliderect(lixo):
            pontuacao += 5
            lixos.remove(lixo)
            if not som_coleta_tocando:
                som_coleta_tocando = True
    if not lixos:
        tela_fase_concluida()
        lixos = gerar_lixos(10)  # Gera nova fase

    # Desenhar elementos na tela
    TELA.blit(fundo, (0, 0))
    TELA.blit(leo_img, (leo.x, leo.y))
    for i, inimigo in enumerate(inimigos):
        imagem = barata_img if tipos_inimigos[i] == "barata" else aranha_img if tipos_inimigos[i] == "aranha" else rato_img
        TELA.blit(imagem, (inimigo.x, inimigo.y))
    for lixo in lixos:
        TELA.blit(lixo_img, (lixo.x, lixo.y))

    # Exibir informações na tela
    fonte = pygame.font.SysFont(None, 36)
    TELA.blit(fonte.render(f"Vidas: {vidas}", True, (255, 0, 0)), (10, 10))
    TELA.blit(fonte.render(f"Pontuação: {pontuacao}", True, (0, 0, 255)), (10, 50))
    pygame.display.update()

    # Reseta o som de coleta após ele terminar de tocar
    if not pygame.mixer.get_busy():
        som_coleta_tocando = False

pygame.quit()
