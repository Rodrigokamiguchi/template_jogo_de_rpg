from random import randint

lista_npcs = []
# informação do player
player = {
    "nome": "Mario",
    "level": 1,
    "exp": 0,
    "exp_max": 50,
    "hp": 100,
    "hp_max": 100,
    "dano": 25,
    "inventario": {
        "pocao": 3,
    },
}

# desenvolvendo o npc
def criar_npc(level):
    if level == 10:
        nome = "Boss Monstro"
        dano = 50  # Dano do boss
    else:
        nome = f"Monstro {level}"
        dano = 5 * level
    
    novo_npc = {
        "nome": nome,
        "level": level,
        "dano": dano,
        "hp": 100 * level,
        "hp_max": 100 * level,
        "exp": 7 * level,
        "derrotado": False,  # Para verificar se foi derrotado
    }
    return novo_npc

def gerar_npcs(n_npcs):
    for x in range(1, n_npcs + 1):  # Gera de 1 a n_npcs
        npc = criar_npc(x)
        lista_npcs.append(npc)

def selecionar_npc():
    print("\nEscolha um NPC para lutar:")
    for i, npc in enumerate(lista_npcs):
        if not npc["derrotado"] and npc["level"] <= player["level"]:  # Mostra apenas NPCs não derrotados e liberados
            print(f"{i+1}. {npc['nome']} - Level {npc['level']}")
    try:
        escolha = int(input("Digite o número do NPC: ")) - 1
        if 0 <= escolha < len(lista_npcs) and not lista_npcs[escolha]["derrotado"] and lista_npcs[escolha]["level"] <= player["level"]:
            return lista_npcs[escolha]
        else:
            print("Escolha inválida. Tente novamente.")
            return selecionar_npc()  # Recursivamente pede nova escolha
    except ValueError:
        print("Por favor, insira um número válido.")
        return selecionar_npc()  # Recursivamente pede nova escolha

# desenvolvendo o player
def exibir_player():
    print(
        f"Nome: {player['nome']} // Level: {player['level']} // Dano: {player['dano']} // HP: {player['hp']}/{player['hp_max']} // EXP: {player['exp']}/{player['exp_max']}"
    )

def reset_player():
    player["hp"] = player["hp_max"]

def reset_npc(npc):
    npc["hp"] = npc["hp_max"]

def distribuir_experiencia(exp_npc):
    player["exp"] += exp_npc
    if player["exp"] >= player["exp_max"]:
        level_up()

def level_up():
    global player
    if player["exp"] >= player["exp_max"]:
        player["level"] += 1
        player["exp"] -= player["exp_max"]
        player["exp_max"] = int(player["exp_max"] * 1.5)
        player["hp_max"] += 20
        player["dano"] += 5
        player["hp"] = player["hp_max"]  # Recupera vida ao subir de nível
        print(f"Parabéns {player['nome']} subiu para o nível {player['level']}!")

        # Reintroduz os NPCs derrotados após subir de nível
        for npc in lista_npcs:
            if npc["derrotado"]:
                npc["derrotado"] = False  # Marca o NPC como disponível novamente

# desenvolvimento de batalha
def usar_item():
    if "pocao" in player['inventario'] and player['inventario']['pocao'] > 0:
        player["hp"] += 30
        player['inventario']['pocao'] -= 1
        print(f"{player['nome']} usou uma poção e curou 30 HP!")
    else:
        print("Você não tem mais poções.")

def iniciar_batalha(npc):
    reset_npc(npc)  # Reseta o NPC para o máximo de HP
    while player["hp"] > 0 and npc["hp"] > 0:
        acao = input("Escolha uma ação (atacar/defender/item): ").lower()
        if acao == "atacar":
            atacar_npc(npc)
        elif acao == "defender":
            player["hp"] += 10  # Defesa cura um pouco
        elif acao == "item":
            usar_item()
        
        if npc["hp"] > 0:  # O NPC ataca apenas se ainda estiver vivo
            atacar_player(npc)
        
        exibir_info_batalha(npc)

    if player["hp"] > 0:  # Verifica se o jogador venceu
        print(f"{player['nome']} venceu e ganhou {npc['exp']} de EXP!")
        distribuir_experiencia(npc["exp"])  # Distribuir experiência para o jogador
        npc["derrotado"] = True  # Marca o NPC como derrotado
        exibir_player()
    else:
        print(f"O {npc['nome']} venceu!")

# atacar_npc(npc) - npc:hp - player:dano
def atacar_npc(npc):
    dano = randint(player["dano"] - 5, player["dano"] + 5)
    npc["hp"] -= dano
    print(f"{player['nome']} atacou e causou {dano} de dano.")

# atacar_player(npc) - player:hp - npc:dano
def atacar_player(npc):
    dano = randint(npc["dano"] - 2, npc["dano"] + 2)
    player["hp"] -= dano
    print(f"{npc['nome']} atacou e causou {dano} de dano.")

# fim da batalha
def exibir_info_batalha(npc):
    player_hp_bar = "|" * (player["hp"] * 10 // player["hp_max"])
    npc_hp_bar = "|" * (npc["hp"] * 10 // npc["hp_max"])
    print(f"{player['nome']} HP: {player_hp_bar} ({player['hp']}/{player['hp_max']})")
    print(f"{npc['nome']} HP: {npc_hp_bar} ({npc['hp']}/{npc['hp_max']})")


# informações do jogo

gerar_npcs(10)  # Gera 10 NPCs, incluindo o boss

while True:  # Loop principal do jogo
    if all(npc["derrotado"] for npc in lista_npcs):  # Verifica se todos os NPCs foram derrotados
        print("Parabéns! Você derrotou todos os NPCs!")
        break
    
    npc_selecionado = selecionar_npc()
    iniciar_batalha(npc_selecionado)
