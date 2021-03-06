import random


class Quest:
    def __init__(self, name, enemyIdx) -> None:
        self.name = name
        self.reward = None
        self.enemyIdx = enemyIdx

class Money(int):
    pass

class Status:
    def __init__(self, hitpoint: int, strength: int) -> None:
        self.hitpoint = hitpoint
        self.max_hitpoint = hitpoint
        self.strength = strength

class Ability:
    def __init__(self, name, p=1) -> None:
        self.name = name
        self.p = p
        self._type = 0

    def execute(self):
        pass

    def getAbiliyInfo(self, player=1):
        pass

    def getType(self):
        return self._type

class AttackAbility(Ability):
    def execute(self, source: "Player", target: "Player"):
        damage = source.job_class.status.strength * self.p
        damage = int(damage)
        target.job_class.status.hitpoint -= damage
        return damage

    def getAbiliyInfo(self, player=1):
        if player:
            return [0, 1]
        else:
            return [1, 0]

class HealAbility(Ability):
    def execute(self, source: "Player", target: "Player"):
        heal = source.job_class.status.hitpoint // self.p
        heal = int(heal)
        if target.job_class.status.max_hitpoint > target.job_class.status.hitpoint + heal:
            target.job_class.status.hitpoint += heal
        else:
            heal = target.job_class.status.max_hitpoint - target.job_class.status.hitpoint
            target.job_class.status.hitpoint = target.job_class.status.max_hitpoint
        return heal

    def getType(self):
        return self._type+1

    def getAbiliyInfo(self, player=1):
        if player:
            return [0, 0]
        else:
            return [1, 1]

class JobClass:
    def __init__(self, name, status: Status, abilities: list[Ability]) -> None:
        self.name = name
        self.status = status
        self.abilities = abilities

class Player:
    def __init__(self, name, money, job_class: JobClass) -> None:
        self.name = name
        self.money = money
        self.job_class: JobClass = job_class

    def choose_ability(self, player=1):
        if player:
            for i, ability in enumerate(self.job_class.abilities):
                print(i, ability.name)
            return int(input("> "))

        abilitys = []
        rates = []
        for ability in self.job_class.abilities:
            abilitys.append(ability)
            ability_type = ability.getType()
            if ability_type == 1:
                rate = min(
                    1,
                    1-(self.job_class.status.hitpoint / self.job_class.status.max_hitpoint)*(1/ability.p)
                )
                if rate <= 0:
                    rate = random.random()
            else:
                rate = random.uniform(abs(1/ability.p-0.5), 1)
            rates.append(rate)
        return self.job_class.abilities.index(random.choices(self.job_class.abilities, rates)[0])

    def exec_ability(self, idx, **kwargs):
        return self.job_class.abilities[idx].execute(**kwargs)

    def msg(self, _type, player=1):
        if player:
            msgs = ["{}???{}???????????????????????????!", "{}???HP{}????????????!"]
        else:
            msgs = ["{}???{}???????????????????????????!", "{}???HP{}????????????!"]
        return msgs[_type]


def battle(player: Player, enemy: Player):

    print(f"{enemy.name}????????????!")
    actor = [player, enemy]
    while True:
        print(f"{player.name}????????????! HP:{player.job_class.status.hitpoint}/STR:{player.job_class.status.strength}")
        ability_idx = player.choose_ability()
        ability: Ability = player.job_class.abilities[ability_idx]
        sidx, tidx = ability.getAbiliyInfo()

        print(f"{player.name}???{ability.name}!")
        ability_type = ability.getType()
        msg = player.msg(ability_type)

        d = player.exec_ability(ability_idx, source=actor[sidx], target=actor[tidx])
        if ability_type:
            if d == 0:
                print("HP???????????????!")
            else:
                print(msg.format(player.name, d))
                print(f"HP:{player.job_class.status.hitpoint-d}->HP:{player.job_class.status.hitpoint}")
        else:
            print(msg.format(enemy.name, d))
        if enemy.job_class.status.hitpoint <= 0:
            print(f"{enemy.name}???????????????!")
            print(f"{enemy.money}G???????????????!")
            player.money += enemy.money
            print(f"{player.money-enemy.money}G->{player.money}G")
            return 1

        print(f"{enemy.name}(HP:{enemy.job_class.status.hitpoint})????????????!")
        enemy_ability_idx = enemy.choose_ability(0)
        enemy_ability: Ability = enemy.job_class.abilities[enemy_ability_idx]
        enemy_ability_type = enemy_ability.getType()
        sidx, tidx = enemy_ability.getAbiliyInfo(0)
        enemy_msg = enemy.msg(enemy_ability_type, 0)

        print(f"{enemy.name}???{enemy_ability.name}")
        d = enemy.exec_ability(enemy_ability_idx, source=actor[sidx], target=actor[tidx])
        if enemy_ability_type:
            print(enemy_msg.format(enemy.name, d))
        else:
            print(enemy_msg.format(player.name, d))
        if player.job_class.status.hitpoint <= 0:
            print(f"{player.name}??????????????????!")
            return -1


if __name__ == "__main__":
    from copy import deepcopy
    name = input("Enter your name:")

    player = Player(
        name,
        Money(0),
        JobClass(
            "??????",
            Status(2000, 800),
            [HealAbility("??????"), AttackAbility("??????"), AttackAbility("2?????????", 2), AttackAbility("10?????????", 10)]
        )
    )
    slime = Player(
        "????????????",
        Money(300),
        JobClass(
            "????????????",
            Status(1200, 600),
            [AttackAbility("??????")]
        )
    )
    dragon = Player(
        "????????????",
        Money(1000),
        JobClass(
            "????????????",
            Status(3000, 900),
            [AttackAbility("??????"), AttackAbility("3?????????", 3), HealAbility("??????")]
        )
    )
    debug_enemy = Player(
        "??????????????????",
        Money(10**10-1),
        JobClass(
            "??????????????????",
            Status(10**5-1, 0),
            [AttackAbility("??????"), AttackAbility("10?????????", 10), HealAbility("2?????????", 2), HealAbility("10?????????", 10)]
        )
    )
    enemies = [slime, dragon]
    quests: list[Quest] = [
        Quest("??????????????????", 0),
        Quest("??????????????????", 1)
    ]
    for i, quest in enumerate(quests):
        print(i, quest.name)
    print("-1 ???????????????")
    quest_idx = int(input("> "))
    if 0 <= quest_idx:
        enemy = enemies[quests[quest_idx].enemyIdx]
    else:
        enemy = debug_enemy
    winner = battle(player, deepcopy(enemy))
    if winner == 1:
        print("You Win!")
    else:
        print("You Lose!")
    input("Please Press Any Key...")