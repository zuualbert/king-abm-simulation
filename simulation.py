import random
import networkx as nx
from collections import defaultdict, Counter

random.seed(42)

N = 60
G = nx.barabasi_albert_graph(N, m=3, seed=42)

agents = {}
ids = list(range(N))
random.shuffle(ids)
for i in ids[:25]:
    agents[i] = 'A'
for i in ids[25:50]:
    agents[i] = 'B'
for i in ids[50:60]:
    agents[i] = 'C'

P_REMIX_A = 0.40
P_SHARE_B = 0.55
P_CORRECT_C = 0.65
P_A_REMIX_FICTION = 0.50

contents = []
agent_new_content = defaultdict(list)
cid = 0

def add_content(origin, ctype, parent=None):
    global cid
    c = {'id': cid, 'type': ctype, 'origin': origin, 'parent': parent}
    cid += 1
    contents.append(c)
    agent_new_content[origin].append(c)
    return c

seeds = random.sample([n for n in range(N) if agents[n] == 'B'], 6)
seed_content = add_content(-1, 'SEED')
seen = defaultdict(set)

inbox = defaultdict(list)
for s in seeds:
    for nb in G.neighbors(s):
        inbox[nb].append(0)

ROUNDS = 12
MAX_TOTAL_CONTENT = 500
MAX_INBOX_PER_AGENT = 8

for round_num in range(ROUNDS):
    if len(contents) >= MAX_TOTAL_CONTENT:
        break
    agent_new_content.clear()
    new_inbox = defaultdict(list)
    for node in range(N):
        atype = agents[node]
        msgs = inbox.get(node, [])
        if len(msgs) > MAX_INBOX_PER_AGENT:
            msgs = random.sample(msgs, MAX_INBOX_PER_AGENT)
        for msg_id in msgs:
            if msg_id in seen[node]:
                continue
            seen[node].add(msg_id)
            msg = next((c for c in contents if c['id'] == msg_id), None)
            if msg is None:
                continue
            mt = msg['type']
            if atype == 'A':
                if mt in ('SEED', 'BLIND') and random.random() < P_REMIX_A:
                    nc = add_content(node, 'FICTION', parent=msg_id)
                    for nb in G.neighbors(node):
                        new_inbox[nb].append(nc['id'])
                elif mt == 'FICTION' and random.random() < P_A_REMIX_FICTION:
                    nc = add_content(node, 'FICTION', parent=msg_id)
                    for nb in G.neighbors(node):
                        new_inbox[nb].append(nc['id'])
            elif atype == 'B':
                if mt in ('SEED', 'BLIND', 'FICTION') and random.random() < P_SHARE_B:
                    nc = add_content(node, 'BLIND', parent=msg_id)
                    for nb in G.neighbors(node):
                        new_inbox[nb].append(nc['id'])
                elif mt == 'CORRECTION' and random.random() < 0.15:
                    nc = add_content(node, 'CORRECTION', parent=msg_id)
                    for nb in G.neighbors(node):
                        new_inbox[nb].append(nc['id'])
            elif atype == 'C':
                if mt in ('SEED', 'BLIND') and random.random() < P_CORRECT_C:
                    nc = add_content(node, 'CORRECTION', parent=msg_id)
                    for nb in G.neighbors(node):
                        new_inbox[nb].append(nc['id'])
                elif mt == 'FICTION' and random.random() < 0.03:
                    nc = add_content(node, 'FICTION', parent=msg_id)
                    for nb in G.neighbors(node):
                        new_inbox[nb].append(nc['id'])
                elif mt == 'CORRECTION' and random.random() < 0.15:
                    nc = add_content(node, 'CORRECTION', parent=msg_id)
                    for nb in G.neighbors(node):
                        new_inbox[nb].append(nc['id'])
    inbox = new_inbox

c_count = Counter(c['type'] for c in contents if c['type'] != 'SEED')
total = sum(c_count.values())
print(f"总产出: {total}")
print(f"  FICTION: {c_count['FICTION']} ({c_count['FICTION']/total*100:.1f}%)")
print(f"  BLIND: {c_count['BLIND']} ({c_count['BLIND']/total*100:.1f}%)")
print(f"  CORRECTION: {c_count['CORRECTION']} ({c_count['CORRECTION']/total*100:.1f}%)")

fiction_parents = set(c['parent'] for c in contents if c['parent'] is not None
                      and any(pc['type'] == 'FICTION' for pc in contents if pc['id'] == c['parent']))
blind_parents = set(c['parent'] for c in contents if c['parent'] is not None
                    and any(pc['type'] == 'BLIND' for pc in contents if pc['id'] == c['parent']))
print(f"\n二次创作率 FICTION: {len(fiction_parents)}/{c_count['FICTION']} = {len(fiction_parents)/c_count['FICTION']*100:.1f}%")
print(f"二次创作率 BLIND: {len(blind_parents)}/{c_count['BLIND']} = {len(blind_parents)/c_count['BLIND']*100:.1f}%")

corr_blind = sum(1 for c in contents if c['type'] == 'CORRECTION' and c['parent'] is not None
                 and any(pc['type'] in ('SEED', 'BLIND') for pc in contents if pc['id'] == c['parent']))
corr_fiction = sum(1 for c in contents if c['type'] == 'CORRECTION' and c['parent'] is not None
                   and any(pc['type'] == 'FICTION' for pc in contents if pc['id'] == c['parent']))
print(f"\n辟谣针对 BLIND: {corr_blind}")
print(f"辟谣针对 FICTION: {corr_fiction}")
