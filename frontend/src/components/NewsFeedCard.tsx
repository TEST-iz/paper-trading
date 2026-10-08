type cardProps = {
    date: string;
    title: string;
    summary: string;
    sent_t: string;
    sent_s: string;
}

const SENT_COLOURS: Record<string, string> = {
        "POSITIVE": "text-emerald-500 font-semibold",
        "NEGATIVE": "text-rose-500 font-semibold",
        "NEUTRAL": "text-gray-500 font-semibold",
};

const checkSign = (n: number) => {
  if (n > 0) return "POSITIVE";
  if (n < 0) return "NEGATIVE";
  return "NEUTRAL";
};

function NewsFeedCard({date, title, summary, sent_t, sent_s}: cardProps) {
    const pubDate = new Date(date);
    const englishDate = pubDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    const sentTSign = checkSign(+sent_t);
    const sentSSign = checkSign(+sent_s);
    const sentTStyle = SENT_COLOURS[sentTSign];
    const sentSStyle = SENT_COLOURS[sentSSign];
    
    return (
        <>
        <div className="flex h-[200px] w-[350px] flex-col justify-around border-1 border-[#1269cc] rounded-lg mt-0.75 p-1.5 mb-2">
            <p className="text-xs">{englishDate}</p>
            <p className="break-words">{title}</p>
            <p className="line-clamp-3 break-normal text-xs">{summary}</p>
            <p className="text-sm">Title Sentiment: <span className={sentTStyle}>{(+sent_t).toPrecision(3)}</span></p>
            <p className="text-sm">Summary Sentiment: <span className={sentSStyle}>{(+sent_s).toPrecision(3)}</span></p>
        </div>
        </>
    )


}

export default NewsFeedCard;