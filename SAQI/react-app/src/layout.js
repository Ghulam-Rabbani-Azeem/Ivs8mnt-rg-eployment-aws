import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from "axios";
import { Chart } from "react-google-charts";

 
export const options = {
  chart: {
    title: "Box Office Earnings in First Two Weeks of Opening",
    subtitle: "in millions of dollars (USD)",
  },
};


const App = () => {
  const [rangeValue, setRangeValue] = useState(0.5);
  const [fileNames, setFileNames] = useState([]);
  const [inputValue2, setInputValue2] = useState('');

  const handleSubmit2 = (e) => {
    e.preventDefault();
    
    const url = "http://127.0.0.1:8000/add";
    axios
      .post(url, {
        data: inputValue2,
        headers: { "Access-Control-Allow-Origin": "*" },
      })
      .then((response) => {
        // Handle the response as needed
        console.log("Response:", response);
        const data = JSON.parse(response.data);

        // Set the array of file names to state
        setFileNames(data);
    
    
      })
      .catch((error) => {
        // Handle errors if any
        console.error("Error:", error);
      });
    // Reset the input after submitting
    setInputValue2('');
  };
 
   const handleFormSubmit = (event) => {
    event.preventDefault();
    const url = "http://127.0.0.1:8000/ratio";
    axios
      .post(url, {
        data: rangeValue,
        headers: { "Access-Control-Allow-Origin": "*" },
      })
      .then((response) => {
        // Handle the response as needed
        console.log("Response:", response);
        const data = JSON.parse(response.data);

        // Set the array of file names to state
        setFileNames(data);
    
    
      })
      .catch((error) => {
        // Handle errors if any
        console.error("Error:", error);
      });
  };
  

  const handleRangeChange = (event) => {
    setRangeValue(parseFloat(event.target.value)); // Update the rangeValue state
  };
  // convert the data format for google chat

 const data = [["Date"],];

 fileNames.forEach((item) => {
  data[0].push(item.name);
});
const maxLength = Math.max(...fileNames.map(item => item.prediction.length));

for (let i = 1; i < maxLength; i++) {
  const row = [i + 1]; // Adding incrementing numbers starting from 1
  fileNames.forEach((item) => {
    const val = item.prediction[i] ? item.prediction[i][0] : ''; // Check if the value exists, if not, insert an empty string
    row.push(val);
  });
  data.push(row);
}
  

 

  return (
    <div className="App">
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <a className="navbar-brand" href="/">
          Your Logo
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ml-auto">
            <li className="nav-item">
              <a className="nav-link" href="/">
                Home
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/about">
                About
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/contact">
                Contact
              </a>
            </li>
          </ul>
        </div>
      </nav>

      {/* Main Body */}
      <main className="container mt-4">
        <h1>Main Content</h1>

      

        <p>We have limited data sets but user can add new data set  </p>
        <form onSubmit={handleSubmit2} className="d-flex align-items-center p-5">
      <input
        type="text"
        value={inputValue2}
        onChange={(e) => setInputValue2(e.target.value)}
        className="form-control mr-2"
        placeholder="Enter something"
      />
      <button type="submit" className="btn btn-primary">
        Add
      </button>
    </form>

        <div >
         {/* Safe Stocks with Low Growth */}
      
      
        <div className="row">
     
          <div className="col-6 mb-4">
            <div className="card">
            <h2 className="text-center mb-4">Safe Stocks with Low Growth</h2>
              <div className="card-body">
                <h5 className="card-title">Stock 1</h5>
                <p className="card-text">
                  Description about the stock and its attributes.
                </p>
                <a href="#" className="btn btn-primary">
                  Details
                </a>
              </div>
            </div>
          </div>

           {/* Risky Stocks with High Growth */}
      
     
          <div className="col-6 mb-4">
            
            <div className="card">
            <h2 className="text-center mb-4">Risky Stocks with High Growth</h2>
              <div className="card-body">
                <h5 className="card-title">Stock A</h5>
                <p className="card-text">
                  Description about the stock and its attributes.
                </p>
                <a href="#" className="btn btn-primary">
                  Details
                </a>
              </div>
            </div>
          </div>
          {/* Add more cards for other stocks */}
          <form onSubmit={handleFormSubmit}>
            <div> <h4>Change risk ratio</h4></div>
          <label htmlFor="customRange1" className="form-label">
              Current Value: <strong className='text-danger'> {rangeValue}</strong>
            </label>
            <input
              type="range"
              className="form-range"
              id="customRange1"
              min="0"
              max="10"
              step="0.1"
              value={rangeValue}
              onChange={handleRangeChange}
            />
           
            <button type="submit" className="btn btn-primary mt-3">
              Submit
            </button>
         </form>
        </div>
      </div>
      <div>
      
      <div className="container">
      {fileNames.map((item, index) => (
        <div key={index} className="table-container">
          <h3>Prophet Prediction for {item.name}</h3>
          <table className="table table-bordered table-striped">
            <thead className="thead-dark">
              <tr>
                <th scope="col">Date</th>
                <th scope="col">{item.name}</th>
              </tr>
            </thead>
            <tbody>
              {item.prediction.map((prediction, idx) => (
                <tr key={idx}>
                  <td>2024 Month {idx + 1}</td>
                  <td>{prediction}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
    </div>
    <Chart
      chartType="Line"
      width="100%"
      height="400px"
      data={data}
      options={options}
    />
      </main>

      {/* Footer */}
      {/* <footer className="bg-dark text-white text-center py-3">
        <p className="mb-0">© {new Date().getFullYear()} Your Website Name. All Rights Reserved.</p>
      </footer> */}
    </div>
  );
};

export default App;
