import { FormEvent, StrictMode, useState } from 'react';
import { render } from 'react-dom';
import { ipcRenderer } from 'electron';
import { CustomDropzone, Slides, VideoPlayer } from './components';

import './app.css';

const custom = window.thoth;

const outputDir = custom.joinPaths('/tmp', 'json');

const App = (): JSX.Element => {
  const [fileName, setFileName] = useState('');
  const [ocrPath, setOcrPath] = useState('');
  const [speechPath, setSpeechPath] = useState('');
  const [showVideo, setShowVideo] = useState(false);
  const [tempPath, setTempPath] = useState('');

  const handleSubmit = (e: FormEvent): void => {
    e.preventDefault();

    ipcRenderer
      .invoke('get-temp-path')
      .then(async (path) => {
        setTempPath(path);
        return await custom.runThoth(fileName, path);
      })
      .then(() => ipcRenderer.invoke('get-result-dir'))
      .then((resultPath) => {
        setShowVideo(true);
        setOcrPath(`${resultPath}${fileName.replace('.', '-')}-ocr.json`);
        setSpeechPath(`${resultPath}${fileName.replace('.', '-')}-speech.json`);
      })
      .catch((reason) => {
        console.error(JSON.stringify(reason));
      });
  };

  return (
    <div className="container">
      <div className="video">
        {showVideo ? (
          <form onSubmit={handleSubmit}>
            <CustomDropzone setter={setFileName} />
            <input type="submit" value="Submit" />
          </form>
        ) : (
          <VideoPlayer />
        )}
      </div>
      <div className="transcript" style={{ backgroundColor: 'green' }}></div>
      <div
        className="slides"
        style={{ backgroundColor: 'cornflowerblue' }}
      ></div>
    </div>
  );
};

render(
  <StrictMode>
    <App />
  </StrictMode>,
  document.getElementById('app'),
);
