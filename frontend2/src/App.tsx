import logo from "/logo.png";
import "./App.css";
import React from "react";
import { useState } from "react";

const URL_REGEX =
  /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/;

type SearchResult = {
  score: number;
  product: {
    brand: string;
    price: number;
    image_url: string;
    review: number;
  };
};

function App() {
  const [searchResults, setSearchResults] =
    useState<SearchResult[]>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [minPrice, setMinPrice] =
    useState<number>(0);
  const [maxPrice, setMaxPrice] =
    useState<number>(100);

  const onSubmit = (
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();
    setError("");
    setSearchResults([]);
    setLoading(true);

    if (!URL_REGEX.test(imageUrl)) {
      setError(
        "Invalid image URL. Please enter a valid URL.",
      );
      setLoading(false);
      return;
    }

    fetch("http://0.0.0.0:8000/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        image_url: imageUrl,
        min_price: minPrice,
        max_price: maxPrice,
      }),
    })
      .then((response) => {
        console.log(response);
        return response.json();
      })
      .then((data) => {
        console.log("Success:", data);
        setSearchResults(data.results);
      })
      .catch(() => {
        setLoading(false);
        setError(
          "An error occurred. Please try again later.",
        );
      });
  };

  console.log(searchResults);

  return (
    <>
      <div className="search-container">
        <div>
          <a target="_blank">
            <img
              src={logo}
              className="logo"
              alt="Fashion Finder logo"
            />
          </a>
        </div>
        <form
          className="search-form"
          onSubmit={onSubmit}
        >
          <label htmlFor="linkInput">
            Paste the link to your purse's image
          </label>
          <input
            value={imageUrl}
            onChange={(event) =>
              setImageUrl(event.target.value)
            }
            type="text"
            name="linkInput"
            placeholder="The URL of your purse's image"
            required
          />
          <label htmlFor="search">
            Define your price range($)
          </label>
          <div
            className="price-range"
            style={{
              marginTop: 0,
              marginBottom: "5px",
            }}
          >
            <input
              type="number"
              placeholder="Min price($)"
              value={minPrice}
              onChange={(event) =>
                setMinPrice(
                  Number(event.target.value),
                )
              }
              required
            />
            <input
              type="number"
              placeholder="Max price($)"
              value={maxPrice}
              onChange={(event) =>
                setMaxPrice(
                  Number(event.target.value),
                )
              }
              required
            />
          </div>
          <button
            type="submit"
            className="search-btn"
          >
            Search
          </button>
        </form>
      </div>
      {searchResults &&
      searchResults.length > 0 ? (
        <div>
          <div className="results">
            {searchResults.map(
              (result, index) => {
                return (
                  <div
                    className="result"
                    key={index}
                    onClick={() =>
                      window.open(
                        `file://${result.product.image_url}`,
                        "_blank",
                      )
                    }
                  >
                    <img
                      src={`file://${result.product.image_url}`}
                      alt={result.product.brand}
                      height={150}
                    />
                    <div className="result-info">
                      <h3>
                        {result.product.brand}
                      </h3>
                      <p>
                        ${result.product.price}
                      </p>
                    </div>
                  </div>
                );
              },
            )}
          </div>
        </div>
      ) : loading ? (
        <p className="animate-pulse">
          Loading...
        </p>
      ) : (
        ""
      )}
      {error && <p className="error">{error}</p>}
    </>
  );
}

export default App;
