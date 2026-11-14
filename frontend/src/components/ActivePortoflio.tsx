import { useEffect, useState } from 'react';

type Portfolio = {
    comp: string;
    shares: number;
    last_price: number;
    updated_at: string
}

function ActivePortfolio() {

  const [data, setData] = useState<Portfolio[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/portfolio')
      .then(res => res.json())
      .then((result: Portfolio[]) => {
        setData(result);
        setLoading(false);
      })
      .catch(err => {
        console.log("Error", err);
        setLoading(false);
      });
  }, [])


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
            {loading ? "Loading..." : 
              data.map((item) => (
              <tr key={item.comp} className="">
                <td className="py-4">{item.comp}</td>
                <td className="py-4">{item.shares}</td>
                <td className="py-4 text-right">${item.last_price.toFixed(2)}</td>
              </tr>
            ))
            }
          </tbody>
        </table>
      </div>

    </div>
  );
}

export default ActivePortfolio