import React ,{ useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const search = async () => {
    const response = await axios.get(`http://127.0.0.1:8000/search/?query=${query}`);
    setResults(response.data.results);
  };

  return (
    <div className="container">
      <h1> Wyszukiwarka modeli</h1>
      <input 
        type="text" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
        placeholder="Wpisz np. Hawker Hurricane 1:72" 
      />
      <button onClick={search}>Szukaj</button>
      
      <ul>
        {results.map((item, index) => (
          <li key={index}>
            <a href={item.link} target="_blank" rel="noopener noreferrer">
              {item.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
