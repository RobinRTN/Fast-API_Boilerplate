import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Helmet, HelmetProvider } from "react-helmet-async";
import { AuthProvider } from './components/context/AuthContext';
import Home from './components/Home';
import SignUp from './components/SignUp';
import Login from './components/Login';
import { Toaster } from "react-hot-toast";

function App() {

  return (
    <Router>
      <AuthProvider>
        <HelmetProvider>  {/* ✅ Wrap everything inside HelmetProvider */}
          <Toaster />
          <Helmet>
            <title>Pick Sous</title>
            <meta name="Pick Sous" content="Tout tout de suite !" />
          </Helmet>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </HelmetProvider>
      </AuthProvider>
    </Router>
  )
}

export default App

