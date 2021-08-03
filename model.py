import pymysql.cursors
import model.modcfg as mcfg

def writestats(player, cpu, pwin):
    connection = pymysql.connect(host=mcfg.host,
                                 user=mcfg.user,
                                 password=mcfg.password,
                                 db=mcfg.db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `rpsls` (`player`, `cpu`, `pwin`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (player, cpu, pwin,))
            connection.commit()

    finally:
        connection.close()



def getstats(player, choice, outcome):
    connection = pymysql.connect(host=mcfg.host,
                                 user=mcfg.user,
                                 password=mcfg.password,
                                 db=mcfg.db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = (f"SELECT COUNT(*) as 'C' from `rpsls` WHERE `{player}` = %s and `pwin` = %s")
        cursor.execute(sql, (choice, outcome))
        result = cursor.fetchall()
        cursor.close()
        return result


def rpsls_stats():
    statkey = { 'cpu' : {
                    'rock' : { 'w' : 0, 'l' : 0, 'd' : 0 , 't' : 0},
                    'paper' : { 'w' : 0, 'l' : 0, 'd' : 0, 't' : 0 },
                    'scissors' : { 'w' : 0, 'l' : 0, 'd' : 0, 't' : 0  },
                    'lizard' : { 'w' : 0, 'l' : 0, 'd' : 0, 't' : 0  },
                    'spoc' : { 'w' : 0, 'l' : 0, 'd' : 0, 't' : 0  }
                },
                'player' : {
                    'rock' : { 'w' : 0, 'l' : 0, 'd' : 0, 't' : 0  },
                    'paper' : { 'w' : 0, 'l' : 0, 'd' : 0, 't' : 0  },
                    'scissors' : { 'w' : 0, 'l' : 0, 'd' : 0, 't' : 0  },
                    'lizard' : { 'w' : 0, 'l' : 0, 'd' : 0, 't' : 0  },
                    'spoc' : { 'w' : 0, 'l' : 0, 'd' : 0, 't' : 0  }
                }
            }

    for k in statkey.keys():
        for k2 in statkey[k].keys():
            statkey[k][k2]['w'] = getstats(k, k2, 'w')[0]['C']
            statkey[k][k2]['l'] = getstats(k, k2, 'l')[0]['C']
            statkey[k][k2]['d'] = getstats(k, k2, 'd')[0]['C']
            statkey[k][k2]['t'] = statkey[k][k2]['w'] + statkey[k][k2]['l'] + statkey[k][k2]['d']

    return statkey


def process_stats(statkey):
    # CPU Stats
    # most winning
    cpu_wins = []
    v = max(int(d['w']) for d in statkey['cpu'].values())
    for key in statkey['cpu'].keys():
        if statkey['cpu'][key]['w'] == v:
            cpu_wins.append(key)
    if len(cpu_wins) > 1:
        cpu_wins = ' or '.join(cpu_wins)
    else:
        cpu_wins = cpu_wins[0]
    # most losing
    cpu_loses = []
    v = max(int(d['l']) for d in statkey['cpu'].values())
    for key in statkey['cpu'].keys():
        if statkey['cpu'][key]['l'] == v:
            cpu_loses.append(key)
    if len(cpu_loses) > 1:
        cpu_loses = ' or '.join(cpu_loses)
    else:
        cpu_loses = cpu_loses[0]
    # most used
    cpu_most = []
    v = max(int(d['w'] + d['l'] + d['d']) for d in statkey['cpu'].values())
    for key in statkey['cpu'].keys():
        if statkey['cpu'][key]['l'] + statkey['cpu'][key]['w'] + statkey['cpu'][key]['d']== v:
            cpu_most.append(key)
    if len(cpu_most) > 1:
        cpu_most = ' or '.join(cpu_most)
    else:
        cpu_most = cpu_most[0]
    # Player Stats
    # most winning
    player_wins = []
    v = max(int(d['w']) for d in statkey['player'].values())
    for key in statkey['player'].keys():
        if statkey['player'][key]['w'] == v:
            player_wins.append(key)
    if len(player_wins) > 1:
        player_wins = ' or '.join(player_wins)
    else:
        player_wins = player_wins[0]
    # most losing
    player_loses = []
    v = max(int(d['l']) for d in statkey['player'].values())
    for key in statkey['player'].keys():
        if statkey['player'][key]['l'] == v:
            player_loses.append(key)
    if len(player_loses) > 1:
        player_loses = ' or '.join(player_loses)
    else:
        player_loses = player_loses[0]
    # most used
    player_most = []
    v = max(int(d['w'] + d['l'] + d['d']) for d in statkey['player'].values())
    for key in statkey['player'].keys():
        if statkey['player'][key]['l'] + statkey['player'][key]['w'] + statkey['player'][key]['d']== v:
            player_most.append(key)
    if len(player_most) > 1:
        player_most = ' or '.join(player_most)
    else:
        player_most = player_most[0]

    out = []

    out += [f"The most commonly used option by the CPU is { cpu_most }"]
    out += [f"The CPU wins most often with: { cpu_wins }"]
    out += [f"The CPU loses most often with:  { cpu_loses }"]
    out += [f"The most commonly used option by players is { player_most }"]
    out += [f"Players win most often with: { player_wins }"]
    out += [f"Players lose most often with:  { player_loses }"]

    return out





