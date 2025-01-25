import logo from "/logo.png";
import "./App.css";
import React from 'react';
import { useState } from "react";

const URL_REGEX =
  /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/;

const mockSearchResults: SearchResult[] = [
  {
    imageUrl:
      "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcT7RrJeTX8dM5BdFDel_YOMwqzlWAplYYnAYXWLE7GqQFBOc2FJsiGUWKDP49eWapdYCvnrBGsINaSuQwT6Yy-tdV5ajza5vx7T9oI3Z71SbP7FD6Wtwheaig",
    title: "Elegant Leather Tote Bag",
    price: 179,
    link: "https://www.katespadeoutlet.com/products/kayla-large-shoulder-bag/KK055-001.html?KSNY=true&gStoreCode=KS5742&gQT=1",
  },
  {
    imageUrl:
      "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQCB7t_3Tz7fmQlJxQWB-xpYELydFG4fuKjjsldcRUuVJQgchttJQse45dfRygMJupp0fnV5VfH5NarmFZOsLikI9UjfgbXFzyz0A85TKkA53PiB9jczGwIfg",
    title: "Coach Women's Teri Shoulder Bag in Signature Leather",
    price: 229,
    link: "https://www.coachoutlet.com/products/teri-shoulder-bag-in-signature-leather/CY774-IMBLK.html?COHNA=true&gQT=1",
  },
  {
    imageUrl:
      "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcTTisO2MZeII1Ey0OLEzibOtsHdFmaFXJsi2k3TOBkIFo8gF3Rjkr65gdQwD6ZiJ82FXYHzwEr5VLZcv_RNdZUWBXR-hpnBMuphCIRsy32hFJMccC2FaAwZ",
    title: "Mini Clutch Purse with Zipper Closure",
    price: 16,
    link: "https://www.amazon.com/CYHTWSDJ-Shoulder-Handbag-Clutch-Closure/dp/B0B65FNCYM?source=ps-sl-shoppingads-lpcontext&smid=A9K87X7FFPA2N&gQT=1",
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
  const [error, setError] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [minPrice, setMinPrice] = useState<number>(0);
  const [maxPrice, setMaxPrice] = useState<number>(100);

  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setSearchResults([]);
    setLoading(true);

    if (!URL_REGEX.test(imageUrl)) {
      setError("Invalid image URL. Please enter a valid URL.");
      setLoading(false);
      return;
    }

    fetch("https://example.com/api/data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        imageUrl,
        minPrice,
        maxPrice,
      }),
    })
      .then((response) => {
        console.log(response);
        return response.json();
      })
      .then((data) => {
        console.log("Success:", data);
      })
      .catch(() => {
        setLoading(false);
        setError("An error occurred. Please try again later.");
      });
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
            value={imageUrl}
            onChange={(event) => setImageUrl(event.target.value)}
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
        <div>
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
        </div>
      ) : loading ? (
        <p className="animate-pulse">Loading...</p>
      ) : (
        ""
      )}
      {error && <p className="error">{error}</p>}
    </>
  );
}

export default App;
