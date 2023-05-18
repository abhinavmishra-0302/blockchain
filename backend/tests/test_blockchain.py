import time

from backend.blockchain.block import Block
from backend.blockchain.blockchain import Blockchain

from backend.config.config import SECONDS, MINE_RATE

from backend.utils.hex_to_binary import hex_to_binary


def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty


def test_block_quickly_mined():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    block = Block.mine_block(last_block, 'bar')
    assert block.difficulty == last_block.difficulty + 1


def test_block_slowly_mined():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    time.sleep(MINE_RATE / SECONDS)
    block = Block.mine_block(last_block, 'bar')
    assert block.difficulty == last_block.difficulty - 1


def test_mining_rate_limit_at_1():
    last_block = Block(
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        'test_data',
        1,
        0
    )

    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'foo')

    assert mined_block.difficulty == 1


def test_is_valid_chain():
    blockchain = Blockchain()

    for i in range(3):
        blockchain.add_block(i)

    Blockchain.is_valid_chain(blockchain.chain)

# def test_replace_chain(blockchain_three_blocks):
#    blockchain = Blockchain()
#
#   blockchain.replace_chain(blockchain_three_blocks)
#
#   assert blockchain.chain == blockchain_three_blocks.chain
