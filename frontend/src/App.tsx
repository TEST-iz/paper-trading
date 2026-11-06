// import { useState } from 'react'
import ExecutionLog from './components/ExecutionLog'
import NewsFeed from './components/NewsFeed'
import ActivePortfolio from './components/ActivePortoflio'
import Navbar from './components/Navbar'
import Graph from './components/Graph'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      {/* Main container with max width, centered, and padded from screen borders */}
      <main className="max-w-[1600px] mx-auto px-6 py-6 flex flex-col gap-6">
        {/* Graph box */}
        <div className="w-full">
          <Graph />
        </div>

        {/* Bottom 3 boxes laid out in a responsive grid/flex row with equal spacing */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 w-full">
          <ActivePortfolio />
          <NewsFeed />
          <ExecutionLog />
        </div>
      </main>
    </div>
  )
}

export default App