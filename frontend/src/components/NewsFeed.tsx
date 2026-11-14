import { useEffect, useState } from 'react';
import NewsFeedCard from "./NewsFeedCard";

type NewsCard = {
    guid: string
    comp: string
    title: string
    summary: string,
    url: string,
    pub_date: string,
    sentiment_title: number,
    sentiment_summary: number
}

function NewsFeed() {

    const [data, setData] = useState<NewsCard[]>([]);
    const [loading, setLoading] = useState(true);


    useEffect(() => {
        fetch('http://localhost:8000/news')
            .then(res => res.json())
            .then((result: NewsCard[]) => {
                setData(result);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed", err);
                setLoading(false);
            });
    }, []);

    return (
        <>
        <div className="flex h-[450px] w-full flex-col items-center border-1 border-[#1269cc] rounded-lg mt-0.75 p-1.5">
            <div className="flex flex-col items-start w-full mb-1 mt-2 ml-5 shrink-0">
                <p className="text-lg mb-1"> RECENT NEWS FEED</p>
            </div>
            
            <div className="flex-1 min-h-0 w-full overflow-y-auto flex flex-col items-center px-2.5">

                {loading ? "Loading...": 
                    data.map((item) => (
                        <NewsFeedCard 
                            key={item.guid}
                            date={item.pub_date}
                            title={item.title}
                            summary={item.summary}
                            sent_t={String(item.sentiment_title)}
                            sent_s={String(item.sentiment_summary)} 
                        />
                    ))            
                }

                {/* <NewsFeedCard
                    date="2026-09-27T17:00:41Z"
                    title="Qualcomm Stock Has an Opportunity Investors May Be Underestimating"
                    summary="Qualcomm just posted 61% automotive growth and raised its non-handset target to $40 billion, yet the market keeps valuing it like a company living and dying by smartphone chips. Something in that gap is worth a closer look."
                    sent_t="-0.8310036063194275"
                    sent_s ="0.0"
                />

                <NewsFeedCard
                    date="2026-09-27T17:00:41Z"
                    title="Qualcomm Stock Has an Opportunity Investors May Be Underestimating"
                    summary="Qualcomm just posted 61% automotive growth and raised its non-handset target to $40 billion, yet the market keeps valuing it like a company living and dying by smartphone chips. Something in that gap is worth a closer look."
                    sent_t="0.52"
                    sent_s ="0.1"
                />

                <NewsFeedCard
                    date="2026-09-27T17:00:41Z"
                    title="Qualcomm Stock Has an Opportunity Investors May Be Underestimating"
                    summary="Qualcomm just posted 61% automotive growth and raised its non-handset target to $40 billion, yet the market keeps valuing it like a company living and dying by smartphone chips. Something in that gap is worth a closer look."
                    sent_t="-0.8310036063194275"
                    sent_s ="0.5544"
                /> */}

            </div>
        </div>
        </>
    );
}

export default NewsFeed;