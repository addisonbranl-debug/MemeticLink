import React, { useState, useRef, useCallback, useEffect } from 'react';
import Webcam from 'react-webcam';
import './index.css';

const API = "/api/memetic";

export default function App() {
  const [screen, setScreen] = useState('title');
  const [photo, setPhoto] = useState(null);
  const [test,setTest] =useState([]);
  const webcamRef = useRef(null);

  useEffect(() => {
    fetch(API)
      .then((res) => res.json())
      .then(setTest);
  }, []);

  // Function to capture the photo
  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
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
          screenshotFormat="image/jpeg"
          width="100%"
          videoConstraints={{ facingMode: "user" }}
        />
      </div>
      <MemeButton text={test.text} onClick={capture} />
    </>
  );

  // --- SCREEN 3: Result (With your Face!) ---
  const ResultScreen = () => (
    <>
      <h2>THE JUXTAPOSITION</h2>
      <div className="result-container">
        {/* Left Box: The "Meme" (Placeholder for now) */}
        <div className="meme-box" style={{background: 'blue'}}>
           <span style={{fontSize: '3rem'}}>🤖</span>
        </div>
        
        {/* Right Box: YOU */}
        <div className="meme-box" style={{ backgroundImage: `url(${photo})`, backgroundSize: 'cover' }}>
        </div>
      </div>
      <MemeButton text="TRY AGAIN" onClick={() => setScreen('title')} />
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