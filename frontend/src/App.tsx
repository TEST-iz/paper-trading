// import { useState } from 'react'
import './App.css'
import './components/ExecutionLogItem'
import ExecutionLogItem from './components/ExecutionLogItem'

function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
    <h1>What's up</h1>
    <ExecutionLogItem 
      action="SELL"
      ticker="AAPL"
      shares={10}
      price={1243.3}
    />
    </>
  )
}

export default App
