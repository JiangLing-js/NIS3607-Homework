import random
import copy
from tqdm import tqdm
import time
MAX_ORACLE_QUERY = 100

class Block:
    def __init__(self, node_id, previous_hash):
        self.node_id = node_id
        self.previous_hash = previous_hash

class Node:
    def __init__(self, node_id, block_success_rate):
        self.node_id = node_id
        self.block_success_rate = block_success_rate
        self.blockchain = [Block(0, "0")]

    def mine_block(self, max_oracle_query):
        ctr = 0
        while ctr < max_oracle_query:
            if random.random() < self.block_success_rate:
                new_block = Block(self.node_id, self.blockchain[-1].node_id)
                self.blockchain.append(new_block)
                break
            ctr += 1

def select_chain(nodes):
    max_length = max(len(node.blockchain) for node in nodes)
    longest_chains = [node for node in nodes if len(node.blockchain) == max_length]

    selected_node = random.choice(longest_chains)
    for node in nodes:
        node.blockchain = copy.deepcopy(selected_node.blockchain)
    return selected_node.blockchain


def simulate_blockchain(node_count, block_success_rate, rounds, seed=None, flag=True):
    if seed is not None:
        random.seed(seed)

    nodes = [Node(node_id, block_success_rate) for node_id in range(node_count)]
    previous_chain_length = 1

    with tqdm(total=rounds, dynamic_ncols=False) as pbar:
        for round_num in range(1, rounds+1):  # Start from 1 to avoid division by zero
            for node in nodes:
                node.mine_block(MAX_ORACLE_QUERY)
            selected_chain = select_chain(nodes)
            current_chain_length = len(selected_chain)
            growth_rate = (current_chain_length - previous_chain_length) / round_num
            pbar.set_description(f"Chain Growth Rate: {growth_rate:.4f}")
            pbar.update(1)
        time.sleep(1)

    growth_rate = (current_chain_length-previous_chain_length)/rounds
    if flag:
        print(f"Final Blockchain Growth Rate with block success rate {block_success_rate} is {growth_rate:.4f}")
    if not flag:
        print(f"Final Blockchain Growth Rate with node count {node_count} is {growth_rate:.4f}")



if __name__ == "__main__":
    node_count1 = 500
    block_success_rate1 = 1e-7
    block_success_rates = [1e-7, 1e-6, 1e-5, 1e-4]
    node_counts = [100, 500, 1000, 2000]
    rounds = 2000
    seed = 123

    # Simulate blockchain growth
    for block_success_rate in block_success_rates:
        simulate_blockchain(node_count1, block_success_rate, rounds, seed=seed)

    for node_count in node_counts:
        simulate_blockchain(node_count, block_success_rate1, rounds, seed=seed, flag=False)
