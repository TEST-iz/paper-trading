type cardProps = {
    date: string;
    title: string;
    summary: string;
    sent_t: string;
    sent_s: string;
}

function NewsFeedCard({date, title, summary, sent_t, sent_s}: cardProps) {
    const pubDate = new Date(date);
    const englishDate = pubDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    
    return (
        <>
        <div className="flex h-[200px] w-[350px] flex-col justify-around border-1 border-[#1269cc] rounded-lg mt-0.75 p-1.5 ml-3">
            <p className="text-xs">{englishDate}</p>
            <p className="break-words">{title}</p>
            <p className="line-clamp-3 break-normal text-xs">{summary}</p>
            <p className="text-sm">Title Sentiment: {(+sent_t).toPrecision(3)}</p>
            <p className="text-sm">Summary Sentiment: {(+sent_s).toPrecision(3)}</p>
        </div>
        </>
    )


}

export default NewsFeedCard;