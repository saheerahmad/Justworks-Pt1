import React, { useState } from 'react';
import './App.css';


function App() {

  // var showDiv;
  //   if(localStorage.getItem("showDiv") == null) {
  //       showDiv = true;
  //   }
  //   else {
  //       showDiv = localStorage.getItem("showDiv")
  //   }

  //   if (showDiv) {
  //         document.getElementById('Import').style.display = 'block';
  //   }
  //   else {
  //       document.getElementById('Import').remove();
  //   }

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
    // document.getElementById("Import").
    document.getElementById('Import').remove();
    // localStorage.setItem("showDiv", false);



    fetch("http://127.0.0.1:8000/getSummary/")
    .then( res => res.blob() )
    .then( blob => {
      var file = window.URL.createObjectURL(blob);
      window.location.assign(file);
    });
  }

  return (
    <div id='body'>
      <div id="Import">
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
    </div>
    

  );
}

export default App;
