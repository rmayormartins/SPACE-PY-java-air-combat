---
title: Java-Air-Combat
emoji: ⯐🛦🛧
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# ⯐🛦🛧 Java Air Combat - Arena de Batalha Aérea

Uma ferramenta educativa gamificada para aprendizado de programação Java através de combate aéreo entre aeronaves programáveis.

## Desenvolvedor
Desenvolvido por Ramon Mayor Martins (2025)
- Email: ramon.mayor@ifsc.edu.br
- Homepage: https://rmayormartins.github.io/
- Twitter: @rmayormartins
- GitHub: https://github.com/rmayormartins
- Space: https://huggingface.co/rmayormartins
- Instituição: IFSC - Instituto Federal de Santa Catarina

## 🎮 Sobre o Jogo

Java Air Combat é uma plataforma onde você programa sua própria aeronave de combate em Java e a coloca para batalhar contra outras aeronaves. É uma metodologia de **Gamificação no nível Modify** de código, desenvolvida para a disciplina de Programação.

### ✨ Características Principais

- **Sistema de Pontos**: Distribua 100 pontos entre 11 atributos diferentes
- **Combate em Tempo Real**: Visualize suas aeronaves batalhando em uma arena ASCII colorida
- **Estratégias Avançadas**: Implemente táticas de movimento, altitude e combate
- **Novos Recursos**: Radar, tiro duplo, mísseis nucleares e mais!

## 🚀 Como Usar

1. **Carregar Templates**: Clique nos botões para carregar o código base de cada time
2. **Personalizar Aeronaves**: Distribua seus 100 pontos entre os atributos
3. **Configurar Arena**: Ajuste tamanho, posições iniciais e vida das aeronaves
4. **Batalhar**: Clique em "🔥 Combate!" e assista à batalha!

## 📊 Atributos das Aeronaves

| Atributo | Faixa | Descrição |
|----------|-------|-----------|
| **speed** | 1-10 | Velocidade de movimento |
| **fireRate** | 1-10 | Taxa de disparo |
| **maneuverability** | 1-10 | Facilita mudanças de altitude |
| **shotPower** | 5-20 | Dano do tiro normal |
| **supersonicPower** | 10-30 | Dano do tiro supersônico |
| **missilePower** | 15-40 | Dano do míssil especial |
| **defense** | 5-25 | Reduz dano recebido |
| **stealthChance** | 0-20 | Chance de esquiva |
| **radar** | 0-10 | Detecção de projéteis |
| **doubleShot** | 0-10 | Tiro em duas altitudes |
| **nuclearPower** | 0-10 | Poder do míssil nuclear |

> **Importante**: A soma de todos os atributos não pode exceder 100 pontos!

## 🎯 Tipos de Projéteis

- **Tiro Normal** (`->`, `<-`): Básico, frequente
- **Tiro Supersônico** (`>>`, `<<`): Mais rápido e poderoso  
- **Míssil Especial** (`=>`, `<=`): Alto dano, cooldown de 3 turnos
- **Tiro Duplo** (`=>`, `<=`): Ataca em duas altitudes simultaneamente
- **Míssil Nuclear** (`-N->`, `<-N-`): Dano massivo, cooldown de 5 turnos

## 🏗️ Configurações da Arena

### Tabela de Configurações
| Configuração | Faixa | Descrição |
|-------------|-------|-----------|
| **Largura da Tela** | 50-200 | Define a largura do campo de batalha |
| **Altura do Campo** | 3-7 | Define o número de linhas/altitudes possíveis |
| **Posição Inicial Time 1** | 0-49 | Define onde o Time 1 começa na arena |
| **Posição Inicial Time 2** | 51-200 | Define onde o Time 2 começa na arena |
| **Vida Time 1** | 50-500 | Define a vida inicial da aeronave do Time 1 |
| **Vida Time 2** | 50-500 | Define a vida inicial da aeronave do Time 2 |

## 🎨 Representação Visual

