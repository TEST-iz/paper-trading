import { useEffect, useState } from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

type PortfolioSnapshot = {
    timestamp: string;
    cash_balance: number;
    stock_value: number;
    total_value: number;
    run_type: 'MORNING' | 'EVENING';
    timeLabel?: string;
};

function Graph() {

    const [data, setData] = useState<PortfolioSnapshot[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://localhost:8000/portfolio-history')
            .then(res => res.json())
            .then((result: PortfolioSnapshot[]) => {
                const formatted = result.map(item => ({
                    ...item,
                    total_value: Number(Number(+item.total_value).toFixed(2)),
                    timeLabel: new Date(item.timestamp).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
                }));
                setData(formatted);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch portfolio history:", err);
                setLoading(false);
            });
    }, []);

    return (
        <div className="flex h-[300px] w-full flex-col items-center border-1 border-[#1269cc] rounded-lg mt-0.75 p-1.5">
            <h2 className="text-xs font-bold tracking-wider text-slate-400 mb-4">PORTFOLIO NET WORTH OVER TIME</h2>
            <h2 className="text-xs mb-4">{loading ? "Loading..." : data.length > 0 ? `Current Value: $${data[data.length - 1].total_value.toFixed(2)}` : "cooked"}</h2>
            
            <div className="h-[250px] w-full">
                {loading ? "Loading..." :
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#00ba7c" stopOpacity={0.4}/>
                                <stop offset="95%" stopColor="#00ba7c" stopOpacity={0.0}/>
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                        <XAxis dataKey="timeLabel" stroke="#64748b" textAnchor="end" tick={{ fontSize: 10 }} />
                        <YAxis stroke="#64748b" domain={['auto', 'auto']} tick={{ fontSize: 10 }} />
                        <Tooltip 
                            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                        />
                        <Area type="monotone" dataKey="total_value" stroke="#00ba7c" strokeWidth={2} fillOpacity={1} fill="url(#colorValue)" />
                    </AreaChart>
                </ResponsiveContainer>
                }
            </div>
        </div>
    );
}

export default Graph;