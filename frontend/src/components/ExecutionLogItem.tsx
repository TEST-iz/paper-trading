import styles from "./ExecutionLogItem.module.css";

type ItemProps = {
    action: string;
    ticker: string;
    shares: number;
    price: number;
}


function ExecutionLogItem({ action, ticker, shares, price }: ItemProps) {
    return (
        <>
        <div className={styles.item}>
            <p>{action}, {ticker}, {shares}, {price}</p>
        </div>
        </>
    );
}

export default ExecutionLogItem
