type ItemProps = {
    action: string;
    ticker: string;
    shares: number;
    price: number;
}

const ACTION_COLOURS: Record<string, string> = {
        BUY: "text-emerald-500 font-semibold",
        SELL: "text-rose-500 font-semibold",
};

function ExecutionLogItem({ action, ticker, shares, price }: ItemProps) {    
    const actionStyle = ACTION_COLOURS[action.toUpperCase()] ?? "text-gray-500 font-semibold";

    return (
        <>
        <div className="flex shrink-0 h-[50px] w-[265px] flex-row items-center justify-start border-t-1 border-t-[#1269cc] mt-0.75">
            <p className="text-sm justify-start">
                <span className={actionStyle}>[{action}]</span> {ticker} - {shares} shares @ ${price}
            </p>
        </div>
        </>
    );
}

export default ExecutionLogItem
