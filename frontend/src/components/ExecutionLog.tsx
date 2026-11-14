import { useEffect, useState} from 'react';
import ExecutionLogItem from "./ExecutionLogItem";

type Trade = {
    id: number;
    comp: string;
    action: 'BUY' | 'SELL';
    shares: number;
    price: number;
    total_amount: number;
    timestamp: string;
}


function ExecutionLog() {

    const [data, setData] = useState<Trade[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://localhost:8000/trade_history')
            .then(res => res.json())
            .then((result: Trade[]) => {
                setData(result);
                setLoading(false);
            })
            .catch(err => {
                console.log("Error", err);
                setLoading(false);
            });
    }, []);

    return (
        <>
        <div className="flex h-[450px] w-full flex-col items-center border-1 border-[#1269cc] rounded-lg mt-0.75 p-1.5">
            <div className="flex flex-col items-start w-full mb-3 mt-2 ml-5 shrink-0">
                <p className="text-lg mb-1">EXECUTION AUDIT LOG</p>
                <p className="text-sm">List of executed paper trades</p>
            </div>

            <div className="flex-1 min-h-0 w-full overflow-y-auto flex flex-col items-center px-2.5">
                {loading ? "Loading..." :
                    data.map((item) => (
                        <ExecutionLogItem 
                            key={item.id}
                            ticker={item.comp}
                            action={item.action}
                            shares={item.shares}
                            price={item.price}
                        />
                    ))  
                }
                
                {/* <ExecutionLogItem 
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
                    /> */}
            </div>
        </div>
        </>
    )
}

export default ExecutionLog;