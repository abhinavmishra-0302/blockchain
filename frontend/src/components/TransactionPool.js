import React, {useState, useEffect} from "react";
import {Link} from "react-router-dom";
import {API_BASE_URL, SECONDS_JS} from "../config";
import Transaction from "./Transaction";
import {Button} from "react-bootstrap";
import history from "../history";

const POLL_INTERVAL = 10 * SECONDS_JS

function TransactionPool() {
    const [transactions, setTransactions] = useState([])


    const fetchTransaction = () => {
        fetch(`${API_BASE_URL}/transactions`)
            .then(response => response.json())
            .then(json => {
                console.log('transaction json', json)
                setTransactions(json)
            })
    }

    useEffect(() => {
        fetchTransaction()

        const intervalId = setInterval(fetchTransaction, POLL_INTERVAL)

        return () => clearInterval(intervalId)
    }, [])

    function fetchMineBlock() {
        fetch(`${API_BASE_URL}/blockchain/mine`)
            .then(() => {
                alert("Success")

                history.push("/blockchain")
            })
    }

    return (<div className="TransactionPool">
        <Link to="/">Home</Link>
        <hr/>
        <h3>
            Transaction Pool
        </h3>
        <div>
            {transactions.map(transaction => (<div key={transaction.id}>
                <hr/>
                <Transaction transaction={transaction}/>
            </div>))}
        </div>
        <hr/>
        <Button variant="danger"
        onClick={fetchMineBlock}>
            Mine a block on these transactions
        </Button>
    </div>)
}

export default TransactionPool