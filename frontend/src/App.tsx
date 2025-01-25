import logo from "/logo.png";
import "./App.css";
import { useState } from "react";

const mockSearchResults: SearchResult[] = [
  {
    imageUrl:
      "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcT7RrJeTX8dM5BdFDel_YOMwqzlWAplYYnAYXWLE7GqQFBOc2FJsiGUWKDP49eWapdYCvnrBGsINaSuQwT6Yy-tdV5ajza5vx7T9oI3Z71SbP7FD6Wtwheaig",
    title: "Elegant Leather Tote Bag",
    price: 120,
    link: "https://www.nordstrom.com/s/essential-soft-leather-tote/8039805?origin=category-personalizedsort&breadcrumb=Home/Women/Handbags/Tote%20Bags&color=200",
  },
  {
    imageUrl:
      "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQCB7t_3Tz7fmQlJxQWB-xpYELydFG4fuKjjsldcRUuVJQgchttJQse45dfRygMJupp0fnV5VfH5NarmFZOsLikI9UjfgbXFzyz0A85TKkA53PiB9jczGwIfg",
    title: "Classic Crossbody Purse",
    price: 85,
    link: "https://example.com/product/classic-crossbody-purse",
  },
  {
    imageUrl:
      "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcTTisO2MZeII1Ey0OLEzibOtsHdFmaFXJsi2k3TOBkIFo8gF3Rjkr65gdQwD6ZiJ82FXYHzwEr5VLZcv_RNdZUWBXR-hpnBMuphCIRsy32hFJMccC2FaAwZ",
    title: "Chic Quilted Handbag",
    price: 150,
    link: "https://n.nordstrommedia.com/it/dc63ebb4-1077-4f75-a67e-3a4848845a99.jpeg?crop=pad&trim=color&w=1950&h=2990&dpr=2",
  },
];

type SearchResult = {
  imageUrl: string;
  title: string;
  price: number;
  link: string;
};

function App() {
  const [searchResults, setSearchResults] =
    useState<SearchResult[]>(mockSearchResults);
  const [loading, setLoading] = useState(false);
  const [enteredLink, setEnteredLink] = useState("");
  const [minPrice, setMinPrice] = useState<number>(0);
  const [maxPrice, setMaxPrice] = useState<number>(100);

  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSearchResults([]);
    setLoading(true);
    console.log(enteredLink, minPrice, maxPrice);
  };

  return (
    <>
        <div className="search-container">
          <div>
            <a target="_blank">
              <img src={logo} className="logo" alt="Fashion Finder logo" />
            </a>
          </div>
          <form className="search-form" onSubmit={onSubmit}>
            <label htmlFor="linkInput">
              Paste the link to your purse's image
            </label>
            <input
              value={enteredLink}
              onChange={(event) => setEnteredLink(event.target.value)}
              type="text"
              name="linkInput"
              placeholder="The URL of your purse's image"
              required
            />
            <label htmlFor="search">Define your price range($)</label>
            <div
              className="price-range"
              style={{ marginTop: 0, marginBottom: "5px" }}
            >
              <input
                type="number"
                placeholder="Min price($)"
                value={minPrice}
                onChange={(event) => setMinPrice(Number(event.target.value))}
                required
              />
              <input
                type="number"
                placeholder="Max price($)"
                value={maxPrice}
                onChange={(event) => setMaxPrice(Number(event.target.value))}
                required
              />
            </div>
            <button type="submit" className="search-btn">
              Search
            </button>
          </form>
        </div> 
        {searchResults.length > 0 ? (
          <div className="results">
            {searchResults.map((result, index) => {
              return (
                <div
                  className="result"
                  key={index}
                  onClick={() => window.open(result.link, "_blank")}
                >
                  <img src={result.imageUrl} alt={result.title} height={150} />
                  <div className="result-info">
                    <h3>{result.title}</h3>
                    <p>${result.price}</p>
                  </div>
                </div>
              );
            })}
          </div>
        ) : loading ? (
          <p className="animate-pulse">Loading...</p>
        ) : (
          ""
        )}
    </>
  );
}

export default App;
