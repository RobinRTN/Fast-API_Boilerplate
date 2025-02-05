import { useAuth } from "./context/AuthContext";
import { IoMdExit } from "react-icons/io";
import { IoMdHeart } from "react-icons/io";
import { GiSevenPointedStar } from "react-icons/gi";
import { useApi } from "./context/useApi";
import BrandCommand from "./BrandCommand";
import { useState, useEffect, useRef } from "react";
// import { toast } from "react-hot-toast";
import { io, Socket } from "socket.io-client";
import { Link } from "react-router-dom";
import { Button } from "./ui/button";

interface canalItem {
    "_id": string,
    "title": string,
    "brand_title": string,
    "price": string,
    "garment_url": string,
    "photo_url": string,
    "status": string,
    "size_title": string,
    "favorite_count": string,
    "channel_id": string,
    "websocket": boolean,
}

const URL = import.meta.env.VITE_APP_PRODUCTION === 'production' ? "https://picks-sous.xyz" : "http://localhost:4430";

function Home() {
    const { isAuth, logout } = useAuth();
    const [canalData, setCanalData] = useState<canalItem[]>([]);
    const [selectedChannelId, setSelectedChannelId] = useState<number | null>(null);
    const [socket, setSocket] = useState< Socket | null>(null)
    const api = useApi();
    const scrollRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        if (scrollRef.current) {
            console.log("Scrolling to bottom");
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    };

    // Scroll to bottom when data changes
    useEffect(() => {
        scrollToBottom();
    }, [canalData]);

    useEffect(() => {
      return () => {
          if (socket) {
              socket.disconnect();
          }
      };
  }, [socket]);

    const connectToChannelWebSocket = (channelId: number) => {
      if (socket) {
          socket.disconnect();
          setSocket(null);
      }

      const newSocket = io(`${URL}`, {
        transports: ["websocket"], // Force WebSocket transport
        withCredentials: true, // Ensure it sends authentication cookies
        reconnection: true,
        reconnectionAttempts: 5, // Limit reconnection attempts
        reconnectionDelay: 1000, // 1 second between attempts
        timeout: 20000, // Give up after 20 seconds if no response
    });

    // ✅ Handle connection established
    newSocket.on("connect", () => {
        console.log(`Connected to WebSocket for channel ${channelId}`);
        newSocket.emit("subscribe", { channelId }); // Ensure subscription is explicit
    });

    // ✅ Handle incoming data securely
    newSocket.on(`channel_${channelId}_update`, (data) => {
        console.log(`Update for channel ${channelId}:`, data);

        if (!data || typeof data !== "object" || !data.title || !data.price) { 
            console.error("Invalid WebSocket data received. Ignoring update.");
            return;
        }

        setCanalData((prevData) => [...prevData, data]);  // ✅ Only update with valid objects
    });

    // ✅ Handle disconnection and cleanup
    newSocket.on("disconnect", (reason) => {
        console.warn(`Disconnected from WebSocket for channel ${channelId}: ${reason}`);
    });

    newSocket.on("error", (error) => {
        console.error(`WebSocket error for channel ${channelId}:`, error);
    });

    setSocket(newSocket);
  };


    const fetchChannelData = async (channelId: number) => {
        try {
            const response = await api.get(`/items/canal/${channelId}`);
            // console.log(response);
            if (!response || !Array.isArray(response.data)) {
                console.log("Response from server missing or invalid");
                return;
            }
            const lastItems = response.data.slice(-40);
            setCanalData(lastItems);
            console.log("Last item length = ", lastItems.length);
            connectToChannelWebSocket(channelId);
        } catch (error) {
            setCanalData([]);
            // toast.error("Erreur de chargement")
            console.error("Error: ", error);
        } finally {
            setSelectedChannelId(channelId);
        }
    }

    if (isAuth) {
        return (
            <div className="flex h-screen">
                <div className="border-r-4 border-[#F2F2F2] flex flex-col justify-between pe-2">
                    <div>
                        <div className="header m-1 mb-3 py-2 px-4 flex items-center justify-center bg-white rounded cursor-pointer">
                            <img src="/drip.png" alt="Logo picture" className="h-10 w-10 me-3"/>
                            <h1 className="font-bold text-center">PICKS SOUS</h1>
                        </div>
                        <BrandCommand fetchChannelData={fetchChannelData} selectedChannelId={selectedChannelId}/>
                    </div>
                    <div className="m-1 flex justify-center items-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 bg-primary text-primary-foreground hover:bg-primary/90 h-10" onClick={() => logout()}>
                        <IoMdExit />
                    </div>
                </div>
                { canalData.length > 0 ? (
                    <div ref={scrollRef} className="flex-1 h-full overflow-y-auto">
                        <div className="flex flex-wrap container my-3 ">
                                {
                                    canalData.map(element =>
                                        (
                                            <a href={element.garment_url} target="_blank" rel="noopener noreferrer" className={`m-2 px-4 py-4 rounded-[2px] flex flex-col items-center w-[220px] hover:bg-[#adcbd057] cursor-pointer transition relative ${element.websocket ? "bg-[#adcbd038]" : ""}`} key={element._id}>
                                                <img
                                                    src={element.photo_url}
                                                    alt="garment_picture"
                                                    className="h-44 w-44 object-cover rounded-[2px]"
                                                />
                                                <div className="w-full">
                                                    <h1 className="mt-2 text-sm max-h-[20px] overflow-hidden font-bold mb-2 text-gray-600">
                                                    {element.title}
                                                    </h1>
                                                    <div className="flex justify-start items-center mb-2">
                                                    <p className="text-xs me-1">{element.favorite_count}</p>
                                                    <IoMdHeart className="text-[#aec3c7]" />
                                                    </div>
                                                    <p className="text-xs mb-2">Taille {element.size_title}</p>
                                                    <p className="text-xs text-[#337984] bold mb-2">
                                                    {element.price ? element.price : "inconnu"} €
                                                    </p>
                                                </div>
                                                {element.websocket && (
                                                    <GiSevenPointedStar className="text-[#aec3c7] absolute bottom-1 right-1" />
                                                )}
                                            </a>

                                        )
                                    )
                                }
                        </div>
                    </div>
                ) : (
                    <div className="flex-1 flex justify-center container mt-3">
                        <div className="mt-24">
                            <img src="/drip.png" alt="Logo picture" className="h-28 w-28 me-3 animate-spinSlow"/>
                        </div>
                    </div>
                )}
            </div>
        );
    }

    return (
        <div className="flex w-screen flex-col items-center justify-center mt-5">
            <h1>This is the Landing Page</h1>
            <div className="flex justify-evenly items-center mt-3">
                <Link to="/signup">
                    <Button>
                        S'inscrire
                    </Button>
                </Link>
                <Link to="/login">
                    <Button>
                        Se connecter
                    </Button>
                </Link>
            </div>
        </div>
    );
}

export default Home;
