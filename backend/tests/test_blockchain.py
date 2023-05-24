import time

import pytest

from backend.blockchain.block import Block
from backend.blockchain.blockchain import Blockchain

from backend.config.config import SECONDS, MINE_RATE

from backend.utils.hex_to_binary import hex_to_binary
from backend.wallet.transactions import Transactions
from backend.wallet.wallet import Wallet


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


@pytest.fixture
def blockchain_three_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block([Transactions(Wallet(), 'recipient', i).to_json()])
    return blockchain


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

def test_valid_transaction_chain(blockchain_three_blocks):
    Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)


def test_valid_transaction_duplicate_transactions(blockchain_three_blocks):
    transaction = Transactions(Wallet(), 'recipient', 1).to_json()
    blockchain_three_blocks.add_block([transaction, transaction])

    with pytest.raises(Exception, match='is not unique'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)


def test_valid_transaction_chain_multiple_rewards(blockchain_three_blocks):
    reward_1 = Transactions.reward_transaction(Wallet()).to_json()
    reward_2 = Transactions.reward_transaction(Wallet()).to_json()

    blockchain_three_blocks.add_block([reward_1, reward_2])

    with pytest.raises(Exception, match='There can only be one mining reward per block.'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)


def test_is_valid_transaction_chain_bad_transaction(blockchain_three_blocks):
    bad_transaction = Transactions(Wallet(), 'recipient', 1)
    bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)
    blockchain_three_blocks.add_block([bad_transaction.to_json()])

    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)


def test_is_valid_transaction_chain_bad_historic_balance(blockchain_three_blocks):
    wallet = Wallet()
    bad_transaction = Transactions(wallet, 'recipient', 1)
    bad_transaction.output[wallet.address] = 9000
    bad_transaction.input['amount'] = 9001
    bad_transaction.input['signature'] = wallet.sign(bad_transaction.output)

    blockchain_three_blocks.add_block([bad_transaction.to_json()])

    with pytest.raises(Exception, match='has an invalid input amount'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)
