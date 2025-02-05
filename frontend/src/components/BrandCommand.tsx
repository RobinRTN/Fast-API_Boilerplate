import { IoMdAddCircle } from "react-icons/io";

interface BrandCommandProps {
    fetchChannelData: (channelId: number) => void;
    selectedChannelId: number | null;
  }

  const BrandCommand: React.FC<BrandCommandProps> = ({ fetchChannelData, selectedChannelId }) => {

    const prefBrands = {
        "Nike": 1,
        "Carhartt": 2,
        "Jack Wolveskin": 3,
        "Arcteryx": 4,
        "Levis": 5,
        "Patagonia": 6
    }

    return (
        <div className="px-2 max-h-[500px] overflow-y-auto overflow-x-hidden">
            <p className="text-sm text-center text-gray-500 mb-2 border-b-2 pb-1">Canaux communs</p>
            <ul>
                {  Object.entries(prefBrands).map(([brand, channelId]) => {
                    return (
                        // <li key={brand} className="text-sm px-2 py-1 rounded trransition-colors hover:bg-[#ccdde0]" onClick={() => fetchChannelData(channelId)}>
                        <li key={brand} className={`text-sm px-2 py-1 my-1 rounded transition-colors  ${selectedChannelId === channelId ? "bg-[#aec3c7]" : "hover:bg-[#ccdde0]"}`} onClick={() => fetchChannelData(channelId)}>
                            {brand}
                        </li>
                    )
                })
                }
            </ul>
            <p className="mt-4 text-sm text-center text-gray-500 mb-2 border-b-2 pb-1">Canaux perso</p>
            <button className="flex text-[#478690] justify-center text-center items-center text-sm py-2 my-1 rounded transition-colors w-full hover:bg-[#ccdde0]">
                <p className="me-1">Ajouter</p>
                <IoMdAddCircle />
            </button>
        </div>
    );
}

export default BrandCommand;