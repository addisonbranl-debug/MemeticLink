import React, { useState, useRef, useCallback, useEffect } from 'react';
import Webcam from 'react-webcam';
import './index.css';

const API = "/api/memetic";

export default function App() {
  const [screen, setScreen] = useState('title');
  const [photo, setPhoto] = useState(null);
  const [test,setTest] =useState([]);
  const [idnum,setIDNum] = useState(1);
  const webcamRef = useRef(null);
  const numPhotos = 7;

  useEffect(() => {
    fetch(API)
      .then((res) => res.json())
      .then(setTest);
  }, []);



  // Function to capture the photo
  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setIDNum(Math.floor(Math.random() * numPhotos) + 1);
    setPhoto(imageSrc);
    setScreen('result');
  }, [webcamRef]);

  // --- ATOM: Button ---
  const MemeButton = ({ onClick, text }) => (
    <button className="btn-meme" onClick={onClick}>
      {text}
    </button>
  );

  // --- SCREEN 1: Title ---
  const TitleScreen = () => (
    <>
      <h1 className="meme-title">Memetic<br/>Link</h1>
      <div className="meme-subtitle">EST. 2025</div>
      <MemeButton text="START" onClick={() => setScreen('camera')} />
    </>
  );

  // --- SCREEN 2: Camera (Real!) ---
  const CameraScreen = () => (
    <>
      <h2>TAKE YOUR PHOTO</h2>
      <div className="camera-container">
        <Webcam
          audio={false}
          ref={webcamRef}
          mirrored={true}
          screenshotFormat="image/jpeg"
          width="120%"
          videoConstraints={{ facingMode: "user" }}
        />
      </div>
      <MemeButton text="Meme Me" onClick={capture} />
    </>
  );

  // --- SCREEN 3: Result (With your Face!) ---
  const ResultScreen = () => (
    <>
      <h2>THE JUXTAPOSITION</h2>
      <div className="result-container">
        {/* Left Box: The "Meme" (Placeholder for now) */}
        <div className="meme-box">
           {/* <span style={{fontSize: '3rem'}}>🤖</span> */}
           <img className="result-image" src={`/api/image/${idnum}`} style={{width: '100%', height: '100%', objectFit: 'cover'}}/>
        </div>
        
        {/* Right Box: YOU */}
        {/* style={{ backgroundImage: `url(${photo})`, backgroundSize: 'cover' }} */}
        <div className="user-box" >
          <img className="result-image" src={photo} style={{width: '100%', height: '100%', objectFit: 'cover'}}/>
        </div>
      </div>
      <MemeButton text="Try Again" onClick={() => setScreen('title')} />
    </>
  );

  return (
    <div className="meme-app-container">
      <div className="meme-stage">
        {screen === 'title' && <TitleScreen />}
        {screen === 'camera' && <CameraScreen />}
        {screen === 'result' && <ResultScreen />}
      </div>
    </div>
  );
}