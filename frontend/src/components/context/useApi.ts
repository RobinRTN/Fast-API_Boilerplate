import axios from "axios";
import { useAuth } from "./AuthContext";
import { useNavigate } from "react-router-dom";

const URL = import.meta.env.VITE_APP_PRODUCTION=== 'production' ? "https://picks-sous.xyz" : "http://localhost:4430";

export const useApi = () => {
    const { logout } = useAuth();
    const navigate  = useNavigate();

    const axiosInstance = axios.create({
        baseURL: `${URL}/api`,
        withCredentials: true,
        headers: {
            "Content-Type": "application/json",
        }
    });

    axiosInstance.interceptors.response.use(
        (response) => response,
        async (error) => {
          if (error.response?.status === 401) {
            console.error("Unauthorized. Trying to refresh it...");
            try {
              await axios.post(`${URL}/api/refresh`, {}, {withCredentials: true});
              return axiosInstance.request(error.config);
            } catch {
              console.log("Refresh token also outdated, logging out the user");
              logout();
              navigate("/login");
            }
          }
          return Promise.reject(error);
        }
      );


    return axiosInstance;
}
