// import { useState } from 'react'
import './App.css'
import NewsFeedCard from './components/NewsFeedCard'
import ExecutionLog from './components/ExecutionLog'

function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
    <h1>What's up</h1>
    <NewsFeedCard
      date="2026-09-27T17:00:41Z"
      title="Qualcomm Stock Has an Opportunity Investors May Be Underestimating"
      summary="Qualcomm just posted 61% automotive growth and raised its non-handset target to $40 billion, yet the market keeps valuing it like a company living and dying by smartphone chips. Something in that gap is worth a closer look."
      sent_t="-0.8310036063194275"
      sent_s ="0.0"
    />
    <ExecutionLog />
    </>
  )
}

export default App
