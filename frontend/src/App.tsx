// import { useState } from 'react'
import './App.css'
import ExecutionLog from './components/ExecutionLog'
import NewsFeed from './components/NewsFeed'

function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
    <h1>What's up</h1>
    <ExecutionLog />
    <NewsFeed />
    </>
  )
}

export default App
