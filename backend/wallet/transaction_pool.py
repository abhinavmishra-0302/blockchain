class TransactionPool:
    def __int__(self):
        self.transaction_map = {}

    def set_transaction(self, transaction):
        """
        Set a transaction in transaction pool.
        """
        self.transaction_map[transaction.id] = transaction