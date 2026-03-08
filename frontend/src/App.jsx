import Navbar from "./components/Navbar"
import Signup from "./pages/Signup"
import Login from "./pages/Login"
import Home from "./pages/Home"
import Account from "./pages/Account"
import DetailedRecipe from "./pages/DetailedRecipe"
import { Route, Routes } from "react-router-dom"

function App() {
  return (
    <>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/Account" element={<Account />}/>
          <Route path="/Recipe" element={<DetailedRecipe />} />
        </Routes>
      </div>
    </>
  )
}

export default App