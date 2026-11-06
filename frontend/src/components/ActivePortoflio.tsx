const portfolioData = [
  { id: 1, ticker: 'AAPL', shares: 25, lastPrice: 189.50 },
  { id: 2, ticker: 'MSFT', shares: 10, lastPrice: 420.75 },
  { id: 2, ticker: 'MSFT', shares: 10, lastPrice: 420.75 },
  { id: 2, ticker: 'MSFT', shares: 10, lastPrice: 420.75 },
  { id: 2, ticker: 'MSFT', shares: 10, lastPrice: 420.75 },
];

function ActivePortfolio() {
  return (
    <div className="flex h-[450px] w-full flex-col border-1 border-[#1269cc] rounded-lg mt-0.75 p-1.5">
      
        <div className="flex flex-col items-start w-full mb-3 mt-2 ml-3 shrink-0">
            <p className="text-lg mb-1">ACTIVE PORTFOLIO</p>
        </div>

      <div className="overflow-x-auto px-3">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b text-[11px] tracking-wider">
              <th className="py-3">TICKER</th>
              <th className="py-3">SHARES</th>
              <th className="py-3 text-right">LAST PRICE</th>
            </tr>
          </thead>
          <tbody className="divide-y text-sm">
            {portfolioData.map((item) => (
              <tr key={item.id} className="">
                <td className="py-4">{item.ticker}</td>
                <td className="py-4">{item.shares}</td>
                <td className="py-4 text-right">${item.lastPrice.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}

export default ActivePortfolio