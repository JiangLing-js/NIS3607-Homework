import copy
import random
from tqdm import tqdm
from pow_simulate import Block
import time
class HonestNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.blockchain = [Block(0, "0")]

class SelfishNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.public_chain = [Block(0, "0")]
        self.blockchain = [Block(0, "0")]
        self.private_chain_length = 0

class BlockchainSimulation:
    def __init__(self, adv_rate, rounds, seed=None):
        self.adv_rate = adv_rate
        self.rounds = rounds
        self.seed = seed
        self.honest_nodes = HonestNode(1)
        self.selfish_node = SelfishNode(-1)
        self.judge = False

    def simulate(self):
        if self.seed is not None:
            random.seed(self.seed)

        with tqdm(total=self.rounds, dynamic_ncols=False) as pbar:
            for _ in range(self.rounds):
                if random.random() <= self.adv_rate:
                    self.selfish_miner(self.selfish_node)

                else:
                    self.honest_miner(self.honest_nodes)

                self.select_chain()
                if self.block_count(1) > 0:
                    pbar.set_description(
                        f"The proportion of selfish mining profits: {self.block_count(-1) / (self.block_count(1)+self.block_count(-1)):.4f}")
                pbar.update(1)
        print(self.block_count(-1), self.block_count(1))
        print(f"In {self.adv_rate}: The proportion of selfish mining profits: {self.block_count(-1) / (self.block_count(1)+self.block_count(-1)):.4f}")
        time.sleep(1)


    def select_chain(self):
        if len(self.selfish_node.public_chain) > len(self.honest_nodes.blockchain):
            self.honest_nodes.blockchain = copy.deepcopy(self.selfish_node.public_chain)

        elif len(self.selfish_node.public_chain) < len(self.honest_nodes.blockchain):
            self.selfish_node.public_chain = copy.deepcopy(self.honest_nodes.blockchain)

        else:
            self.honest_nodes.blockchain = copy.deepcopy(self.selfish_node.public_chain)


    def selfish_miner(self, node):
        block = Block(-1, "selfish")
        node.blockchain.append(block)
        node.private_chain_length += 1
        delta = len(self.selfish_node.blockchain) - len(self.selfish_node.public_chain)
        if delta == 0 and node.private_chain_length == 2:
            node.private_chain_length = 0
            node.public_chain = copy.deepcopy(node.blockchain)


    def honest_miner(self, node):
        block = Block(1, "honest")
        node.blockchain.append(block)
        delta = len(self.selfish_node.blockchain) - len(self.selfish_node.public_chain)
        if delta == 0:
            self.selfish_node.blockchain = copy.deepcopy(node.blockchain)
            self.selfish_node.private_chain_length = 0

        elif delta == 1:
            self.selfish_node.public_chain = copy.deepcopy(self.selfish_node.blockchain)
            self.selfish_node.private_chain_length = 0
            if random.random() < 0.5:
                self.selfish_node.public_chain = node.blockchain
                self.selfish_node.blockchain = node.blockchain
            else:
                node.blockchain = self.selfish_node.public_chain

        elif delta == 2:
            self.selfish_node.public_chain = copy.deepcopy(self.selfish_node.blockchain)
            self.selfish_node.private_chain_length = 0

        else:
            self.selfish_node.public_chain = copy.deepcopy(self.selfish_node.blockchain[:len(self.selfish_node.public_chain) + 1])
            self.selfish_node.private_chain_length -= 2

    def block_count(self, id):
        count = 0
        for block in self.honest_nodes.blockchain:
            if block.node_id == id:
                count += 1
        return count
if __name__ == "__main__":
    adv_rates = [0.1, 0.2, 0.3, 0.4]
    rounds = 5000
    seed = 123

    for adv_rate in adv_rates:
        simulation = BlockchainSimulation(adv_rate, rounds, seed)
        simulation.simulate()
