import React, { useState } from 'react';
import './Home.css';

function Home() {
  const [file, setFile] = useState(null);
  const fileChangeHandler = (e) => {
    setFile(e.target.files[0]);
    console.log(e.target.files[0])
  }

  const handleSubmit = (e) => {
    const formData = new FormData();
    formData.append(
      "file",
      file,
      file.name
    );

    const reqOptions = {
      method: "POST",
      body: formData
    };
    fetch("http://127.0.0.1:8000/submitCSV/", reqOptions).then(response => response.json().then(function(response){
      console.log(response)
    }));
    
    
  }

  return (
    <div className="Import">
      <form>
        <input
            name='data'
            type={"file"}
            id={"csvFileInput"}
            accept={".csv"}
            onChange={fileChangeHandler}
        />

        <button onClick={handleSubmit}>
            IMPORT CSV
        </button>
      </form>
    </div>
  );
}

export default Home;