### Aeronaves e Projéteis
| Símbolo | Origem | Significado |
|---------|--------|-------------|
| `T1` | Time 1 | Aeronave do Time 1 |
| `T2` | Time 2 | Aeronave do Time 2 |
| `->` | Time 1 | Tiro normal do Time 1 |
| `<-` | Time 2 | Tiro normal do Time 2 |
| `>>` | Time 1 | Tiro supersônico do Time 1 |
| `<<` | Time 2 | Tiro supersônico do Time 2 |
| `=>` | Time 1 | Míssil especial do Time 1 |
| `<=` | Time 2 | Míssil especial do Time 2 |
| `=>` | Time 1 | Tiro duplo do Time 1 |
| `<=` | Time 2 | Tiro duplo do Time 2 |
| `-N->` | Time 1 | Míssil nuclear do Time 1 |
| `<-N-` | Time 2 | Míssil nuclear do Time 2 |

### Alertas do Sistema
| Emoji | Mensagem | Significado |
|-------|----------|-------------|
| ❤️ | Vida Time X: 100 | Mostra a vida atual da aeronave |
| 💥 | Aeronave atingida! | Indica que uma aeronave foi atingida |
| 👻 | Aeronave esquivou! | Indica esquiva bem-sucedida |
| 📡 | Radar detectou projétil! | O radar detectou um projétil inimigo |
| ☢️ | Míssil nuclear lançado! | Alerta sobre míssil nuclear |
| 🏆 | Time X venceu! | Indica o vencedor da batalha |

## 💡 Dicas de Estratégia

1. **Equilíbrio**: Aeronaves balanceadas são mais eficazes que especializadas
2. **Contramedidas**: Defesa baixa? Compense com manobrabilidade e furtividade
3. **Movimento Inteligente**: Crie padrões ao invés de movimento aleatório
4. **Use o Radar**: Detecte projéteis e implemente esquivas automáticas
5. **Tiro Duplo**: Aumente chances de acerto atacando múltiplas altitudes
6. **Mísseis Nucleares**: Use estrategicamente - alto dano, mas longo cooldown

## 🔧 Métodos Personalizáveis

| Método | Parâmetros | Retorno | Descrição |
|--------|------------|---------|-----------|
| `move()` | nenhum | int | Controla movimento horizontal |
| `changeAltitude()` | nenhum | int | Controla mudanças de altitude |
| `shoot()` | posX, direction | Projectile | Dispara tiro normal |
| `shootSupersonic()` | posX, direction | Projectile | Dispara tiro supersônico |
| `specialMissile()` | posX, direction | Projectile | Dispara míssil especial |
| `doubleShot()` | posX, direction | Projectile | Implementa tiro duplo |
| `nuclearMissile()` | posX, direction | Projectile | Controla mísseis nucleares |
| `radarScan()` | projectiles, enemyPosX, enemyPosY | void | Processa informações do radar |

## 📚 Conceitos de Programação Aplicados

Esta ferramenta ensina conceitos fundamentais de programação:

- **Herança**: Aeronaves estendem a classe abstrata `Aircraft`
- **Polimorfismo**: Métodos abstratos implementados de forma única por cada aeronave
- **Encapsulamento**: Atributos protegidos e métodos públicos bem definidos
- **Abstração**: Interface comum para diferentes tipos de aeronaves
- **Lógica Algorítmica**: Estratégias de movimento, combate e tomada de decisão

## 🏫 Uso Educacional

### Objetivos de Aprendizagem
- Programação Orientada a Objetos em Java
- Conceitos de herança e polimorfismo
- Lógica de programação e algoritmos
- Estratégia computacional
- Debugging e otimização de código
- Pensamento algorítmico aplicado a jogos

### Metodologia
- **Gamificação no nível Modify**: Estudantes modificam código existente para criar estratégias únicas
- **Aprendizado baseado em competição**: Motiva experimentação e refinamento
- **Feedback visual imediato**: Resultados das estratégias são vistos em tempo real

## 🔄 Desenvolvimento Local

Para rodar localmente:

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python app.py
```

**Requisitos do sistema:**
- Java JDK 8+ instalado
- Python 3.7+
- Gradio 4.44.0

## 🤝 Contribuições

Este projeto é educacional e está aberto a melhorias:
- Novas funcionalidades de combate
- Estratégias de IA mais avançadas
- Melhorias na interface
- Correções de bugs
- Otimizações de performance

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE). Use livremente em contextos acadêmicos e de aprendizado.

---

🎮 **Bons combates e boa programação!** ✈️🚁💥