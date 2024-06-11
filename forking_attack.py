import random
import time
from tqdm import tqdm

MAX_ORACLE_QUERY = 100

from pow_simulate import Node as HonestNode, Block, select_chain

class ADVNode():
    def __init__(self, node_id, block_success_rate):
        self.node_id = node_id
        self.attack_success_rate = block_success_rate
        self.blockchain = [Block(0, "0")]

    def mine_block(self, max_oracle_query):
        ctr = 0
        while ctr < max_oracle_query:
            if random.random() < self.attack_success_rate:
                # Perform fork attack
                # Randomly choose to mine on the honest chain or fork
                new_block = Block(self.node_id, self.blockchain[-1].node_id)
                self.blockchain.append(new_block)
                break
            ctr += 1

def simulate_blockchain(node_count, adv_rate, block_success_rate, rounds, seed=None):
    if seed is not None:
        random.seed(seed)
    honests = int(node_count*(1-adv_rate))
    advx = node_count-honests
    length = 6
    count = 0
    with tqdm(total=rounds, dynamic_ncols=False) as pbar:
        for round_num in range(1, rounds+1):  # Start from 1 to avoid division by zero
            nodes_honest = [HonestNode(node_id, block_success_rate) for node_id in range(honests)]
            nodes_adv = [ADVNode(node_id + honests, block_success_rate) for node_id in range(advx)]
            flag = False
            while not flag:
                for node in nodes_honest:
                    node.mine_block(MAX_ORACLE_QUERY)
                for node in nodes_adv:
                    node.mine_block(MAX_ORACLE_QUERY)

                selected_chain_h = select_chain(nodes_honest)
                selected_chain_a = select_chain(nodes_adv)
                current_chain_length_h = len(selected_chain_h)-1
                current_chain_length_a = len(selected_chain_a)-1
                if current_chain_length_h > length or current_chain_length_a > length:
                    flag = True
                    if current_chain_length_a > current_chain_length_h:
                        count += 1
                    elif current_chain_length_a == current_chain_length_h:
                        if random.random() < 0.5:
                            count += 1
            pbar.update(1)
        time.sleep(1)
        print(f"length:{length}, adv_rate:{adv_rate}, Percentage of Fork Attack: {(count / rounds):.4f}")



if __name__ == "__main__":
    node_count = 100
    adv_rates = [0.1, 0.2, 0.3, 0.4]
    rounds = 1000
    seed = 123
    block_success_rate = 1e-5
    # Simulate blockchain growth
    for adv_rate in adv_rates:
        simulate_blockchain(node_count, adv_rate, block_success_rate, rounds, seed=seed)



