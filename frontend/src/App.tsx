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
      <div className="flex flex-col mx-4 sm:mx-6 mt-5 gap-4">
        <div className="w-full">
          <Graph />
        </div>

        <div className="flex flex-col lg:flex-row gap-4 w-full">
          <div className="w-full lg:flex-[1.67] min-w-0">
            <ActivePortfolio />
          </div>
          
          <div className="w-full lg:flex-[1] min-w-0">
            <NewsFeed />
          </div>
          
          <div className="w-full lg:flex-[1] min-w-0">
            <ExecutionLog />
          </div>
        </div>
      </div>
    </>
  )
}

export default App;