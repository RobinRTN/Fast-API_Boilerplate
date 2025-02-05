import React, { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';

const URL = import.meta.env.VITE_APP_PRODUCTION === 'production' ? "https://picks-sous.xyz" : "http://localhost:4430";

interface AuthContextType {
  isAuth: boolean;
  login: () => void;
  logout: () => void;
}

interface AuthProviderProps {
  children: React.ReactNode;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    console.log("Inside the useEffect that fetches the refresh and access in the cookies!");
    
    const checkAuth = async () => {
      try {
        const response = await axios.get(`${URL}/api/me`, {withCredentials: true});
        if (response.status === 200 ) {
          setIsAuth(true);
        }
      } catch (error: any) {
        console.log("Failed to make the call");
        setIsAuth(false)
      }
    }
    checkAuth();
  }, []);

  const login = () => {
    console.log("Inside the logging method of Auth - with: ");
    setIsAuth(true);
  };

  const logout = () => {
    console.log("Loggout from the app, erasing elements in the cookies");
    setIsAuth(false);
  };

  return (
    <AuthContext.Provider value={{isAuth, login, logout}}>
      {children}
    </AuthContext.Provider>
  );

};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
