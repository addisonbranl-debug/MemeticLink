import React, { useState, useRef, useCallback, useEffect } from 'react';
import Webcam from 'react-webcam';
import './index.css';

const API = "/api/memetic";

export default function App() {
  const [screen, setScreen] = useState('title');
  const [photo, setPhoto] = useState(null);
  const [meme, setMeme] = useState(null);
  const [loading, setLoading] = useState(false); // New State
  const webcamRef = useRef(null);

  const capture = useCallback(async () => {
    setLoading(true); // Start Loading
    
    try {
      const imageSrc = webcamRef.current.getScreenshot();
      setPhoto(imageSrc);
      
      const blob = await fetch(imageSrc).then(r => r.blob());
      const imgData = new FormData();
      imgData.append("image", blob, "userImg.jpg");

      const response = await fetch("http://127.0.0.1:5000/api/upload", {
        method: "POST",
        body: imgData,
      });

      const memeblob = await response.blob();
      const imageUrl = URL.createObjectURL(memeblob);
      setMeme(imageUrl);
      
      setScreen('result');
    } catch (e) {
      console.error(e);
      setScreen('camera');
    } finally {
      setLoading(false); // Stop Loading
    }
  }, [webcamRef]);

  const MemeButton = ({ onClick, text }) => (
    <button className="btn-meme" onClick={onClick}>
      {text}
    </button>
  );

  const TitleScreen = () => (
    <>
      <h1 className="meme-title">Memetic<br/>Link</h1>
      <div className="meme-subtitle">EST. 2025</div>
      <MemeButton text="START" onClick={() => setScreen('camera')} />
    </>
  );

  const CameraScreen = () => (
    <>
      {loading ? (
        <div className="loading-stage">
          <div className="scan-bar"></div>
          <h2 className="loading-text">ANALYZING BIOMETRICS...</h2>
        </div>
      ) : (
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
      )}
    </>
  ); 

  const ResultScreen = () => (
    <>
      <h2>THE JUXTAPOSITION</h2>
      <div className="result-container">
        <div className="meme-box">
           <img className="result-image" src={meme} style={{width: '100%', height: '100%', objectFit: 'cover'}}/>
        </div>
        <div className="user-box" >
          <img className="result-image" src={photo} style={{width: '100%', height: '100%', objectFit: 'cover'}}/>
        </div>
      </div>
      <MemeButton text="Try Again" onClick={() => { setMeme(null); setScreen('title'); }} />
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
