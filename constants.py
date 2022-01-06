CHARMS = [
    "Wayward Compass",
    "Gathering Swarm",
    "Stalwart Shell",
    "Soul Catcher",
    "Shaman Stone",
    "Soul Eater",
    "Dashmaster",
    "Sprintmaster",
    "Grubsong",
    "Grubberflys Elegy",
    "Fragile Heart",
    "Fragile Greed",
    "Fragile Strength",
    "Spell Twister",
    "Steady Body",
    "Heavy Blow",
    "Quick Slash",
    "Longnail",
    "Mark of Pride",
    "Fury of the Fallen",
    "Thorns of Agony",
    "Baldur Shell",
    "Flukenest",
    "Defenders Crest",
    "Glowing Womb",
    "Quick Focus",
    "Deep Focus",
    "Lifeblood Heart",
    "Lifeblood Core",
    "Jonis Blessing",
    "Hiveblood",
    "Spore Shroom",
    "Sharp Shadow",
    "Shape of Unn",
    "Nailmasters Glory",
    "Weaversong",
    "Dream Wielder",
    "Dreamshield",
    "Carefree Melody",
    "Kingsoul",
]

# {"Wayward Compass": 1, "Gathering Swarm": 2, ...}
CHARMS_ORDINALS = {charm: idx for idx, charm in enumerate(CHARMS, start=1)}
# "Grimmchild / Carefree Melody"

CHARM_COSTS = {
    'Gathering Swarm': 1,
    'Defenders Crest': 1,
    'Flukenest': 3,
    'Thorns of Agony': 1,
    'Mark of Pride': 3,
    'Steady Body': 1,
    'Heavy Blow': 2,
    'Sharp Shadow': 2,
    'Spore Shroom': 1,
    'Longnail': 2,
    'Shaman Stone': 3,
    'Wayward Compass': 1,
    'Soul Catcher': 2,
    'Soul Eater': 4,
    'Glowing Womb': 2,
    'Fragile Heart': 2,
    'Fragile Greed': 2,
    'Fragile Strength': 3,
    'Nailmasters Glory': 1,
    'Jonis Blessing': 4,
    'Shape of Unn': 2,
    'Hiveblood': 4,
    'Grubsong': 1,
    'Dream Wielder': 1,
    'Dashmaster': 2,
    'Quick Slash': 3,
    'Spell Twister': 2,
    'Deep Focus': 4,
    'Grubberflys Elegy': 3,
    'Kingsoul': 5,
    'Sprintmaster': 1,
    'Dreamshield': 3,
    'Weaversong': 2,
    'Stalwart Shell': 2,
    'Carefree Melody': 2,
    'Baldur Shell': 2,
    'Fury of the Fallen': 2,
    'Quick Focus': 3,
    'Lifeblood Heart': 2,
    'Lifeblood Core': 3,
}
