# order of charms like order of gotCharm_ and charmCost_ in user data
CHARMS = [
    "Gathering Swarm",
    "Wayward Compass",
    "Grubsong",
    "Stalwart Shell",
    "Baldur Shell",
    "Fury of the Fallen",
    "Quick Focus",
    "Lifeblood Heart",
    "Lifeblood Core",
    "Defenders Crest",
    "Flukenest",
    "Thorns of Agony",
    "Mark of Pride",
    "Steady Body",
    "Heavy Blow",
    "Sharp Shadow",
    "Spore Shroom",
    "Longnail",
    "Shaman Stone",
    "Soul Catcher",
    "Soul Eater",
    "Glowing Womb",
    "Fragile Heart",
    "Fragile Greed",
    "Fragile Strength",
    "Nailmasters Glory",
    "Jonis Blessing",
    "Shape of Unn",
    "Hiveblood",
    "Dream Wielder",
    "Dashmaster",
    "Quick Slash",
    "Spell Twister",
    "Deep Focus",
    "Grubberflys Elegy",
    "Void Heart",
    # The Grimm Troupe DLC
    "Sprintmaster",
    "Dreamshield",
    "Weaversong",
    "Carefree Melody"
]

# {"Gathering Swarm": 1, "Wayward Compass": 2, ...}
CHARMS_ORDINALS = {charm: idx for idx, charm in enumerate(CHARMS, start=1)}

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
    'Void Heart': 0
}

CHARMS_DISPLAY_ORDER = [
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
    "Void Heart",
]
