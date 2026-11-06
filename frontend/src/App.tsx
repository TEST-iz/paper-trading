// import { useState } from 'react'
import ExecutionLog from './components/ExecutionLog'
import NewsFeed from './components/NewsFeed'
import ActivePortfolio from './components/ActivePortoflio'
import Navbar from './components/Navbar'
import Graph from './components/Graph'

function App() {
  return (
    <>
      <Navbar />
      <div className="flex flex-col mx-6 mt-5 gap-4">
        {/* Graph takes full width */}
        <div className="w-full">
          <Graph />
        </div>

        <div className="flex flex-row gap-2 w-full">
          <div className="flex-[1.67] min-w-0">
            <ActivePortfolio />
          </div>
          
          <div className="flex-[1] min-w-0">
            <NewsFeed />
          </div>
          
          <div className="flex-[1] min-w-0">
            <ExecutionLog />
          </div>
        </div>
      </div>
    </>
  )
}

export default App