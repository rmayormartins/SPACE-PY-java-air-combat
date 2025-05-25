import gradio as gr
import os
import subprocess
import time
from collections import deque
import shutil
import re

def format_colors(text):
    """Remove todos os códigos de cor e deixa apenas texto puro"""
    import re
    
    # Remover qualquer código ANSI
    ansi_pattern = r'\x1b\[[0-9;]*m|\[([0-9;]*)m'
    text = re.sub(ansi_pattern, '', text)
    
    # Remover códigos unicode de escape
    text = text.replace("\\u001B[31m", "")
    text = text.replace("\\u001B[34m", "")
    text = text.replace("\\u001B[32m", "")
    text = text.replace("\\u001B[0m", "")
    
    # Remover códigos sem escape
    text = text.replace("[31m", "")
    text = text.replace("[34m", "")
    text = text.replace("[32m", "")
    text = text.replace("[0m", "")
    
    # NÃO alterar os símbolos das aeronaves - deixar como estão
    # > e < são as aeronaves e devem aparecer normalmente
    
    return text

def check_and_install_java():
    """Verifica se Java está instalado e tenta instalar se necessário"""
    try:
        # Verificar se javac está disponível
        result = subprocess.run(["javac", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            return True, "Java já está instalado"
    except FileNotFoundError:
        pass
    
    try:
        # Tentar instalar Java usando apt-get
        print("🔧 Instalando Java...")
        subprocess.run(["apt-get", "update"], check=True, capture_output=True)
        subprocess.run(["apt-get", "install", "-y", "default-jdk"], check=True, capture_output=True)
        
        # Verificar se a instalação funcionou
        result = subprocess.run(["javac", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            return True, "Java instalado com sucesso"
    except Exception as e:
        pass
    
    # Se chegou até aqui, não conseguiu instalar
    return False, "Não foi possível instalar Java automaticamente"

# Verificar Java na inicialização
java_available, java_message = check_and_install_java()
print(f"Status do Java: {java_message}")

# Criar pasta para armazenar as classes Java
os.makedirs("combat_classes", exist_ok=True)

# Templates de código para as aeronaves com altura dinâmica e novos atributos
TEAM1_TEMPLATE = '''import java.util.ArrayList;
import java.util.Random;

/**
 * Time 1 - Configure sua aeronave!
 *
 * SISTEMA DE PONTOS:
 * - Você tem 100 pontos para distribuir entre os atributos
 * - Escolha com sabedoria para criar uma aeronave competitiva
 *
 * ATRIBUTOS:
 * - speed: Velocidade da aeronave (1-10) - Afeta quão rápido sua aeronave pode se mover
 * - fireRate: Taxa de disparo (1-10) - Controla com que frequência sua aeronave pode atirar
 * - maneuverability: Manobrabilidade (1-10) - Facilita mudanças de altitude e esquivas
 * - shotPower: Poder do tiro normal (5-20) - Dano causado por tiros normais
 * - supersonicPower: Poder do tiro supersônico (10-30) - Dano causado por tiros supersônicos
 * - missilePower: Poder do míssil (15-40) - Dano causado pelo míssil especial
 * - defense: Defesa (5-25) - Reduz o dano recebido
 * - stealthChance: Chance de furtividade (0-20) - Probabilidade de evitar ataques
 * - radar: Radar (0-10) - Capacidade de detectar projéteis inimigos
 * - doubleShot: Tiro duplo (0-10) - Permite disparar em duas altitudes diferentes
 * - nuclearPower: Poder nuclear (0-10) - Poder do míssil nuclear (dano massivo)
 * 
 * SÍMBOLOS:
 * - Aeronave: T1 (Time 1)
 * - Tiro normal: ->
 * - Tiro supersônico: >>
 * - Míssil especial: =>
 * - Tiro duplo: =>
 * - Míssil nuclear: -N->
 */
public class Team1Aircraft extends Aircraft {
    private Random random = new Random();
    private int maxAltitude; // Armazena a altura máxima do campo

    public Team1Aircraft() {
        super(
            // DISTRIBUA 100 PONTOS ENTRE ESSES ATRIBUTOS
            5,  // Velocidade (1-10)
            5,  // Taxa de fogo (1-10)
            5,  // Manobrabilidade (1-10)
            15, // Dano do tiro normal (5-20)
            20, // Dano do tiro supersônico (10-30)
            25, // Dano do míssil (15-40)
            15, // Defesa (5-25)
            5,  // Chance de furtividade (0-20)
            2,  // Radar (0-10)
            2,  // Tiro duplo (0-10)
            1,  // Poder nuclear (0-10)
            "▶" // Símbolo da aeronave (não altere)
        );

        // IMPORTANTE: A soma de todos os atributos deve ser <= 100
        // Exemplo: 5+5+5+15+20+25+15+5+2+2+1 = 100

        // Verifica dinamicamente a altura do campo (será definida pelo BattleMain)
        try {
            String heightEnv = System.getProperty("battlefield.height", "3");
            maxAltitude = Integer.parseInt(heightEnv) - 1;
        } catch (Exception e) {
            maxAltitude = 2; // Valor padrão se não conseguir ler
        }
    }

    /**
     * Controla o movimento da aeronave.
     * Valor padrão: Movimento aleatório baseado na velocidade
     * Dica: Você pode personalizar para criar padrões de movimento mais inteligentes
     */
    @Override
    public int move() {
        // Retorna um número entre -speed/2 e +speed
        return random.nextInt(speed + 1) - speed / 2;
    }

    /**
     * Controla a mudança de altitude da aeronave.
     * Valor padrão: Mudança aleatória entre subir, descer ou manter altitude
     * Dica: Uma boa estratégia pode aumentar suas chances de esquiva
     */
    @Override
    public int changeAltitude() {
        int direction = random.nextInt(3) - 1; // -1 (descer), 0 (manter), 1 (subir)
        this.posY = Math.max(0, Math.min(maxAltitude, posY + direction));
        return direction;
    }

    /**
     * Tiro normal - mais frequente, menos dano
     */
    @Override
    public Projectile shoot(int posX, int direction) {
        return new Projectile(posX, this.posY, direction, 1, "->");
    }

    /**
     * Tiro supersônico - mais rápido, mais dano
     */
    @Override
    public Projectile shootSupersonic(int posX, int direction) {
        return new Projectile(posX, this.posY, direction, 2, ">>");
    }

    /**
     * Míssil especial - muito dano, com cooldown
     */
    @Override
    public Projectile specialMissile(int posX, int direction) {
        if (missileCooldown == 0) {
            missileCooldown = 3; // Espera 3 turnos para usar novamente
            return new Projectile(posX, this.posY, direction, 1, "=>");
        }
        missileCooldown--;
        return null;
    }

    /**
     * Tiro duplo - ataca em duas altitudes diferentes
     */
    @Override
    public Projectile doubleShot(int posX, int direction) {
        // Define a segunda altitude para o tiro (diferente da atual)
        int currentAlt = this.posY;
        int secondAlt = (currentAlt + 1) % (maxAltitude + 1);

        // Guarda essa altitude para ser usada pelo BattleMain
        this.secondShotAltitude = secondAlt;

        // Retorna o projétil principal
        return new Projectile(posX, this.posY, direction, 1, "=>");
    }

    /**
     * Míssil nuclear - dano massivo
     */
    @Override
    public Projectile nuclearMissile(int posX, int direction) {
        if (missileCooldown == 0) {
            missileCooldown = 5; // Longo cooldown para o poder nuclear
            return new Projectile(posX, this.posY, direction, 1, "-]=>");
        }
        return null;
    }

    /**
     * Radar - detecta projéteis inimigos
     */
    @Override
    public void radarScan(ArrayList<Projectile> projectiles, int enemyPosX, int enemyPosY) {
        // Implementação básica: apenas detecta projéteis próximos
        // Em uma implementação mais avançada, você poderia usar essas informações
        // para ajustar seu movimento e evitar projéteis
    }
}'''

TEAM2_TEMPLATE = '''import java.util.ArrayList;
import java.util.Random;

/**
 * Time 2 - Configure sua aeronave!
 *
 * SISTEMA DE PONTOS:
 * - Você tem 100 pontos para distribuir entre os atributos
 * - Escolha com sabedoria para criar uma aeronave competitiva
 *
 * ATRIBUTOS:
 * - speed: Velocidade da aeronave (1-10) - Afeta quão rápido sua aeronave pode se mover
 * - fireRate: Taxa de disparo (1-10) - Controla com que frequência sua aeronave pode atirar
 * - maneuverability: Manobrabilidade (1-10) - Facilita mudanças de altitude e esquivas
 * - shotPower: Poder do tiro normal (5-20) - Dano causado por tiros normais
 * - supersonicPower: Poder do tiro supersônico (10-30) - Dano causado por tiros supersônicos
 * - missilePower: Poder do míssil (15-40) - Dano causado pelo míssil especial
 * - defense: Defesa (5-25) - Reduz o dano recebido
 * - stealthChance: Chance de furtividade (0-20) - Probabilidade de evitar ataques
 * - radar: Radar (0-10) - Capacidade de detectar projéteis inimigos
 * - doubleShot: Tiro duplo (0-10) - Permite disparar em duas altitudes diferentes
 * - nuclearPower: Poder nuclear (0-10) - Poder do míssil nuclear (dano massivo)
 * 
 * SÍMBOLOS:
 * - Aeronave: T2 (Time 2)
 * - Tiro normal: <-
 * - Tiro supersônico: <<
 * - Míssil especial: <=
 * - Tiro duplo: <=
 * - Míssil nuclear: <-N-
 */
public class Team2Aircraft extends Aircraft {
    private Random random = new Random();
    private int maxAltitude; // Armazena a altura máxima do campo

    public Team2Aircraft() {
        super(
            // DISTRIBUA 100 PONTOS ENTRE ESSES ATRIBUTOS
            5,  // Velocidade (1-10)
            5,  // Taxa de fogo (1-10)
            5,  // Manobrabilidade (1-10)
            15, // Dano do tiro normal (5-20)
            20, // Dano do tiro supersônico (10-30)
            25, // Dano do míssil (15-40)
            15, // Defesa (5-25)
            5,  // Chance de furtividade (0-20)
            2,  // Radar (0-10)
            2,  // Tiro duplo (0-10)
            1,  // Poder nuclear (0-10)
            "◀" // Símbolo da aeronave (não altere)
        );

        // IMPORTANTE: A soma de todos os atributos deve ser <= 100
        // Exemplo: 5+5+5+15+20+25+15+5+2+2+1 = 100

        // Verifica dinamicamente a altura do campo (será definida pelo BattleMain)
        try {
            String heightEnv = System.getProperty("battlefield.height", "3");
            maxAltitude = Integer.parseInt(heightEnv) - 1;
        } catch (Exception e) {
            maxAltitude = 2; // Valor padrão se não conseguir ler
        }
    }

    /**
     * Controla o movimento da aeronave.
     * Valor padrão: Movimento aleatório baseado na velocidade
     * Dica: Você pode personalizar para criar padrões de movimento mais inteligentes
     */
    @Override
    public int move() {
        // Retorna um número entre -speed/2 e +speed
        return random.nextInt(speed + 1) - speed / 2;
    }

    /**
     * Controla a mudança de altitude da aeronave.
     * Valor padrão: Mudança aleatória entre subir, descer ou manter altitude
     * Dica: Uma boa estratégia pode aumentar suas chances de esquiva
     */
    @Override
    public int changeAltitude() {
        int direction = random.nextInt(3) - 1; // -1 (descer), 0 (manter), 1 (subir)
        this.posY = Math.max(0, Math.min(maxAltitude, posY + direction));
        return direction;
    }

    /**
     * Tiro normal - mais frequente, menos dano
     */
    @Override
    public Projectile shoot(int posX, int direction) {
        return new Projectile(posX, this.posY, direction, 1, "<-");
    }

    /**
     * Tiro supersônico - mais rápido, mais dano
     */
    @Override
    public Projectile shootSupersonic(int posX, int direction) {
        return new Projectile(posX, this.posY, direction, 2, "<<");
    }

    /**
     * Míssil especial - muito dano, com cooldown
     */
    @Override
    public Projectile specialMissile(int posX, int direction) {
        if (missileCooldown == 0) {
            missileCooldown = 3; // Espera 3 turnos para usar novamente
            return new Projectile(posX, this.posY, direction, 1, "<=");
        }
        missileCooldown--;
        return null;
    }

    /**
     * Tiro duplo - ataca em duas altitudes diferentes
     */
    @Override
    public Projectile doubleShot(int posX, int direction) {
        // Define a segunda altitude para o tiro (diferente da atual)
        int currentAlt = this.posY;
        int secondAlt = (currentAlt + 1) % (maxAltitude + 1);

        // Guarda essa altitude para ser usada pelo BattleMain
        this.secondShotAltitude = secondAlt;

        // Retorna o projétil principal
        return new Projectile(posX, this.posY, direction, 1, "<=");
    }

    /**
     * Míssil nuclear - dano massivo
     */
    @Override
    public Projectile nuclearMissile(int posX, int direction) {
        if (missileCooldown == 0) {
            missileCooldown = 5; // Longo cooldown para o poder nuclear
            return new Projectile(posX, this.posY, direction, 1, "<[=-");
        }
        return null;
    }

    /**
     * Radar - detecta projéteis inimigos
     */
    @Override
    public void radarScan(ArrayList<Projectile> projectiles, int enemyPosX, int enemyPosY) {
        // Implementação básica: apenas detecta projéteis próximos
        // Em uma implementação mais avançada, você poderia usar essas informações
        // para ajustar seu movimento e evitar projéteis
    }
}'''

# Código base das classes Aircraft e Projectile
aircraft_code = """
import java.util.ArrayList;

public abstract class Aircraft {
    protected int health;  // Agora definido externamente
    protected int speed;
    protected int fireRate;
    protected int maneuverability;
    protected int shotPower;
    protected int supersonicPower;
    protected int missilePower;
    protected int defense;
    protected int stealthChance;
    protected int radar;
    protected int doubleShot;
    protected int doubleShotPower;
    protected int nuclearPower;
    protected int secondShotAltitude = -1;
    protected int missileCooldown = 0;
    protected int posY = 1;
    protected String symbol;
    protected static final int TOTAL_POINTS = 100;

    public Aircraft(int speed, int fireRate, int maneuverability, int shotPower, int supersonicPower,
                    int missilePower, int defense, int stealthChance, int radar, int doubleShot,
                    int nuclearPower, String symbol) {
        this.health = 100;  // Valor padrão que será substituído
        this.speed = speed;
        this.fireRate = fireRate;
        this.maneuverability = maneuverability;
        this.shotPower = shotPower;
        this.supersonicPower = supersonicPower;
        this.missilePower = missilePower;
        this.defense = defense;
        this.stealthChance = stealthChance;
        this.radar = radar;
        this.doubleShot = doubleShot;
        this.doubleShotPower = doubleShot;
        this.nuclearPower = nuclearPower;
        this.symbol = symbol;

        validateAttributes();
    }

    public void setInitialHealth(int health) {
        this.health = health;
    }

    private void validateAttributes() {
        int total = speed + fireRate + maneuverability + shotPower + supersonicPower +
                   missilePower + defense + stealthChance + radar + doubleShot + nuclearPower;
        if (total > TOTAL_POINTS) {
            throw new IllegalArgumentException("Erro: A soma dos atributos excede " + TOTAL_POINTS + " pontos! Total: " + total);
        }
    }

    public abstract int move();
    public abstract int changeAltitude();
    public abstract Projectile shoot(int posX, int direction);
    public abstract Projectile shootSupersonic(int posX, int direction);
    public abstract Projectile specialMissile(int posX, int direction);
    public abstract Projectile doubleShot(int posX, int direction);
    public abstract Projectile nuclearMissile(int posX, int direction);
    public abstract void radarScan(ArrayList<Projectile> projectiles, int enemyPosX, int enemyPosY);

    public int getHealth() {
        return health;
    }

    public void takeDamage(int damage) {
        this.health -= Math.max(0, damage - (defense / 10));
    }

    public boolean isAlive() {
        return health > 0;
    }

    public int getPositionY() {
        return posY;
    }

    public int getSecondShotAltitude() {
        int alt = secondShotAltitude;
        secondShotAltitude = -1; // Reset após uso
        return alt;
    }
}
"""

projectile_code = """
public class Projectile {
    int posX;
    int posY;
    int direction;
    int speed;
    String symbol;
    int power = 0;  // Poder do projétil, usado para dano personalizado

    public Projectile(int posX, int posY, int direction, int speed, String symbol) {
        this.posX = posX;
        this.posY = posY;
        this.direction = direction;
        this.speed = speed;
        this.symbol = symbol;
    }

    public Projectile(int posX, int posY, int direction, int speed, String symbol, int power) {
        this(posX, posY, direction, speed, symbol);
        this.power = power;
    }

    public void move() {
        posX += direction * speed;
    }

    public boolean isOutOfBounds(int screenWidth) {
        return (posX < 0 || posX >= screenWidth);
    }

    public int getPower() {
        return power;
    }
}
"""

def run_battle(code1, code2, screen_width, battlefield_height, p1_start_pos, p2_start_pos, team1_health, team2_health):
    # Verificar se Java está disponível
    if not java_available:
        yield f"""
        <div style="padding:20px; background-color:#ffe6e6; border:2px solid #ff4444; border-radius:5px; margin:10px;">
            <h3 style="color:#cc0000;">❌ Java não está disponível</h3>
            <p>Este aplicativo requer Java para compilar e executar as aeronaves.</p>
            <p><strong>Soluções:</strong></p>
            <ul>
                <li>Execute localmente com Java instalado</li>
                <li>Use um ambiente Docker com Java</li>
                <li>Aguarde enquanto tentamos instalar Java automaticamente...</li>
            </ul>
            <p><em>Status: {java_message}</em></p>
        </div>
        """
        return
    
    # Caminhos dos arquivos Java
    aircraft_path = "combat_classes/Aircraft.java"
    projectile_path = "combat_classes/Projectile.java"
    class1_path = "combat_classes/Team1Aircraft.java"
    class2_path = "combat_classes/Team2Aircraft.java"
    main_path = "combat_classes/BattleMain.java"

    # Gerar o código do BattleMain com os parâmetros configuráveis
    battle_main_code = f"""
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Random;

public class BattleMain {{
    public static void main(String[] args) {{
        // Definir a altura do campo como propriedade do sistema
        System.setProperty("battlefield.height", "{battlefield_height}");

        Aircraft team1 = new Team1Aircraft();
        Aircraft team2 = new Team2Aircraft();

        // Definir a vida inicial de cada aeronave
        team1.setInitialHealth({team1_health});
        team2.setInitialHealth({team2_health});

        Random random = new Random();

        int p1PosX = {p1_start_pos};
        int p2PosX = {p2_start_pos};
        int screenWidth = {screen_width};
        int battlefieldHeight = {battlefield_height};
        ArrayList<Projectile> projectiles = new ArrayList<>();

        // Inicializar as altitudes das naves em uma posição média do campo
        team1.posY = battlefieldHeight / 2;
        team2.posY = battlefieldHeight / 2;

        while (team1.isAlive() && team2.isAlive()) {{
            System.out.println("\\n=== NOVO TURNO ===");
            System.out.flush();

            String[][] battlefield = new String[battlefieldHeight][screenWidth];
            for (int row = 0; row < battlefieldHeight; row++) {{
                for (int i = 0; i < screenWidth; i++) {{
                    battlefield[row][i] = " ";
                }}
            }}

            // Radar scan para detectar projéteis
            team1.radarScan(projectiles, p2PosX, team2.getPositionY());
            team2.radarScan(projectiles, p1PosX, team1.getPositionY());

            // Movimento das aeronaves
            p1PosX += team1.move();
            p2PosX += team2.move();
            p1PosX = Math.max(0, Math.min(screenWidth - 1, p1PosX));
            p2PosX = Math.max(0, Math.min(screenWidth - 1, p2PosX));

            // Mudança de altitude
            team1.changeAltitude();
            team2.changeAltitude();
            // Garantir que a altitude não exceda o novo tamanho do campo de batalha
            team1.posY = Math.min(team1.posY, battlefieldHeight - 1);
            team2.posY = Math.min(team2.posY, battlefieldHeight - 1);

            // Atirar para Time 1
            if (random.nextInt(10) < team1.fireRate) {{
                Projectile shot = null;
                int shotType = random.nextInt(100);

                // Escolha aleatória do tipo de tiro baseado na probabilidade
                if (shotType < 5 && team1.nuclearPower > 0) {{
                    // Tiro nuclear (baixa probabilidade)
                    shot = team1.nuclearMissile(p1PosX, 1);
                    if (shot != null) {{
                        System.out.println("!!! Time 1 lançou um MISSIL NUCLEAR!");
                    }}
                }} else if (shotType < 15 && team1.doubleShot > 0) {{
                    // Tiro duplo
                    shot = team1.doubleShot(p1PosX, 1);
                    if (shot != null) {{
                        System.out.println(">>> Time 1 disparou um TIRO DUPLO!");
                        // Adicionar o segundo projétil em uma altitude diferente
                        int secAlt = team1.getSecondShotAltitude();
                        if (secAlt >= 0 && secAlt < battlefieldHeight) {{
                            projectiles.add(new Projectile(p1PosX, secAlt, 1, 1, "->", team1.doubleShotPower));
                        }}
                    }}
                }} else if (shotType < 30) {{
                    // Míssil especial
                    shot = team1.specialMissile(p1PosX, 1);
                }} else if (shotType < 60) {{
                    // Tiro supersônico
                    shot = team1.shootSupersonic(p1PosX, 1);
                }} else {{
                    // Tiro normal
                    shot = team1.shoot(p1PosX, 1);
                }}

                if (shot != null) {{
                    // Garantir que a altitude do projétil não exceda o campo de batalha
                    shot.posY = Math.min(shot.posY, battlefieldHeight - 1);
                    projectiles.add(shot);
                }}
            }}

            // Atirar para Time 2
            if (random.nextInt(10) < team2.fireRate) {{
                Projectile shot = null;
                int shotType = random.nextInt(100);

                // Escolha aleatória do tipo de tiro baseado na probabilidade
                if (shotType < 5 && team2.nuclearPower > 0) {{
                    // Tiro nuclear (baixa probabilidade)
                    shot = team2.nuclearMissile(p2PosX, -1);
                    if (shot != null) {{
                        System.out.println("!!! Time 2 lançou um MISSIL NUCLEAR!");
                    }}
                }} else if (shotType < 15 && team2.doubleShot > 0) {{
                    // Tiro duplo
                    shot = team2.doubleShot(p2PosX, -1);
                    if (shot != null) {{
                        System.out.println("<<< Time 2 disparou um TIRO DUPLO!");
                        // Adicionar o segundo projétil em uma altitude diferente
                        int secAlt = team2.getSecondShotAltitude();
                        if (secAlt >= 0 && secAlt < battlefieldHeight) {{
                            projectiles.add(new Projectile(p2PosX, secAlt, -1, 1, "<-", team2.doubleShotPower));
                        }}
                    }}
                }} else if (shotType < 30) {{
                    // Míssil especial
                    shot = team2.specialMissile(p2PosX, -1);
                }} else if (shotType < 60) {{
                    // Tiro supersônico
                    shot = team2.shootSupersonic(p2PosX, -1);
                }} else {{
                    // Tiro normal
                    shot = team2.shoot(p2PosX, -1);
                }}

                if (shot != null) {{
                    // Garantir que a altitude do projétil não exceda o campo de batalha
                    shot.posY = Math.min(shot.posY, battlefieldHeight - 1);
                    projectiles.add(shot);
                }}
            }}

            // Posicionar aeronaves no campo de batalha sem cores
            battlefield[team1.getPositionY()][p1PosX] = team1.symbol;  // Time 1
            battlefield[team2.getPositionY()][p2PosX] = team2.symbol;  // Time 2

            // Mover projéteis e verificar colisões
            Iterator<Projectile> iterator = projectiles.iterator();
            while (iterator.hasNext()) {{
                Projectile p = iterator.next();
                p.move();

                // Verificar colisões com Time 1
                if (p.posX == p1PosX && p.posY == team1.getPositionY()) {{
                    int damage = 0;

                    // Verificar se o projétil tem poder personalizado
                    if (p.getPower() > 0) {{
                        damage = p.getPower();
                    }} else if (p.symbol.contains("<-N-")) {{ // Míssil nuclear do Time 2
                        damage = team2.nuclearPower * 2;
                        System.out.println("!!! MISSIL NUCLEAR do Time 2 atingiu o Time 1!");
                    }} else if (p.symbol.contains("<=")) {{ // Tiro duplo do Time 2
                        damage = team2.doubleShotPower;
                    }} else if (p.symbol.equals("<=")) {{
                        damage = team2.missilePower;
                    }} else if (p.symbol.equals("<<")) {{
                        damage = team2.supersonicPower;
                    }} else {{
                        damage = team2.shotPower;
                    }}

                    if (random.nextInt(100) >= team1.stealthChance) {{
                        team1.takeDamage(damage);
                        System.out.println("*** Aeronave do Time 1 atingida! -" + damage + " pontos");
                    }} else {{
                        System.out.println("--- Aeronave do Time 1 esquivou!");
                        if (team1.radar > 0) {{
                            System.out.println("... Radar do Time 1 detectou o projétil!");
                        }}
                    }}
                    iterator.remove();
                    continue;
                }}

                // Verificar colisões com Time 2
                if (p.posX == p2PosX && p.posY == team2.getPositionY()) {{
                    int damage = 0;

                    // Verificar se o projétil tem poder personalizado
                    if (p.getPower() > 0) {{
                        damage = p.getPower();
                    }} else if (p.symbol.contains("-N->")) {{ // Míssil nuclear do Time 1
                        damage = team1.nuclearPower * 2;
                        System.out.println("!!! MISSIL NUCLEAR do Time 1 atingiu o Time 2!");
                    }} else if (p.symbol.contains("=>")) {{ // Tiro duplo do Time 1
                        damage = team1.doubleShotPower;
                    }} else if (p.symbol.equals("=>")) {{
                        damage = team1.missilePower;
                    }} else if (p.symbol.equals(">>")) {{
                        damage = team1.supersonicPower;
                    }} else {{
                        damage = team1.shotPower;
                    }}

                    if (random.nextInt(100) >= team2.stealthChance) {{
                        team2.takeDamage(damage);
                        System.out.println("*** Aeronave do Time 2 atingida! -" + damage + " pontos");
                    }} else {{
                        System.out.println("--- Aeronave do Time 2 esquivou!");
                        if (team2.radar > 0) {{
                            System.out.println("... Radar do Time 2 detectou o projétil!");
                        }}
                    }}
                    iterator.remove();
                    continue;
                }}

                // Remover projéteis fora dos limites
                if (p.isOutOfBounds(screenWidth)) {{
                    iterator.remove();
                    continue;
                }}

                // Mostrar projéteis no campo de batalha sem cores
                if (p.posX >= 0 && p.posX < screenWidth && p.posY >= 0 && p.posY < battlefieldHeight) {{
                    battlefield[p.posY][p.posX] = p.symbol;
                }}
            }}

            // Mostrar campo de batalha
            for (int row = 0; row < battlefieldHeight; row++) {{
                for (int i = 0; i < screenWidth; i++) {{
                    System.out.print(battlefield[row][i]);
                }}
                System.out.println();
            }}

            // Mostrar status de vida e posições das aeronaves
            System.out.println("Vida Time 1: " + team1.getHealth() + " | Vida Time 2: " + team2.getHealth());
            System.out.println("Posições - Time 1: (" + p1PosX + "," + team1.getPositionY() + ") | Time 2: (" + p2PosX + "," + team2.getPositionY() + ")");
            System.out.flush();

            // Pausa para visualização
            try {{
                Thread.sleep(200);
            }} catch (InterruptedException e) {{
                System.err.println("Erro na pausa: " + e.getMessage());
            }}
        }}

        if (team1.isAlive()) {{
            System.out.println("*** Time 1 venceu! ***");
        }} else {{
            System.out.println("*** Time 2 venceu! ***");
        }}
        System.out.flush();
    }}
}}"""

    # Salvar os arquivos Java
    with open(aircraft_path, "w") as f:
        f.write(aircraft_code)
    with open(projectile_path, "w") as f:
        f.write(projectile_code)
    with open(class1_path, "w") as f1:
        f1.write(code1)
    with open(class2_path, "w") as f2:
        f2.write(code2)
    with open(main_path, "w") as f_main:
        f_main.write(battle_main_code)

    try:
        # Compilar os arquivos Java
        for java_file in [aircraft_path, projectile_path, class1_path, class2_path, main_path]:
            compile_result = subprocess.run(["javac", "-cp", "combat_classes", "-d", "combat_classes", java_file], capture_output=True, text=True)
            if compile_result.returncode != 0:
                return f"❌ Erro na compilação:\\n{compile_result.stderr}"

        # Executar a simulação
        process = subprocess.Popen(
            ["java", "-cp", "combat_classes", "BattleMain"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Usar deque para manter os últimos turnos na visualização
        turnos = deque(maxlen=4)  # Últimos 4 turnos para visualização fluida

        # Guardar saída completa
        saida_completa = ""
        turno_atual = ""
        coletando_turno = False
        resultado_final = None

        for line in iter(process.stdout.readline, ""):
            saida_completa += line

            # Detectar novo turno
            if "=== NOVO TURNO ===" in line:
                if turno_atual:
                    turnos.append(turno_atual)
                turno_atual = line
                coletando_turno = True
            elif coletando_turno:
                turno_atual += line

            # Verificar se é o resultado final
            if "venceu" in line:
                resultado_final = line

            # Atualizar a cada turno
            texto = "".join(list(turnos)) + turno_atual

            # Conversão de cores usando função robusta
            formatted_texto = format_colors(texto)

            # Script de scroll
            scroll_js = """
            <script>
            (function() {
                function forceScrollBottom() {
                    const container = document.getElementById('battle-container');
                    if (container) {
                        container.scrollTop = container.scrollHeight * 10;
                        setTimeout(() => {
                            container.scrollTop = container.scrollHeight * 10;
                        }, 50);
                    }
                }
                forceScrollBottom();
                const scrollInterval = setInterval(forceScrollBottom, 100);
                setTimeout(() => { clearInterval(scrollInterval); }, 2000);
            })();
            </script>
            """

            html_output = f"""
            <div id="battle-container" style="height:400px; overflow:auto; border:1px solid #ccc; padding:10px;
                                             font-family:monospace; white-space:pre; background-color:#f8f8f8;">
                {formatted_texto}
            </div>
            {scroll_js}
            """

            yield html_output
            time.sleep(0.05)

        # Ao final, mostrar resultado destacado
        if resultado_final:
            # Usar função robusta para formatar cores
            formatted_saida = format_colors(saida_completa)

            vencedor = "Time 1" if "Time 1 venceu" in resultado_final else "Time 2"
            cor = "blue" if vencedor == "Time 1" else "red"

            final_scroll_js = """
            <script>
            (function() {
                function finalForceScroll() {
                    const container = document.querySelector('#historico-completo');
                    if (container) {
                        container.scrollTop = container.scrollHeight * 20;
                    }
                }
                finalForceScroll();
                for (let i = 1; i <= 20; i++) {
                    setTimeout(finalForceScroll, i * 100);
                }
                const scrollInterval = setInterval(finalForceScroll, 200);
                setTimeout(() => { clearInterval(scrollInterval); }, 5000);
            })();
            </script>
            """

            final_html = f"""
            <div>
                <div style="padding:15px; background-color:#e9f7e9; border:2px solid #4CAF50;
                            margin:15px 0; text-align:center; border-radius:5px;">
                    <h3 style="color:{cor}; margin:0; font-size:24px;">🏆 {vencedor} VENCEU! 🏆</h3>
                </div>

                <h4>Histórico Completo da Batalha:</h4>

                <div id="historico-completo" style="height:500px; overflow:auto; border:1px solid #ccc; padding:10px;
                           font-family:monospace; white-space:pre; background-color:#f8f8f8;">
                    {formatted_saida}
                </div>
                {final_scroll_js}
            </div>
            """

            yield final_html

    except Exception as e:
        yield f"⚠ Erro inesperado: {str(e)}"

# Funções para carregar templates
def load_team1_template():
    return TEAM1_TEMPLATE

def load_team2_template():
    return TEAM2_TEMPLATE

# Função para preparar e executar a batalha
def prepare_battle(code1, code2, width, height, p1_pos, p2_auto, p2_pos, t1_health, t2_health):
    # Se a posição do Time 2 é automática, calcule-a com base na largura
    final_p2_pos = width - 2 if p2_auto else p2_pos
    # Executar a simulação e retornar o iterador
    for output in run_battle(code1, code2, width, height, p1_pos, final_p2_pos, t1_health, t2_health):
        yield output

# Interface Gradio
with gr.Blocks(title="Java Air Combat", theme=gr.themes.Soft()) as app:
    gr.Markdown("# ⯐🛦🛧 JAVA-Aircraft-Combat - Time 1 vs Time 2")

    gr.Markdown("""
    ## Instruções Rápidas

    1. Use os botões "Carregar Template" para obter um modelo editável para cada time
    2. Personalize os atributos da aeronave (máximo de 100 pontos)
    3. Configure a arena no painel de configurações abaixo se desejar
    4. Clique em "🔥 Combate!" para iniciar a batalha

    **NOVIDADES**: Agora suas aeronaves podem ter radar para detectar projéteis, tiro duplo para atacar em duas altitudes diferentes e até mísseis nucleares para dano massivo!
    """)

    with gr.Row():
        with gr.Column():
            team1_code = gr.Textbox(label="🟦 Código Time 1", lines=20, placeholder="Clique em 'Carregar Template Time 1' para começar")
            team1_template_btn = gr.Button("📝 Carregar Template Time 1", variant="secondary")

        with gr.Column():
            team2_code = gr.Textbox(label="🟥 Código Time 2", lines=20, placeholder="Clique em 'Carregar Template Time 2' para começar")
            team2_template_btn = gr.Button("📝 Carregar Template Time 2", variant="secondary")

    # Conectar botões às funções
    team1_template_btn.click(load_team1_template, inputs=[], outputs=team1_code)
    team2_template_btn.click(load_team2_template, inputs=[], outputs=team2_code)

    with gr.Accordion("⚙️ Configurações da Arena", open=False):
        with gr.Row():
            screen_width = gr.Slider(minimum=50, maximum=200, value=100, step=10,
                                   label="Largura da Tela", info="Define a largura do campo de batalha")
            battlefield_height = gr.Slider(minimum=3, maximum=7, value=3, step=1,
                                        label="Altura do Campo", info="Define o número de linhas no campo de batalha")

        with gr.Row():
            p1_start_pos = gr.Slider(minimum=0, maximum=49, value=2, step=1,
                                   label="Posição Inicial Time 1", info="Define onde o Time 1 começa na arena")
            p2_start_pos_auto = gr.Checkbox(label="Posicionar Time 2 automaticamente",
                                          info="Se marcado, o Time 2 será posicionado no lado oposto", value=True)
            p2_start_pos = gr.Slider(minimum=51, maximum=200, value=98, step=1,
                                   label="Posição Inicial Time 2", info="Define onde o Time 2 começa na arena",
                                   visible=False)

        with gr.Row():
            team1_health = gr.Slider(minimum=50, maximum=500, value=100, step=10,
                                    label="❤️ Vida Time 1", info="Define a vida inicial da aeronave do Time 1")
            team2_health = gr.Slider(minimum=50, maximum=500, value=100, step=10,
                                    label="❤️ Vida Time 2", info="Define a vida inicial da aeronave do Time 2")

        # Botão para equalizar as vidas
        def equalize_health(health_value):
            return health_value, health_value

        equalize_btn = gr.Button("🔄 Igualar Vidas", variant="secondary")
        equalize_btn.click(fn=equalize_health, inputs=team1_health, outputs=[team1_health, team2_health])

        # Lógica para mostrar/esconder a posição do Time 2
        def toggle_p2_pos(auto_checked):
            return {"visible": not auto_checked}

        p2_start_pos_auto.change(toggle_p2_pos, inputs=p2_start_pos_auto, outputs=p2_start_pos)

        # Atualizar posição do Time 2 automaticamente com base na largura da tela
        def update_p2_pos(width):
            return width - 2

        screen_width.change(update_p2_pos, inputs=screen_width, outputs=p2_start_pos)

    btn = gr.Button("🔥 Combate!", variant="primary", size="lg")
    
    # Configurar o componente HTML
    css = """
    <style>
    #battle-result .prose {
        padding: 0 !important;
        margin: 0 !important;
        display: block !important;
        visibility: visible !important;
    }
    </style>
    """

    output = gr.HTML(label="Resultado do Combate", elem_id="battle-result", value=css)
    
    # Conectar o botão à função
    btn.click(fn=prepare_battle,
              inputs=[team1_code, team2_code, screen_width, battlefield_height,
                     p1_start_pos, p2_start_pos_auto, p2_start_pos,
                     team1_health, team2_health],
              outputs=output)

    # Adicionar informações de rodapé
    gr.Markdown("""
    ### Dicas
    - Equilibre seus pontos! Uma distribuição balanceada geralmente é melhor.
    - Lembre que cada atributo tem limites (indicados nos comentários).
    - O radar permite detectar projéteis inimigos e realizar manobras evasivas automáticas.
    - O tiro duplo ataca em duas altitudes ao mesmo tempo, aumentando suas chances de acerto.
    - O míssil nuclear causa dano massivo, mas tem um longo cooldown de 5 turnos.
    - Use toda a altura do campo (configure nas opções) para estratégias mais interessantes!
    - Agora você pode ajustar a vida inicial das aeronaves para batalhas mais longas ou equilibrar times desiguais!

    Desenvolvido para a disciplina de Programação. Bons combates!
    """)

if __name__ == "__main__":
    app.launch()