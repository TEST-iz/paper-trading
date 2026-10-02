type ItemProps = {
    action: string;
    ticker: string;
    shares: number;
    price: number;
}

const ACTION_COLORS: Record<string, string> = {
        BUY: "text-emerald-500 font-semibold",
        SELL: "text-rose-500 font-semibold",
};

function ExecutionLogItem({ action, ticker, shares, price }: ItemProps) {    
    const actionStyle = ACTION_COLORS[action.toUpperCase()] ?? "text-gray-500 font-semibold";

    return (
        <>
        <div className="flex h-[50px] w-[350px] flex-row items-center justify-around border-1 border-[#1269cc] mt-0.75">
            <p>
                <span className={actionStyle}>[{action}]</span> {ticker} - {shares} shares @ ${price}
            </p>
        </div>
        </>
    );
}

export default ExecutionLogItem
