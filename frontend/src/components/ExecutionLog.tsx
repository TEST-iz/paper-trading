import ExecutionLogItem from "./ExecutionLogItem";

function ExecutionLog() {
    return (
        <>
        <div className="flex h-[300px] w-[300px] flex-col items-center border-1 border-[#1269cc] rounded-lg mt-0.75 p-1.5 ml-3">
            <div className="flex flex-col items-start w-full mb-3.5 ml-5 shrink-0">
                <p className="text-lg mb-1">EXECUTION AUDIT LOG</p>
                <p className="text-sm">List of executed paper trades</p>
            </div>

            <div className="flex-1 min-h-0 w-full overflow-y-auto flex flex-col items-center">
                <ExecutionLogItem 
                    action="SELL"
                    ticker="AAPL"
                    shares={10}
                    price={1243.3}
                    />
                    <ExecutionLogItem 
                    action="BUY"
                    ticker="RBLX"
                    shares={67}
                    price={6.77}
                    />
                    <ExecutionLogItem 
                    action="SELL"
                    ticker="MSFT"
                    shares={3}
                    price={46.23}
                    />
                    <ExecutionLogItem 
                    action="SELL"
                    ticker="GOOG"
                    shares={67}
                    price={2.99}
                    />
                    <ExecutionLogItem 
                    action="BUY"
                    ticker="TSLA"
                    shares={1}
                    price={4.00}
                    />
            </div>
        </div>
        </>
    )
}

export default ExecutionLog;