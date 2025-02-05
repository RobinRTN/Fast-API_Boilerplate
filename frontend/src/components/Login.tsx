import { Button } from "./ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { useState } from "react";
import { toast } from "react-hot-toast";
import axios from "axios";
import { useAuth } from "./context/AuthContext";
import { Link, useNavigate } from "react-router-dom";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";

const URL = import.meta.env.VITE_APP_PRODUCTION === 'production' ? "https://picks-sous.xyz" : "http://localhost:4430";
const GOOGLE_CLIENT = "1007725109700-h9go6r2e7bosait1f8u01sru5kqt7rdn.apps.googleusercontent.com"; 

function Login() {
  const [password, setPassword] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await axios.post(`${URL}/api/login`, {
        'email': email,
        'password': password
      }, {
        withCredentials: true
      });
      if (response.status === 200) {
        login()
        toast.success("Connexion réussie");
        navigate("/");
      } else {
        toast.error("Identifiants incorrects !");
      }
    }
    catch (err: any) {
        if (err.response.data.msg) {
            toast.error(err.response.data.msg);
        } else {
            toast.error("Une erreur est survenue !")
        }
    }
  }

  const handleGoogleLogin = async (credentialResponse: any) => {
    if (!credentialResponse.credential) {
      toast.error("Authentification echouee !");
    }
    console.log(credentialResponse);
    const idToken = credentialResponse.credential;
    console.log(idToken);

    try {
      const response = await axios.post(`${URL}/api/users/auth/google`, {idToken}, {withCredentials: true});
      if (response.status === 200) {
        toast.success("Connexion reussie");
        login();
        navigate("/");
      } else {
        toast.error("Connexion Google a echoue");
      }
    } catch (error) {
      console.error("error while google oauth: ", error);
      toast.error("Connexion Google a echoue");
    }
  }

  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT}>
      <div className="flex justify-center items-center w-screen mt-20 flex-col">
          <img src="/drip.png" alt="Logo picture" className="h-32 w-32 mb-3"/>
          <Card className="mx-auto max-w-sm px-2">
          <CardHeader>
              <CardTitle className="text-2xl">Se connecter</CardTitle>
              <CardDescription>
              Entre ton email et mot de passe
              </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} >
              <div className="grid gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                        onChange={(e) => setEmail(e.target.value)}
                        id="email"
                        type="email"
                        placeholder="m@example.com"
                        required
                        />
                  </div>
                  <div className="grid gap-2">
                    <div className="flex items-center">
                        <Label htmlFor="password">Mot de passe</Label>
                    </div>
                    <Input id="password" type="password" required onChange={(e) => setPassword(e.target.value)}/>
                  </div>
                  <Button type="submit" className="w-full">
                  Se connecter
                  </Button>
              </div>
            </form>
            <div className="mt-4">
              <GoogleLogin onSuccess={handleGoogleLogin} onError={() => toast.error("Google Auth Failed first step!")} />
            </div>
          </CardContent>
          </Card>
          <Link to="/signup" className="mt-2 text-sm">
              <p>Pas encore de compte ? <span className="underline font-normal">S'inscrire</span></p>
          </Link>
      </div>
    </GoogleOAuthProvider>
  )
}

export default Login;
